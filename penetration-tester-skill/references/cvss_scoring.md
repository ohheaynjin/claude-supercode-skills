# CVSS 채점 참고자료

## 개요
침투 테스트를 위한 CVSS(Common Vulnerability Scoring System) 채점에 대한 종합 가이드입니다.

## CVSS v3.1 개요

CVSS v3.1은 취약점을 특성화하고 평가하기 위한 프레임워크를 제공합니다. 점수 범위는 0.0~10.0입니다.

## 기본 측정항목

### 공격 벡터(AV)

취약점이 악용되는 방식.

| 미터법 | 가치 | 점수 | 설명 |
|---------|----------|---------|-------------|
| 네트워크(N) | 0.85 | 네트워크를 통해 악용 가능 |
| 인접(A) | 0.62 | 동일한 논리 네트워크 필요 |
| 로컬(L) | 0.55 | 로컬 액세스 필요 |
| 물리적(P) | 0.2 | 물리적 액세스가 필요합니다 |

### 공격 복잡성(AC)

공격자가 통제할 수 없는 조건.

| 미터법 | 가치 | 점수 | 설명 |
|---------|----------|---------|-------------|
| 낮음(L) | 0.77 | 특별한 접근 조건 없음 |
| 높음(H) | 0.44 | 특수한 조건이 필요함 |

### 필요한 권한(PR)

공격자가 악용하기 전에 소유해야 하는 권한입니다.

| 미터법 | 가치 | 점수 | 설명 |
|---------|----------|---------|-------------|
| 없음(N) | 0.85 | 권한이 필요하지 않습니다 |
| 낮음(L) | 0.62 | 낮은 권한 필요 |
| 높음(H) | 0.27 | 높은 권한 필요 |

### 사용자 상호작용(UI)

악용을 위해 사용자 상호 작용이 필요한지 여부입니다.

| 미터법 | 가치 | 점수 | 설명 |
|---------|----------|---------|-------------|
| 없음(N) | 0.85 | 사용자 상호 작용이 필요하지 않습니다 |
| 필수(R) | 0.62 | 사용자 상호작용 필요 |

### 범위(S)

취약한 구성 요소가 다른 구성 요소에 영향을 줍니까?

| 미터법 | 가치 | 설명 |
|---------|---------|------------|
| 변함없음(U) | 취약한 구성요소만 |
| 변경됨(C) | 다른 구성요소에 영향을 미침 |

### 기밀성(C)

데이터 기밀성에 영향을 미칩니다.

| 미터법 | 가치 | 설명 |
|---------|---------|------------|
| 높음(H) | 기밀성 완전 상실 |
| 낮음(L) | 일부 데이터 손실 |
| 없음(N) | 영향 없음 |

### 무결성(I)

데이터 무결성에 미치는 영향.

| 미터법 | 가치 | 설명 |
|---------|---------|------------|
| 높음(H) | 완전성 상실 |
| 낮음(L) | 일부 데이터 수정 |
| 없음(N) | 영향 없음 |

### 가용성(A)

구성 요소의 가용성에 미치는 영향.

| 미터법 | 가치 | 설명 |
|---------|---------|------------|
| 높음(H) | 가용성의 총 손실 |
| 낮음(L) | 성능 저하 |
| 없음(N) | 영향 없음 |

## 기본 점수 계산
```python
#!/usr/bin/env python3
def calculate_base_score(av, ac, pr, ui, scope, c, i, a):
    """Calculate CVSS v3.1 base score"""
    
    # Metric values mapping
    av_values = {'N': 0.85, 'A': 0.62, 'L': 0.55, 'P': 0.2}
    ac_values = {'L': 0.77, 'H': 0.44}
    pr_values = {'N': 0.85, 'L': 0.62, 'H': 0.27}
    ui_values = {'N': 0.85, 'R': 0.62}
    cia_values = {'H': 0.56, 'L': 0.22, 'N': 0.0}
    
    # Impact calculation
    iss = 1 - ((1 - cia_values[c]) * 
                 (1 - cia_values[i]) * 
                 (1 - cia_values[a]))
    
    # Impact sub-score
    if scope == 'C':
        impact = 7.52 * (iss - 0.029) - 3.25 * (iss - 0.02)**15
    else:
        impact = 6.42 * iss
    
    # Exploitability
    exploitability = 8.22 * av_values[av] * ac_values[ac] * pr_values[pr] * ui_values[ui]
    
    # Base score
    if impact <= 0:
        return 0.0
    
    if scope == 'C':
        base = min(10, impact + exploitability)
    else:
        base = min(10, (impact + exploitability) * 1.08)
    
    return round(base, 1)
```
## 심각도 등급

