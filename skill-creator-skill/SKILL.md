---
name: skill-creator
description: 효과적인 기술을 만들기 위한 가이드입니다. 이 기술은 사용자가 전문 지식, 워크플로 또는 도구 통합을 통해 Claude의 기능을 확장하는 새로운 기술을 만들거나 기존 기술을 업데이트하려는 경우에 사용해야 합니다.
---
# 스킬 크리에이터

## 목적

고품질의 효과적인 스킬 생성을 안내하는 메타 스킬입니다. 전문 지식, 워크플로우 또는 도구 통합을 통해 Claude의 역량을 향상시키는 기술 구축을 위한 템플릿, 모범 사례 및 구조적 지침을 제공합니다.

## 사용 시기

- 새로운 스킬을 만들고 싶은 사용자
- 사용자가 기존 기술을 업데이트하거나 개선하기를 원합니다.
- 사용자가 기술 문서를 구성하는 방법을 묻습니다.
- 특정 도메인이나 워크플로에 대한 기술 설계가 필요한 경우
- 기술이 모범 사례를 따르도록 하고 싶습니다.

## 핵심 스킬 구조

### 필수 구성요소

모든 기술에는 다음 요소가 있어야 합니다.

1. **머리말**
```yaml
   ---
   name: skill-name
   description: One-line description when to use this skill
   ---
   ```
2. **제목 및 목적**
```markdown
   # Skill Name
   
   ## Purpose
   Clear, concise statement of what this skill does
   ```
3. **사용 시기**
```markdown
   ## When to Use
   - Specific trigger 1
   - Specific trigger 2
   - Context where this helps
   ```
4. **핵심 기능**
```markdown
   ## Core Capabilities
   
   ### Domain Expertise
   - Key knowledge area 1
   - Key knowledge area 2
   
   ### Tools & Methods
   - Specific techniques
   - Frameworks used
   ```
### 선택사항이지만 권장되는 구성요소

5. **워크플로**
```markdown
   ## Workflow
   
   1. Step 1: What to do first
   2. Step 2: Next action
   3. Step 3: Final deliverable
   ```
6. **모범 사례**
```markdown
   ## Best Practices
   
   - Do this
   - Avoid that
   - Remember this
   ```
7. **예**
```markdown
   ## Examples
   
   ### Example 1: Common Use Case
   **Input**: User request
   **Approach**: How to handle
   **Output**: Expected result
   ```
8. **안티패턴**
```markdown
   ## Anti-Patterns
   
   ❌ **Don't**: Bad practice
   ✅ **Do**: Good alternative
   ```
## 스킬 생성 작업 흐름

### 1단계: 범위 정의

스스로에게 물어보세요:
- 이 기술은 어떤 문제를 해결하는가?
- 누가 사용할 것인가?
- 무엇이 사용을 유발하나요?
- 예상되는 결과는 무엇인가?

### 2단계: 핵심 지식 파악

문서:
- 도메인별 용어
- 주요 개념 및 원리
- 이 영역의 일반적인 패턴
- 관련 도구 및 기술

### 3단계: 워크플로 구조화

지도 작성:
- 입장조건
- 단계별 프로세스
- 결정 포인트
- 종료 기준 및 결과물

### 4단계: 실용적인 요소 추가

포함:
- 실제 사례
- 피해야 할 일반적인 함정
- 현장 모범 사례
- 품질기준

### 5단계: 지우기 트리거 작성

"사용 시기"를 구체적으로 작성하십시오.
- ✅ "사용자는 PostgreSQL 데이터베이스에 대한 SQL 쿼리 최적화가 필요합니다"
- ❌ "사용자에게 데이터베이스 도움이 필요합니다."

- ✅ "분산 시스템의 생산 중단 디버깅"
- ❌ "버그 수정"

## 스킬 품질 기준

### 명확성
- [ ] 이름은 설명이 필요합니다.
- [ ] 사용 시기를 명확하게 설명하는 설명
- [ ] 목적을 1~2문장으로 표현함
- [ ] 설명 없이 전문 용어 사용 불가

### 완전성
- [ ] 모든 필수 섹션이 있음
- [ ] 작업 흐름이 실행 가능합니다.
- [ ] 일반적인 사례에 대한 예시
- [ ] 가장자리 사례 해결됨

### 특이성
- [ ] 트리거가 구체적입니다.
- [ ] 단계가 따라갈 수 있을 만큼 상세합니다.
- [ ] 도구/방법의 이름이 명시적으로 지정되었습니다.
- [ ] 성공 기준이 정의됨

