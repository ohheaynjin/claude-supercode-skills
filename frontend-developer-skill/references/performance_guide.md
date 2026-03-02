# 프론트엔드 성능 가이드

## 핵심 웹 바이탈

### 콘텐츠가 포함된 최대 페인트(LCP)

**목표:** < 2.5초

LCP는 뷰포트에 표시되는 가장 큰 콘텐츠 요소의 로딩 성능을 측정합니다.
```typescript
// Optimize LCP
// 1. Remove render-blocking resources
<link rel="preload" href="critical.css" as="style">
<link rel="preconnect" href="https://fonts.googleapis.com">

// 2. Lazy load images
<img 
  loading="lazy" 
  src="image.jpg" 
  alt="Description"
/>

// 3. Use modern image formats
<picture>
  <source type="image/webp" srcset="image.webp">
  <source type="image/jpeg" srcset="image.jpg">
  <img src="image.jpg" alt="Description">
</picture>
```
### 첫 번째 입력 지연(FID)

**목표:** < 100밀리초

FID는 사용자가 페이지와 처음 상호작용하는 시간부터 브라우저가 응답하는 시간까지의 시간을 측정합니다.
```typescript
// Minimize JavaScript execution
// 1. Code split by routes
const Dashboard = lazy(() => import('./Dashboard'));

// 2. Reduce main thread work
// Avoid long-running synchronous operations
const heavyTask = () => {
  // BAD: Blocks main thread
  for (let i = 0; i < 1000000; i++) {
    processItem(i);
  }
};

// GOOD: Use Web Workers or break into chunks
const chunkedTask = async () => {
  for (let i = 0; i < 100; i++) {
    await new Promise(resolve => requestAnimationFrame(resolve));
    processItem(i);
  }
};

// 3. Debounce event handlers
const debounce = <T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): ((...args: Parameters<T>) => void) => {
  let timeoutId: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
};

const handleInput = debounce((value: string) => {
  // Expensive operation
}, 300);
```
### 누적 레이아웃 변경(CLS)

**목표:** < 0.1

CLS는 로드되는 페이지 레이아웃의 안정성을 측정합니다.
```typescript
// Reserve space for dynamic content
// BAD
<div>
  <img src="image.jpg" alt="" />
</div>

// GOOD
<div style={{ width: '300px', height: '200px' }}>
  <img src="image.jpg" alt="" />
</div>

// Use skeleton loading
<SkeletonLoader width="100%" height="200px" />

// Avoid injecting content above existing content
// BAD
setTimeout(() => {
  document.body.insertBefore(newElement, existingElement);
}, 1000);

// GOOD
const container = useRef<HTMLDivElement>(null);
useEffect(() => {
  if (container.current) {
    container.current.appendChild(newElement);
  }
}, []);
```
## 코드 분할

### 경로 기반 분할
```typescript
import { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';

// Lazy load routes
const Home = lazy(() => import('./pages/Home'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

// Add loading fallback
function App() {
  return (
    <Suspense fallback={<PageLoader />}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```
### 구성요소 기반 분할
```typescript
import { lazy, Suspense } from 'react';

const HeavyChart = lazy(() => import('./HeavyChart'));

export const Dashboard: React.FC = () => {
  const [showChart, setShowChart] = useState(false);

  return (
    <div>
      <button onClick={() => setShowChart(true)}>Show Chart</button>
      {showChart && (
        <Suspense fallback={<LoadingSpinner />}>
          <HeavyChart />
        </Suspense>
      )}
    </div>
  );
};
```
## 나무 흔들기

### 적절한 수입품
```javascript
// BAD - Imports entire library
import _ from 'lodash';

// GOOD - Import only what's needed
import { debounce, throttle } from 'lodash';

// EVEN BETTER - Use tree-shakeable libraries
import { debounce } from 'lodash-es';
```
### 동적 가져오기
```typescript
// Load heavy libraries only when needed
const loadChart = async () => {
  const { Chart } = await import('chart.js');
  // Use Chart
};
```
## 번들 최적화

### 웹팩 구성
```javascript
// webpack.config.js
module.exports = {
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          priority: 10,
        },
        common: {
          minChunks: 2,
          priority: 5,
          reuseExistingChunk: true,
        },
      },
    },
    runtimeChunk: 'single',
  },
};
```
### Vite 구성
```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          ui: ['@mui/material', '@mui/icons-material'],
        },
      },
    },
    chunkSizeWarningLimit: 1000,
  },
});
```
## 메모리 관리

