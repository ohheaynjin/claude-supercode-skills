---
name: frontend-developer-skill
description: React, Vue, Angular 및 상태 관리, 테스트, 성능 최적화를 포함한 최신 도구를 사용하여 최신 웹 애플리케이션을 구축하기 위한 포괄적인 프런트엔드 개발 전문가
---
# 프론트엔드 개발자 스킬

## 목적

최신 프레임워크(React, Vue, Next.js), 포괄적인 도구 설정, 상태 관리 패턴, 테스트 인프라 및 성능 최적화 전략을 사용하여 프로덕션에 즉시 사용 가능한 웹 애플리케이션을 구축하기 위한 완전한 프런트엔드 개발 전문 지식을 제공합니다.

## 사용 시기

- 처음부터 새로운 React, Vue 또는 Angular 애플리케이션 구축
- 최신 프런트엔드 도구 설정(Vite, ESLint, Prettier, 테스트 프레임워크)
- Redux Toolkit, Zustand 또는 Context API를 사용하여 상태 관리 구현
- 토큰 관리 및 보호된 경로로 인증 흐름 구성
- 프로덕션 배포를 위한 번들 크기 및 성능 최적화
- 컴포넌트 라이브러리 및 디자인 시스템 생성
- 종합 테스트 설정(단위, 통합, E2E)

## 빠른 시작

**다음과 같은 경우에 이 스킬을 호출하세요:**
- React, Vue 또는 Angular 애플리케이션 구축
- 프런트엔드 도구 설정(Vite, ESLint, Prettier)
- 상태 관리 구현(Redux Toolkit, Zustand, Context)
- 인증 흐름 구성
- 번들 크기 및 성능 최적화
- 테스트 설정(Vitest, Jest, Playwright)

**다음과 같은 경우에는 호출하지 마세요.**
- 백엔드 API만 필요 → 백엔드 개발자 사용
- 데이터베이스 최적화 → 데이터베이스 최적화 도구 사용
- DevOps/배포만 해당 → devops-engineer 사용
- 코드 없이 UI/UX 디자인 → ui-designer 사용

## 의사결정 프레임워크

### 프레임워크 선택
```
Frontend Framework Selection
├─ New Project (greenfield)
│   ├─ Needs SEO + server-side rendering
│   │   ├─ Team knows React → Next.js 14+
│   │   ├─ Team knows Vue → Nuxt.js 3+
│   │   └─ Team flexible → Next.js (ecosystem advantage)
│   │
│   ├─ SPA without SSR requirements
│   │   ├─ React experience → React 18+ (Vite)
│   │   ├─ Vue experience → Vue 3 (Vite)
│   │   └─ Enterprise/complex forms → Angular 15+
│   │
│   └─ Static site (blog, docs)
│       └─ Astro, Next.js SSG, or Vite + React
│
└─ Existing Project
    └─ Continue with existing framework (consistency)
```
### 상태 관리 선택

| 시나리오 | 도서관 | 번들 크기 | 사용 사례 |
|------------|---------|-------------|----------|
| 간단한 로컬 상태 | useState, useReducer | 0KB | 구성요소 수준 상태 |
| 공유 상태(2~3개 구성 요소) | 컨텍스트 API | 0KB | 테마, 인증, 단순 글로벌 |
| 중간 규모 앱(슬라이스 10개 미만) | 주스탄 | ~1KB | 대부분의 앱, 우수한 DX |
| 대형 앱(슬라이스 10개 이상) | Redux 툴킷 | ~11KB | 엔터프라이즈, 시간 여행 디버그 |
| 서버 상태 | 탄스택 쿼리 | ~12KB | API 데이터, 캐싱 |

### 스타일링 접근 방식
```
Styling Decision
├─ Rapid prototyping → Tailwind CSS
├─ Component library → Radix UI + Tailwind
├─ Dynamic theming → CSS-in-JS (Styled Components, Emotion)
├─ Large team → CSS Modules or Tailwind + Design Tokens
└─ Performance-critical → Plain CSS / SCSS
```
## 모범 사례

