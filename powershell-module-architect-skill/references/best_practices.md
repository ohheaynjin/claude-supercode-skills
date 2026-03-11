# PowerShell 모듈 모범 사례

## 개요

이 가이드에서는 PowerShell 모듈 개발, 테스트 및 배포에 대한 모범 사례를 간략하게 설명합니다.

## 코드 품질

### PSScriptAnalyzer 규칙

```powershell
# Install PSScriptAnalyzer
Install-Module PSScriptAnalyzer

# Run analysis on module
Invoke-ScriptAnalyzer -Path ".\MyModule" -Recurse

# Run specific rules
Invoke-ScriptAnalyzer -Path ".\MyModule" -Rules @(
    'PSUseApprovedVerbs',
    'PSAvoidUsingCmdletAliases',
    'PSProvideCommentHelp'
)

# Enable strict mode
$env:POWERSHELL_FORMAT_SETTINGS = @{
    Enable = $true
    Rules = @('PSUseCorrectCasing')
}
```

### 코드 스타일 지침

#### 명명 규칙

```powershell
# Good: Approved verbs
Get-Item
Set-Item
New-Item
Remove-Item
Test-Item
Update-Item

# Bad: Non-approved verbs
Retrieve-Item
Modify-Item
Make-Item
Delete-Item
Check-Item
```

#### 변수 이름 지정

```powershell
# Good: PascalCase for variables, camelCase for parameters
$ServerName
$ConfigurationData
param(
    [string]$serverName,
    [hashtable]$configData
)

# Bad: Inconsistent casing
$servername
$ConfigData
```

### 오류 처리

#### Try-Catch-Finally 패턴

```powershell
function Invoke-Operation {
    [CmdletBinding()]
    param(
        [string]$Path
    )
    
    try {
        # Validate input
        if (-not (Test-Path $Path)) {
            throw "Path does not exist: $Path"
        }
        
        # Perform operation
        $result = Get-Content -Path $Path
        
        return $result
    }
    catch [System.IO.FileNotFoundException] {
        Write-Error "File not found: $Path"
        throw
    }
    catch {
        Write-Error "Unexpected error: $_"
        throw
    }
    finally {
        # Cleanup
        Write-Verbose "Operation completed"
    }
}
```

#### 사용자 정의 오류 메시지

```powershell
function Set-Configuration {
    [CmdletBinding()]
    param(
        [string]$Key,
        [string]$Value
    )
    
    try {
        Set-ItemProperty -Path "HKLM:\Software\MyApp" -Name $Key -Value $Value
    }
    catch {
        $errorId = "ConfigurationSetFailed"
        $category = [System.Management.Automation.ErrorCategory]::InvalidOperation
        $errorRecord = [System.Management.Automation.ErrorRecord]::new(
            $_.Exception,
            $errorId,
            $category,
            $Key
        )
        
        $PSCmdlet.WriteError($errorRecord)
    }
}
```

## 매개변수 검증

### 내장 유효성 검사기

```powershell
param(
    # Validate not null or empty
    [Parameter(Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string]$Name,
    
    # Validate set of values
    [Parameter(Mandatory=$true)]
    [ValidateSet('Enable', 'Disable', 'Toggle')]
    [string]$Action,
    
    # Validate range
    [Parameter(Mandatory=$false)]
    [ValidateRange(1, 100)]
    [int]$Count,
    
    # Validate pattern
    [Parameter(Mandatory=$false)]
    [ValidatePattern('^[a-zA-Z0-9]+$')]
    [string]$Identifier,
    
    # Validate script
    [Parameter(Mandatory=$true)]
    [ValidateScript({
        if (-not (Test-Path $_)) {
            throw "Path does not exist: $_"
        }
        $true
    })]
    [string]$Path,
    
    # Validate length
    [Parameter(Mandatory=$false)]
    [ValidateLength(1, 50)]
    [string]$Description,
    
    # Validate credential
    [Parameter(Mandatory=$false)]
    [pscredential]$Credential
)
```

### 사용자 정의 유효성 검사기

```powershell
function Validate-EmailAddress {
    param(
        [Parameter(Mandatory=$true)]
        [string]$EmailAddress
    )
    
    if ($EmailAddress -notmatch '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$') {
        throw "Invalid email address format"
    }
}

# Usage
param(
    [ValidateScript({
        try {
            Validate-EmailAddress -EmailAddress $_
        }
        catch {
            throw $_
        }
    })]
    [string]$Email
)
```

## 성능 최적화

### 파이프라인 모범 사례

```powershell
# Good: Use pipeline
Get-ChildItem | Where-Object Extension -eq '.txt' | ForEach-Object Name

# Bad: Use variables
$files = Get-ChildItem
$txtFiles = $files | Where-Object { $_.Extension -eq '.txt' }
$names = $txtFiles | ForEach-Object { $_.Name }
```

### 객체 생성

```powershell
# Good: Use PSCustomObject
$object = [PSCustomObject]@{
    Name = "Test"
    Value = 123
}

# Better: Use OrderedDictionary for predictable properties
$object = [PSCustomObject][ordered]@{
    Name = "Test"
    Value = 123
}
```

### 불필요한 작업을 피하세요