| 점수 범위 | 심각도 | 색상 |
|-------------|----------|---------|
| 9.0 - 10.0 | 심각 | 🔴 |
| 7.0 - 8.9 | 높음 | 🟠 |
| 4.0 - 6.9 | 중간 | 🟡 |
| 0.1 - 3.9 | 낮음 | 🟢 |
| 0.0 | 없음 | ⚪ |

## 공격 유형별 일반적인 CVSS 점수

### SQL 주입
```
Attack Vector: Network (N) - 0.85
Attack Complexity: Low (L) - 0.77
Privileges Required: None (N) - 0.85
User Interaction: None (N) - 0.85
Scope: Unchanged (U)
Confidentiality: High (H) - 0.56
Integrity: High (H) - 0.56
Availability: High (H) - 0.56

Score: 9.8 (Critical)
```
### 교차 사이트 스크립팅(반영)
```
Attack Vector: Network (N) - 0.85
Attack Complexity: Low (L) - 0.77
Privileges Required: None (N) - 0.85
User Interaction: Required (R) - 0.62
Scope: Unchanged (U)
Confidentiality: Low (L) - 0.22
Integrity: Low (L) - 0.22
Availability: None (N) - 0.0

Score: 6.1 (Medium)
```
### 저장된 XSS
```
Attack Vector: Network (N) - 0.85
Attack Complexity: Low (L) - 0.77
Privileges Required: None (N) - 0.85
User Interaction: Required (R) - 0.62
Scope: Changed (C)
Confidentiality: High (H) - 0.56
Integrity: High (H) - 0.56
Availability: None (N) - 0.0

Score: 8.1 (High)
```
### CSRF
```
Attack Vector: Network (N) - 0.85
Attack Complexity: Low (L) - 0.77
Privileges Required: None (N) - 0.85
User Interaction: Required (R) - 0.62
Scope: Unchanged (U)
Confidentiality: Low (L) - 0.22
Integrity: High (H) - 0.56
Availability: None (N) - 0.0

Score: 6.5 (Medium)
```
### 손상된 액세스 제어
```
Attack Vector: Network (N) - 0.85
Attack Complexity: Low (L) - 0.77
Privileges Required: Low (L) - 0.62
User Interaction: None (N) - 0.85
Scope: Changed (C)
Confidentiality: High (H) - 0.56
Integrity: High (H) - 0.56
Availability: High (H) - 0.56

Score: 9.6 (Critical)
```
### 하드코딩된 자격 증명
```
Attack Vector: Network (N) - 0.85
Attack Complexity: Low (L) - 0.77
Privileges Required: None (N) - 0.85
User Interaction: None (N) - 0.85
Scope: Unchanged (U)
Confidentiality: High (H) - 0.56
Integrity: None (N) - 0.0
Availability: None (N) - 0.0

Score: 9.8 (Critical)
```
## 시간 측정항목(선택사항)

### 익스플로잇 코드 성숙도(E)
- **정의되지 않음(X):** 점수를 할당하지 않음
- **증명되지 않음(U):** 익스플로잇 코드가 존재하지 않습니다.
- **개념 증명(P):** 개념 증명 코드
- **기능(F):** 기능적 익스플로잇 존재
- **높음(H):** 안정적이고 무기화된 악용

### 교정 수준(R)
- **정의되지 않음(X):** 점수를 할당하지 않음
- **공식 픽스(O):** 공급업체에서 픽스를 발행했습니다.
- **임시 수정(T):** 임시 해결 방법 사용 가능
- **해결 방법(W):** 공급업체가 아닌 경우 해결 방법 사용 가능
- **사용 불가(U):** 사용 가능한 수정 사항 없음

### 보고 신뢰도(C)
- **정의되지 않음(X):** 점수를 할당하지 않음
- **알 수 없음(U):** 알 수 없음
- **합리적(R):** 합리적인 자신감
- **확인됨 (C):** 취약점 확인됨

## 환경 지표(선택 사항)

### 기밀 유지 요구 사항(CR)
- **정의되지 않음(X):** 점수를 할당하지 않음
- **낮음(L):** 조직에 미치는 영향이 낮음
- **중간(M):** 조직에 미치는 중간 영향
- **높음(H):** 조직에 미치는 영향이 높음

### 무결성 요구사항(IR)
기밀성 요구 사항과 동일

### 가용성 요구 사항(AR)
기밀성 요구 사항과 동일

### 수정된 기본 측정항목
기본 측정항목과 동일하지만 환경에 맞게 조정됨

