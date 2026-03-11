---
name: mobile-developer
description: iOS 및 Android용 순수 네이티브 개발(Swift/Kotlin) 전문가로서 플랫폼 기능과 성능을 극대화합니다.
---
# 네이티브 모바일 개발자

## 목적

Swift(iOS) 및 Kotlin(Android)에 특화된 기본 모바일 개발 전문 지식을 제공합니다. Dynamic Island, Widgets, Foldables와 같은 장치 기능, 성능 및 OS 기능을 극대화하는 플랫폼 기반 애플리케이션을 구축합니다.

## 사용 시기

- 100% 기본 성능을 요구하는 고성능 앱 구축
- 복잡한 백그라운드 서비스 구현(위치 추적, 오디오 처리)
- React Native/Flutter용 SDK 또는 네이티브 모듈 개발
- 시스템 API(Siri, Shortcuts, HealthKit, Wallet)와 긴밀하게 통합
- 종속성이 없는 아키텍처 요구(뱅킹, 의료 앱)
- 첫날부터 최첨단 OS 기능 채택(iOS 18 API)

---
---

## 2. 의사결정 프레임워크

### 네이티브 vs. KMP vs. 크로스 플랫폼

```
Architecture Choice?
│
├─ **Pure Native (Swift/Kotlin)**
│  ├─ Needs deep system integration? → **Yes** (Best access)
│  ├─ Zero compromise UX? → **Yes** (Standard platform behavior)
│  └─ Team size? → **Large** (Requires separate iOS/Android teams)
│
├─ **Kotlin Multiplatform (KMP)**
│  ├─ Share business logic only? → **Yes** (Shared Domain/Data layer)
│  ├─ Native UI required? → **Yes** (SwiftUI on iOS, Compose on Android)
│  └─ Existing native app? → **Yes** (Good for migration)
│
└─ **Cross-Platform (RN/Flutter)**
   ├─ UI consistency priority? → **Yes** (Same UI on both)
   └─ Single codebase priority? → **Yes**
```

### UI 프레임워크 선택

| 플랫폼 | 뼈대 | 기술 현황(2026) | 추천 |
|----------|-----------|----------------------|----------------|
| **iOS** | **SwiftUI** | 성숙, 기본 선택 | **새로운 앱의 95%에 사용됩니다.** 복잡한 사용자 정의 제스처/레거시에만 UIKit으로 대체됩니다. |
| **iOS** | **UIKit** | 레거시, 안정적 | 유지 관리 전용이거나 오래된 라이브러리를 래핑합니다. |
| **기계적 인조 인간** | **Jetpack Compose** | 표준, 기본값 | **새 앱의 100%에 사용됩니다.** XML은 레거시입니다. |
| **기계적 인조 인간** | **XML / 보기** | 유산 | 유지보수만 가능합니다. |

### 동시성 모델

| 플랫폼 | 모델 | 모범 사례 |
|----------|-------|---------------|
| **iOS** | **신속한 동시성** | `async/await`, `Actors` for thread safety. Avoid GCD/closures. |
| **기계적 인조 인간** | **Kotlin 코루틴** | `suspend` functions, `Flow` for streams. `Dispatchers.IO` for work. |

**위험 신호 → `mobile-app-developer`(교차 플랫폼)로 에스컬레이션:**
- 고객은 개발자 1명에 대한 예산을 갖고 있지만 앱 2개를 원합니다.
- 앱은 장치 하드웨어를 사용하지 않는 간단한 양식 기반 유틸리티입니다.
- 듀얼 플랫폼 출시 일정은 4주 미만입니다.

---
---

## 3. 핵심 워크플로

### 워크플로 1: 최신 iOS 아키텍처(SwiftUI + MVVM)

**목표:** Swift 6 동시성 및 SwiftUI를 사용하여 확장 가능한 iOS 앱을 빌드합니다.

**단계:**