### 유용성
- [ ] 스캔 및 탐색이 용이함
- [ ] 일관된 형식
- [ ] 논리적 섹션 순서 지정
- [ ] 도움이 되는 상호 참조

## 스킬 템플릿

### 기술 도메인 기술 템플릿
```markdown
---
name: domain-expert
description: Use when user needs [specific technical task] in [technology/domain]
---

# Domain Expert

## Purpose

Expert in [domain] specializing in [specific areas]. Helps with [key problems solved].

## When to Use

- User needs [specific task 1]
- Working with [technology] and needs [help type]
- Troubleshooting [specific problem type]
- Designing [architectural element]

## Core Capabilities

### [Domain] Expertise
- [Technology 1] - [version/specifics]
- [Technology 2] - [what aspects]
- [Pattern/practice] - [when/how]

### Key Techniques
- **[Technique 1]**: [What it solves]
- **[Technique 2]**: [When to use]
- **[Technique 3]**: [How it helps]

## Workflow

1. **Understand Requirements**
   - Clarify [specific aspects]
   - Identify [constraints]

2. **Apply [Domain] Patterns**
   - Use [pattern 1] for [scenario]
   - Consider [trade-off]

3. **Implement Solution**
   - Follow [best practice]
   - Ensure [quality criteria]

4. **Validate**
   - Test [aspects]
   - Verify [requirements met]

## Best Practices

- **[Practice 1]**: [Reasoning]
- **[Practice 2]**: [Benefit]
- **[Practice 3]**: [Why important]

## Common Patterns

### [Pattern 1]
**When**: [Scenario]
**How**: [Implementation approach]
**Why**: [Benefits]

### [Pattern 2]
**When**: [Scenario]
**How**: [Implementation approach]
**Why**: [Benefits]

## Anti-Patterns

❌ **Don't**: [Bad practice]
   - Why it fails: [Reason]
   - Better approach: [Alternative]

❌ **Avoid**: [Common mistake]
   - Problem: [What goes wrong]
   - Instead: [Correct way]

## Examples

### Example 1: [Common Scenario]
**Context**: [Situation]
**Approach**: [Solution steps]
**Result**: [Outcome]

## Tools & Technologies

- **[Tool 1]**: [Version] - [Use for what]
- **[Tool 2]**: [Version] - [Use for what]
- **[Framework]**: [Version] - [Key features used]
```
### 프로세스/워크플로 기술 템플릿
```markdown
---
name: process-specialist
description: Use when user needs [specific process/workflow] for [outcome]
---

# Process Specialist

## Purpose

Guides [specific process] to achieve [specific outcome]. Ensures [quality aspects] through [methodology].

## When to Use

- Need to [execute process]
- Want to ensure [quality outcome]
- Working on [scenario requiring this process]

## Core Process

### Phase 1: [Name]
**Goal**: [What to achieve]

Steps:
1. [Action 1]: [Details]
2. [Action 2]: [Details]
3. [Action 3]: [Details]

**Outputs**: [What you have after this phase]

### Phase 2: [Name]
**Goal**: [What to achieve]

Steps:
1. [Action 1]: [Details]
2. [Action 2]: [Details]

**Outputs**: [What you have after this phase]

### Phase 3: [Name]
**Goal**: [What to achieve]

Steps:
1. [Action 1]: [Details]
2. [Action 2]: [Details]

**Deliverable**: [Final output]

## Decision Points

### When to [Decision]
- If [condition], then [choice A]
- If [condition], then [choice B]

## Quality Gates

After each phase, verify:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Best Practices

- **[Practice]**: [Why it matters]
- **[Practice]**: [Impact on quality]

## Common Pitfalls

- **Pitfall**: [What people do wrong]
  - **Impact**: [What happens]
  - **Solution**: [How to avoid]
```
## 글쓰기 팁

### 구체적으로 작성하세요
❌ "데이터베이스 작업 시 사용"
✅ "PostgreSQL 14+ 프로덕션 데이터베이스에 대한 SQL 쿼리를 최적화할 때 사용"

### 실행 가능
❌ "보안을 생각해보세요"
✅ "OWASP ZAP 스캔을 실행하고 심각도가 높은 결과를 모두 검토하세요"

### 구조화하라
일관된 제목 수준을 사용합니다.
-`##`주요 섹션에 대한
-`###`하위 섹션의 경우
-`####`자세한 분석을 위해

