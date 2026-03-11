# 인류 기술 사양 준수 보고서

**생성**: 2026-01-16
**출처**: 인류 공식 문서(docs.claude.com/en/docs/claude-code/skills)

---

## 요약

| 미터법 | 세다 | 상태 |
|--------|-------|--------|
| 총 스킬 디렉토리 | 160 | - |
| SKILL.md 파일 존재 | 161 | ✅ 100% |
| 누락된 SKILL.md 파일 | 0 | ✅ 합격 |
| 올바른 대소문자(SKILL.md) | 161 | ✅ 합격 |
| 깔끔한 머리말 | 161 | ✅ 합격 |
| 3인칭 음성 | 161 | ✅ 합격 |
| **500줄 미만** | **161** | ✅ **통과** |
| 점진적 공개 파일 | 50 | ✅ 생성됨 |

---

## 인류 사양 요구 사항

### 필수(필수) - 모두 통과 ✅

| 요구 사항 | 상태 |
|-------------|--------|
| 이름이 지정된 파일 `SKILL.md`(대소문자 구분) | ✅ 합격 |
| YAML 머리말`---`마커 | ✅ 합격 |
|`name`필드(소문자, 하이픈, 최대 64자) | ✅ 합격 |
|`description`필드(최대 1024자) | ✅ 합격 |
| 설명의 3인칭 음성 | ✅ 합격 |

### 권장(모범 사례) - 모두 통과 ✅

| 추천 | 상태 |
|----------------|--------|
| SKILL.md를 500줄 미만으로 유지하세요 | ✅ PASS (전체 161개 파일) |
| 추가 머리말 필드 없음 | ✅ 합격 |
| 설명에 유발 용어 포함 | ✅ 합격 |
| 대용량 콘텐츠에 대한 점진적 공개 | ✅ PASS(25개 스킬 분할) |

---

## 점진적 공개 구현

Anthropic의 권장 패턴을 사용하여 25개의 기술이 분할되었습니다.

| 기능 | 원래의 | 새로운 SKILL.md | 참조 파일 |
|-------|----------|--------------|-----------------|
| 레일 전문가 | 1244 | 151 | REFERENCE.md, EXAMPLES.md |
| 백엔드 개발자 | 1239 | 203 | REFERENCE.md, EXAMPLES.md |
| UI 디자이너 | 991 | 205 | REFERENCE.md, EXAMPLES.md |
| cpp-프로 | 969 | 164 | REFERENCE.md, EXAMPLES.md |
| 프론트엔드 개발자 | 953 | 218 | REFERENCE.md, EXAMPLES.md |
| nextjs 개발자 | 932 | 161 | REFERENCE.md, EXAMPLES.md |
| 뷰 전문가 | 813 | 137 | REFERENCE.md, EXAMPLES.md |
| 데브옵스 엔지니어 | 788 | 153 | REFERENCE.md, EXAMPLES.md |
| SQL-프로 | 779 | 159 | REFERENCE.md, EXAMPLES.md |
| 포스트그레스 프로 | 685 | 166 | REFERENCE.md, EXAMPLES.md |
| 풀스택 개발자 | 685 | 179 | REFERENCE.md, EXAMPLES.md |
| 기술 자문 | 684 | 272 | REFERENCE.md, EXAMPLES.md |
| Kotlin 전문가 | 666 | 185 | REFERENCE.md, EXAMPLES.md |
| 녹 엔지니어 | 663 | 202 | REFERENCE.md, EXAMPLES.md |
| dotnet-framework-4.8-전문가 | 625 | 194 | REFERENCE.md, EXAMPLES.md |
| 반응 전문가 | 612 | 190 | REFERENCE.md, EXAMPLES.md |
| 데이터 엔지니어 | 603 | 159 | REFERENCE.md, EXAMPLES.md |
| 쿠버네티스 전문가 | 593 | 143 | REFERENCE.md, EXAMPLES.md |
| 코드베이스 탐색 | 589 | 193 | REFERENCE.md, EXAMPLES.md |
| 데이터베이스 관리자 | 581 | 128 | REFERENCE.md, EXAMPLES.md |
| 데이터베이스 최적화 프로그램 | 568 | 192 | REFERENCE.md, EXAMPLES.md |
| 파이썬 프로 | 557 | 233 | REFERENCE.md, EXAMPLES.md |
| LLM 건축가 | 534 | 200 | REFERENCE.md, EXAMPLES.md |
| graphql-건축가 | 526 | 236 | REFERENCE.md, EXAMPLES.md |
| powershell 모듈 설계자 | 518 | 274 | REFERENCE.md, EXAMPLES.md |

---

## 변경 사항

### 세션 1: 핵심 규정 준수
1. 4개의 파일 이름을 변경했습니다.`skill.md` → `SKILL.md`2. 빈 디렉토리에 대해 56개의 새로운 SKILL.md 파일을 생성했습니다.
3. 76개 파일의 머리말 정리(비사양 필드 제거)
4. 모든 설명에 3인칭 음성이 확인되었습니다.

### 세션 2: 점진적 공개
5. 대용량 파일 25개를 SKILL.md + REFERENCE.md + EXAMPLES.md로 분할합니다.
6. 이제 모든 SKILL.md 파일이 500줄 미만입니다.
7. 50개의 참조 파일 생성(25 REFERENCE.md + 25 EXAMPLES.md)

---

## 파일 구조(인류적 규격)

```
skill-name-skill/
├── SKILL.md              # Main file (< 500 lines)
├── REFERENCE.md          # Technical details (loaded on demand)
└── EXAMPLES.md           # Code examples (loaded on demand)
```

---

## 서문 템플릿(인류적 준수)

```yaml
---
name: skill-name-here
description: Third-person description with trigger terms. Use when [scenarios].
---
```

---

## 최종 준수 점수

**인류 사양을 준수하는 161/161개 파일** ✅

- ✅ 모든 필수 필드가 존재합니다.
- ✅ 모든 모범 사례를 따랐습니다.
- ✅ 점진적 공개 시행
- ✅ 500줄 이하의 모든 파일

**완전한 규정 준수 달성**