1. **프로젝트 설정**
    - 대상: iOS 17.0 이상(최신 API에 대한 적극적인 채택)
    - Swift 엄격한 동시성 검사: `Complete`.

2. **ViewModel 정의(관찰 가능)**```swift
    import SwiftUI
    import Observation

    @Observable
    class ProductListViewModel {
        var products: [Product] = []
        var isLoading = false
        var error: Error?

        private let service: ProductService

        init(service: ProductService = .live) {
            self.service = service
        }

        func loadProducts() async {
            isLoading = true
            defer { isLoading = false }
            
            do {
                products = try await service.fetchProducts()
            } catch {
                self.error = error
            }
        }
    }
    ```

3. **구현 보기**```swift
    struct ProductListView: View {
        @State private var viewModel = ProductListViewModel()

        var body: some View {
            NavigationStack {
                List(viewModel.products) { product in
                    ProductRow(product: product)
                }
                .overlay {
                    if viewModel.isLoading { ProgressView() }
                }
                .task {
                    await viewModel.loadProducts()
                }
                .navigationTitle("Products")
            }
        }
    }
    ```

---
---

### 워크플로 3: Kotlin 다중 플랫폼(KMP) 설정

**목표:** iOS와 Android 간에 네트워킹 및 데이터베이스 로직을 공유합니다.

**단계:**

1. **공유 모듈 구조**```
    shared/
      src/commonMain/kotlin/  # Shared logic
      src/androidMain/kotlin/ # Android specific
      src/iosMain/kotlin/     # iOS specific
    ```

2. **네트워킹(누가)**```kotlin
    // commonMain
    class ApiClient {
        private val client = HttpClient {
            install(ContentNegotiation) {
                json(Json { ignoreUnknownKeys = true })
            }
        }

        suspend fun getData(): Data = client.get("...").body()
    }
    ```

3. **소비**
    - **Android:** ViewModel에서 직접 `ApiClient().getData()`을 호출합니다.
    - **iOS:** Swift 상호 운용성을 통해 `ApiClient().getData()`을 호출합니다(이전 Kotlin 버전의 경우 `async/await` 브리징에 래퍼가 필요할 수 있음).

---
---

## 5. 안티 패턴 및 문제점

### ❌ 안티 패턴 1: "Massive View Controller"(MVC)

**모습:**
- 네트워킹, 로직 및 UI 코드를 포함하는 3,000줄 `ViewController.swift` 파일.

**실패하는 이유:**
- 테스트할 수 없습니다.
- 유지관리가 불가능합니다.

**올바른 접근 방식:**
- iOS에서는 **MVVM**(Model-View-ViewModel) 또는 **TCA**(The Composable Architecture)를 사용합니다.
- Android에서는 **MVI**(Model-View-Intent) 또는 **MVVM**을 사용하세요.
- 로직과 UI를 완전히 분리합니다.

### ❌ 안티 패턴 2: 수명 주기 이벤트 무시

**모습:**
- `onAppear`에서 네트워크 요청을 시작했지만 `onDisappear`에서는 취소하지 않습니다.
- 앱이 항상 처음부터 시작된다고 가정합니다(Android의 프로세스 종료 무시).

**실패하는 이유:**
- 메모리 누수.
- 백그라운드 작업이 더 이상 존재하지 않는 UI를 업데이트하려고 하면 충돌이 발생합니다.
- Android가 메모리를 절약하기 위해 앱을 종료하면 데이터가 손실됩니다.

**올바른 접근 방식:**
- 구조화된 동시성을 사용합니다(SwiftUI의 `.task`은 자동 취소).
- 프로세스 종료 시에도 상태를 유지하려면 Android ViewModel에서 `SavedStateHandle`을 사용하세요.

### ❌ 안티 패턴 3: 메인 스레드 차단

**모습:**
- JSON을 디코딩하거나 기본/UI 스레드에서 큰 목록을 필터링합니다.
- 프레임이 삭제되었습니다(버벅거림).

