# Kotlin 전문가 - 코드 예제 및 패턴

이 문서에는 Kotlin 개발을 위한 코드 예제, 안티 패턴, 실제 구현 패턴이 포함되어 있습니다.

## 안티 패턴 1: 코루틴 범위 누출

**모습:**
```kotlin
// WRONG: Leaking GlobalScope
class MyActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        GlobalScope.launch { // Memory leak! Activity may be destroyed
            val data = fetchData()
            updateUI(data) // May crash if activity is gone
        }
    }
}

// WRONG: Uncontrolled lifecycleScope
class MyViewModel : ViewModel() {
    fun loadData() {
        // This is fine in ViewModel, but not for one-off requests
        viewModelScope.launch {
            while (true) { // Infinite loop, never cancelled properly
                fetchAndUpdate()
                delay(5000)
            }
        }
    }
}
```

**실패하는 이유:**
- **메모리 누수**: GlobalScope는 영원히 존재하며 파괴된 활동에 대한 참조를 보유합니다.
- **충돌**: 활동이 종료된 후 UI를 업데이트하려고 합니다.
- **좀비 코루틴**: 취소 확인이 없는 무한 루프

**올바른 접근 방식:**
```kotlin
// CORRECT: Lifecycle-aware scope
class MyActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        lifecycleScope.launch { // Automatically cancelled when Activity destroyed
            val data = fetchData()
            updateUI(data)
        }
    }
}

// CORRECT: Controlled polling with cancellation
class MyViewModel : ViewModel() {
    private var pollingJob: Job? = null
    
    fun startPolling() {
        pollingJob?.cancel() // Cancel previous job
        pollingJob = viewModelScope.launch {
            while (isActive) { // Check for cancellation
                fetchAndUpdate()
                delay(5000)
            }
        }
    }
    
    fun stopPolling() {
        pollingJob?.cancel()
    }
    
    override fun onCleared() {
        super.onCleared()
        pollingJob?.cancel() // Explicit cleanup
    }
}
```

**범위 선택 가이드:**
- **활동/프래그먼트**: 사용`lifecycleScope`(수명 주기에 따라 자동 취소됨)
- **ViewModel**: 사용`viewModelScope`(ViewModel이 지워지면 자동 취소됨)
- **애플리케이션 수준**: 사용`CoroutineScope(SupervisorJob() + Dispatchers.Main)`수동 정리 사용
- **안함**: 사용`GlobalScope`프로덕션 코드에서

---

## 안티 패턴 2: 메인 디스패처 차단

**모습:**
```kotlin
// WRONG: Blocking Main thread
viewModelScope.launch(Dispatchers.Main) {
    val data = database.query() // Blocking I/O on Main!
    val result = heavyComputation(data) // CPU-intensive on Main!
    updateUI(result)
}

// WRONG: Mixing blocking and suspend
suspend fun loadData(): Data {
    Thread.sleep(1000) // NEVER use Thread.sleep in suspend functions!
    return fetchFromNetwork()
}
```

**실패하는 이유:**
- **ANR(애플리케이션이 응답하지 않음)**: UI가 5초 이상 정지됨
- **Janky UI**: 프레임이 60fps 미만으로 떨어지면 끊김 현상이 발생합니다.
- **낭비된 정지**: 사용`Thread.sleep`코루틴을 정지하는 대신 스레드를 차단합니다.
- **메인 스레드 고갈**: 다른 UI 업데이트를 실행할 수 없습니다.

**올바른 접근 방식:**
```kotlin
// CORRECT: Use appropriate dispatchers
viewModelScope.launch {
    val data = withContext(Dispatchers.IO) {
        database.query() // I/O operations on IO dispatcher
    }
    
    val result = withContext(Dispatchers.Default) {
        heavyComputation(data) // CPU work on Default dispatcher
    }
    
    // Automatically back on Main dispatcher
    updateUI(result)
}

// CORRECT: Use delay instead of Thread.sleep
suspend fun loadData(): Data {
    delay(1000) // Suspends coroutine, doesn't block thread
    return fetchFromNetwork()
}

// CORRECT: Explicit dispatcher for repository
class Repository(
    private val ioDispatcher: CoroutineDispatcher = Dispatchers.IO
) {
    suspend fun getData(): Data = withContext(ioDispatcher) {
        database.query()
    }
}
```

