# 번들러 가이드

## 개요

최신 웹 애플리케이션은 번들러를 사용하여 브라우저 사용을 위한 소스 코드를 변환, 최적화 및 번들링합니다. 이 가이드에서는 주요 번들러와 해당 구성을 다룹니다.

## 웹팩

### 기본 구성
```javascript
const path = require('path');

module.exports = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
  },
  mode: 'production',
};
```
### 로더
```javascript
module.exports = {
  module: {
    rules: [
      // JavaScript/TypeScript
      {
        test: /\.(ts|tsx|js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              '@babel/preset-env',
              '@babel/preset-react',
              '@babel/preset-typescript',
            ],
          },
        },
      },
      
      // CSS
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
      
      // Images
      {
        test: /\.(png|jpe?g|gif|svg)$/,
        type: 'asset/resource',
      },
      
      // Fonts
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/,
        type: 'asset/resource',
      },
    ],
  },
};
```
### 플러그인
```javascript
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');

module.exports = {
  plugins: [
    new CleanWebpackPlugin(),
    
    new HtmlWebpackPlugin({
      template: './public/index.html',
      filename: 'index.html',
      minify: true,
    }),
    
    new MiniCssExtractPlugin({
      filename: '[name].[contenthash].css',
      chunkFilename: '[name].[contenthash].css',
    }),
  ],
};
```
### 최적화
```javascript
const TerserPlugin = require('terser-webpack-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');

module.exports = {
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          compress: {
            drop_console: true,
          },
        },
      }),
      new CssMinimizerPlugin(),
    ],
    
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
        },
      },
    },
    
    runtimeChunk: 'single',
  },
};
```
## 비테

### 구성
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  
  resolve: {
    alias: {
      '@': '/src',
    },
  },
  
  build: {
    outDir: 'dist',
    sourcemap: true,
    
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
        },
      },
    },
  },
  
  server: {
    port: 3000,
    open: true,
  },
});
```
### 플러그인
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import eslint from 'vite-plugin-eslint';
import svgr from 'vite-plugin-svgr';

export default defineConfig({
  plugins: [
    react(),
    eslint(),
    svgr(),
  ],
});
```
### 환경 변수
```typescript
export default defineConfig({
  define: {
    __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
    __API_URL__: JSON.stringify(process.env.VITE_API_URL),
  },
});
```
## 에스빌드

### 기본 사용법
```javascript
const esbuild = require('esbuild');

esbuild.build({
  entryPoints: ['src/index.js'],
  bundle: true,
  outfile: 'dist/bundle.js',
  minify: true,
  sourcemap: true,
  target: 'es2015',
});
```
### 시청 모드
```javascript
esbuild.context({
  entryPoints: ['src/index.js'],
  outfile: 'dist/bundle.js',
  bundle: true,
}).then(ctx => {
  ctx.watch();
});
```
## 터보팩

### 구성
```javascript
module.exports = {
  experimental: {
    turbo: {},
  },
};
```
### 개발 서버
```javascript
const { createServer } = require('turbo');

createServer({
  entry: './src/index.js',
  dev: true,
  hmr: true,
});
```
## 비교

| 기능 | 웹팩 | VITE | 에스빌드 | 터보팩 |
|---------|----------|-------|----------|------------|
| 빌드 속도 | 천천히 | 빠른 | 매우 빠름 | 매우 빠름 |
| HMR | 좋음 | 우수 | 좋음 | 우수 |
| 생태계 | 광범위한 | 성장 | 한정 | 신규 |
| 구성 | 복잡한 | 단순 | 단순 | 단순 |
| 타입스크립트 | 로더를 통해 | 네이티브 | 네이티브 | 네이티브 |
| 학습 곡선 | 높음 | 낮음 | 낮음 | 낮음 |

## 언제 어느 것을 사용해야 하는가?

### 웹팩
- 필요한 최대 구성 가능성
- 고급 최적화 필요
- 레거시 브라우저 지원
- 대기업 애플리케이션

### 비테
- 최신 브라우저 지원
- 빠른 개발 경험
- TypeScript 우선
- React/Vue/Svelte 프로젝트

### 에스빌드
- 최대 빌드 속도
- 간단한 프로젝트
- 최소한의 의존성
- 빌드 시간 변환만 해당

### 터보팩
- Next.js 프로젝트
- 최대 성능
- React 기반 애플리케이션
- 최첨단을 유지하고 싶다

## 모범 사례

### 성능
```javascript
// Enable persistent cache
module.exports = {
  cache: {
    type: 'filesystem',
    cacheDirectory: '.webpack_cache',
  },
};
```
### 번들 크기
```javascript
// Analyze bundle size
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer');

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      openAnalyzer: false,
    }),
  ],
};
```
### 개발
```javascript
// Fast rebuilds
module.exports = {
  devtool: 'eval-cheap-module-source-map',
  cache: true,
};
```
### 생산
```javascript
// Optimize for production
module.exports = {
  mode: 'production',
  optimization: {
    minimize: true,
    usedExports: true,
    sideEffects: true,
  },
};
```
