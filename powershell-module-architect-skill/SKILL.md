---
name: powershell-module-architect
description: 사용자가 PowerShell 모듈 디자인, 함수 구조, 재사용 가능한 라이브러리, 프로필 최적화 또는 PowerShell 5.1 및 PowerShell 7+ 전반의 버전 간 호환성이 필요할 때 사용합니다.
---
# PowerShell 모듈 설계자

## 목적

구조화되고 재사용 가능하며 유지 관리 가능한 PowerShell 모듈 생성을 전문으로 하는 PowerShell 모듈 설계 및 아키텍처 전문 지식을 제공합니다. 엔터프라이즈 PowerShell 환경을 위한 모듈 아키텍처, 기능 설계, 버전 간 호환성 및 프로필 최적화에 중점을 둡니다.

## 사용 시기

- 흩어져 있는 스크립트를 구조화되고 재사용 가능한 모듈로 변환
- Public/Private 기능 분리를 통한 모듈 아키텍처 설계
- 버전 간 호환 모듈 생성(PowerShell 5.1 및 7+)
- 더 빠른 로드 시간을 위해 PowerShell 프로필 최적화
- 적절한 매개변수 검증을 통해 고급 기능 구축

## 빠른 시작

**다음과 같은 경우에 이 스킬을 호출하세요:**
- 흩어져 있는 스크립트를 구조화되고 재사용 가능한 모듈로 변환
- Public/Private 기능 분리를 통한 모듈 아키텍처 설계
- 버전 간 호환 모듈 생성(PowerShell 5.1 및 7+)
- 더 빠른 로드 시간을 위해 PowerShell 프로필 최적화
- 적절한 매개변수 검증을 통해 고급 기능 구축

**다음과 같은 경우에는 호출하지 마세요**
- 재사용되지 않는 간단한 일회용 스크립트(powershell-5.1-expert 또는 powershell-7-expert 사용)
- 기능 추가가 필요한 잘 구성된 모듈이 이미 있음(관련 도메인 기술 사용)
- UI 개발(대신 powershell-ui-architect 사용)
- 보안 강화(대신 powershell-security-hardening 사용)

## 의사결정 프레임워크

### 모듈을 생성해야 하는 경우

| 대본 | 추천 |
|----------|----------------|
| 3개 이상의 관련 기능 | 모듈 생성 |
| 팀 간 공유 필요 | 모듈 + 매니페스트 만들기 |
| 일회용 자동화 | 스크립트로 유지 |
| 복잡한 매개변수 세트 | 모듈의 고급 기능 |
| 버전 호환성 필요 | 호환성 레이어가 있는 모듈 |

### 모듈 구조 결정

```
Script Organization Need
│
├─ Few related functions (3-10)?
│  └─ Single .psm1 with inline functions
│
├─ Many functions (10+)?
│  └─ Dot-source pattern (Public/Private folders)
│
├─ Publishing to gallery?
│  └─ Full manifest + tests + docs
│
└─ Team collaboration?
   └─ Git repo + CI/CD + Pester tests
```

## 핵심 작업 흐름: 스크립트를 모듈로 변환

**사용 사례:** 10-50개의 흩어져 있는 .ps1 스크립트를 체계적인 모듈로 리팩터링

### 1단계: 분석

```powershell
# Inventory existing scripts
$scripts = Get-ChildItem -Path ./scripts -Filter *.ps1 -Recurse

# Analyze function signatures
foreach ($script in $scripts) {
    $content = Get-Content $script.FullName -Raw
    $functions = [regex]::Matches($content, 'function\s+(\S+)')
    
    Write-Host "$($script.Name): $($functions.Count) functions"
}

# Expected output:
# AD-UserManagement.ps1: 12 functions
# AD-GroupManagement.ps1: 8 functions
# Common-Helpers.ps1: 15 functions (candidates for Private/)
```

### 2단계: 모듈 구조 설계

```powershell
# Create module skeleton
$moduleName = "Organization.ActiveDirectory"
$modulePath = "./modules/$moduleName"

New-Item -Path "$modulePath/Public" -ItemType Directory -Force
New-Item -Path "$modulePath/Private" -ItemType Directory -Force
New-Item -Path "$modulePath/Tests" -ItemType Directory -Force
New-Item -Path "$modulePath/$moduleName.psm1" -ItemType File -Force
New-Item -Path "$modulePath/$moduleName.psd1" -ItemType File -Force
```

### 3단계: 기능 분류

```
Public functions (exported to users):
  ├─ Get-OrgADUser
  ├─ New-OrgADUser
  ├─ Set-OrgADUser
  ├─ Remove-OrgADUser
  └─ ... (user-facing functions)

Private functions (internal helpers):
  ├─ _ValidateDomainConnection
  ├─ _BuildDistinguishedName
  ├─ _ConvertToCanonicalName
  └─ ... (utility functions)
```

### 4단계: 모듈 파일 구현