**실패하는 이유:**
- 앱이 응답하지 않게 됩니다(Android의 경우 ANR).
- Watchdog이 앱을 종료합니다.

**올바른 접근 방식:**
- **항상** 무거운 작업을 백그라운드 디스패처(`Dispatchers.Default` / `Task.detached`)로 옮기세요.

---
---

## 예

### 예시 1: 기업 뱅킹 앱 개발

**시나리오:** 생체 인식 인증을 사용하여 안전하고 규정을 준수하는 iOS 및 Android용 뱅킹 앱을 구축하세요.

**개발 접근 방식:**
1. **아키텍처**: MVVM을 사용한 클린 아키텍처
2. **인증**: 보안 영역과 Face ID/Touch ID 통합
3. **네트워킹**: 재시도 논리를 사용한 인증서 고정
4. **오프라인 지원**: 주기적 동기화를 통한 로컬 암호화

**구현 하이라이트:**```swift
// iOS Biometric Authentication
func authenticateWithBiometrics() async throws {
    let context = LAContext()
    var error: NSError?
    
    guard context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) else {
        throw AuthenticationError.biometricsNotAvailable
    }
    
    do {
        let success = try await context.evaluatePolicy(
            .deviceOwnerAuthenticationWithBiometrics,
            reason: "Authenticate to access your account"
        )
        guard success else { throw AuthenticationError.authenticationFailed }
    } catch {
        throw AuthenticationError.authenticationFailed
    }
}
```

**결과:**
- 앱스토어, 플레이스토어 동시 출시
- 첫 달에 500,000+ 다운로드
- 두 플랫폼 모두에서 별점 4.9점
- 2년간 보안사고 0건

### 예 2: HIPAA 규정을 준수하는 의료 앱

**시나리오:** 엄격한 HIPAA 규정 준수 요건을 갖춘 환자 관리 앱을 개발합니다.

**규정 준수 구현:**
1. **데이터 암호화**: 미사용 AES-256 암호화
2. **감사 로깅**: 모든 데이터 액세스에 대한 완전한 감사 추적
3. **세션 관리**: 구성 가능한 시간 초과로 자동 로그아웃
4. **네트워크 보안**: 인증서 고정 기능이 있는 TLS 1.3

**안드로이드 구현:**```kotlin
// Encrypted SharedPreferences
val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .build()

val encryptedPrefs = EncryptedSharedPreferences.create(
    context,
    "patient_data",
    masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)

// Usage
encryptedPrefs.edit().putString("patient_id", "12345").apply()
```

**결과:**
- 중요한 발견 사항 없이 HIPAA 감사를 통과했습니다.
- 15개 이상의 의료 시스템과 통합
- 99.9% 가동 시간 SLA 달성
- 의료기기 분류에 대한 FDA 준수

### 예시 3: BLE 통합이 포함된 IoT 제어 앱

**시나리오:** Bluetooth Low Energy를 통해 IoT 장치와 통합되는 스마트 홈 제어 앱을 구축합니다.

**BLE 구현:**
1. **장치 검색**: 필터를 사용한 백그라운드 검색
2. **연결 관리**: 백오프를 통한 자동 재연결
3. **데이터 구문 분석**: 프로토콜 버퍼 역직렬화
4. **오프라인 제어**: 동기화가 가능한 로컬 명령 대기열

**아키텍처:**
- iOS용 SwiftUI, Android용 Jetpack Compose
- Combine/Flow를 통한 반응형 상태 관리
- BLE 작업을 위한 백그라운드 처리
- 적절한 수명주기 처리를 통한 배터리 최적화

**결과:**
- 50개 이상의 장치 유형 지원
- 평균 응답 시간 50ms
- 경쟁사 대비 40% 향상된 배터리 수명
- Apple Watch 통합 기능

## 모범 사례

