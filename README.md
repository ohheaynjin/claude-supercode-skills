# 클로드 슈퍼코드 스킬

**Claude Code, Gemini CLI 및 Google Antigravity를 위한 161가지 AI 에이전트 기술**

AI 코딩 도우미의 기능을 확장하는 전문 AI 코딩 기술의 포괄적인 컬렉션입니다. 각 기술은 전문 소프트웨어 개발을 위한 도메인별 지식, 워크플로 및 모범 사례를 제공합니다.

## 지원되는 플랫폼

| 플랫폼 | 지점 | 스킬 파일 | 설치 위치 |
|------------|---------|------------|------|
| **클로드 코드** |`main` | `SKILL.md` | `~/.claude/skills/`|
| **제미니 CLI** |`gemini-cli` | `skill.yaml` | `~/.gemini/skills/`|
| **반중력** |`antigravity` | `skill.yaml` | `~/.gemini/antigravity/skills/`|

## 빠른 설치

### 클로드 코드(앤트로픽)
```bash
# Clone main branch
git clone https://github.com/404kidwiz/claude-supercode-skills.git ~/.claude/skills

# Or add specific skills
git clone https://github.com/404kidwiz/claude-supercode-skills.git /tmp/skills
cp -r /tmp/skills/python-pro-skill ~/.claude/skills/
```
### 제미니 CLI
```bash
# Clone gemini-cli branch
git clone -b gemini-cli https://github.com/404kidwiz/claude-supercode-skills.git ~/.gemini/skills
```
### 구글 반중력
```bash
# Clone antigravity branch
mkdir -p ~/.gemini/antigravity
git clone -b antigravity https://github.com/404kidwiz/claude-supercode-skills.git ~/.gemini/antigravity/skills
```
## 카테고리별 스킬

### 개발 - 언어 (21)

| 스킬 | 설명 |
|-------|-------------|
|`cpp-pro-skill`| 성능 최적화 및 시스템 프로그래밍을 담당하는 C++20 전문가 |
|`csharp-developer-skill`| .NET Core 및 EF Core를 사용한 .NET 8 및 C# 12 |
|`dotnet-core-expert-skill`| MAUI 및 최신 C#을 사용한 .NET 8 크로스 플랫폼 |
|`dotnet-framework-4.8-expert-skill`| WCF 및 ASP.NET MVC가 포함된 레거시 .NET Framework |
|`elixir-expert-skill`| 동시 애플리케이션을 위한 Elixir, Phoenix 및 OTP |
|`golang-pro-skill`| 고루틴, 채널 및 stdlib를 갖춘 Go 1.21+ |
|`java-architect-skill`| Java 21, Spring Boot 3 및 Jakarta EE |
|`javascript-pro-skill`| ES2023+, Node.js 및 비동기 패턴 |
|`kotlin-specialist-skill`| Kotlin 2.0, KMP, 코루틴 및 Ktor |
|`laravel-specialist-skill`| Laravel 11+, Octane 및 Livewire 3 |
|`php-pro-skill`| 최신 패턴과 Composer를 갖춘 PHP 8.2+ |
|`python-pro-skill`| Python 3.11+, 유형 주석 및 FastAPI |
|`rails-expert-skill`| Hotwire, Turbo 및 Stimulus가 포함된 Rails 7+ |
|`rust-engineer-skill`| Rust 비동기, 소유권 패턴, FFI 및 WASM |
|`spring-boot-engineer-skill`| Spring Boot 3+, 가상 스레드 및 클라우드 네이티브 |
|`swift-expert-skill`| SwiftUI 및 결합이 포함된 iOS/macOS |
|`typescript-pro-skill`| TypeScript 5+ 고급 유형 및 제네릭 |

### 개발 - 프론트엔드(12)