### 시각적 표시기 사용
- ✅ 모범 사례
- ❌ 안티패턴의 경우
- 🔍 조사 단계
- ⚠️ 경고용
- 💡 팁

### 컨텍스트 포함
해야 할 일만 나열하지 말고 그 이유를 설명하세요.
```markdown
## Instead of:
- Use connection pooling

## Write:
- **Use connection pooling** (pg-pool for PostgreSQL)
  - Reduces connection overhead by 80%
  - Critical for applications with >100 concurrent users
  - Configure pool size = (core count × 2) + effective_spindle_count
```
## 스킬 유지

### 업데이트 시기
- 핵심기술 신규 버전 출시
- 현장에서 더 나은 관행이 등장합니다.
- 사용자 피드백에 따르면 격차가 드러납니다.
- 관련 스킬이 생성됩니다. (상호참조)

### 버전 관리
머리말에 다음을 추가하는 것을 고려해보세요:
```yaml
---
name: skill-name
description: One-line description
---
```
## 스킬 통합

### 상호 참조
관련 스킬 링크:
```markdown
## Related Skills
- Use [[debugger-skill]] when issues arise
- Combine with [[performance-engineer-skill]] for optimization
- Precede with [[architect-reviewer-skill]] for design validation
```
### 스킬 구성
복잡한 워크플로에서는 기술을 연결할 수 있습니다.
```markdown
## Workflow
1. Use [[requirement-analyst]] to gather needs
2. Apply this skill for implementation
3. Use [[code-reviewer]] for quality assurance
4. Use [[deployment-engineer]] to ship
```
## 예

### 예시 1: Python Pro 기술 만들기

**컨텍스트**: 고급 Python 개발을 위한 기술이 필요합니다.

**프로세스**:
1. 범위 정의: FastAPI 및 유형 안전성에 중점을 둔 Python 3.11+
2. 트리거 식별: "최신 Python", "유형 힌트", "FastAPI"
3. 구조 핵심 기능:
   - Python 3.11+ 기능(일치 문, 입력 개선)
   - FastAPI 프레임워크 패턴
   - 유형 주석 모범 사례
4. 워크플로우 추가: 디자인 API → 유형 모델 → 경로 구현 → 테스트
5. 예시 포함: 전체 유형 주석이 포함된 FastAPI 경로

**결과**: 최신 Python 개발을 위한 집중적이고 실행 가능한 기술

### 예 2: Git 워크플로 기술 만들기

**컨텍스트**: 팀의 Git 분기 전략을 체계화해야 함

**프로세스**:
1. 범위 정의: 기능 개발을 위한 Git 워크플로
2. 트리거 식별: "브랜치 생성", "PR 생성", "git 워크플로"
3. 단계별 구조:
   - 지점 생성
   - 개발주기
   - 홍보과정
   - 병합 전략
4. 결정 포인트 추가: 리베이스할 때와 병합할 때
5. 예시 포함: 표준 기능 개발 흐름

**결과**: 일관된 Git 사용을 위한 명확한 절차 가이드

## 검증 체크리스트

기술을 마무리하기 전에 다음을 확인하세요.

### 구조
- [ ] 서문 작성 완료(이름, 설명)
- [ ] 제목 및 목적이 명확함
- [ ] "사용 시기" 섹션에는 특정 트리거가 있습니다.
- [ ] 잘 정의된 핵심 기능

### 내용
- [ ] 정보가 정확하고 최신입니다.
- [ ] 예시가 현실적이고 도움이 됩니다.
- [ ] 모범 사례가 타당합니다.
- [ ] 안티 패턴은 대안을 보여줍니다.

### 유용성
- [ ] 정보를 빠르게 스캔하고 찾을 수 있습니다.
- [ ] 섹션이 논리적으로 흐름
- [ ] 형식이 일관됩니다.
- [ ] 상호 참조가 정확함

### 품질
- [ ] 철자/문법 오류 없음
- [ ] 기술 용어 정의
- [ ] 코드 예제(있는 경우)가 정확합니다.
- [ ] 위의 모든 품질 기준을 충족합니다.

## 메타: 이 스킬에 대해

이 기술 자체는 그것이 가르치는 원리를 보여줍니다.
- 명확한 머리말과 구조
- 특정 "사용 시기" 트리거
- 실행 가능한 워크플로우
- 구체적인 예
- 품질기준

스킬을 만들 때 이를 가이드이자 템플릿으로 사용하세요.