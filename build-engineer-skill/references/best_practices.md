# 빌드 엔지니어 - 모범 사례

이 가이드에서는 빌드 시스템 구성, 최적화, 코드 분할 및 배포에 대한 모범 사례를 간략하게 설명합니다.

## 핵심 원칙

### 빠른 빌드

- 캐싱 활성화(파일 시스템, Babel 캐시, 영구 캐시)
- 가능한 경우 병렬 처리를 사용합니다.
- 오버헤드를 최소화하기 위해 빌드 구성 최적화
- 현대적이고 빠른 번들러(Vite, esbuild, Turbopack) 사용
- 빌드 시간 모니터링 및 병목 현상 최적화

### 소형 번들

- 코드 분할 전략 구현
- 트리쉐이크 미사용 코드
- 압축 출력(축소, gzip, brotli)
- 지연 로딩을 위해 동적 임포트 사용
- 정기적으로 번들 크기를 분석합니다.
- 사용하지 않는 종속성을 제거합니다.

### 개발자 경험

- 빠른 HMR(핫 모듈 교체)
- 소스 맵으로 오류 메시지 지우기
- 손쉬운 로컬 개발 설정
- API 호출을 위한 프록시 구성
- 환경변수 관리
- 디버깅을 위한 소스 맵 생성

## 빌드 도구 선택

### 도구 비교

| 도구 | 강점 | 사용 사례 |
|------|-------------|------------|
| 웹팩 | 고도로 구성 가능한 거대한 생태계 | 복잡한 빌드, 레거시 프로젝트 |
| VITE | 빠르고, HMR, 간단한 구성 | 최신 프로젝트, Vue/React |
| 에스빌드 | 매우 빠르고 최소한의 구성 | 프로덕션 빌드, 간단한 프로젝트 |
| 터보팩 | 차세대 Rust 기반 | 성능이 중요한 새 프로젝트 |
| 롤업 | 도서관에 적합 | 패키지/라이브러리 개발 |
| 소포 | 제로 구성, 빠른 | 빠른 프로토타이핑, 소규모 프로젝트 |

### 각각을 사용해야 하는 경우

- **Webpack**: 복잡한 엔터프라이즈 애플리케이션, 레거시 마이그레이션
- **Vite**: 최신 웹 앱, Vue/React 프로젝트, DX 우선순위
- **esbuild**: 프로덕션 빌드, 성능이 중요하고 간단한 설정
- **터보팩**: 새로운 프로젝트, 성능 실험, 얼리 어답터
- **롤업**: 라이브러리/패키지 개발, 트리 쉐이킹 포커스
- **소포**: 빠른 프로토타입, 학습 프로젝트, 구성 필요 없음

## 웹팩 구성

### 최적화

#### 성능
```javascript
module.exports = {
  cache: {
    type: 'filesystem',
    cacheDirectory: '.webpack_cache',
  },
  parallelism: true, // Use all CPU cores
  stats: {
    preset: 'minimal', // Reduce output
  },
}
```
#### 코드 분할
```javascript
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
  },
}
```
### 로더
```javascript
module.exports = {
  module: {
    rules: [
      {
        test: /\.(ts|tsx)$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
}
```
## Vite 구성

### 최적화

#### 빌드 옵션
```typescript
export default defineConfig({
  build: {
    minify: 'terser',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
        },
      },
    },
  },
})
```
#### 성능
```typescript
export default defineConfig({
  optimizeDeps: {
    include: ['react', 'react-dom'],
  },
  server: {
    hmr: {
      overlay: true,
    },
  },
})
```
### 플러그인
```typescript
import react from '@vitejs/plugin-react';
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    react(),
    visualizer({
      open: false,
      gzipSize: true,
    }),
  ],
})
```
## 코드 분할 전략

### 경로 기반 분할

- 지연 로드 경로 구성요소
- React.lazy() 또는 이와 유사한 것을 사용하십시오.
- 장점: 빠른 초기 로드, 병렬 다운로드
```typescript
const Home = lazy(() => import('./pages/Home'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
```
### 구성요소 기반 분할

- 게으른 로드가 많은 구성 요소
- 동적 가져오기 사용
- 장점: 요청 시 구성요소 로드
```typescript
const HeavyChart = lazy(() => import('./components/HeavyChart'));
```
### 공급업체 분할

- 별도의 타사 라이브러리
- 공급업체 청크를 별도로 캐시합니다.
- 이점: 캐싱 개선, 재구축 속도 향상
```javascript
// Webpack
splitChunks: {
  cacheGroups: {
    vendor: {
      test: /[\\/]node_modules[\\/]/,
      name: 'vendors',
    },
  },
}
```
### 라이브러리 분할

