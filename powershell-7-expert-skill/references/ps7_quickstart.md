# PowerShell 7 전문가 - 빠른 시작 가이드

## 개요

이 기술은 PowerShell의 최신 크로스 플랫폼 버전인 PowerShell 7+에 대한 전문 지식을 제공합니다. REST API 자동화, 컨테이너 지원 및 클라우드 통합이 포함됩니다.

## 전제 조건

- PowerShell 7.0 이상이 설치되어 있습니다.
- 크로스 플랫폼 지원(Windows, Linux, macOS)
- REST API 호출을 위한 인터넷 액세스(선택 사항)

## 시작하기

### 1. 파워셸 7을 설치한다

#### 윈도우```powershell
# Using winget
winget install Microsoft.PowerShell

# Or download from GitHub
# https://github.com/PowerShell/PowerShell/releases
```

#### 리눅스(우분투)```bash
# Download and install
wget https://github.com/PowerShell/PowerShell/releases/download/v7.4.0/powershell_7.4.0-1.deb_amd64.deb
sudo dpkg -i powershell_7.4.0-1.deb_amd64.deb
```

#### 맥OS```bash
# Using Homebrew
brew install powershell
```

### 2. 설치 확인

```powershell
# Check version
$PSVersionTable.PSVersion

# Check platform
if ($IsWindows) { Write-Host "Running on Windows" }
if ($IsLinux) { Write-Host "Running on Linux" }
if ($IsMacOS) { Write-Host "Running on macOS" }
```

### 3. 크로스 플랫폼 자동화

```powershell
# Run cross-platform deployment
.\scripts\crossplatform_automation.ps1 -TargetOS Linux -Action Deploy -ApiEndpoint "https://api.example.com"

# Configure platform
.\scripts\crossplatform_automation.ps1 -TargetOS Windows -Action Configure -ConfigurationData @{
    Setting1 = "Value1"
    Setting2 = "Value2"
}

# Monitor platform
.\scripts\crossplatform_automation.ps1 -TargetOS macOS -Action Monitor
```

### 4. REST API 소비

```powershell
# Basic GET request
.\scripts\rest_api_consumer.ps1 -Uri "https://api.github.com/user" -Method GET

# With authentication
.\scripts\rest_api_consumer.ps1 `
    -Uri "https://api.example.com/data" `
    -Method POST `
    -AuthType Bearer `
    -Token "your-token-here" `
    -Body @{
        name = "Test"
        value = 123
    }

# With retry logic
.\scripts\rest_api_consumer.ps1 `
    -Uri "https://api.example.com/data" `
    -Method GET `
    -MaxRetries 5 `
    -RetryDelaySeconds 2
```

### 5. PowerShell 갤러리에 게시

```powershell
# Publish module
.\scripts\publish_to_gallery.ps1 `
    -ModulePath "./MyModule" `
    -ApiKey "your-api-key" `
    -SkipTests:$false

# Publish as prerelease
.\scripts\publish_to_gallery.ps1 `
    -ModulePath "./MyModule" `
    -ApiKey "your-api-key" `
    -Prerelease
```

## 최신 PowerShell 7 기능

### 삼항 연산자

```powershell
# Old way
$result = if ($condition) { "yes" } else { "no" }

# New way
$result = $condition ? "yes" : "no"
```

### 널 병합 연산자

```powershell
# Old way
if ($null -eq $value) {
    $value = "default"
}

# New way
$value = $value ?? "default"
```

### 파이프라인 체인 운영자

```powershell
# Old way
Get-ChildItem | Where-Object { $_.Extension -eq '.txt' }

# New way
Get-ChildItem | Where-Object Extension -eq '.txt'

# Chain operators
Get-ChildItem | Where-Object Extension -eq '.txt' | ForEach-Object FullName
```

### Foreach 메서드

```powershell
# Old way
1..5 | ForEach-Object { Write-Host $_ }

# New way
1..5.ForEach({ Write-Host $_ })
```

### Where 메소드