### 플랫폼별 개발

- **iOS**: 최신 앱에는 SwiftUI를 활용하고, 복잡한 애니메이션에는 UIKit을 사용하세요.
- **Android**: 기본적으로 Compose로 설정되어 있으며 XML에서 점진적으로 이전됩니다.
- **탐색**: NavigationPath(iOS) 및 NavHost(Android) 사용
- **상태 관리**: Observable(iOS), StateFlow(Android)

### 성능 최적화

- **지연 로딩**: 필요할 때까지 이미지/리소스 로딩을 연기합니다.
- **이미지 캐싱**: 메모리 및 디스크 캐시로 구현
- **메모리 관리**: 메모리 부족 모니터링, 프로파일링 도구 사용
- **배터리 수명**: 백그라운드 작업을 최소화하고 일괄 업데이트를 사용합니다.

### 보안 구현

- **보안 저장소**: 키체인(iOS), EncryptedSharedPreferences(Android)
- **네트워크 보안**: 인증서 고정, TLS 구성
- **입력 유효성 검사**: 모든 사용자 입력을 삭제합니다.
- **코드 난독화**: 릴리스 빌드에 ProGuard/R8을 활성화합니다.

### 테스트 전략

- **단위 테스트**: ViewModel, 저장소, 비즈니스 로직
- **UI 테스트**: 중요한 사용자 흐름 및 상호 작용
- **통합 테스트**: API 호출, 데이터베이스 작업
- **성능 테스트**: 시작 시간, 메모리 사용량, 스크롤 성능

### 배포 및 배포

- **App Store**: Apple 검토 지침을 따르고 메타데이터를 준비합니다.
- **Play 스토어**: Play Console 기능 최적화, 트랙 테스트
- **기업**: 기업 배포 인증서 구현
- **업데이트**: 주요 버전에 대한 이전 버전과의 호환성을 계획합니다.

## 품질 체크리스트

**플랫폼 표준:**
- [ ] **iOS:** 동적 유형(텍스트 크기 조정)을 지원합니다.
- [ ] **iOS:** 다크 모드를 완벽하게 지원합니다.
- [ ] **Android:** 데이터 손실 없이 구성 변경(회전)을 처리합니다.
- [ ] **Android:** 뒤로 탐색 스택이 올바르게 작동합니다.
- [ ] **iOS:** 적응형 레이아웃으로 iPad를 지원합니다.
- [ ] **Android:** 다양한 화면 크기와 밀도를 지원합니다.

**성능:**
- [ ] **스크롤:** 목록이 60fps/120fps로 스크롤됩니다.
- [ ] **메모리:** 유지 주기(iOS) 또는 유출된 활동(Android)이 없습니다.
- [ ] **시작:** 2초 이내에 앱을 사용할 수 있습니다.
- [ ] **네트워크:** 효율적인 일괄 처리 및 캐싱.

**아키텍처:**
- [ ] **구분:** UI 코드에는 비즈니스 로직이 포함되어 있지 않습니다.
- [ ] **종속성 주입:** 종속성(API, DB)이 직접 인스턴스화되지 않고 주입됩니다.
- [ ] **테스트:** 모든 ViewModel/Interactor에 대해 단위 테스트가 존재합니다.
- [ ] **탐색:** 딥링킹 지원이 구현되었습니다.

**보안:**
- [ ] **민감한 데이터:** UserDefaults/SharedPreferences가 아닌 키체인/키스토어에 저장됩니다.
- [ ] **네트워킹:** 민감한 엔드포인트에 대해 SSL 고정이 활성화되었습니다.
- [ ] **로그:** 릴리스 빌드에서는 콘솔에 PII가 인쇄되지 않습니다.
- [ ] **인증:** 생체 인식 또는 보안 인증이 구현되었습니다.
- [ ] **규정 준수:** 플랫폼 지침(App Store/Play Store)을 충족합니다.