```powershell
# Bad: Repeated property access
if ($object.Property -eq 'value') {
    $result = $object.Property
}

# Good: Cache property access
$propertyValue = $object.Property
if ($propertyValue -eq 'value') {
    $result = $propertyValue
}
```

## 테스트

### 테스트 조직

```
Tests/
├── Unit/
│   ├── Public/
│   │   ├── Get-Item.Tests.ps1
│   │   └── Set-Item.Tests.ps1
│   └── Private/
│       └── Helper-Function.Tests.ps1
├── Integration/
│   └── EndToEnd.Tests.ps1
└── Tests.ps1
```

### 테스트 구조

```powershell
Describe "Get-Item Unit Tests" {
    BeforeAll {
        Import-Module "$PSScriptRoot\..\..\MyModule.psd1"
    }
    
    Context "Parameter Validation" {
        It "Should accept valid name" {
            { Get-Item -Name "Test" } | Should -Not -Throw
        }
        
        It "Should reject empty name" {
            { Get-Item -Name "" } | Should -Throw
        }
    }
    
    Context "Output Validation" {
        It "Should return PSObject" {
            $result = Get-Item -Name "Test"
            $result | Should -BeOfType System.Management.Automation.PSObject
        }
        
        It "Should have Name property" {
            $result = Get-Item -Name "Test"
            $result.PSObject.Properties.Name | Should -Contain 'Name'
        }
    }
}
```

## 보안

### 보안 문자열

```powershell
# Read credential securely
$credential = Get-Credential
$password = $credential.Password | ConvertFrom-SecureString

# Create secure string
$secureString = Read-Host "Enter password" -AsSecureString

# Use in commands
Invoke-Command -ComputerName "server" -Credential $credential
```

### 실행 정책

```powershell
# Check execution policy
Get-ExecutionPolicy -List

# Set execution policy
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### 서명 스크립트

```powershell
# Sign script
Set-AuthenticodeSignature -FilePath ".\script.ps1" -Certificate $cert

# Verify signature
Get-AuthenticodeSignature -FilePath ".\script.ps1"
```

## 문서

### 설명 기반 도움말

```powershell
<#
.SYNOPSIS
    Brief description of the function
.DESCRIPTION
    Detailed description of what the function does
.PARAMETER Parameter1
    Description of Parameter1
.PARAMETER Parameter2
    Description of Parameter2
.EXAMPLE
    PS C:\> Get-Item -Name "Test"
    Returns the item named "Test"
.EXAMPLE
    PS C:\> Get-Item -Id 123
    Returns the item with ID 123
.INPUTS
    String, Integer
.OUTPUTS
    System.Management.Automation.PSObject
.NOTES
    Additional information about the function
.LINK
    https://docs.example.com/get-item
#>
```

### 외부 문서

1. **README.md**: 모듈 개요 및 빠른 시작
2. **CHANGELOG.md**: 버전 기록 및 변경 사항
3. **라이선스**: 라이선스 정보
4. **CONTRIBUTING.md**: 기여 지침
5. **예/**: 사용 예

## 버전 관리

### 의미적 버전 관리

```
MAJOR.MINOR.PATCH

MAJOR: Incompatible API changes
MINOR: Backward-compatible functionality additions
PATCH: Backward-compatible bug fixes
```

### 모듈 매니페스트 버전

```powershell
@{
    ModuleVersion = '1.2.3'
    # ...
}
```

### 출시 프로세스

1. 매니페스트의 버전 업데이트
2. CHANGELOG.md 업데이트
3. 버전 관리의 태그 릴리스
4. 테스트 실행
5. 갤러리에 게시
6. 릴리스 노트 작성

## 분포

### 파워셸 갤러리

```powershell
# Publish module
Publish-Module -Path ".\MyModule" -NuGetApiKey "your-api-key"

# Update module
Update-Module -Name MyModule

# Find module
Find-Module -Name MyModule
```

### 개인 저장소

```powershell
# Register private repository
Register-PSRepository -Name "MyRepo" -SourceLocation "https://myrepo.local/nuget"

# Publish to private repository
Publish-Module -Path ".\MyModule" -NuGetApiKey "your-api-key" -Repository MyRepo
```

## 문제 해결

### 일반적인 문제

**문제:** 설치 후 모듈을 찾을 수 없음

**해결책:** 모듈 경로 새로 고침```powershell
Import-Module MyModule -Force
```

**문제:** 함수가 내보내지지 않음

**해결책:** 매니페스트에서 FunctionsToExport를 확인하세요.```powershell
Get-Module MyModule | Select-Object ExportedFunctions
```

**문제:** 테스트 실패

**해결책:** 자세한 출력으로 Pester를 실행하세요.```powershell
Invoke-Pester -Path ".\Tests" -Verbose
```

## 자원

- [PSScriptAnalyzer 규칙](https://github.com/PowerShell/PSScriptAnalyzer#rules)
- [페스터 문서](https://pester.dev/docs/)
- [PowerShell 모범 사례](https://docs.microsoft.com/en-us/powershell/scripting/dev-cross-plat/best-practices)
- [PowerShell 갤러리 지침](https://docs.microsoft.com/en-us/powershell/gallery/psgallery/publishing-guidelines)