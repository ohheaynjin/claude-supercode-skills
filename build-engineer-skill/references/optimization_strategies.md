# 최적화 전략 구축

## 개요

빠르고 효율적인 웹 애플리케이션을 제공하려면 빌드 최적화가 중요합니다. 이 가이드에서는 빌드 파이프라인 전반에 걸친 포괄적인 최적화 전략을 다룹니다.

## 코드 분할

### 경로 기반 분할
```typescript
import { lazy, Suspense } from 'react';

const Home = lazy(() => import('./pages/Home'));
const Dashboard = lazy(() => import('./pages/Dashboard'));

export const App = () => (
  <Suspense fallback={<Loading />}>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  </Suspense>
);
```
### 구성요소 기반 분할
```typescript
import { lazy, Suspense } from 'react';

const HeavyChart = lazy(() => import('./HeavyChart'));

export const Dashboard = () => {
  const [showChart, setShowChart] = useState(false);

  return (
    <div>
      <button onClick={() => setShowChart(true)}>
        Show Chart
      </button>
      {showChart && (
        <Suspense fallback={<Loading />}>
          <HeavyChart />
        </Suspense>
      )}
    </div>
  );
};
```
### 공급업체 분할
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
      },
    },
  },
};
```
## 나무 흔들기

### ES 모듈
```javascript
//GOOD - ES modules
export { func1, func2 } from './utils';

// BAD - CommonJS
module.exports = { func1, func2 };
```
### Package.json 부작용
```json
{
  "sideEffects": false,
  "sideEffects": ["*.css", "./src/**/*.scss"]
}
```
### 웹팩 구성
```javascript
module.exports = {
  optimization: {
    usedExports: true,
    sideEffects: true,
  },
};
```
## 축소

### 자바스크립트
```javascript
// Terser configuration
const TerserPlugin = require('terser-webpack-plugin');

module.exports = {
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          compress: {
            drop_console: true,
            pure_funcs: ['console.log'],
            dead_code: true,
            unused: true,
          },
          mangle: {
            safari10: true,
          },
        },
      }),
    ],
  },
};
```
### CSS
```javascript
// CSS Nano configuration
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');

module.exports = {
  optimization: {
    minimizer: [
      new CssMinimizerPlugin({
        minimizerOptions: {
          preset: [
            'default',
            {
              discardComments: { removeAll: true },
              normalizeWhitespace: true,
              minifyFontValues: true,
            },
          ],
        },
      }),
    ],
  },
};
```
### HTML
```javascript
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  plugins: [
    new HtmlWebpackPlugin({
      minify: {
        removeComments: true,
        collapseWhitespace: true,
        removeAttributeQuotes: true,
        minifyJS: true,
        minifyCSS: true,
      },
    }),
  ],
};
```
## 번들 분석

### 웹팩 번들 분석기
```javascript
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer');

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      openAnalyzer: false,
      generateStatsFile: true,
      statsFilename: 'bundle-stats.json',
    }),
  ],
};
```
### 소스 맵 탐색기
```bash
npm run build
npm run build:analyze
```
## 자산 최적화

### 이미지
```javascript
const ImageMinimizerPlugin = require('image-minimizer-webpack-plugin');

module.exports = {
  module: {
    rules: [
      {
        test: /\.(jpe?g|png|gif|svg)$/i,
        type: 'asset',
        parser: {
          dataUrlCondition: {
            maxSize: 8 * 1024,
          },
        },
        generator: {
          filename: 'images/[name].[contenthash][ext]',
        },
        use: [
          {
            loader: ImageMinimizerPlugin.loader,
            options: {
              minimizer: {
                implementation: ImageMinimizerPlugin.imageminGenerate,
                options: {
                  plugins: [
                    ['imagemin-mozjpeg', { quality: 75 }],
                    ['imagemin-pngquant', { quality: [0.65, 0.9] }],
                  ],
                },
              },
            },
          },
        ],
      },
    ],
  },
};
```
### 글꼴
```javascript
module.exports = {
  module: {
    rules: [
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/,
        type: 'asset/resource',
        generator: {
          filename: 'fonts/[name][ext]',
        },
      },
    ],
  },
};
```
### SVG 최적화
```javascript
const SvgrWebpackPlugin = require('svg-sprite-loader');

