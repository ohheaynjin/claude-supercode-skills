# Kotlin 전문가 - 기술 참조

이 문서에는 Kotlin 개발을 위한 자세한 워크플로, 기술 사양, 고급 패턴이 포함되어 있습니다.

## 워크플로: Flow를 사용하여 코루틴 기반 데이터 계층 구현

**목표:** UI 상태 관리를 위해 StateFlow를 사용하여 반응형 저장소 패턴을 구축합니다.

### 1단계: 데이터 모델 정의
```kotlin
import kotlinx.serialization.Serializable

@Serializable
data class Product(
    val id: String,
    val name: String,
    val price: Double,
    val stock: Int
)

sealed class UiState<out T> {
    object Idle : UiState<Nothing>()
    object Loading : UiState<Nothing>()
    data class Success<T>(val data: T) : UiState<T>()
    data class Error(val message: String) : UiState<Nothing>()
}
```
### 2단계: Flow를 사용하여 저장소 만들기
```kotlin
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

class ProductRepository(
    private val apiClient: ApiClient,
    private val dispatcher: CoroutineDispatcher = Dispatchers.IO
) {
    private val _products = MutableStateFlow<UiState<List<Product>>>(UiState.Idle)
    val products: StateFlow<UiState<List<Product>>> = _products.asStateFlow()
    
    private val _selectedProduct = MutableStateFlow<Product?>(null)
    val selectedProduct: StateFlow<Product?> = _selectedProduct.asStateFlow()
    
    // Search products with debounce
    fun searchProducts(query: String): Flow<List<Product>> = flow {
        delay(300) // Debounce
        val result = apiClient.searchProducts(query)
        emit(result.getOrDefault(emptyList()))
    }.flowOn(dispatcher)
    
    suspend fun loadProducts() {
        _products.value = UiState.Loading
        
        withContext(dispatcher) {
            apiClient.getProducts()
                .onSuccess { data ->
                    _products.value = UiState.Success(data)
                }
                .onFailure { error ->
                    _products.value = UiState.Error(error.message ?: "Unknown error")
                }
        }
    }
    
    fun observeProduct(productId: String): Flow<Product?> = flow {
        while (currentCoroutineContext().isActive) {
            val product = apiClient.getProduct(productId).getOrNull()
            emit(product)
            delay(5000) // Poll every 5 seconds
        }
    }.flowOn(dispatcher)
    
    fun selectProduct(product: Product) {
        _selectedProduct.value = product
    }
}
```
### 3단계: ViewModel 만들기(Android)
```kotlin
// Android ViewModel
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope

class ProductViewModel(
    private val repository: ProductRepository
) : ViewModel() {
    
    val products: StateFlow<UiState<List<Product>>> = repository.products
    val selectedProduct: StateFlow<Product?> = repository.selectedProduct
    
    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery.asStateFlow()
    
    val searchResults: StateFlow<List<Product>> = searchQuery
        .debounce(300)
        .distinctUntilChanged()
        .flatMapLatest { query ->
            if (query.isBlank()) flowOf(emptyList())
            else repository.searchProducts(query)
        }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = emptyList()
        )
    
    init {
        loadProducts()
    }
    
    fun loadProducts() {
        viewModelScope.launch {
            repository.loadProducts()
        }
    }
    
    fun search(query: String) {
        _searchQuery.value = query
    }
    
    fun selectProduct(product: Product) {
        repository.selectProduct(product)
    }
}
```
### 4단계: UI에서 사용(Jetpack Compose)
```kotlin
import androidx.compose.runtime.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items

@Composable
fun ProductScreen(viewModel: ProductViewModel) {
    val uiState by viewModel.products.collectAsState()
    val searchQuery by viewModel.searchQuery.collectAsState()
    val searchResults by viewModel.searchResults.collectAsState()
    
    Column {
        TextField(
            value = searchQuery,
            onValueChange = { viewModel.search(it) },
            placeholder = { Text("Search products...") }
        )
        
        when (uiState) {
            is UiState.Idle -> Text("Pull to refresh")
            is UiState.Loading -> CircularProgressIndicator()
            is UiState.Success -> {
                val products = (uiState as UiState.Success).data
                LazyColumn {
                    items(products) { product ->
                        ProductItem(product) { viewModel.selectProduct(product) }
                    }
                }
            }
            is UiState.Error -> {
                Text("Error: ${(uiState as UiState.Error).message}")
            }
        }
    }
}
```
### 5단계: 취소를 올바르게 처리하기
```kotlin
class ProductViewModel : ViewModel() {
    private var pollingJob: Job? = null
    
    fun startPolling(productId: String) {
        pollingJob?.cancel() // Cancel previous polling
        pollingJob = viewModelScope.launch {
            repository.observeProduct(productId)
                .catch { e -> 
                    Log.e("ProductVM", "Polling error", e) 
                }
                .collect { product ->
                    // Update UI with latest product data
                }
        }
    }
    
    override fun onCleared() {
        super.onCleared()
        pollingJob?.cancel() // Cleanup
    }
}
```
**예상 결과:**
- StateFlow를 통한 반응형 UI 업데이트(단일 정보 소스)
- 검색을 위한 자동 디바운싱 및 중복 제거
- 적절한 수명주기 인식 코루틴 범위 지정
- 깔끔한 분리 : Repository(데이터) → ViewModel(비즈니스 로직) → UI(프레젠테이션)