| 스킬 | 설명 |
|-------|-------------|
|`angular-architect-skill`| Angular 15개 이상의 엔터프라이즈 패턴 및 NgRx |
|`frontend-developer-skill`| 최신 프런트엔드 개발 도구 및 패턴 |
|`frontend-ui-ux-engineer-skill`| 멋진 UI/UX를 위한 디자이너 겸 개발자 |
|`nextjs-developer-skill`| Next.js 14+, 앱 라우터 및 서버 구성요소 |
|`react-native-specialist-skill`| React Native 크로스 플랫폼 모바일 개발 |
|`react-specialist-skill`| React 18+, 후크, 동시 기능, Zustand |
|`threejs-pro-skill`| Three.js, WebGL, React Three Fiber 및 WebGPU |
|`vue-expert-skill`| Vue 3 컴포지션 API, Pinia 및 Nuxt.js |
|`canvas-design-skill`| 디자인 철학을 활용한 PNG/PDF의 시각 예술 |
|`algorithmic-art-skill`| p5.js 및 시드 임의성을 사용한 생성 아트 |
|`ui-designer-skill`| 시각적 UI 디자인 및 구성 요소 시스템 |
|`theme-factory-skill`| 미리 설정된 테마로 아티팩트 스타일링 |

### 개발 - 백엔드 (8)

| 스킬 | 설명 |
|-------|-------------|
|`backend-developer-skill`| 프로덕션 준비가 완료된 서버 측 애플리케이션 |
|`django-developer-skill`| Django 4+, DRF, PostgreSQL 및 Celery |
|`graphql-architect-skill`| GraphQL 스키마, 연합 및 해석기 |
|`api-designer-skill`| OpenAPI 3.1을 사용한 REST/GraphQL API |
|`websocket-engineer-skill`| 실시간 WebSocket 및 Socket.IO 시스템 |
|`kafka-engineer-skill`| Apache Kafka 스트리밍 및 이벤트 처리 |
|`event-driven-architect-skill`| AsyncAPI 및 CloudEvents를 사용하는 비동기 시스템 |
|`payment-integration-skill`| Stripe, PayPal, Adyen 통합 |

### 개발 - 모바일 (4)

| 스킬 | 설명 |
|-------|-------------|
|`flutter-expert-skill`| Flutter 3+, Dart 및 Firebase 통합 |
|`mobile-app-developer-skill`| 네이티브/크로스 플랫폼 iOS 및 Android |
|`mobile-developer-skill`| React Native 및 Flutter 개발 |
|`macos-developer-skill`| SwiftUI를 사용한 macOS 개발 |

### 개발 - 데스크톱(3)

| 스킬 | 설명 |
|-------|-------------|
|`electron-pro-skill`| 자동 업데이트 기능을 갖춘 Electron 데스크탑 앱 |
|`windows-app-developer-skill`| WinUI 3, WPF 및 Windows 앱 SDK |
|`game-developer-skill`| Unity, Unreal 및 사용자 정의 게임 엔진 |

### 개발 - 풀스택 (2)

| 스킬 | 설명 |
|-------|-------------|
|`fullstack-developer-skill`| 프런트엔드-백엔드 통합 및 아키텍처 |
|`mcp-developer-skill`| 모델 컨텍스트 프로토콜 서버 및 클라이언트 |

### 건축 및 디자인 (9)

| 스킬 | 설명 |
|-------|-------------|
|`architect-reviewer-skill`| 시스템 설계 검증 및 패턴 평가 |
|`cloud-architect-skill`| AWS, Azure, GCP 멀티 클라우드 전략 |
|`microservices-architect-skill`| 서비스 분해 및 오케스트레이션 |
|`solution-architect-skill`| TOGAF 적용을 통한 엔터프라이즈 솔루션 |
|`legacy-modernizer-skill`| Strangler Fig, CDC 및 부패방지 레이어 |
|`refactoring-specialist-skill`| 디자인 패턴과 SOLID 원칙 |
|`llm-architect-skill`| LLM 배포 및 최적화 전략 |
|`workflow-orchestrator-skill`| 임시, Camunda 및 이벤트 기반 워크플로우 |
|`context-manager-skill`| 벡터 데이터베이스, RAG 및 컨텍스트 최적화 |

### DevOps 및 인프라 (16)

