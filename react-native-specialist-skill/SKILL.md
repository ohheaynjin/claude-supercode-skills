---
name: react-native-specialist
description: React Native(새 아키텍처), TurboModules, Fabric 및 Expo 전문가입니다. 네이티브 모듈 개발 및 성능 최적화를 전문으로 합니다.
---
# 리액트 네이티브 전문가

## 목적

"새로운 아키텍처"(Fabric/TurboModules), JSI 및 Expo 워크플로를 전문으로 하는 React Native 개발 전문 지식을 제공합니다. 맞춤형 네이티브 모듈과 최적화된 JavaScript-네이티브 브리지를 사용하여 고성능 크로스 플랫폼 모바일 애플리케이션을 구축합니다.

## 사용 시기

- 새로운 아키텍처로 고성능 React Native 앱 구축
- 사용자 정의 기본 모듈 또는 뷰 관리자 작성(TurboModules/Fabric)
- Expo 파이프라인 구성(EAS 빌드, 업데이트, 구성 플러그인)
- 기본 충돌(Xcode/Android Studio) 또는 브리지 병목 현상 디버깅
- 기존 아키텍처(Bridge)에서 새로운 아키텍처(JSI)로 마이그레이션
- 복잡한 네이티브 SDK(Maps, WebRTC, Bluetooth) 통합

## 예

### 예시 1: 새로운 아키텍처 마이그레이션

**시나리오:** 대규모 프로덕션 앱을 Bridge에서 Fabric/TurboModules로 마이그레이션합니다.

**구현:**
1. 새로운 아키텍처 플래그를 점진적으로 활성화했습니다.
2. 기본 모듈을 TurboModule로 변환
3. 복잡한 UI를 위한 Fabric 구성 요소 구현
4. Codegen을 사용하여 네이티브 브리지 코드 생성
5. 새로운 아키텍처를 활성화하여 철저한 테스트를 거쳤습니다.

**결과:**
- 40% 더 빠른 UI 렌더링
- 번들 크기가 30% 더 작아졌습니다.
- 기본 경계를 넘어 향상된 유형 안전성
- 더 나은 충돌 보고 및 디버깅

### 예시 2: 사용자 정의 네이티브 모듈

**시나리오:** 피트니스 앱을 위해 Bluetooth Low Energy를 통합해야 합니다.

**구현:**
1. TypeScript 네이티브 모듈 인터페이스 생성
2. 네이티브 코드 구현 (iOS용 Swift, Android용 Kotlin)
3. 크로스 플랫폼 액세스를 위해 노출된 RNTurboModule
4. 적절한 메모리 관리 및 수명주기 처리가 추가되었습니다.
5. 포괄적인 오류 처리 구현

**결과:**
- 두 플랫폼 모두에서 원활하게 작동하는 BLE 작업
- 유형 안전 브리지는 런타임 오류를 방지합니다.
- 기존 네이티브 모듈보다 50% 적은 코드
- RN 업그레이드를 통해 유지

### 예시 3: 성능 최적화

**시나리오:** 앱에서 버벅거리는 스크롤 및 메모리 문제가 발생합니다.

**구현:**
1. 헤르메스 엔진 활성화
2. FlatList를 FlashList로 대체했습니다.
3. 메모이제이션 구현 (useMemo, useCallback)
4. 이미지 및 무거운 구성 요소에 대한 지연 로딩 추가
5. 최적화된 네이티브 브리지 통신

**결과:**
- 이제 스크롤이 일관되게 60fps로 유지됩니다.
- 메모리 사용량이 40% 감소했습니다.
- 앱 실행 시간이 35% 단축되었습니다.
- 충돌률이 60% 감소했습니다.

## 모범 사례

### 건축학

- **새 아키텍처**: Fabric/TurboModules 활성화 및 사용
- **네이티브 모듈**: 유형 안전을 위해 Codegen을 사용합니다.
- **탐색**: React Navigation 또는 Expo Router 사용
- **상태 관리**: 적절한 솔루션 선택(Zustand, Redux)

### 성능

- **Hermes**: 더 나은 시작 및 런타임을 위해 활성화
- **메모이제이션**: useMemo, useCallback, React.memo 사용
- **목록**: 큰 목록에는 FlashList를 사용하세요.
- **이미지**: 지연 로드 및 적절한 캐시

### 기본 통합

- **수명 주기 관리**: 앱 상태 변경 처리
- **오류 경계**: 기본 오류를 정상적으로 포착합니다.
- **권한**: 요청 및 정상적으로 처리
- **테스트**: 두 플랫폼 모두에서 정기적으로 테스트합니다.