**확인:**
- 검색은 300ms 일시 중지 후 응답합니다(네트워크 스팸 없음).
- 회전하는 장치 상태 유지(ViewModel은 구성 변경에도 유지됨)
- 화면을 떠나면 폴링 작업이 취소됩니다(메모리 누수 없음).
- LeakCanary 및 Profiler로 확인

---

## 패턴: 플랫폼별 구현에 대한 예상/실제

**사용 사례:** 공유 코드에서 플랫폼별 API(파일 시스템, 알림, 센서)에 액세스합니다.
```kotlin
// commonMain/Platform.kt
expect class PlatformStorage {
    suspend fun saveData(key: String, value: String)
    suspend fun loadData(key: String): String?
    suspend fun clearAll()
}

// androidMain/Platform.kt
import android.content.Context
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.first

actual class PlatformStorage(private val context: Context) {
    private val Context.dataStore by preferencesDataStore(name = "settings")
    
    actual suspend fun saveData(key: String, value: String) {
        context.dataStore.edit { prefs ->
            prefs[stringPreferencesKey(key)] = value
        }
    }
    
    actual suspend fun loadData(key: String): String? {
        return context.dataStore.data.first()[stringPreferencesKey(key)]
    }
    
    actual suspend fun clearAll() {
        context.dataStore.edit { it.clear() }
    }
}

// iosMain/Platform.kt
import platform.Foundation.NSUserDefaults

actual class PlatformStorage {
    private val defaults = NSUserDefaults.standardUserDefaults
    
    actual suspend fun saveData(key: String, value: String) {
        defaults.setObject(value, forKey = key)
    }
    
    actual suspend fun loadData(key: String): String? {
        return defaults.stringForKey(key)
    }
    
    actual suspend fun clearAll() {
        defaults.dictionaryRepresentation().keys.forEach { key ->
            defaults.removeObjectForKey(key as String)
        }
    }
}
```
**맞춤 설정 포인트:**
- 민감한 데이터에 대한 암호화 추가(사용`expect/actual`플랫폼 암호화 API의 경우)
- 인라인 클래스를 사용하여 유형이 안전한 키로 확장
- 데이터 변경에 대한 흐름 기반 관찰자 추가

---

## 패턴: Ktor 사용자 정의 플러그인

