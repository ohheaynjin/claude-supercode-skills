# React 전문가 - 기술 참조

## 행동 특성

### 성능 최적화
- React.memo, useMemo, useCallback을 전략적으로 구현
- 구성 요소 구성 및 상태 배치를 통해 다시 렌더링을 최적화합니다.
- 성능 분석을 위해 React DevTools Profiler를 활용합니다.
- 대규모 데이터 세트에 대한 가상 스크롤 및 지연 로딩 구현
- 번들 최적화를 위해 코드 분할 및 동적 가져오기를 사용합니다.

### 구성요소 아키텍처
- 명확한 계약을 통해 구성 가능하고 재사용 가능한 구성 요소 API를 설계합니다.
- 복잡한 UI를 위한 복합 구성요소 패턴 구현
- 유연성을 극대화하기 위해 헤드리스 UI 구성요소 생성
- 일관된 prop 인터페이스와 TypeScript 유형을 설정합니다.
- 렌더 소품 및 하위 소품 패턴을 효과적으로 구현합니다.

### 데이터 흐름 전문성
- 단방향 데이터 흐름 원리의 마스터
- 복잡한 상태 동기화 패턴 구현
- 커스텀 후크로 부작용을 깔끔하게 처리
- 서버와 클라이언트 상태 분리를 효과적으로 관리합니다.
- 전략적 캐싱 전략으로 네트워크 요청 최적화

## 사용 시기

### 이상적인 시나리오
- **최신 웹 애플리케이션**: SPA, PWA 및 복잡한 대화형 UI
- **전자상거래 플랫폼**: 장바구니, 제품 카탈로그, 결제 흐름
- **대시보드**: 실시간 데이터 시각화 및 분석
- **소셜 미디어 애플리케이션**: 피드, 메시징, 실시간 업데이트
- **관리자 패널**: 복잡한 양식, 데이터 테이블 및 관리 인터페이스

### 해결된 문제 영역
- 대규모 React 애플리케이션의 성능 병목 현상
- 복잡한 상태 관리 문제
- 서버-클라이언트 상태 동기화 문제
- 컴포넌트 리렌더링 최적화
- 번들 크기 관리 및 코드 분할

## 개발 워크플로

### 프로젝트 설정
- TypeScript 및 엄격 모드로 React 18+ 구성
- 최적의 개발 경험을 위해 Next.js App Router 또는 Vite를 설정합니다.
- React Testing Library 및 MSW를 이용한 테스트 구현
- ESLint로 Linting을 구성하고 Prettier로 형식을 지정합니다.
- 사전 커밋 후크 및 품질 게이트를 위해 Husky를 설정합니다.

### 부품 개발
- Storybook을 사용하여 구성 요소 중심 개발을 사용합니다.
- 확장 가능한 구성요소 아키텍처를 위한 원자적 설계 원칙을 구현합니다.
- 포괄적인 소품 유형 및 문서 작성
- 일관된 명명 규칙 및 파일 구성 설정
- 유연한 API를 위해 렌더링 소품과 복합 패턴을 사용합니다.

### 성능 최적화
- React Profiler 모니터링 및 분석 구현
- 코드 분할 및 지연 로딩을 전략적으로 사용
- 트리 쉐이킹 및 동적 가져오기를 통해 번들 크기 최적화
- 큰 목록에 대한 가상 스크롤 구현
- 재렌더링 패턴을 모니터링하고 최적화합니다.

## 워크플로: TanStack 쿼리를 사용하여 서버 상태 구현

**사용 사례:** 서버 데이터를 효율적으로 가져오고, 캐시하고, 동기화합니다.

### 1. TanStack 쿼리 설정
```bash
npm install @tanstack/react-query
```


```tsx
// App.tsx - Configure QueryClient
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000,  // Consider data fresh for 1 minute
      cacheTime: 5 * 60 * 1000,  // Keep in cache for 5 minutes
      retry: 3,  // Retry failed requests 3 times
      refetchOnWindowFocus: false,  // Don't auto-refetch on window focus
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Dashboard />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```
### 2. 기본 쿼리(GET 요청)
```tsx
import { useQuery } from '@tanstack/react-query';

interface User {
  id: number;
  name: string;
  email: string;
}

function UserProfile({ userId }: { userId: number }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['user', userId],  // Unique key for caching
    queryFn: async () => {
      const response = await fetch(`/api/users/${userId}`);
      if (!response.ok) throw new Error('Failed to fetch user');
      return response.json() as Promise<User>;
    },
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!data) return null;

  return (
    <div>
      <h1>{data.name}</h1>
      <p>{data.email}</p>
    </div>
  );
}

// Data automatically cached! Second mount uses cached data.
```
### 3. 돌연변이(POST/PUT/DELETE)
```tsx
import { useMutation, useQueryClient } from '@tanstack/react-query';

function UserForm() {
  const queryClient = useQueryClient();

  const createUser = useMutation({
    mutationFn: async (userData: Omit<User, 'id'>) => {
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData),
      });
      if (!response.ok) throw new Error('Failed to create user');
      return response.json();
    },
    onSuccess: () => {
      // Invalidate and refetch users list
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    createUser.mutate({
      name: formData.get('name') as string,
      email: formData.get('email') as string,
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="name" required />
      <input name="email" type="email" required />
      <button type="submit" disabled={createUser.isPending}>
        {createUser.isPending ? 'Creating...' : 'Create User'}
      </button>
      {createUser.isError && <p>Error: {createUser.error.message}</p>}
      {createUser.isSuccess && <p>User created!</p>}
    </form>
  );
}
```
### 4. 낙관적인 업데이트
```tsx
const updateUser = useMutation({
  mutationFn: async ({ id, ...data }: Partial<User> & { id: number }) => {
    const response = await fetch(`/api/users/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },
  
  onMutate: async (newUser) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: ['user', newUser.id] });

    // Snapshot previous value
    const previousUser = queryClient.getQueryData(['user', newUser.id]);

    // Optimistically update UI
    queryClient.setQueryData(['user', newUser.id], newUser);

    // Return context for rollback
    return { previousUser };
  },
  
  onError: (err, newUser, context) => {
    // Rollback on error
    if (context?.previousUser) {
      queryClient.setQueryData(
        ['user', newUser.id],
        context.previousUser
      );
    }
  },
  
  onSettled: (data, error, variables) => {
    // Refetch to ensure sync
    queryClient.invalidateQueries({ queryKey: ['user', variables.id] });
  },
});

// User sees instant update, rolls back if server fails
```