```powershell
# Organization.ActiveDirectory.psm1

# Dot-source Private functions first
$Private = @(Get-ChildItem -Path $PSScriptRoot\Private\*.ps1 -ErrorAction SilentlyContinue)
foreach ($import in $Private) {
    try {
        . $import.FullName
    } catch {
        Write-Error "Failed to import private function $($import.FullName): $_"
    }
}

# Dot-source Public functions
$Public = @(Get-ChildItem -Path $PSScriptRoot\Public\*.ps1 -ErrorAction SilentlyContinue)
foreach ($import in $Public) {
    try {
        . $import.FullName
    } catch {
        Write-Error "Failed to import public function $($import.FullName): $_"
    }
}

# Export Public functions explicitly
Export-ModuleMember -Function $Public.BaseName
```

### 5단계: 모듈 매니페스트 생성

```powershell
# Generate manifest
$manifestParams = @{
    Path              = "$modulePath/$moduleName.psd1"
    RootModule        = "$moduleName.psm1"
    ModuleVersion     = '1.0.0'
    Author            = 'IT Team'
    CompanyName       = 'Organization'
    Description       = 'Active Directory management functions'
    PowerShellVersion = '5.1'  # Minimum version
    FunctionsToExport = @(
        'Get-OrgADUser',
        'New-OrgADUser',
        'Set-OrgADUser',
        'Remove-OrgADUser'
    )
    VariablesToExport = @()
    AliasesToExport   = @()
}
New-ModuleManifest @manifestParams
```

### 6단계: Pester 테스트 추가

```powershell
# Tests/Module.Tests.ps1
BeforeAll {
    Import-Module "$PSScriptRoot/../Organization.ActiveDirectory.psd1" -Force
}

Describe "Organization.ActiveDirectory Module" {
    It "Exports expected functions" {
        $commands = Get-Command -Module Organization.ActiveDirectory
        $commands.Count | Should -BeGreaterThan 0
    }
    
    It "Has valid module manifest" {
        $manifest = Test-ModuleManifest -Path "$PSScriptRoot/../Organization.ActiveDirectory.psd1"
        $manifest.Version | Should -Be '1.0.0'
    }
}

Describe "Get-OrgADUser" {
    It "Accepts Identity parameter" {
        { Get-OrgADUser -Identity "testuser" -WhatIf } | Should -Not -Throw
    }
}
```

## 빠른 참조: 고급 기능 템플릿

```powershell
function Get-OrgUser {
    <#
    .SYNOPSIS
        Retrieves Active Directory user by name.
    
    .DESCRIPTION
        Queries Active Directory for user object and returns detailed properties.
    
    .PARAMETER Name
        The username or SamAccountName to search for.
    
    .EXAMPLE
        Get-OrgUser -Name "jdoe"
        
        Returns all properties for user jdoe.
    
    .EXAMPLE
        "jdoe", "asmith" | Get-OrgUser
        
        Retrieves multiple users via pipeline.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory, ValueFromPipeline)]
        [ValidateNotNullOrEmpty()]
        [string]$Name
    )
    
    process {
        Get-ADUser -Identity $Name -Properties *
    }
}
```

## 통합 패턴

### powershell-5.1-전문가
- **Handoff**: 모듈 아키텍처 설계 → 5.1 전문가가 Windows 특정 기능 구현
- **협업**: 5.1 호환성을 고려한 모듈 구조 결정

### powershell-7-전문가
- **핸드오프**: 모듈 구조 정의 → 7명의 전문가가 최신 구문 최적화 추가
- **협업**: 버전 감지를 이용한 듀얼 모드 기능

### windows-인프라-관리자
- **Handoff**: 모듈 아키텍처 → Windows 관리자가 도메인별 로직을 구현합니다.
- **공동 책임**: Active Directory, GPO, DNS 모듈 기능

### Azure 인프라 엔지니어
- **핸드오프**: 모듈 패턴 → Azure 엔지니어가 클라우드 자동화 모듈 구축
- **통합**: 온프레미스와 Azure를 결합한 크로스 클라우드 모듈

## 위험 신호 - 에스컬레이션해야 하는 경우

| 관찰 | 행동 |
|-------------|--------|
| 단일 모듈에 100개 이상의 기능 | 하위 모듈로 분할하는 것을 고려하세요. |
| 복잡한 버전 간 문제 | powershell-5.1 및 7 전문가에게 문의하세요. |
| 성능 <1s 프로필 로드 | 지연 로딩 패턴 적용 |
| 보안에 민감한 작업 | powershell 보안 강화 포함 |

## 추가 리소스

- **자세한 기술 참조**: [REFERENCE.md](REFERENCE.md) 참조
  - 프로필 최적화 작업 흐름
  - 모듈 매니페스트 템플릿
  - 동적 매개변수 패턴
  
- **코드 예제 및 패턴**: [EXAMPLES.md](EXAMPLES.md) 참조
  - 안티 패턴(모놀리식 파일, 도움말 누락)
  - 버전 간 호환성 패턴
  - 고급 매개변수 검증