```powershell
# Old way
$numbers = 1..100
$even = $numbers | Where-Object { $_ % 2 -eq 0 }

# New way
$numbers = 1..100
$even = $numbers.Where({ $_ % 2 -eq 0 })
```

## 컨테이너 지원

### 도커 통합

```powershell
# Check Docker availability
docker --version

# Run container
docker run -d --name ps7-container -p 8080:80 nginx

# List containers
docker ps

# Stop container
docker stop ps7-container

# Remove container
docker rm ps7-container
```

### 컨테이너의 PowerShell

```powershell
# Run PowerShell in container
docker run --rm -it mcr.microsoft.com/powershell:latest

# Mount local directory
docker run --rm -it -v ${PWD}:/data mcr.microsoft.com/powershell:latest

# Run script in container
docker run --rm -v ${PWD}:/data mcr.microsoft.com/powershell:latest pwsh -File /data/script.ps1
```

## 타입스크립트 통합

```typescript
import PowerShell7Manager from './scripts/ps7_wrapper';

const ps7 = new PowerShell7Manager('./scripts');

// Cross-platform automation
await ps7.crossPlatformAutomation({
  targetOS: 'Linux',
  action: 'Deploy',
  apiEndpoint: 'https://api.example.com',
  containerImage: 'nginx:latest',
  configurationData: {
    ENV: 'production'
  }
});

// REST API call
await ps7.consumeRestApi({
  uri: 'https://api.github.com/user',
  method: 'GET',
  authType: 'Bearer',
  token: 'github-token',
  maxRetries: 3
});

// Publish module
await ps7.publishToGallery({
  modulePath: './MyModule',
  apiKey: 'psgallery-api-key',
  skipTests: false
});
```

## 모범 사례

1. PS 7 전용 스크립트에는 `#Requires -Version 7.0`을 사용하세요.
2. `$IsWindows`, `$IsLinux`, `$IsMacOS`과의 플랫폼 호환성을 확인하세요.
3. 크로스 플랫폼 경로에는 슬래시 `/`를 사용하세요.
4. 적절한 오류 처리 및 로깅 구현
5. 코드 품질을 위해 PSScriptAnalyzer를 사용하세요
6. Pester로 포괄적인 테스트 작성
7. 내보낸 모든 기능을 문서화하세요.
8. 모듈에 의미론적 버전 관리를 사용하세요.

## 문제 해결

### PowerShell 7을 찾을 수 없음

**오류:** pwsh: 명령을 찾을 수 없습니다.

**해결책:** 공식 저장소에서 PowerShell 7을 설치합니다.

### 교차 플랫폼 경로 문제

**오류:** 경로 구분 기호로 인해 파일을 찾을 수 없습니다.

**해결책:** 경로에 `Join-Path` 또는 슬래시 `/`를 사용하세요.

### REST API 오류

**오류:** 상태 코드 401로 인해 API 요청이 실패했습니다.

**해결책:** 인증 자격 증명 및 토큰 유효성을 확인하세요.

### 모듈 가져오기 실패

**오류:** 파일이나 어셈블리를 로드할 수 없습니다.

**해결책:** 모듈 종속성 및 .NET 버전 요구 사항을 확인하세요.

## 다음 단계

- 고급 주제에 대한 `references/` 디렉터리 탐색
- PowerShell 7 모범 사례는 `modern_ps_guide.md`을 검토하세요.
- 원하는 상태 구성을 보려면 `dsc_patterns.md`을 확인하세요.
- JEA(Just Enough Administration)에 대해 알아보세요.

## 지원하다

문제나 질문이 있는 경우 다음을 참조하세요.
- [PowerShell 7 설명서](https://docs.microsoft.com/en-us/powershell/scripting/whats-new/what-s-new-in-powershell-70)
- [PowerShell GitHub 리포지토리](https://github.com/PowerShell/PowerShell)
- [PowerShell 커뮤니티](https://github.com/PowerShell/PowerShell/discussions)