## CVSS 계산기
```python
#!/usr/bin/env python3
"""
CVSS v3.1 Calculator
Usage: python3 cvss_calculator.py
"""

from typing import Dict, Tuple

class CVSSCalculator:
    def __init__(self):
        self.metrics = {
            'AV': {'N': 0.85, 'A': 0.62, 'L': 0.55, 'P': 0.2},
            'AC': {'L': 0.77, 'H': 0.44},
            'PR': {'N': 0.85, 'L': 0.62, 'H': 0.27},
            'UI': {'N': 0.85, 'R': 0.62},
            'CIA': {'H': 0.56, 'L': 0.22, 'N': 0.0}
        }
    
    def calculate_base(self, av: str, ac: str, pr: str, ui: str, 
                     scope: str, c: str, i: str, a: str) -> Tuple[float, str]:
        """Calculate base score and severity"""
        
        # Impact sub-score
        iss = 1 - ((1 - self.metrics['CIA'][c]) * 
                     (1 - self.metrics['CIA'][i]) * 
                     (1 - self.metrics['CIA'][a]))
        
        # Impact calculation
        if scope == 'C':
            impact = 7.52 * (iss - 0.029) - 3.25 * (iss - 0.02)**15
        else:
            impact = 6.42 * iss
        
        # Exploitability
        exploitability = (8.22 * self.metrics['AV'][av] * 
                       self.metrics['AC'][ac] * 
                       self.metrics['PR'][pr] * 
                       self.metrics['UI'][ui])
        
        # Base score
        if impact <= 0:
            base_score = 0.0
        elif scope == 'C':
            base_score = min(10, impact + exploitability)
        else:
            base_score = min(10, (impact + exploitability) * 1.08)
        
        return round(base_score, 1), self._get_severity(base_score)
    
    def _get_severity(self, score: float) -> str:
        """Get severity rating from score"""
        if score >= 9.0:
            return "Critical"
        elif score >= 7.0:
            return "High"
        elif score >= 4.0:
            return "Medium"
        elif score > 0.0:
            return "Low"
        else:
            return "None"

# Example usage
if __name__ == '__main__':
    calc = CVSSCalculator()
    
    # SQL Injection example
    score, severity = calc.calculate_base('N', 'L', 'N', 'N', 'U', 'H', 'H', 'H')
    print(f"SQL Injection: {score} ({severity})")
    
    # XSS example
    score, severity = calc.calculate_base('N', 'L', 'N', 'R', 'U', 'L', 'L', 'N')
    print(f"Reflected XSS: {score} ({severity})")
```
## CVSS 문자열 형식
```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
         |  |  |  |  |  |  |  |
         |  |  |  |  |  |  |  + Availability
         |  |  |  |  |  |  + Integrity
         |  |  |  |  |  + Confidentiality
         |  |  |  |  + Scope
         |  |  |  + User Interaction
         |  |  + Privileges Required
         |  + Attack Complexity
         + Attack Vector
```
## 빠른 참조 카드
```
┌─────────────────────────────────────────────────────────┐
│                    CVSS v3.1                         │
├─────────────────────────────────────────────────────────┤
│                                                     │
│  AV  N(0.85)  A(0.62)  L(0.55)  P(0.2)         │
│  AC  L(0.77)  H(0.44)                              │
│  PR  N(0.85)  L(0.62)  H(0.27)                     │
│  UI  N(0.85)  R(0.62)                             │
│  CIA H(0.56)  L(0.22)  N(0.0)                     │
│                                                     │
│  Critical 9.0-10.0  High 7.0-8.9                   │
│  Medium 4.0-6.9    Low 0.1-3.9                     │
│                                                     │
│  Impact = 6.42 × ISS (Scope Unchanged)             │
│  Impact = 7.52 × (ISS-0.029) - 3.25×(ISS-0.02)^15 │
│            (Scope Changed)                           │
│                                                     │
│  Exploitability = 8.22 × AV × AC × PR × UI          │
│                                                     │
└─────────────────────────────────────────────────────────┘
```
## 모범 사례

1. **보수적으로 행동하세요:** 의심스러운 경우에는 점수를 낮추세요
2. **가정 문서화:** 가정한 내용을 기록합니다.
3. **계산기 사용:** 공식 CVSS 계산기를 사용하세요.
4. **상황 고려:** 환경에 맞게 조정
5. **정기적으로 검토:** 점수는 새로운 정보에 따라 변경될 수 있습니다.

## 참고자료

- [First.org CVSS 계산기](https://www.first.org/cvss/calculator/3.1)
- [NIST CVSS 표준](https://nvd.nist.gov/vuln-metrics/cvss)
- [CVSS v3.1 사양](https://www.first.org/cvss/specation-document)