| 스킬 | 설명 |
|-------|-------------|
|`devops-engineer-skill`| CI/CD 자동화 및 SRE 사례 |
|`deployment-engineer-skill`| Jenkins, GitHub Actions, GitLab을 사용한 CI/CD |
|`kubernetes-specialist-skill`| EKS, AKS, GKE 전반에 걸친 K8s 오케스트레이션 |
|`terraform-engineer-skill`| 코드형 인프라 및 클라우드 아키텍처 |
|`azure-infra-engineer-skill`| Azure 인프라 및 Bicep IaC |
|`platform-engineer-skill`| 내부 개발자 플랫폼 및 셀프 서비스 |
|`sre-engineer-skill`| SLO, 오류 예산 및 사고 관리 |
|`build-engineer-skill`| 시스템 구축 및 최적화 |
|`build-skill`| 편집 및 패키징 전문가 |
|`chaos-engineer-skill`| 실패 주입 및 탄력성 테스트 |
|`devops-incident-responder-skill`| 사고 감지 및 근본 원인 분석 |
|`incident-responder-skill`| 보안 및 운영 사고 대응 |
|`network-engineer-skill`| 네트워크 아키텍처 및 제로 트러스트 |
|`video-engineer-skill`| 비디오 처리 및 스트리밍 프로토콜 |
|`iot-engineer-skill`| 엣지 컴퓨팅 및 센서 네트워크 |
|`embedded-systems-skill`| RTOS, 마이크로컨트롤러 및 펌웨어 |

### 데이터 및 AI/ML (14)

| 스킬 | 설명 |
|-------|-------------|
|`ai-engineer-skill`| LLM, RAG 및 자율 에이전트 |
|`data-analyst-skill`| BI, 시각화 및 통계분석 |
|`data-engineer-skill`| 확장 가능한 데이터 파이프라인 및 ETL/ELT |
|`data-researcher-skill`| 데이터 발견 및 통찰력 추출 |
|`data-scientist-skill`| ML, EDA 및 예측 모델링 |
|`machine-learning-engineer-skill`| ML 모델 배포 및 추론 |
|`ml-engineer-skill`| ML 시스템 개발 및 파이프라인 |
|`mlops-engineer-skill`| ML 수명주기 및 생산 모니터링 |
|`nlp-engineer-skill`| 포옹 얼굴을 사용한 NLP, spaCy, LangChain |
|`prompt-engineer-skill`| 신속한 디자인과 사고의 사슬 |
|`quant-analyst-skill`| 알고리즘 거래 및 재무 분석 |
|`csv-data-wrangler-skill`| 고성능 CSV 처리 |
|`knowledge-synthesizer-skill`| 온톨로지 구축 및 GraphRAG |
|`trend-analyst-skill`| 예측 및 시장 정보 |

### 데이터베이스 (5)

| 스킬 | 설명 |
|-------|-------------|
|`database-administrator-skill`| PostgreSQL, MySQL, MongoDB HA 및 튜닝 |
|`database-optimizer-skill`| 쿼리 최적화 및 인덱스 전략 |
|`postgres-pro-skill`| PostgreSQL 관리 및 최적화 |
|`sql-pro-skill`| 주요 플랫폼 전반에 걸친 SQL 개발 |
|`fintech-engineer-skill`| 복식 원장 및 고정밀 수학 |

### 보안 (9)

| 스킬 | 설명 |
|-------|-------------|
|`security-auditor-skill`| 인프라 보안 및 제로 트러스트 |
|`security-engineer-skill`| DevSecOps 및 취약점 관리 |
|`penetration-tester-skill`| 윤리적 해킹 및 보안 테스트 |
|`ad-security-reviewer-skill`| Active Directory 보안 분석 |
|`compliance-auditor-skill`| SOC2, HIPAA, GDPR 준수 |
|`powershell-security-hardening-skill`| Windows 보안 구성 |
|`risk-manager-skill`| 재무 및 운영 위험 평가 |
|`legal-advisor-skill`| 계약, 규정 준수 및 IP 지침 |
|`dependency-manager-skill`| 패키지 관리 및 공급망 보안 |