**사용 사례:** 로깅, 인증, 속도 제한을 위한 재사용 가능한 미들웨어입니다.
```kotlin
// Custom request timing plugin
val RequestTimingPlugin = createApplicationPlugin(name = "RequestTiming") {
    onCall { call ->
        val startTime = System.currentTimeMillis()
        
        call.response.pipeline.intercept(ApplicationSendPipeline.After) {
            val duration = System.currentTimeMillis() - startTime
            call.response.headers.append("X-Response-Time", "${duration}ms")
            application.log.info("${call.request.uri} took ${duration}ms")
        }
    }
}

// Usage
fun Application.module() {
    install(RequestTimingPlugin)
}

// Rate limiting plugin
data class RateLimitConfig(
    val maxRequests: Int = 100,
    val windowMs: Long = 60_000
)

val RateLimitPlugin = createApplicationPlugin(
    name = "RateLimit",
    createConfiguration = ::RateLimitConfig
) {
    val requestCounts = mutableMapOf<String, MutableList<Long>>()
    
    onCall { call ->
        val clientId = call.request.headers["X-API-Key"] ?: call.request.origin.remoteHost
        val now = System.currentTimeMillis()
        
        val timestamps = requestCounts.getOrPut(clientId) { mutableListOf() }
        timestamps.removeIf { it < now - pluginConfig.windowMs }
        
        if (timestamps.size >= pluginConfig.maxRequests) {
            call.respond(HttpStatusCode.TooManyRequests, "Rate limit exceeded")
            finish()
        } else {
            timestamps.add(now)
        }
    }
}

// Usage with custom config
install(RateLimitPlugin) {
    maxRequests = 50
    windowMs = 30_000 // 30 seconds
}
```
**맞춤 설정 포인트:**
- 분산 속도 제한에 Redis 사용
- IP 기반 vs API 키 기반 전략 추가
- 지수 백오프 헤더 구현

---

## 패턴: SupervisorScope를 사용한 구조적 동시성

**사용 사례:** 한 번의 실패로 인해 다른 실패가 취소되지 않는 병렬 작업을 실행합니다.
```kotlin
class DataSyncManager {
    suspend fun syncAll(): SyncResult = supervisorScope {
        val userDeferred = async { syncUsers() }
        val productsDeferred = async { syncProducts() }
        val ordersDeferred = async { syncOrders() }
        
        val userResult = runCatching { userDeferred.await() }
        val productResult = runCatching { productsDeferred.await() }
        val orderResult = runCatching { ordersDeferred.await() }
        
        SyncResult(
            users = userResult.getOrNull(),
            products = productResult.getOrNull(),
            orders = orderResult.getOrNull(),
            errors = listOfNotNull(
                userResult.exceptionOrNull(),
                productResult.exceptionOrNull(),
                orderResult.exceptionOrNull()
            )
        )
    }
    
    private suspend fun syncUsers(): List<User> = withContext(Dispatchers.IO) {
        // Sync logic
    }
    
    // ... other sync methods
}

data class SyncResult(
    val users: List<User>?,
    val products: List<Product>?,
    val orders: List<Order>?,
    val errors: List<Throwable>
) {
    val isFullSuccess: Boolean get() = errors.isEmpty()
    val isPartialSuccess: Boolean get() = errors.isNotEmpty() && 
        (users != null || products != null || orders != null)
}
```
**맞춤 설정 포인트:**
- 사용`coroutineScope`대신 실패가 발생하면 모두 취소되어야 합니다.
- 지수 백오프를 사용한 재시도 논리 추가
- SharedFlow로 진행 상황 추적 구현

---

## 발송자 지침

| 디스패처 | 사용 대상 | 스레드 풀 |
|------------|---------|------------|
| **디스패처.메인** | UI 업데이트만 | 메인/UI 스레드 |
| **Dispatchers.IO** | 네트워크, 데이터베이스, 파일 I/O | 최대 64개 스레드 |
| **디스패처.기본값** | CPU 집약적인 작업 | CPU 코어 수 |
| **Dispatchers.Unconfined** | 고급 사용 전용(테스트) | 스레드 풀 없음 |

**모범 사례:**
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
```