1. **기능적 구성요소 사용** - Modern React 패턴
2. **후크 활용** - 가능하면 클래스 구성 요소를 피하세요.
3. **비용이 많이 드는 작업을 메모하세요** - useMemo, useCallback 사용
4. **지연 로드 구성 요소** - 초기 번들 크기 줄이기
5. **모든 것을 입력하세요** - TypeScript 활용
6. **철저한 테스트** - 단위, 통합, E2E 테스트
7. **이미지 최적화** - 최신 형식과 지연 로딩 사용
8. **오류 경계 구현** - 오류를 적절하게 포착합니다.
9. **접근 가능하도록 만들기** - ARIA 라벨, 키보드 탐색
10. **성능 모니터링** - 핵심 웹 바이탈 추적

## 일반적인 패턴

### 사용자 정의 후크
```typescript
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [url]);

  return { data, loading, error };
}
```
### 컨테이너/프레젠테이션
```typescript
// Presentational (dumb)
const UserList = ({ users, onUserClick }: UserListProps) => (
  <ul>
    {users.map(user => (
      <li key={user.id} onClick={() => onUserClick(user.id)}>
        {user.name}
      </li>
    ))}
  </ul>
);

// Container (smart)
const UserListContainer = () => {
  const { users, fetchUsers } = useUsers();
  useEffect(() => fetchUsers(), [fetchUsers]);
  return <UserList users={users} onUserClick={handleClick} />;
};
```
## 문제 해결

### 일반적인 문제

**상태가 업데이트되지 않음**
- 올바른 Setter를 사용하고 있는지 확인
- useEffect에서 종속성 배열 확인
- 구성요소가 다시 렌더링되는지 확인

**구성요소가 다시 렌더링되지 않음**
- 불필요한 재렌더링 확인
- 메모이제이션이 작동하는지 확인하세요.
- 소품 변경 사항 검토

**성능 문제**
- React DevTools를 사용한 프로필
- 묶음 크기가 큰지 확인하세요.
- 불필요한 재렌더링 검토
- 코드 분할 구현

**테스트 실패**
- 테스트 설정 확인
- 모의 구현 확인
- 비동기 처리 검토
- 적절한 청소를 보장합니다.

## 품질 체크리스트

### 아키텍처
- [ ] 프레임워크 선택이 타당함
- [ ] 상태 관리 지우기(서버와 클라이언트 상태 분리)
- [ ] 구성요소 구조 논리적
- [ ] 코드 분할 구현

### 코드 품질
- [ ] TypeScript 엄격 모드 활성화
- [ ] ESLint + Prettier 구성
- [ ] 중요한 경로에 대한 테스트가 존재합니다.
- [ ] 프롭 드릴링 없음(상태 관리 사용)

### 성능
- [ ] 번들 크기 최적화됨(<200KB gzip으로 압축됨)
- [ ] 값비싼 작업을 메모했습니다.
- [ ] 이미지 최적화(지연 로딩, WebP)
- [ ] 평가된 타사 라이브러리

### 테스트
- [ ] 테스트 프레임워크 구성됨
- [ ] 테스트된 중요 경로
- [ ] E2E 테스트가 존재합니다.

### 보안
- [ ] 환경변수 확보
- [ ] 입력 삭제
- [ ] 인증 토큰 보안
- [ ] 감사된 종속성

## 통합 패턴

### 반응 전문가
- **핸드오프:** 프론트엔드 개발자가 도구 설정 → 반응 전문가가 복잡한 구성요소 로직을 구현함
- **도구:** 둘 다 React를 사용합니다. 프론트엔드 개발자가 생태계 툴링을 처리합니다.

### nextjs-개발자
- **Handoff:** SSR/SEO가 필요한 경우 → Next.js 관련 기능을 위해 Handoff
- **도구:** 프론트엔드 개발자는 Vite/CRA를 사용합니다. nextjs-developer는 Next.js App Router를 사용합니다.

### 백엔드 개발자
- **Handoff:** 프론트엔드 개발자가 API 클라이언트 구현 → 백엔드 개발자가 API 계약 제공
- **도구:** 프론트엔드 개발자는 Axios/Fetch, TanStack Query를 사용합니다.

### 프론트엔드-UI-UX-엔지니어
- **핸드오프:** frontend-developer가 컴포넌트 구조 설정 → frontend-ui-ux-engine 스타일
- **도구:** 둘 다 React를 사용합니다. frontend-ui-ux-engineer, Framer Motion, Tailwind 디자인 토큰 추가

## 추가 리소스

- **자세한 기술 참조**: [REFERENCE.md](REFERENCE.md) 참조
- **코드 예제 및 패턴**: [EXAMPLES.md](EXAMPLES.md) 참조