### 테스트 및 품질 (6)

| 스킬 | 설명 |
|-------|-------------|
|`test-automator-skill`| 테스트 프레임워크 선택 및 자동화 |
|`qa-expert-skill`| 테스트 전략 및 품질 프로세스 |
|`accessibility-tester-skill`| WCAG 2.1 AA 규정 준수 및 감사 |
|`performance-testing-skill`| 부하 테스트 및 성능 최적화 |
|`performance-engineer-skill`| 애플리케이션 최적화 및 프로파일링 |
|`code-reviewer-skill`| 보안을 갖춘 품질 중심의 코드 검토 |

### 디버깅 및 분석 (5)

| 스킬 | 설명 |
|-------|-------------|
|`debugger-skill`| 고급 디버깅 및 근본 원인 분석 |
|`error-detective-skill`| 마이크로서비스 전반의 오류 패턴 분석 |
|`error-detector-skill`| 오류 분석 및 패턴 감지 |
|`error-coordinator-skill`| 다중 에이전트 복원력 및 자가 치유 |
|`codebase-exploration-skill`| 코드베이스에 대한 심층적인 상황별 grep |

### 문서 (6)

| 스킬 | 설명 |
|-------|-------------|
|`document-writer-skill`| 기술 문서, ADR 및 RFC |
|`documentation-engineer-skill`| 문서화 시스템 및 지식 공유 |
|`technical-writer-skill`| API 문서, 사용자 가이드 및 튜토리얼 |
|`api-documenter-skill`| OpenAPI/Swagger 사양 |
|`docx-skill`| Word 문서 자동화 |
|`pptx-skill`| 파워포인트 자동화 |
|`pdf-skill`| PDF 생성 및 조작 |
|`xlsx-skill`| Excel 워크플로 자동화 |

### 윈도우 및 파워셸 (7)

| 스킬 | 설명 |
|-------|-------------|
|`windows-infra-admin-skill`| AD, DNS/DHCP 및 그룹 정책 |
|`m365-admin-skill`| Microsoft 365 관리 및 그래프 API |
|`powershell-5.1-expert-skill`| WMI/ADSI가 포함된 레거시 Windows PowerShell |
|`powershell-7-expert-skill`| 크로스 플랫폼 PowerShell 코어 |
|`powershell-module-architect-skill`| PowerShell 모듈 설계 및 구조 |
|`powershell-ui-architect-skill`| WinForms/WPF를 사용한 PowerShell GUI/TUI |
|`it-ops-orchestrator-skill`| 도메인 간 IT 작업 조정 |

### 프로젝트 관리 (7)

| 스킬 | 설명 |
|-------|-------------|
|`product-manager-skill`| 제품 전략 및 로드맵 개발 |
|`project-manager-skill`| 전통적이고 민첩한 프로젝트 관리 |
|`scrum-master-skill`| 스크럼 촉진 및 팀 코칭 |
|`business-analyst-skill`| 요구사항 엔지니어링 및 BPMN |
|`bmad-bmm-analyst-skill`| BMAD 방법론 비즈니스 분석 |
|`bmad-master-skill`| BMAD 워크플로우 조정 |
|`ux-researcher-skill`| 사용자 조사 및 행동 분석 |

### 연구 및 분석 (5)

| 스킬 | 설명 |
|-------|-------------|
|`research-analyst-skill`| 다중 소스 연구 및 합성 |
|`market-researcher-skill`| 시장 분석 및 소비자 통찰력 |
|`competitive-analyst-skill`| 경쟁사 분석 및 포지셔닝 |
|`search-specialist-skill`| 고급 정보 검색 |
|`technical-advisory-skill`| 아키텍처 결정을 위한 전문가 지침 |

### 커뮤니케이션 및 마케팅 (5)