### 개발

- **Expo 작업 흐름**: 빠른 개발을 위해 Expo 사용
- **EAS 빌드**: CI/CD 빌드에 사용
- **업데이트**: 무선 업데이트를 위해 EAS 업데이트를 사용하세요.
- **TypeScript**: 모든 코드에 사용

---
---

## 2. 의사결정 프레임워크

### 아키텍처 선택

```
Which architecture to use?
│
├─ **New Architecture (Default for 0.76+)**
│  ├─ **TurboModules:** Lazy-loaded native modules (Sync/Async).
│  ├─ **Fabric:** C++ Shadow Tree for UI (No bridge serialization).
│  ├─ **Codegen:** Type-safe spec for Native <-> JS communication.
│  └─ **Bridgeless Mode:** Removes the legacy bridge entirely.
│
└─ **Old Architecture (Legacy)**
   ├─ **Bridge:** Async JSON serialization (Slow for large data).
   └─ **Maintenance:** Only for unmigrated legacy libraries.
```

### 엑스포와 CLI

| 특징 | 엑스포(관리) | React Native CLI(베어) |
|---------|----------------|-------------------------|
| **설정** | Instant (`create-expo-app`) | 복잡함(JDK, Xcode, Pod) |
| **네이티브 코드** | **구성 플러그인**(기본 파일 자동 수정) | Direct file editing (`AppDelegate.m`) |
| **업그레이드** | `npx expo install --fix` (Stable sets) | 수동 비교(업그레이드 도우미) |
| **빌드** | **EAS 빌드**(클라우드) | 로컬 또는 CI(Fastlane) |
| **업데이트** | **EAS 업데이트**(OTA) | 코드푸시(마이크로소프트) |

### 성과 전략

1. **JSI:** 직접 C++ 호출. JSON 직렬화가 없습니다.
2. **재애니메이션:** UI 스레드 애니메이션(Worklet).
3. **FlashList:** 재활용 보기(FlatList 대체).
4. **Hermes:** 바이트코드 사전 컴파일(즉시 시작).

**위험 신호 → `mobile-developer`(기본)로 에스컬레이션:**
- React Native 엔진 코어 수정(C++)
- 모호한 ProGuard/R8 충돌 디버깅
- 처음부터 낮은 수준의 Metal/OpenGL 렌더러 작성

---
---

## 3. 핵심 워크플로

### 작업 흐름 1: TurboModule 만들기(새 아치)

**목표:** JSI를 통해 기본 배터리 수준에 동기적으로 액세스합니다.

**단계:**

1. **사양 정의(`NativeBattery.ts`)**```typescript
    import type { TurboModule } from 'react-native';
    import { TurboModuleRegistry } from 'react-native';

    export interface Spec extends TurboModule {
      getBatteryLevel(): number;
    }

    export default TurboModuleRegistry.getEnforcing<Spec>('RTNBattery');
    ```

2. **코드 생성**
    - `yarn codegen`을(를) 실행하세요. C++ 인터페이스를 생성합니다.

3. **iOS 구현(`RTNBattery.mm`)**```objectivec
    - (NSNumber *)getBatteryLevel {
      [UIDevice currentDevice].batteryMonitoringEnabled = YES;
      return @([UIDevice currentDevice].batteryLevel);
    }
    
    - (std::shared_ptr<facebook::react::TurboModule>)getTurboModule:
        (const facebook::react::ObjCTurboModule::InitParams &)params {
      return std::make_shared<facebook::react::NativeBatterySpecJSI>(params);
    }
    ```

4. **Android 구현(`BatteryModule.kt`)**```kotlin
    class BatteryModule(context: ReactApplicationContext) : NativeBatterySpec(context) {
      override fun getName() = "RTNBattery"
      
      override fun getBatteryLevel(): Double {
        val manager = context.getSystemService(Context.BATTERY_SERVICE) as BatteryManager
        return manager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY).toDouble()
      }
    }
    ```

---
---

### 워크플로 3: 다시 애니메이션된 Worklet

**목표:** UI 스레드에서 60fps 드래그 동작.

**단계:**

1. **설정**```tsx
    import { useSharedValue, useAnimatedStyle, withSpring } from 'react-native-reanimated';
    import { GestureDetector, Gesture } from 'react-native-gesture-handler';
    ```