---

## 예: KMP 공유 모듈 완성

### 프로젝트 구조
```
shared/
├── build.gradle.kts
├── src/
│   ├── commonMain/kotlin/
│   │   ├── models/
│   │   │   └── Product.kt
│   │   ├── repository/
│   │   │   └── ProductRepository.kt
│   │   └── Platform.kt
│   ├── androidMain/kotlin/
│   │   └── Platform.android.kt
│   └── iosMain/kotlin/
│       └── Platform.ios.kt
```

### 공통 모듈 모델
```kotlin
// commonMain/kotlin/models/Product.kt
@Serializable
data class Product(
    val id: String,
    val name: String,
    val price: Double,
    val description: String? = null
)

@Serializable
data class ApiResponse<T>(
    val success: Boolean,
    val data: T?,
    val error: String? = null
)
```

### 공통 저장소
```kotlin
// commonMain/kotlin/repository/ProductRepository.kt
class ProductRepository(
    private val httpClient: HttpClient,
    private val baseUrl: String
) {
    suspend fun getProducts(): Result<List<Product>> = runCatching {
        val response: ApiResponse<List<Product>> = httpClient.get("$baseUrl/products").body()
        if (response.success && response.data != null) {
            response.data
        } else {
            throw Exception(response.error ?: "Unknown error")
        }
    }
    
    suspend fun getProduct(id: String): Result<Product> = runCatching {
        val response: ApiResponse<Product> = httpClient.get("$baseUrl/products/$id").body()
        if (response.success && response.data != null) {
            response.data
        } else {
            throw Exception(response.error ?: "Product not found")
        }
    }
    
    suspend fun createProduct(product: Product): Result<Product> = runCatching {
        val response: ApiResponse<Product> = httpClient.post("$baseUrl/products") {
            contentType(ContentType.Application.Json)
            setBody(product)
        }.body()
        if (response.success && response.data != null) {
            response.data
        } else {
            throw Exception(response.error ?: "Failed to create product")
        }
    }
}
```

### 플랫폼 예상/실제
```kotlin
// commonMain/kotlin/Platform.kt
expect fun getPlatformName(): String
expect fun createHttpClient(): HttpClient

// androidMain/kotlin/Platform.android.kt
actual fun getPlatformName(): String = "Android"
actual fun createHttpClient(): HttpClient = HttpClient(Android) {
    install(ContentNegotiation) {
        json(Json { ignoreUnknownKeys = true })
    }
    install(Logging) {
        level = LogLevel.INFO
    }
}

// iosMain/kotlin/Platform.ios.kt
actual fun getPlatformName(): String = "iOS"
actual fun createHttpClient(): HttpClient = HttpClient(Darwin) {
    install(ContentNegotiation) {
        json(Json { ignoreUnknownKeys = true })
    }
}
```

---

