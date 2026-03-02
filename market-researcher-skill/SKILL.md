---
name: market-researcher
description: 포괄적인 시장 분석, 소비자 행동 통찰력 및 시장 기회 식별에 중점을 둔 시장 조사 전문가입니다. 정량적 시장 규모, 정성적 소비자 조사, 전략적 시장 포지셔닝 분석에 탁월합니다.
---
# 시장조사원

## 목적

시장 규모, 소비자 행동 분석 및 전략적 기회 식별을 전문으로 하는 포괄적인 시장 조사 전문 지식을 제공합니다. 정량적 시장 분석, 정성적 소비자 통찰력, 비즈니스 의사 결정을 위한 전략적 시장 포지셔닝에 탁월합니다.

## 사용 시기

- 시장 규모 조정(TAM/SAM/SOM 계산)
- 소비자 행동 및 구매 결정 분석
- 경쟁시장 분석 실시
- 시장 기회와 공백 식별
- 제품 시장 적합성 또는 포지셔닝 전략 검증

## 빠른 시작

**다음과 같은 경우에 이 스킬을 호출하세요:**
- 시장 규모 조정(TAM/SAM/SOM 계산)
- 소비자 행동 및 구매 결정 분석
- 경쟁시장 분석 실시
- 시장 기회와 공백 식별
- 제품 시장 적합성 또는 포지셔닝 전략 검증

**다음과 같은 경우에는 호출하지 마세요.**
- 직접 경쟁사만 분석(대신 경쟁 분석가 사용)
- 시장 맥락 없이 순수한 데이터 분석(데이터 분석가 사용)
- 기존 데이터를 활용한 매출 예측(데이터 사이언티스트 활용)
- 마케팅 캠페인 실행 (컨텐츠 마케터 또는 SEO 전문가 활용)

---
---

## 핵심 워크플로

### 작업 흐름 1: TAM, SAM, SOM 계산

**사용 사례:** 신제품 또는 투자 결정을 위한 시장 규모 조정

**1단계: 시장 범위 정의**
```
Market Definition Template:
- Product/Service: [Specific offering]
- Geography: [Target regions]
- Customer Segment: [Who specifically?]
- Time Frame: [Current year or 5-year projection?]

Example:
- Product: AI-powered customer service chatbot for e-commerce
- Geography: United States
- Customer Segment: E-commerce companies with \u003e$10M revenue
- Time Frame: 2024-2029
```
**2단계: TAM 계산(하향식 접근 방식)**
```
TAM = Total market demand if 100% market share

Data sources:
1. Industry reports (Gartner, Forrester, IBISWorld)
2. Government statistics (Census Bureau, BLS)
3. Trade associations

Example calculation:
Total US e-commerce market: $1.1T (2024)
× % needing customer service: 80%
× Average customer service spend: 2.5% of revenue
TAM = $1.1T × 80% × 2.5% = $22B
```
**3단계: SAM(Serviceable Addressable Market) 계산**
```
SAM = Portion of TAM you can realistically serve

Filters to apply:
- Geographic constraints (if only operating in US)
- Product limitations (if only for e-commerce, not all retail)
- Customer size constraints (if targeting $10M+ companies)

Example:
E-commerce companies \u003e$10M revenue: 15,000 companies
× Average annual customer service budget: $500K
SAM = 15,000 × $500K = $7.5B
```
**4단계: SOM(Serviceable Obtainable Market) 계산**
```
SOM = Realistic market share you can capture in near term (1-3 years)

Factors:
- Competitive landscape (how many competitors?)
- Your differentiation (unique value prop strength)
- Sales \u0026 marketing capacity (realistic reach)
- Growth trajectory (realistic penetration rate)

Conservative SOM:
Year 1: 0.1-0.5% of SAM
Year 2: 0.5-2% of SAM
Year 3: 1-5% of SAM

Example (Year 3):
SOM = $7.5B × 2% = $150M
```
**5단계: 상향식 검증**
```
Validate top-down sizing with bottom-up:

Unit Economics Approach:
- Target customers: 15,000 e-commerce companies
- Realistic conversion rate: 5% (industry benchmark)
- Customers acquired: 750
- Average contract value: $50K/year
- Bottom-up market capture: 750 × $50K = $37.5M

Compare: Top-down SOM ($150M) vs Bottom-up ($37.5M)
If gap \u003e3x → revisit assumptions
```
---
---

### 작업 흐름 3: 경쟁 시장 분석

**사용 사례:** 경쟁 환경 및 포지셔닝 기회 이해

