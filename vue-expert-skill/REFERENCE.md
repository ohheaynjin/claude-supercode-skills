# Vue Expert - 기술 참조

## 개발 워크플로

### 프로젝트 설정
- Vite 또는 Vue CLI를 사용하여 Vue 3 프로젝트 초기화
- 엄격한 유형 검사로 TypeScript를 구성합니다.
- 상태 관리를 위한 Pinia 설정
- 적절한 경로 가드를 사용하여 Vue 라우터를 구현합니다.
- Vue Test Utils를 사용한 테스트를 위해 Vitest를 구성합니다.

### 부품 개발
- Composition API와 함께 단일 파일 구성 요소를 사용합니다.
- 소품 및 방출을 위한 적절한 TypeScript 인터페이스를 구현합니다.
- 공유 로직을 위한 재사용 가능한 컴포저블 생성
- 디버깅 및 성능 분석을 위해 Vue DevTools를 사용합니다.
- Vue Test Utils를 사용하여 구성 요소 테스트 구현

### 상태 관리
- 적절한 TypeScript 타이핑으로 Pinia 매장을 디자인합니다.
- 액션과 게터를 사용해 적절한 데이터 흐름을 구현합니다.
- 재사용 가능한 스토어 로직을 위해 스토어 컴포저블을 사용합니다.
- 플러그인을 사용하여 지속성 전략 구현
- Vue DevTools로 상태 변경을 모니터링합니다.

## 해결된 문제 영역

- 단일 페이지 애플리케이션의 복잡한 상태 관리
- 반응형 애플리케이션의 성능 최적화
- 구성 요소 통신 및 데이터 흐름 문제
- 클라이언트 측 렌더링 애플리케이션을 위한 SEO 최적화
- 타사 라이브러리 및 API와의 통합

## 반응성 시스템 심층 분석

### 참조 대 반응형

**ref** - 기본 값과 필요할 때 가장 적합합니다.`.value`입장:
```typescript
const count = ref(0)
const name = ref('John')
count.value++ // Access with .value
```
**반응형** - 복잡한 객체에 가장 적합:
```typescript
const user = reactive({
  name: 'John',
  age: 30,
  address: { city: 'NYC' }
})
user.name = 'Jane' // Direct property access
```
### 구조 분해를 위한 toRefs

반응형 객체를 구조분해할 때 다음을 사용하세요.`toRefs`반응성을 유지하기 위해:
```typescript
const user = reactive({ name: 'John', age: 30 })

// BAD - loses reactivity
const { name, age } = user

// GOOD - maintains reactivity
const { name, age } = toRefs(user)
console.log(name.value) // Still reactive!
```
### 계산된 속성

반응 값에 따라 파생된 상태에 대해 계산된 값을 사용합니다.
```typescript
const firstName = ref('John')
const lastName = ref('Doe')

const fullName = computed(() => `${firstName.value} ${lastName.value}`)
```
### 감시 및 WatchEffect

**감시** - 명시적인 종속성, 이전/새 값에 대한 액세스:
```typescript
watch(count, (newValue, oldValue) => {
  console.log(`Count changed from ${oldValue} to ${newValue}`)
}, { immediate: true, deep: true })
```
**watchEffect** - 종속성을 자동 추적합니다.
```typescript
watchEffect(() => {
  console.log(`Count is now: ${count.value}`)
  // Automatically re-runs when count changes
})
```
## 피니아 매장 패턴

### 구문 저장소 설정(권장)
```typescript
export const useUserStore = defineStore('user', () => {
  // State
  const user = ref<User | null>(null)
  const loading = ref(false)
  
  // Getters
  const isAuthenticated = computed(() => !!user.value)
  
  // Actions
  const login = async (credentials: LoginCredentials) => {
    loading.value = true
    try {
      user.value = await userService.login(credentials)
    } finally {
      loading.value = false
    }
  }
  
  return { user, loading, isAuthenticated, login }
})
```
### 매장 구성
```typescript
// Composing stores together
export const useCartStore = defineStore('cart', () => {
  const userStore = useUserStore()
  
  const canCheckout = computed(() => 
    userStore.isAuthenticated && items.value.length > 0
  )
})
```
## Vue 라우터 패턴

### 루트 가드
```typescript
router.beforeEach(async (to, from) => {
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
})
```
### 동적 경로
```typescript
const routes = [
  { path: '/users/:id', component: UserProfile },
  { path: '/products/:category/:id?', component: ProductPage }
]
```
## Nuxt.js 세부 사항

### 파일 기반 라우팅
```
pages/
├── index.vue          → /
├── about.vue          → /about
├── users/
│   ├── index.vue      → /users
│   └── [id].vue       → /users/:id
└── [...slug].vue      → catch-all route
```
### useFetch 및 useAsyncData
```typescript
// Auto-cached, SSR-friendly data fetching
const { data, pending, error, refresh } = await useFetch('/api/users')

// With options
const { data } = await useFetch('/api/users', {
  key: 'users',
  lazy: true,
  server: true,
  transform: (data) => data.users
})
```
### 서버 API 경로
```typescript
// server/api/users.get.ts
export default defineEventHandler(async (event) => {
  const query = getQuery(event)
  return await db.users.findMany({ take: query.limit })
})
```
## 성능 최적화 기술

### 목록 최적화를 위한 v-memo
```vue
<template>
  <div v-for="item in items" :key="item.id" v-memo="[item.selected]">
    <!-- Only re-renders when item.selected changes -->
  </div>
</template>
```
### 코드 분할을 위한 정의AsyncComponent
```typescript
const HeavyComponent = defineAsyncComponent(() =>
  import('./HeavyComponent.vue')
)
```
### 가상 스크롤
```vue
<template>
  <RecycleScroller
    :items="items"
    :item-size="50"
    v-slot="{ item }"
  >
    <ItemComponent :item="item" />
  </RecycleScroller>
</template>
```
## 타입스크립트 통합

### 유형화된 Prop과 방출
```typescript
interface Props {
  user: User
  isEditable?: boolean
}

interface Emits {
  (e: 'update:user', user: User): void
  (e: 'delete', id: string): void
}

const props = withDefaults(defineProps<Props>(), {
  isEditable: false
})
const emit = defineEmits<Emits>()
```
### 입력된 참조
```typescript
const inputRef = ref<HTMLInputElement | null>(null)
const componentRef = ref<InstanceType<typeof MyComponent> | null>(null)
```
### 일반 컴포저블
```typescript
function useAsyncData<T>(asyncFn: () => Promise<T>) {
  const data = ref<T | null>(null) as Ref<T | null>
  const error = ref<Error | null>(null)
  const pending = ref(false)
  
  // ... implementation
  
  return { data, error, pending }
}
```