2. **구현**```tsx
    function Ball() {
      const offset = useSharedValue({ x: 0, y: 0 });

      const gesture = Gesture.Pan()
        .onUpdate((e) => {
          // Runs on UI thread
          offset.value = { x: e.translationX, y: e.translationY };
        })
        .onEnd(() => {
          offset.value = withSpring({ x: 0, y: 0 }); // Snap back
        });

      const style = useAnimatedStyle(() => ({
        transform: [{ translateX: offset.value.x }, { translateY: offset.value.y }]
      }));

      return (
        <GestureDetector gesture={gesture}>
          <Animated.View style={[styles.ball, style]} />
        </GestureDetector>
      );
    }
    ```

---
---

## 5. 안티 패턴 및 문제점

### ❌ 안티 패턴 1: "다리 건너기" 애니메이션

**모습:**
- `Animated.timing`을(를) `useNativeDriver: false`과(와) 함께 사용합니다.
- `useEffect` 및 `setState`의 레이아웃을 계산합니다.

**실패하는 이유:**
- JS 스레드에서 실행됩니다. JS가 사용 중인 경우(데이터 가져오기) 프레임을 삭제합니다.

**올바른 접근 방식:**
- **Reanimated** 또는 `useNativeDriver: true`를 사용하세요.

### ❌ 안티 패턴 2: 헤르메스가 없는 대형 번들

**모습:**
- 안드로이드에서 사용되는 JSC(JavaScriptCore).
- 시작 시간은 5초 정도 소요됩니다.

**실패하는 이유:**
- JSC는 런타임에 JS를 구문 분석합니다. Hermes는 미리 컴파일된 바이트코드를 실행합니다.

**올바른 접근 방식:**
- `podfile` / `build.gradle`(새 Expo의 기본값)에서 **Hermes**를 활성화합니다.

### ❌ 안티 패턴 3: 렌더링 스타일

**모습:**
- `style={{ width: 100, height: 100 }}`

**실패하는 이유:**
- 렌더링할 때마다 새로운 객체를 생성합니다. 힘의 차이.

**올바른 접근 방식:**
- `StyleSheet.create` 또는 `const style = { ... }` 외부 구성요소.

---
---

## 7. 품질 체크리스트

**성능:**
- [ ] **헤르메스:** 활성화되었습니다.
- [ ] **메모:** `useMemo`/`useCallback` 고가의 소품에 사용됩니다.
- [ ] **목록:** `FlatList` 대신 `FlashList`이 사용되었습니다.

**아키텍처:**
- [ ] **새 아치:** Fabric/TurboModule이 활성화되었습니다(라이브러리가 지원하는 경우).
- [ ] **내비게이션:** 기본 화면이 사용되었습니다(React Navigation / Expo Router).

**기본:**
- [ ] **권한:** 정상적으로 처리됩니다(거부해도 충돌하지 않음).
- [ ] **업그레이드:** React Native 버전이 최신 버전입니다(2개의 마이너 버전 이내).

## 안티 패턴

### 아키텍처 안티 패턴

- **브리지 남용**: 기존 아키텍처 브리지의 과도한 사용 - 새 아키텍처로 마이그레이션
- **불필요한 네이티브**: 네이티브로 래핑된 순수 JS 로직 - 단순하게 유지하세요.
- **상태 관리 무질서**: 여러 충돌 상태 솔루션 - 하나로 표준화
- **탐색 중첩**: 깊게 중첩된 탐색기 - 탐색을 얕게 유지

### 성능 방지 패턴

- **모든 것을 다시 렌더링**: React.memo 또는 최적화 없음 - 구성 요소 다시 렌더링 최적화
- **FlatList 남용**: 모든 목록에 FlatList 사용 - 적절한 목록 구성 요소 사용
- **메모리 누수**: 구독을 정리하지 않음 - useEffect에서 정리 사용
- **브리지 병목 현상**: 무거운 브리지 통신 - 크로스 브리지 통화 최소화

### 개발 안티 패턴

- **프로덕션의 디버그 모드**: 프로덕션용으로 빌드하지 않음 - 항상 프로덕션 빌드를 테스트하세요.
- **No Hermes**: Hermes 엔진을 사용하지 않음 - 더 나은 성능을 위해 활성화
- **대형 번들**: 번들 최적화 없음 - RAM 번들 및 압축 사용
- **수동 링크**: 필요하지 않은 경우 수동 기본 링크 - 자동 링크 사용

### 안티 패턴 테스트

- **E2E 테스트 없음**: 단위 테스트만 수행 - Maestro 또는 Detox 테스트 추가
- **플랫폼 조건**: 플랫폼 확인이 너무 많음 - 추상적인 플랫폼 차이
- **하드코딩된 크기**: 고정된 픽셀 값 - 상대 크기 조정 사용
- **testID 누락**: 접근성 식별자 없음 - 테스트를 위해 testID를 추가하세요.