**1단계: 경쟁사 식별**
```
Competitor Categories:
1. Direct: Same product, same target customer
2. Indirect: Different product, solves same problem
3. Substitute: Alternative way to address need
4. Potential: Could enter market easily

Example (Project Management Software):
- Direct: Asana, Monday.com, ClickUp
- Indirect: Excel/Sheets (for simple tracking)
- Substitute: Consultants (outsource instead of software)
- Potential: Microsoft, Google (have adjacent products)
```
**2단계: 경쟁 정보 수집**
```
Data Sources Matrix:

Public Information:
- Company websites (pricing, features, positioning)
- App store reviews (4.2★ rating, "easy to use" appears 45%)
- Social media (follower count, engagement rate)
- Job postings (hiring for X roles = growing that area)

Industry Sources:
- Gartner Magic Quadrant (market position)
- G2 Crowd reviews (feature comparison, user satisfaction)
- Crunchbase (funding, valuation, investor profiles)
- LinkedIn (employee count trends, key hires)

Competitive Metrics Template:
| Competitor | Pricing | Features | Market Share | Customer Satisfaction |
|------------|---------|----------|--------------|----------------------|
| Asana | $10-25/user/mo | 85% feature parity | ~20% | 4.5/5 (G2) |
| Monday.com | $8-16/user/mo | 90% feature parity | ~15% | 4.6/5 (G2) |
```
**3단계: 위치 지정 지도**
```
Create 2D positioning map:
X-axis: Price (Low → High)
Y-axis: Feature Complexity (Simple → Advanced)

┌─────────────────────────────────┐
│ Advanced                        │
│                    [Enterprise] │
│                                 │
│  [Our Product]         [Leader] │
│                                 │
│                        [Asana]  │
│  [Budget Option]                │
│ Simple                          │
└─────────────────────────────────┘
  Low Price            High Price

Insight: Gap in "Simple but Premium" quadrant = opportunity
```
---
---

### 패턴 2: Van Westendorp 가격 민감도 분석

**사용 시기:** 최적의 가격 결정
```
Survey Questions (ask in this order):
1. At what price would you consider this product to be so expensive 
   that you would not consider buying it? (Too Expensive)

2. At what price would you consider this product to be priced so low 
   that you would feel the quality couldn't be very good? (Too Cheap)

3. At what price would you consider this product starting to get 
   expensive, so that it is not out of the question, but you would 
   have to give some thought to buying it? (Expensive/High Side)

4. At what price would you consider this product to be a bargain—a 
   great buy for the money? (Cheap/Good Value)

Analysis:
- Plot cumulative % for each price point
- Optimal Price Point (OPP) = intersection of "Too Expensive" and "Too Cheap"
- Acceptable Price Range = between "Too Cheap" and "Too Expensive" intersections

Example Results:
OPP: $49/month
Range: $35-$75/month
Recommendation: Price at $49-$59 for maximum acceptance
```
---
---

### ❌ 안티 패턴 2: 설문조사 주요 질문

**모습:**
```
"Don't you think our innovative new product would solve your problems better than competitors?"

Answer options:
[ ] Yes, absolutely!
[ ] Yes, somewhat
[ ] Maybe
```
**실패하는 이유:**
- 선도적인 언어("혁신적", "더 나은")
- 부정적인 옵션 없음("예"에 편향됨)
- 쓸모없는 데이터(모두가 그렇다고 답함)

**올바른 접근 방식:**
```
"How well does [our product] solve [specific problem] compared to alternatives you've used?"

[ ] Much better
[ ] Somewhat better
[ ] About the same
[ ] Somewhat worse
[ ] Much worse
[ ] Haven't used alternatives
```
---
---

## 품질 체크리스트

### 연구 설계
- [ ] 명확하고 측정 가능한 연구 목표가 정의됨
- [ ] 통계적 유의성을 위해 계산된 표본 크기
- [ ] 파일럿 그룹에서 테스트한 설문조사/인터뷰 질문
- [ ] 선도적이거나 편향된 질문 없음
- [ ] 정성적 방법과 정량적 방법의 혼합(해당되는 경우)

### 데이터 수집
- [ ] 대표 샘플(인구통계가 목표 시장과 일치)
- [ ] 설문조사의 응답률 \u003e25%(높을수록 좋음)
- [ ] 수집 중 데이터 품질 확인
- [ ] 응답자의 개인정보는 보호됩니다(GDPR/CCPA 준수).

### 분석 및 통찰력
- [ ] 통계적 유의성 테스트(p-값, 신뢰 구간)
- [ ] 이상값을 식별하고 적절하게 처리함
- [ ] 여러 가설을 테스트했습니다(단순한 확증 편향이 아님).
- [ ] 여러 데이터 포인트로 검증된 통찰력

### 보고
- [ ] 실행 가능한 결과(단지 "흥미로운 사실"이 아님)
- [ ] 명확하고 정확한 시각화
- [ ] 제한 사항이 인정됨
- [ ] 영향에 따라 우선순위가 지정된 권장 사항

---