| 스킬 | 설명 |
|-------|-------------|
|`content-marketer-skill`| 콘텐츠 전략 및 SEO 스토리텔링 |
|`sales-engineer-skill`| 기술 데모 및 PoC 검증 |
|`customer-success-manager-skill`| 온보딩, 채택 및 유지 |
|`internal-comms-skill`| 기업 커뮤니케이션 및 변화 관리 |
|`seo-specialist-skill`| 검색 순위 및 유기적 트래픽 |

### 에이전트 오케스트레이션(7)

| 스킬 | 설명 |
|-------|-------------|
|`agent-organizer-skill`| 다중 에이전트 시스템 설계 및 조정 |
|`multi-agent-coordinator-skill`| 확장을 통한 100개 이상의 에이전트 조정 |
|`task-distributor-skill`| 로드 밸런싱 및 토큰 경제학 |
|`performance-monitor-skill`| 에이전트 벤치마킹 및 대기 시간 분석 |
|`explore-skill`| 코드베이스 탐색을 위한 상황별 grep |
|`librarian-skill`| 외부 참고자료 및 문서 검색 |
|`oracle-skill`| 복잡한 결정을 위한 전문가의 추론 |
|`general-skill`| 범용연구 및 과제수행 |
|`plan-skill`| 전략기획 및 업무분류 |

### 개발자 도구 (5)

| 스킬 | 설명 |
|-------|-------------|
|`tooling-engineer-skill`| CLI 유틸리티 및 IDE 확장 |
|`cli-developer-skill`| 명령줄 및 터미널 인터페이스 |
|`git-workflow-manager-skill`| Git 분기 및 협업 전략 |
|`dx-optimizer-skill`| 개발자 포털 및 DORA 측정항목 |
|`skill-creator-skill`| 새로운 기술 창출을 위한 가이드 |

### 전문 (6)

| 스킬 | 설명 |
|-------|-------------|
|`blockchain-developer-skill`| 스마트 계약 및 DeFi 프로토콜 |
|`wordpress-master-skill`| WordPress 테마, 플러그인 및 확장 |
|`slack-expert-skill`| Bolt를 사용한 Slack 앱 개발 |
|`multimodal-looker-skill`| PDF, 이미지 및 다이어그램 분석 |

## 스킬 파일 형식

모든 기술은 마크다운 콘텐츠와 함께 YAML 머리말을 사용합니다.
```yaml
---
name: skill-name
description: Third-person description with trigger phrases. Use when...
---

# Skill Content

Instructions, patterns, and best practices...
```
### 요구 사항

- **이름**: 소문자, 하이픈만 가능, 최대 64자
- **설명**: 3인칭 음성, 최대 1024자, 트리거 문구 포함
- **내용**: 500줄 미만(대규모 기술의 경우 REFERENCE.md 사용)

## 점진적 공개

대규모 스킬(500줄 이상)은 다음과 같이 나뉩니다.

-`SKILL.md` / `skill.yaml`- 핵심 지침(500줄 미만)
-`REFERENCE.md`- 상세한 패턴 및 템플릿
-`EXAMPLES.md`- 코드 예시 및 사용 사례

## 인류적 준수

이 컬렉션은 [공식 인류학 기술 사양](https://docs.claude.com/en/docs/claude-code/skills)을 따릅니다.

- 대소문자를 구분합니다.`SKILL.md`파일 이름(메인 브랜치)
- 깨끗한 앞부분(만`name`그리고`description`)
- 유발 용어가 포함된 3인칭 설명
- 대규모 스킬에 대한 점진적 공개

## 기여

1. 저장소 포크
2. 스킬 디렉터리를 생성합니다:`my-skill-skill/`3. 추가`SKILL.md`적절한 머리말로
4. 유사한 기술의 기존 패턴을 따르십시오.
5. 풀 요청 제출

## 라이선스

MIT 라이선스 - 무료로 사용하고 수정할 수 있습니다.

## 리소스

- [인류 기술 문서](https://docs.claude.com/en/docs/claude-code/skills)
- [인류학적 모범 사례](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Gemini CLI 스킬](https://geminicli.com/docs/cli/skills/)
- [반중력 문서](https://antigravity.google/docs/skills)