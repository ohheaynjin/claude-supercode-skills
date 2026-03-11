---
name: frontend-ui-ux-engineer
description: 디자인 목업 없이도 멋진 UI/UX를 만드는 디자이너 출신 개발자입니다. 코드는 약간 지저분할 수 있지만 시각적 출력은 항상 훌륭합니다.
---
# 프론트엔드 UI/UX 엔지니어

## 목적

디자인 모형 없이도 시각적으로 멋진 사용자 중심 인터페이스를 만드는 데 특화된 프런트엔드 디자인 및 개발 전문 지식을 제공합니다. 창의적인 디자인 사고, 고급 스타일, 애니메이션, 최신 웹 애플리케이션을 위한 접근성 모범 사례를 통해 아름다운 UI/UX를 제작합니다.

## 사용 시기

- 기능적인 UI를 시각적으로 뛰어난 인터페이스로 변환해야 함
- 디자인 목업은 없지만 아름다운 UI가 필요합니다.
- 시각적인 세련미와 미세한 상호작용이 우선입니다.
- 컴포넌트 스타일링에는 창의적인 디자인 사고가 필요합니다.
- 전담 디자이너 없이 사용자 경험 개선 필요

## 빠른 시작

**다음과 같은 경우에 이 스킬을 호출하세요:**
- 기능적인 UI를 시각적으로 뛰어난 인터페이스로 변환해야 함
- 디자인 목업은 없지만, 아름다운 UI가 필요합니다.
- 시각적인 세련미와 미세한 상호작용이 코드의 우아함보다 우선시됩니다.
- 컴포넌트 스타일링에는 창의적인 디자인 사고가 필요합니다.
- 전담 디자이너 없이 사용자 경험 개선 필요

**다음과 같은 경우에는 호출하지 마세요.**
- 백엔드 로직 또는 API 개발이 필요함
- 시각적 변화 없이 순수한 코드 리팩토링
- 성능 최적화가 최우선 과제입니다.
- 보안 중심의 개발 필요
- 데이터베이스 또는 인프라 작업

---
---

## 핵심 워크플로우

### 작업 흐름 1: 기능적 구성 요소를 멋진 UI로 변환

**사용 사례:** 일반 React 구성 요소가 주어지면 시각적으로 예외적으로 만듭니다.

**입력 예:**```tsx
// Before: Functional but plain
function ProductCard({ product }: { product: Product }) {
  return (
    <div>
      <img src={product.image} alt={product.name} />
      <h3>{product.name}</h3>
      <p>${product.price}</p>
      <button>Add to Cart</button>
    </div>
  );
}
```

**단계:**

**1. 시각적 분석(2분)**```
Questions to answer:
- What emotion should this evoke? (Premium? Playful? Trustworthy?)
- What's the visual hierarchy? (Image > Name > Price > CTA)
- What interactions delight users? (Hover effects, smooth transitions)
- Where's the whitespace needed? (Breathing room around elements)
```

**2. 색상 및 타이포그래피 향상**```tsx
// After: Visual foundation established
import { motion } from 'framer-motion';

function ProductCard({ product }: { product: Product }) {
  return (
    <motion.div
      className="group relative overflow-hidden rounded-2xl bg-white shadow-lg transition-shadow hover:shadow-2xl"
      whileHover={{ y: -4 }}
      transition={{ duration: 0.2, ease: 'easeOut' }}
    >
      {/* Image container with aspect ratio */}
      <div className="relative aspect-square overflow-hidden">
        <img
          src={product.image}
          alt={product.name}
          className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
        />
        {/* Gradient overlay for readability */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 transition-opacity group-hover:opacity-100" />
      </div>

      {/* Content with proper spacing */}
      <div className="p-6 space-y-3">
        <h3 className="text-xl font-semibold text-gray-900 line-clamp-2">
          {product.name}
        </h3>
        
        <div className="flex items-baseline gap-2">
          <span className="text-2xl font-bold text-blue-600">
            ${product.price}
          </span>
          {product.compareAtPrice && (
            <span className="text-sm text-gray-500 line-through">
              ${product.compareAtPrice}
            </span>
          )}
        </div>

        {/* Enhanced CTA button */}
        <button className="w-full rounded-lg bg-blue-600 px-6 py-3 font-medium text-white transition-colors hover:bg-blue-700 active:bg-blue-800 disabled:bg-gray-300 disabled:cursor-not-allowed">
          Add to Cart
        </button>
      </div>
    </motion.div>
  );
}
```

**3. 마이크로 인터랙션 및 폴란드어**```tsx
// Final: Delightful interactions added
function ProductCard({ product, onAddToCart }: ProductCardProps) {
  const [isAdded, setIsAdded] = useState(false);

  const handleAddToCart = () => {
    onAddToCart(product);
    setIsAdded(true);
    setTimeout(() => setIsAdded(false), 2000);
  };

  return (
    <motion.div
      layout
      className="group relative overflow-hidden rounded-2xl bg-white shadow-lg transition-shadow hover:shadow-2xl"
      whileHover={{ y: -4 }}
    >
      <div className="relative aspect-square overflow-hidden">
        <img
          src={product.image}
          alt={product.name}
          className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
        />
        
        {/* Sale badge with animation */}
        {product.onSale && (
          <motion.div
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            className="absolute top-4 right-4 rounded-full bg-red-500 px-3 py-1 text-sm font-bold text-white shadow-lg"
          >
            SALE
          </motion.div>
        )}
      </div>

      <div className="p-6 space-y-3">
        <h3 className="text-xl font-semibold text-gray-900 line-clamp-2 transition-colors group-hover:text-blue-600">
          {product.name}
        </h3>
        
        <div className="flex items-baseline gap-2">
          <motion.span
            className="text-2xl font-bold text-blue-600"
            key={product.price} // Re-animate on price change
            initial={{ scale: 1.2, color: '#ef4444' }}
            animate={{ scale: 1, color: '#2563eb' }}
          >
            ${product.price}
          </motion.span>
          {product.compareAtPrice && (
            <span className="text-sm text-gray-500 line-through">
              ${product.compareAtPrice}
            </span>
          )}
        </div>

        {/* Button with success state */}
        <button
          onClick={handleAddToCart}
          className={`
            w-full rounded-lg px-6 py-3 font-medium text-white transition-all
            ${isAdded 
              ? 'bg-green-500 scale-105' 
              : 'bg-blue-600 hover:bg-blue-700 active:scale-95'
            }
          `}
        >
          {isAdded ? (
            <span className="flex items-center justify-center gap-2">
              <CheckIcon className="h-5 w-5" />
              Added!
            </span>
          ) : (
            'Add to Cart'
          )}
        </button>
      </div>
    </motion.div>
  );
}
```

