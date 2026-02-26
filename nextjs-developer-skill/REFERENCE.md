# Next.js 개발자 - 기술 참조

## 행동 특성

### 성능 우선
- 최고의 사용자 경험을 위해 핵심 웹 바이탈(LCP, FID, CLS)을 최적화합니다.
- 전략적 코드 분할 및 지연 로딩 구현
- 원활한 상호작용을 위해 React 18 동시 기능을 사용합니다.
- 이미지, 글꼴 및 타사 스크립트를 효과적으로 최적화합니다.
- 성과를 지속적으로 모니터링하고 측정합니다.

### SEO 우수성
- next-seo 또는 사용자 정의 메타데이터를 사용하여 포괄적인 SEO 메타데이터를 구현합니다.
- 적절한 제목 계층 구조로 의미론적 HTML을 생성합니다.
- 구조화된 데이터 및 스키마 마크업을 사용하여 검색 엔진에 최적화
- 적절한 URL 구조 및 라우팅 패턴 구현
- 애플리케이션 전반에 걸쳐 접근성(a11y) 준수 보장

### 개발자 경험
- 포괄적인 개발 도구 및 워크플로 설정
- 적절한 오류 경계 및 오류 처리 구현
- 재사용 가능한 구성요소 라이브러리 및 설계 시스템 생성
- 일관된 코드 패턴 및 규칙 설정
- 유형 안전성과 더 나은 DX를 위해 TypeScript를 활용합니다.

## 이상적인 시나리오

- **전자상거래**: 서버 측 렌더링을 통해 SEO에 최적화된 온라인 상점
- **콘텐츠 관리**: 블로그, 뉴스 사이트, 콘텐츠가 많은 애플리케이션
- **SaaS 플랫폼**: 인증 및 데이터 관리 기능을 갖춘 풀스택 애플리케이션
- **마케팅 웹사이트**: 고성능 랜딩 페이지 및 마케팅 퍼널
- **대시보드**: 복잡한 데이터 시각화를 갖춘 관리 패널
- **엔터프라이즈 애플리케이션**: 복잡한 비즈니스 로직을 갖춘 확장 가능한 웹 애플리케이션

### 해결된 문제 영역
- 성능 및 SEO 최적화 문제
- 풀스택 애플리케이션의 복잡한 상태 관리
- 데이터베이스 통합 및 데이터 동기화
- 인증 및 승인 패턴
- 타사 통합 및 API 관리

## 개발 워크플로

### 프로젝트 설정
- TypeScript 및 Tailwind CSS를 사용하여 Next.js 14+ 프로젝트를 초기화합니다.
- 코드 품질을 위해 ESLint, Prettier 및 Husky 구성
- 데이터베이스 관리를 위해 Prisma 또는 Drizzle ORM 설정
- 인증을 위해 NextAuth.js 또는 Clerk 구현
- 맞춤형 디자인 시스템으로 Tailwind CSS 구성

### 부품 개발
- Storybook을 사용하여 구성 요소 중심 개발을 사용합니다.
- 재사용 가능한 UI 구성 요소로 원자 디자인 구현
- 포괄적인 소품 인터페이스 및 문서 작성
- 접근 가능한 구성 요소에 Radix UI 또는 Shadcn/ui를 사용합니다.
- 처음부터 적절한 접근성(a11y)을 구현합니다.

### 성능 모니터링
- Next.js Analytics 및 Vercel Speed Insights 설정
- Core Web Vitals 모니터링 구현
- 자동화된 성능 테스트를 위해 Lighthouse CI를 사용합니다.
- @next/bundle-analyzer를 사용하여 번들 크기를 모니터링합니다.
- 성능 예산 및 알림 구현

## 캐싱 전략 선택
```
Data Fetching Caching Strategy
├─ Static data (rarely changes)
│   └─ ✅ Static Generation with ISR
│       • fetch(url, { next: { revalidate: 3600 } })
│       • Revalidate every hour
│       • Example: Blog posts, product catalog
│       • Cost: $0 (served from CDN)
│       • Performance: Instant (cached)
│
├─ Frequently changing data (minutes)
│   ├─ Public data (same for all users)
│   │   └─ ✅ Time-based revalidation
│   │       • fetch(url, { next: { revalidate: 60 } })
│   │       • Revalidate every 60 seconds
│   │       • Example: Stock prices, news feed
│   │
│   └─ User-specific data
│       └─ ✅ No caching
│           • fetch(url, { cache: 'no-store' })
│           • Always fresh data
│           • Example: User cart, personalized dashboard
│
├─ Real-time data (seconds)
│   └─ ⚠️ Client-side fetching
│       • Use SWR or React Query in Client Component
│       • WebSocket for live updates
│       • Example: Live chat, trading dashboard
│
└─ On-demand revalidation
    └─ ✅ Tag-based revalidation
        • fetch(url, { next: { tags: ['products'] } })
        • revalidateTag('products') in Server Action
        • Example: Admin updates trigger cache refresh
        • Performance: Instant after first load
```

**캐싱 전략 비교표:**

| 전략 | 신선도 | 비용 | 성과 | 사용 사례 |
|----------|------------|------|-------------|----------|
|`force-cache`(기본값) | 재검증까지 유효하지 않음 | $0 | 인스턴트(CDN) | 정적 콘텐츠 |
|`{ revalidate: 3600 }`| 최대 1시간 | $0 | 인스턴트(CDN) | 반정적(블로그, 제품) |
|`{ revalidate: 60 }`| 최대 1분 | 낮음 | 빠른 | 자주 업데이트되는(뉴스) |
|`no-store`| 항상 신선한 | 높음 | 느리게 | 사용자별(카트, 프로필) |
|`revalidateTag()`| 주문형 신선함 | 낮음 | 업데이트 후 빠른 속도 | 관리자가 트리거한 업데이트 |
| 클라이언트측(SWR) | 구성 가능 | 중간 | 오래된 재검증을 통해 속도 향상 | 대화형 대시보드 |

## 라우팅 패턴 선택
```
Complex Routing Needs
├─ Modal overlays (don't change URL)
│   └─ ✅ Intercepting Routes
│       • app/@modal/(.)photos/[id]/page.tsx
│       • Intercepts /photos/[id] when navigated from same route
│       • Direct URL access shows full page
│       • Example: Image lightbox, quick view
│
├─ Multiple content areas (dashboard)
│   └─ ✅ Parallel Routes
│       • app/@analytics/page.tsx
│       • app/@users/page.tsx
│       • Render multiple slots simultaneously
│       • Independent loading/error states
│
├─ Conditional rendering based on auth
│   └─ ✅ Route Groups + Layouts
│       • app/(auth)/login/page.tsx
│       • app/(auth)/layout.tsx (no auth UI)
│       • app/(dashboard)/layout.tsx (with nav)
│       • Groups don't affect URL
│
└─ Loading states during navigation
    └─ ✅ Streaming with loading.tsx
        • app/products/loading.tsx
        • Automatic Suspense boundary
        • Progressive page rendering
```

## 유형 안전 모범 사례

- **End-to-End 유형**: 프런트엔드와 백엔드 간에 유형을 공유합니다.
- **API 유형**: API 응답에서 유형을 생성합니다.
- **데이터베이스 유형**: 데이터베이스 엔터티에 대해 ORM 생성 유형을 사용합니다.
- **구성요소 속성**: 모든 구성요소 인터페이스를 강력하게 입력합니다.
- **서버 작업**: 적절한 입력/출력 유형으로 서버 작업을 입력합니다.