## 예: 어떤 REST API인지
```kotlin
// Application.kt
fun Application.module() {
    install(ContentNegotiation) {
        json(Json {
            prettyPrint = true
            isLenient = true
        })
    }
    
    install(CallLogging) {
        level = Level.INFO
        filter { call -> call.request.path().startsWith("/api") }
    }
    
    install(StatusPages) {
        exception<Throwable> { call, cause ->
            call.application.environment.log.error("Unhandled error", cause)
            call.respond(
                HttpStatusCode.InternalServerError,
                ErrorResponse("Internal server error")
            )
        }
        exception<NotFoundException> { call, cause ->
            call.respond(HttpStatusCode.NotFound, ErrorResponse(cause.message ?: "Not found"))
        }
    }
    
    routing {
        route("/api/v1") {
            productRoutes()
            userRoutes()
        }
    }
}

// ProductRoutes.kt
fun Route.productRoutes() {
    val repository: ProductRepository by inject()
    
    route("/products") {
        get {
            val products = repository.findAll()
            call.respond(products)
        }
        
        get("/{id}") {
            val id = call.parameters["id"] ?: throw BadRequestException("Missing id")
            val product = repository.findById(id) ?: throw NotFoundException("Product not found")
            call.respond(product)
        }
        
        post {
            val request = call.receive<CreateProductRequest>()
            val product = repository.create(request)
            call.respond(HttpStatusCode.Created, product)
        }
        
        put("/{id}") {
            val id = call.parameters["id"] ?: throw BadRequestException("Missing id")
            val request = call.receive<UpdateProductRequest>()
            val product = repository.update(id, request) ?: throw NotFoundException("Product not found")
            call.respond(product)
        }
        
        delete("/{id}") {
            val id = call.parameters["id"] ?: throw BadRequestException("Missing id")
            val deleted = repository.delete(id)
            if (deleted) {
                call.respond(HttpStatusCode.NoContent)
            } else {
                throw NotFoundException("Product not found")
            }
        }
    }
}
```

---

## 테스트 패턴

### 리포지토리 테스트
```kotlin
class ProductRepositoryTest {
    private val testDispatcher = StandardTestDispatcher()
    private lateinit var repository: ProductRepository
    private lateinit var mockApiClient: MockApiClient
    
    @Before
    fun setup() {
        Dispatchers.setMain(testDispatcher)
        mockApiClient = MockApiClient()
        repository = ProductRepository(mockApiClient, testDispatcher)
    }
    
    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }
    
    @Test
    fun `loadProducts updates state to Success when API returns data`() = runTest {
        // Given
        val products = listOf(Product("1", "Test", 10.0, 5))
        mockApiClient.setProducts(products)
        
        // When
        repository.loadProducts()
        testDispatcher.scheduler.advanceUntilIdle()
        
        // Then
        val state = repository.products.value
        assertTrue(state is UiState.Success)
        assertEquals(products, (state as UiState.Success).data)
    }
    
    @Test
    fun `loadProducts updates state to Error when API fails`() = runTest {
        // Given
        mockApiClient.setError(IOException("Network error"))
        
        // When
        repository.loadProducts()
        testDispatcher.scheduler.advanceUntilIdle()
        
        // Then
        val state = repository.products.value
        assertTrue(state is UiState.Error)
        assertEquals("Network error", (state as UiState.Error).message)
    }
}
```

### 흐름 테스트
```kotlin
@Test
fun `searchProducts emits results after debounce`() = runTest {
    // Given
    val products = listOf(Product("1", "Test", 10.0, 5))
    mockApiClient.setSearchResults(products)
    
    // When
    val results = mutableListOf<List<Product>>()
    val job = launch {
        repository.searchProducts("test").toList(results)
    }
    
    advanceTimeBy(300) // Wait for debounce
    advanceUntilIdle()
    job.cancel()
    
    // Then
    assertEquals(1, results.size)
    assertEquals(products, results.first())
}
```

---

## Gradle 구성(KMP)
```kotlin
// shared/build.gradle.kts
plugins {
    kotlin("multiplatform")
    kotlin("plugin.serialization")
    id("com.android.library")
}

kotlin {
    androidTarget()
    
    listOf(
        iosX64(),
        iosArm64(),
        iosSimulatorArm64()
    ).forEach {
        it.binaries.framework {
            baseName = "shared"
        }
    }
    
    sourceSets {
        val commonMain by getting {
            dependencies {
                implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
                implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.0")
                implementation("io.ktor:ktor-client-core:2.3.5")
                implementation("io.ktor:ktor-client-content-negotiation:2.3.5")
                implementation("io.ktor:ktor-serialization-kotlinx-json:2.3.5")
            }
        }
        
        val androidMain by getting {
            dependencies {
                implementation("io.ktor:ktor-client-android:2.3.5")
            }
        }
        
        val iosMain by creating {
            dependsOn(commonMain)
            dependencies {
                implementation("io.ktor:ktor-client-darwin:2.3.5")
            }
        }
    }
}
```