- 대규모 라이브러리 분할(React, Vue 등)
- 가능한 경우 CDN에서 로드
- 장점: 더 작은 번들, CDN 캐싱

## 캐싱 전략

### 웹팩 캐싱

#### 파일 시스템 캐시
```javascript
module.exports = {
  cache: {
    type: 'filesystem',
    cacheDirectory: '.webpack_cache',
    maxAge: 604800000, // 1 week
  },
}
```
#### 바벨 캐시
```javascript
{
  test: /\.(js|jsx)$/,
  use: {
    loader: 'babel-loader',
    options: {
      cacheDirectory: true,
    },
  },
}
```
### Vite 캐싱
```typescript
export default defineConfig({
  cacheDir: './node_modules/.vite',
  optimizeDeps: {
    force: false, // Only re-optimizes on change
  },
})
```
### 영구 캐시

- 브라우저 캐싱 헤더 사용
- 서비스 워커 구현
- 정적 자산에 CDN 캐싱 사용
- 적절한 캐시 시간 초과 설정
- 콘텐츠 해시가 포함된 캐시 무효화

## 생산 최적화

### 축소

- JavaScript 축소를 위해 Terser를 사용하세요.
- CSS 최적화를 위해 cssnano 사용
- 데드 코드 제거 활성화
- 프로덕션에서 console.log 제거
- html-minifier로 HTML을 축소하세요

### 자산 최적화

- 이미지 압축(ImageMin, imagemin)
- 최신 이미지 형식(WebP, AVIF) 사용
- SVG 최적화(svgo)
- 글꼴 하위 설정
- 유익한 경우 인라인 소액 자산

### 번들 분석

- webpack-bundle-analyzer를 사용하세요.
- Vite용 롤업 플러그인 시각화 도구 사용
- 번들 크기 구성 분석
- 큰 의존성 식별
- 최적화 기회 찾기
```javascript
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer');

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      openAnalyzer: false,
    }),
  ],
}
```
## 개발 경험

### 핫 모듈 교체(HMR)

- 빠른 피드백을 위해 HMR을 활성화합니다.
- 가능한 경우 HMR 중에 상태를 보존합니다.
- 빌드 오류에 오버레이 사용
- HMR 시간 제한을 적절하게 구성합니다.
- HMR 오류를 정상적으로 처리

### 개발 서버 구성
```javascript
// Webpack
devServer: {
  port: 3000,
  hot: true,
  open: false,
  proxy: {
    '/api': {
      target: 'http://localhost:4000',
      changeOrigin: true,
    },
  },
}

// Vite
server: {
  port: 3000,
  open: false,
  proxy: {
    '/api': {
      target: 'http://localhost:4000',
      changeOrigin: true,
    },
  },
}
```
### 소스 맵

- 사용`source-map`생산을 위해
- 사용`eval-source-map`개발을 위해
- 프로덕션 번들에서 소스 맵 제외
- 소스 맵 호스팅 구성
- 보안에 미치는 영향을 고려하세요.

## 성능 모니터링

### 빌드 시간 모니터링

- CI/CD에서 빌드 시간 추적
- 빌드 시간 저하에 대한 경고
- 느린 빌드 단계 최적화
- 빌드 시간을 줄이기 위한 캐시 종속성
- 빌드 시간 회귀 모니터링

### 번들 크기 모니터링

- 시간 경과에 따른 번들 크기 추적
- 크기 증가에 대한 경고
- 구성에서 크기 예산 설정
- 개별 청크 크기 모니터링
- 총 번들 크기 추적

### 런타임 성능

- 대화형 시간 모니터링(TTI)
- 등대 점수 추적
- 핵심 웹 바이탈 모니터링
- JavaScript 실행 시간 추적
- 번들 구문 분석 시간 모니터링

## 종속성 관리

### 종속성 감사
```bash
# Check for vulnerabilities
npm audit

# Fix vulnerabilities
npm audit fix

# Check outdated packages
npm outdated

# Update packages
npm update
```
### 종속성 최적화

- 사용하지 않는 종속성을 제거합니다.
- 가능하면 더 작은 대안을 사용하십시오.
- 중요한 종속성을 묶음
- 조건부 가져오기에 트리 쉐이킹 사용
- 대규모 라이브러리에는 CDN을 고려하세요.

## 환경 구성

### 환경 변수

- 로컬 개발을 위해 .env 파일 사용
- 빌드에서 환경 변수 로드
- 문서에 필요한 변수
- 시작 시 구성 유효성을 검사합니다.
- .env 파일을 커밋하지 마세요.

