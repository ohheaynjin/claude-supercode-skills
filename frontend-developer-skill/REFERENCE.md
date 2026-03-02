# 프론트엔드 개발자 - 기술 참조

## 작업 흐름 1: 모범 사례를 사용하여 새 React 프로젝트 설정

**목표:** 30분 이내에 TypeScript, 테스트, Linting 및 상태 관리 기능을 갖춘 프로덕션용 부트스트랩 React 앱을 개발합니다.

### 1단계: Vite로 프로젝트 초기화
```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
```
### 2단계: 상태 관리 설정(Zustand)
```bash
npm install zustand
```


```typescript
// src/store/useAppStore.ts
import { create } from 'zustand';

interface AppState {
  user: User | null;
  setUser: (user: User | null) => void;
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  theme: 'light',
  toggleTheme: () => set((state) => ({ 
    theme: state.theme === 'light' ? 'dark' : 'light' 
  })),
}));
```
### 3단계: 서버 상태에 대한 TanStack 쿼리 설정
```bash
npm install @tanstack/react-query
```


```typescript
// src/main.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      retry: 1,
    },
  },
});

ReactDOM.createRoot(document.getElementById('root')!).render(
  <QueryClientProvider client={queryClient}>
    <App />
  </QueryClientProvider>
);
```
### 4단계: 테스트 설정(Vitest + 테스트 라이브러리)
```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom @vitest/ui jsdom
```


```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
  },
});
```
### 5단계: Linting 설정(ESLint + Prettier)
```bash
npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
npm install -D prettier eslint-config-prettier eslint-plugin-prettier
```
### 6단계: Tailwind CSS 추가
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```
**예상 결과:**
- Vite(빠른 HMR)를 사용한 TypeScript 지원 React 프로젝트
- 클라이언트 상태를 위한 Zustand, 서버 상태를 위한 TanStack Query
- 테스트용으로 구성된 Vitest
- 코드 품질을 위한 ESLint + Prettier
- 빠른 스타일링을 위한 Tailwind CSS

**확인:**
```bash
npm run dev        # Dev server starts
npm run test       # Tests pass
npm run lint       # No errors
npm run build      # Production build succeeds
```
## 작업 흐름 2: 제작을 위한 번들 크기 최적화

**목표:** 프로덕션 번들을 500KB 이상에서 <200KB(gzipped)로 줄입니다.

### 1단계: 현재 번들 분석
```bash
npm install -D rollup-plugin-visualizer
```


```typescript
// vite.config.ts
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    react(),
    visualizer({ open: true, gzipSize: true })
  ],
});
```
### 2단계: 코드 분할 구현
```typescript
// src/App.tsx - Route-based code splitting
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Profile = lazy(() => import('./pages/Profile'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```
### 3단계: 무거운 종속성 교체
```bash
# Before: moment.js (70KB) → After: date-fns (2KB per function)
npm uninstall moment
npm install date-fns

# Before: lodash (entire lib) → After: lodash-es (tree-shakeable)
npm uninstall lodash
npm install lodash-es
```


```typescript
// Before
import _ from 'lodash';
_.debounce(fn, 300);

// After (tree-shakeable)
import { debounce } from 'lodash-es';
debounce(fn, 300);
```
### 4단계: 빌드 최적화 구성
```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'ui-vendor': ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu'],
        },
      },
    },
    chunkSizeWarningLimit: 600,
  },
});
```
**예상 결과:**
- 메인 번들: <100KB(gzipped)
- 공급업체 청크: 총 <150KB
- 경로 청크: 각각 20-50KB
- 총 초기 로드: <200KB

## 스크립트 참조

### React 구성요소 스캐폴딩
```bash
ts-node scripts/scaffold_component.tsx <ComponentName> [OPTIONS]
# Options:
# --hooks=<hooks>: Include hooks (useState,useEffect,useCallback)
# --props=<json>: Component props as JSON
# --styles=<type>: CSS type (css, styled-components, emotion, module)
# --no-test: Skip test file generation
```
### 상태 관리 설정
```bash
ts-node scripts/setup_state.ts <stateName> <type>
# Types: redux, zustand, context, jotai, recoil
```
### API 클라이언트 생성
```bash
ts-node scripts/create_api_client.ts <clientType>
# Client types: axios, fetch
```
### 테스트 설정
```bash
ts-node scripts/setup_testing.ts <framework>
# Frameworks: jest, vitest, playwright
```
### 빌드 최적화
```bash
ts-node scripts/optimize_build.ts <bundler>
# Bundlers: vite, webpack
```
### 배포 스크립트
```bash
./scripts/deploy.sh [OPTIONS]
# Options:
# --skip-tests: Skip test execution
# --skip-quality: Skip linting/formatting
# --platform <vercel|netlify|s3|github>: Deployment platform
```
## 참고자료

### 반응 패턴(`references/react_patterns.md`)
- 후크가 있는 기능성 구성 요소
- 컨테이너/프레젠테이션 패턴
- 고차 부품(HOC)
- 맞춤형 후크
- 상태 관리 패턴
- 성능 최적화
- 테스트 패턴
- 오류 처리(오류 경계)
- 양식 처리
- 접근성

### 상태 관리(`references/state_management.md`)
- Redux 툴킷
- 주스탄
- 컨텍스트 API
- 조타이
- 반동
- 비교표
- 언제 무엇을 사용할 것인가
- 모범 사례
- 코드 예시

### 성능 가이드(`references/performance_guide.md`)
- 핵심 웹 바이탈(LCP, FID, CLS)
- 코드 분할(경로 기반, 컴포넌트 기반)
- 나무 흔들기
- 번들 최적화
- 메모리 관리
- 이미지 최적화
- 글꼴 최적화
- 렌더링 최적화(가상화, 메모이제이션)
- 네트워크 최적화
- 성능 모니터링