### 정리 효과
```typescript
useEffect(() => {
  const timer = setInterval(() => {
    console.log('Tick');
  }, 1000);

  const abortController = new AbortController();

  fetch('/api/data', { signal: abortController.signal });

  // Cleanup
  return () => {
    clearInterval(timer);
    abortController.abort();
  };
}, []);
```
### 메모리 누수 방지
```typescript
// BAD - Accumulating data in state
export const List: React.FC = () => {
  const [items, setItems] = useState<Item[]>([]);

  useEffect(() => {
    const interval = setInterval(() => {
      // Keeps adding items without cleanup
      setItems(prev => [...prev, newItem]);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return <>{/* ... */}</>;
};

// GOOD - Limit data size
export const List: React.FC = () => {
  const [items, setItems] = useState<Item[]>([]);
  const MAX_ITEMS = 100;

  useEffect(() => {
    const interval = setInterval(() => {
      setItems(prev => {
        const newItems = [...prev, newItem];
        return newItems.length > MAX_ITEMS
          ? newItems.slice(-MAX_ITEMS)
          : newItems;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return <>{/* ... */}</>;
};
```
## 이미지 최적화

### 반응형 이미지
```typescript
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero Image"
  width={1920}
  height={1080}
  priority
  sizes="(max-width: 768px) 100vw, 50vw"
/>
```
### 지연 로딩
```typescript
<img
  loading="lazy"
  src="image.jpg"
  alt="Description"
  width="800"
  height="600"
/>
```
### 최신 형식
```typescript
<picture>
  <source type="image/avif" srcset="image.avif">
  <source type="image/webp" srcset="image.webp">
  <img src="image.jpg" alt="Description">
</picture>
```
## 글꼴 최적화

### 글꼴 로딩
```html
<!-- Preconnect to font domain -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- Preload critical fonts -->
<link rel="preload" 
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" 
      as="style">

<!-- Async load non-critical fonts -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" 
      rel="stylesheet">
```
### 글꼴 표시
```css
@font-face {
  font-family: 'Inter';
  src: url('inter.woff2') format('woff2');
  font-display: swap;
}
```
## 렌더링 최적화

### 가상화
```typescript
import { FixedSizeList } from 'react-window';

export const VirtualList: React.FC<{ items: any[] }> = ({ items }) => {
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
    <div style={style}>
      {items[index].name}
    </div>
  );

  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {Row}
    </FixedSizeList>
  );
};
```
### 메모
```typescript
// React.memo for components
export const ExpensiveComponent = React.memo(({ data }: { data: Data }) => {
  // Expensive rendering
  return <div>{/* ... */}</div>;
}, (prevProps, nextProps) => {
  return prevProps.data.id === nextProps.data.id;
});

// useMemo for expensive computations
const filteredData = useMemo(() => {
  return data.filter(item => item.isActive);
}, [data]);

// useCallback for stable function references
const handleClick = useCallback(() => {
  console.log('Clicked');
}, []);
```
## 네트워크 최적화

### 일괄 요청
```typescript
// BAD - Individual requests
const fetchData = async () => {
  const user1 = await fetch('/api/users/1');
  const user2 = await fetch('/api/users/2');
  const user3 = await fetch('/api/users/3');
};

// GOOD - Batched request
const fetchData = async () => {
  const response = await fetch('/api/users?ids=1,2,3');
  return response.json();
};
```
### 디바운싱 요청
```typescript
const debounce = <T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): ((...args: Parameters<T>) => void) => {
  let timeoutId: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
};

const handleSearch = debounce((query: string) => {
  fetch(`/api/search?q=${query}`);
}, 300);
```
## 성능 모니터링

### 웹 바이탈 측정
```typescript
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

export const reportWebVitals = (metric: any) => {
  // Send to analytics
  console.log(metric);
  
  // Send to monitoring service
  // analytics.track('Web Vitals', metric);
};

getCLS(reportWebVitals);
getFID(reportWebVitals);
getFCP(reportWebVitals);
getLCP(reportWebVitals);
getTTFB(reportWebVitals);
```
## 도구 및 리소스

- **Lighthouse**: 성능 감사를 위한 Chrome DevTools
- **WebPageTest**: 웹 성능 테스트 도구
- **Chrome DevTools**: 내장된 브라우저 성능 도구
- **번들 분석기**: 번들 크기 및 구성 분석
- **React DevTools**: React 구성 요소용 프로파일러

## 체크리스트

### 배포하기 전에
- [ ] Lighthouse 감사 실행
- [ ] 번들 크기 확인
- [ ] 느린 연결 테스트
- [ ] 지연 로딩이 작동하는지 확인
- [ ] 모바일 장치에서 테스트
- [ ] 핵심 웹 바이탈 확인
- [ ] 이미지 최적화
- [ ] JavaScript 최소화

### 지속적인 모니터링
- [ ] 핵심 웹 바이탈 추적
- [ ] 오류율 모니터링
- [ ] 사용자 참여 지표 추적
- [ ] API 성능 모니터링
- [ ] 번들 크기 변경 추적