### 다중 환경 구성
```javascript
// webpack.config.js
const isProduction = process.env.NODE_ENV === 'production';

module.exports = {
  mode: isProduction ? 'production' : 'development',
  // Environment-specific config
};
```
## 빌드 구성 테스트

### 구성 검증

- 여러 환경에서 테스트 구성
- 모든 플러그인이 올바르게 로드되는지 확인
- 로더가 파일을 확인하는지 확인
- 샘플 파일로 테스트
- 소스 맵 생성 검증

### 빌드 테스트

- 로컬에서 테스트 프로덕션 빌드
- 모든 자산이 생성되었는지 확인
- 스테이징 환경에서 테스트
- 실제 사용자 데이터로 테스트
- CDN 업로드가 작동하는지 확인

## CI/CD 통합

### 빌드 캐싱
```yaml
# GitHub Actions example
- name: Cache node modules
  uses: actions/cache@v2
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```
### 병렬 빌드

- 테스트를 실행하고 병렬로 빌드
- 여러 구성에 매트릭스 빌드를 사용하세요.
- 긴 빌드를 여러 단계로 분할
- 단계 간 빌드 아티팩트 사용

### 배포 자동화

- 성공적인 빌드 시 자동 배포
- 배포 실패 시 롤백
- 블루-그린 배포 전략
- 점진적인 출시를 위한 Canary 릴리스
- 트래픽 라우팅 전 상태 점검

## 보안 모범 사례

### 소스 맵 보안

- 프로덕션 환경에서 전체 소스 맵을 노출하지 마세요.
- 오류 추적 서비스에 소스 맵 업로드
- 필요할 때 숨겨진 소스 맵을 사용하세요
- 보안에 미치는 영향을 고려하세요.

### 종속성 보안

- 종속성을 정기적으로 감사합니다.
- 취약점을 즉시 수정
- 종속성 라이센스 검토
- 알림을 받으려면 Snyk 또는 dependencyabot을 사용하세요.
- CI/CD에서 종속성을 자동으로 패치합니다.

### 빌드 환경 보안

- 격리된 빌드 환경 사용
- 빌드 출력에 비밀을 노출하지 마세요.
- 환경 변수를 위생적으로 처리합니다.
- 안전한 유물 저장소 사용
- 번들에 비밀이 없는지 확인

## 문서

### 빌드 문서

- 문서 구축 구성 결정
- 복잡한 최적화 설명
- 문서 종속성 근거
- 문제 해결 단계 포함
- 문서 환경 요구 사항

### 빌드를 위한 README

- 구축을 위한 빠른 시작 가이드
- 개발 워크플로
- 프로덕션 빌드 지침
- 일반적인 문제 및 해결 방법
- 환경 변수 문서화
- 배포 지침

## 빌드 문제 해결

### 일반적인 패턴

- **느린 빌드**: 캐싱 활성화, 불필요한 플러그인 확인
- **대형 번들**: 번들 분석기로 분석, 분할 구현
- **HMR이 작동하지 않음**: WebSocket을 확인하고 구성을 확인하세요.
- **캐싱 문제**: 캐시 지우기, 권한 확인
- **소스 맵**: 생성 확인, 경로 확인
- **프록시 문제**: 백엔드가 실행 중인지 확인하고 CORS를 확인하세요.

### 디버그 도구

- 사용`--display-modules`웹팩용
- Vite용 번들 분석기 사용
- 통찰력을 얻기 위해 웹팩 통계를 확인하세요.
- 런타임 디버깅을 위해 브라우저 DevTools 사용
- 자산 로딩을 위한 네트워크 탭 모니터링

## 지속적인 개선

### 정기 검토

- 매주 번들 크기를 검토하세요.
- 월별 빌드 시간 분석
- 분기별 종속성 업데이트 검토
- 정기적으로 도구 및 플러그인 업데이트
- 새로운 최적화 기술 모니터링

### 성과예산
```javascript
// webpack.config.js
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin({
      defaultSizes: 'gzip',
      analyzerMode: 'static',
      generateStatsFile: true,
      statsOptions: { source: false },
    }),
  ],
  performance: {
    hints: false,
    maxEntrypointSize: 512000, // 500 KB
    maxAssetSize: 512000, // 500 KB
  },
}
```
### 오류로부터 배우기

- 문서 작성 오류 및 해결 방법
- 내부 지식 베이스 생성
- 팀과 솔루션 공유
- 일반적인 문제를 기반으로 스크립트 업데이트
- 도구 커뮤니티에 다시 기여