module.exports = {
  module: {
    rules: [
      {
        test: /\.svg$/,
        use: ['@svgr/webpack'],
      },
    ],
  },
};
```
## 캐싱

### 파일 시스템 캐시
```javascript
module.exports = {
  cache: {
    type: 'filesystem',
    cacheDirectory: '.webpack_cache',
    maxAge: 1000 * 60 * 60 * 24 * 7, // 1 week
    compression: 'gzip',
  },
};
```
### 바벨 캐시
```javascript
module.exports = {
  module: {
    rules: [
      {
        test: /\.(js|jsx|ts|tsx)$/,
        use: {
          loader: 'babel-loader',
          options: {
            cacheDirectory: true,
            cacheCompression: true,
          },
        },
      },
    ],
  },
};
```
### 영구 빌드
```javascript
module.exports = {
  snapshot: {
    managedPaths: [path.join(process.cwd(), 'node_modules')],
    immutablePaths: [],
    buildDependencies: {
      config: [__filename],
    },
  },
};
```
## 성능 모니터링

### 지표 구축
```javascript
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      reportFilename: './bundle-report.html',
      generateStatsFile: true,
      statsOptions: { source: false },
    }),
  ],
};
```
### 라이트하우스 CI
```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI

on: [push]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Lighthouse CI
        uses: treosh/lighthouse-ci-action@v3
        with:
          urls: |
            https://example.com
          uploadArtifacts: true
          temporaryPublicStorage: true
```
## 환경별 최적화

### 개발
```javascript
module.exports = {
  mode: 'development',
  devtool: 'eval-cheap-module-source-map',
  
  optimization: {
    runtimeChunk: true,
    removeAvailableModules: false,
    removeEmptyChunks: false,
    splitChunks: false,
  },
  
  cache: {
    type: 'memory',
  },
};
```
### 생산
```javascript
module.exports = {
  mode: 'production',
  devtool: 'source-map',
  
  optimization: {
    minimize: true,
    nodeEnv: 'production',
    
    splitChunks: {
      chunks: 'all',
      maxInitialRequests: 25,
      minSize: 20000,
    },
    
    runtimeChunk: 'single',
  },
  
  performance: {
    hints: 'warning',
    maxEntrypointSize: 512000,
    maxAssetSize: 512000,
  },
};
```
## 고급 전략

### 종속성을 위한 DLL 플러그인
```javascript
const webpack = require('webpack');
const path = require('path');

module.exports = {
  entry: {
    vendor: ['react', 'react-dom', 'react-router-dom'],
  },
  output: {
    path: path.join(__dirname, 'dll'),
    filename: '[name].dll.js',
    library: '[name]_library',
  },
  plugins: [
    new webpack.DllPlugin({
      name: '[name]_library',
      path: path.join(__dirname, 'dll', '[name]-manifest.json'),
    }),
  ],
};
```
### 모듈 연합
```javascript
const ModuleFederationPlugin = require('webpack').container
  .ModuleFederationPlugin;

module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: 'app1',
      filename: 'remoteEntry.js',
      exposes: {
        './Button': './src/Button',
      },
      shared: {
        react: { singleton: true, eager: true },
        'react-dom': { singleton: true, eager: true },
      },
    }),
  ],
};
```
### 미리 로드 및 미리 가져오기
```typescript
// Preload critical resources
<link rel="preload" href="/styles/main.css" as="style">
<link rel="preload" href="/fonts/main.woff2" as="font" crossorigin>

// Prefetch likely next navigation
<link rel="prefetch" href="/about.js">
<link rel="prefetch" href="/dashboard.js">
```
## 체크리스트

### 사전 빌드
- [ ] 번들 크기 분석
- [ ] 사용되지 않은 코드 식별
- [ ] 종속성 검토
- [ ] 코드 분할 전략 설정
- [ ] 압축 구성

### 빌드 중
- [ ] 축소 활성화
- [ ] 소스 맵 구성
- [ ] 캐싱 설정
- [ ] 트리 흔들기 활성화
- [ ] 자산 최적화

### 빌드 후
- [ ] 번들 보고서 검토
- [ ] 테스트 로딩 성능
- [ ] 소스 맵이 작동하는지 확인
- [ ] Lighthouse 점수 확인
- [ ] 생산 지표 모니터링

### 연속
- [ ] 시간 경과에 따른 번들 크기 추적
- [ ] 빌드 시간 모니터링
- [ ] Lighthouse CI 결과 검토
- [ ] 정기적으로 종속성을 업데이트합니다.
- [ ] 최적화 전략 검토