**예상 결과:**
- 시각적 매력이 5배 증가했습니다.
- 참여 지표가 20-40% 향상됩니다(일반).
- 마이크로 인터랙션을 통한 사용자 즐거움
- 접근성 유지(ARIA 라벨, 키보드 탐색)

---
---

## 패턴 및 템플릿

### 패턴 1: Glassmorphism 카드

**사용 시기:** 모던하고 고급스러운 미학(다채로운 배경과 잘 어울림)

```tsx
function GlassCard({ children, className = '' }: GlassCardProps) {
  return (
    <div className={`
      relative overflow-hidden rounded-2xl
      backdrop-blur-xl backdrop-saturate-150
      bg-white/10 border border-white/20
      shadow-xl shadow-black/5
      ${className}
    `}>
      {/* Optional gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent opacity-50" />
      
      <div className="relative z-10 p-6">
        {children}
      </div>
    </div>
  );
}
```

---
---

### 패턴 3: Shimmer를 사용한 스켈레톤 로딩

**사용 시기:** 카드, 목록의 로드 상태(스피너보다 UX가 더 좋음)

```tsx
function SkeletonCard() {
  return (
    <div className="relative overflow-hidden rounded-xl bg-gray-200 p-6">
      {/* Shimmer effect */}
      <div className="absolute inset-0 -translate-x-full animate-shimmer bg-gradient-to-r from-transparent via-white/50 to-transparent" />
      
      {/* Skeleton content */}
      <div className="space-y-4">
        <div className="h-4 w-3/4 rounded bg-gray-300" />
        <div className="h-4 w-1/2 rounded bg-gray-300" />
        <div className="h-32 w-full rounded bg-gray-300" />
      </div>
    </div>
  );
}

// Tailwind config (add to tailwind.config.js)
{
  theme: {
    extend: {
      animation: {
        shimmer: 'shimmer 2s infinite',
      },
      keyframes: {
        shimmer: {
          '100%': { transform: 'translateX(100%)' },
        },
      },
    },
  },
}
```

---
---

### ❌ 안티 패턴 2: 색상 대비 무시

**모습:**```css
/* ❌ Gray text on light gray background = unreadable */
.subtle-text {
  color: #999999;
  background: #f0f0f0;
  /* Contrast ratio: 2.1:1 (FAILS WCAG AA 4.5:1 requirement) */
}
```

**실패하는 이유:**
- WCAG AA 접근성 실패(텍스트 대비 4.5:1)
- 시각 장애가 있는 사용자는 콘텐츠를 읽을 수 없습니다.
- 밝은 햇빛에서는 UX가 좋지 않음(모바일 기기)

**올바른 접근 방식:**```css
/* ✅ Sufficient contrast */
.readable-text {
  color: #333333;
  background: #ffffff;
  /* Contrast ratio: 12.6:1 (PASSES WCAG AAA) */
}

/* Or use design system tokens */
.text {
  color: var(--color-text-primary);    /* Guaranteed 4.5:1 */
  background: var(--color-bg-surface); /* Against text color */
}
```

---
---

## 품질 체크리스트

### 시각적 다듬기
- [ ] 색상 팔레트는 최대 3개의 기본 색상 + 중성색을 사용합니다.
- [ ] 타이포그래피 계층 구조 지우기(글꼴 크기 3~5개)
- [ ] 간격은 일관된 크기(4px, 8px, 16px, 24px, 32px...)를 따릅니다.
- [ ] 모든 대화형 요소에 대한 마우스오버 상태
- [ ] 비동기 작업에 대한 로드 상태
- [ ] 유용한 메시지가 포함된 빈 상태

### 접근성
- [ ] 텍스트의 경우 색상 대비 ≥4.5:1(WCAG AA)
- [ ] 모든 대화형 요소에 표시되는 초점 표시기
- [ ] 애니메이션은 `prefers-reduced-motion`을(를) 준수합니다.
- [ ] 모든 이미지의 대체 텍스트
- [ ] 키보드 탐색 작동(Tab, Enter, Esc)

### 반응형 디자인
- [ ] 모바일 우선 접근 방식(320px 기준)
- [ ] 중단점: sm(640px), md(768px), lg(1024px), xl(1280px)
- [ ] 터치 대상 ≥44x44px(모바일)
- [ ] 모바일에서는 가로 스크롤이 불가능합니다.
- [ ] 반응형 이미지(`max-width: 100%`, `height: auto`)

### 성능
- [ ] 애니메이션은 `transform` 및 `opacity`(GPU 가속)을 사용합니다.
- [ ] 이미지 최적화(WebP, 지연 로딩)
- [ ] CSS 번들 <50KB(축소 후)
- [ ] 레이아웃 변경 없음(CLS <0.1)
- [ ] 사전 로드된 글꼴(`<link rel="preload">`)