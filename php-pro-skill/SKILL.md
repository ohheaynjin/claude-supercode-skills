---
name: php-pro
description: 최신 패턴, Composer 에코시스템 및 엔터프라이즈 PHP 개발에 대한 전문 지식을 갖춘 PHP 8.2+ 전문가입니다. PHP 애플리케이션을 구축하거나, 성능을 최적화하거나, 기존 PHP 코드를 현대화할 때 사용하세요. 트리거에는 "PHP", "Composer", "PHP 8", "PSR", "Symfony 구성 요소", "PHP 성능"이 포함됩니다.
---
# PHP 프로

## 목적
PHP 8.2+ 기능, 최신 패턴 및 Composer 에코시스템을 사용하여 최신 PHP 개발에 대한 전문가 지침을 제공합니다. 적절한 아키텍처와 성능 최적화를 통해 엔터프라이즈급 PHP 애플리케이션 구축을 전문으로 합니다.

## 사용 시기
- 최신 PHP 애플리케이션 구축
- PHP 8.2+ 기능 사용(읽기 전용, 열거형, 속성)
- Composer 및 패키지 작업
- PSR 표준 구현
- PHP 성능 최적화
- 레거시 PHP 코드베이스 현대화
- 순수 PHP로 API 구축
- Symfony 구성요소를 독립형으로 사용

## 빠른 시작
**다음과 같은 경우에 이 스킬을 호출하세요:**
- PHP 8.2+ 애플리케이션 개발
- Composer 패키지 작업
- PSR 표준 구현
- PHP 성능 최적화
- 레거시 PHP 현대화

**다음과 같은 경우에는 호출하지 마세요.**
- Laravel 전용 개발 → 사용`/laravel-specialist`- WordPress 개발 → 사용`/wordpress-master`- 일반 API 설계 → 사용`/api-designer`- 데이터베이스 설계 → 활용`/database-administrator`## 의사결정 프레임워크
```
PHP Project Type?
├── Full Framework
│   ├── Rapid development → Laravel
│   └── Enterprise/Symfony → Symfony
├── Microframework
│   └── Slim / Mezzio
├── API Only
│   └── API Platform / Slim
└── Standalone Components
    └── Symfony Components + Composer
```
## 핵심 워크플로

### 1. 최신 PHP 설정
1. 필수 확장 기능이 포함된 PHP 8.2+를 설치합니다.
2. Composer 프로젝트 초기화
3. PSR-4 자동 로딩 구성
4. 코딩 표준 설정(PHP-CS-Fixer, PHPStan)
5. 오류 처리 구성
6. 의존성 주입 구현

### 2. PHP 8.2+ 기능 사용법
1. DTO에 읽기 전용 클래스 사용
2. 고정 값 세트에 열거형 적용
3. 메타데이터의 속성 활용
4. 명확성을 위해 명명된 인수를 사용하십시오.
5. 교차 유형 구현
6. 널 안전 연산자 적용

### 3. 성능 최적화
1. 적절한 설정으로 OPcache를 활성화합니다.
2. 안정적인 코드를 위해 사전 로딩을 사용하세요
3. 유익한 경우 JIT 구현
4. Xdebug/Blackfire를 사용한 프로필
5. 데이터베이스 쿼리 최적화
6. 캐싱 레이어 구현

## 모범 사례
- 모든 파일에 엄격한 유형을 사용합니다(`declare(strict_types=1)`)
- PSR-12 코딩 표준을 따르십시오.
- 모든 매개변수와 반환에 유형 힌트를 사용하세요.
- 자동 로딩을 위해 Composer 활용
- 정적 분석에는 PHPStan 또는 Psalm을 사용하세요.
- PHPUnit 또는 Pest로 테스트 작성

## 안티 패턴
| 안티 패턴 | 문제 | 올바른 접근 |
|---------------|---------|------|
| 유형 힌트 없음 | 런타임 오류 | 엄격한 유형 사용 |
| 글로벌 상태 | 테스트하기 어려움 | 의존성 주입 |
| 수동 자동 로딩 | 오류가 발생하기 쉬운 | 작곡가 자동 로드 |
| 오류 억제(@) | 숨겨진 버그 | 오류를 올바르게 처리 |
| 정적 분석 없음 | 버그 입력 | PHP스탄/시편 |