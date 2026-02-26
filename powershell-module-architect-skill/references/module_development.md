# PowerShell 모듈 개발 가이드

## 개요

이 가이드에서는 구조, 패키징 및 배포를 포함하여 PowerShell 모듈 개발에 대한 모범 사례를 다룹니다.

## 모듈 구조

### 표준 모듈 레이아웃
```
MyModule/
├── MyModule.psd1          # Module manifest
├── MyModule.psm1          # Module script
├── Public/                # Public functions
│   ├── Get-Item.ps1
│   ├── Set-Item.ps1
│   └── Remove-Item.ps1
├── Private/               # Private helper functions
│   ├── Helper-Function.ps1
│   └── Utility-Function.ps1
├── Classes/               # PowerShell classes
│   └── MyClass.ps1
├── Formats/               # Format specifications
│   └── MyModule.format.ps1xml
├── Types/                 # Type extensions
│   └── MyModule.types.ps1xml
├── Tests/                 # Pester tests
│   ├── Unit/
│   │   └── Get-Item.Tests.ps1
│   └── Integration/
│       └── Integration.Tests.ps1
├── Examples/              # Example scripts
│   └── Basic-Usage.ps1
├── en-US/                 # Help files
│   └── about_MyModule.help.txt
├── README.md              # Module documentation
└── LICENSE                # License file
```
## 모듈 매니페스트

### 매니페스트 만들기
```powershell
# MyModule.psd1
@{
    RootModule = 'MyModule.psm1'
    ModuleVersion = '1.0.0'
    GUID = '12345678-1234-1234-1234-123456789012'
    Author = 'Your Name'
    CompanyName = 'Your Company'
    Copyright = '(c) 2024 Your Company'
    Description = 'Description of your module'
    PowerShellVersion = '5.1'
    CompatiblePSEditions = @('Desktop', 'Core')
    FunctionsToExport = @('Get-Item', 'Set-Item', 'Remove-Item')
    CmdletsToExport = @()
    VariablesToExport = @()
    AliasesToExport = @()
    RequiredModules = @()
    Tags = @('PowerShell', 'Module')
    ProjectUri = 'https://github.com/yourusername/MyModule'
    LicenseUri = 'https://github.com/yourusername/MyModule/blob/main/LICENSE'
    ReleaseNotes = 'Initial release'
}
```
### 매니페스트 모범 사례

1. 의미론적 버전 관리(MAJOR.MINOR.PATCH)를 사용합니다.
2. 공개 함수만 내보내기(와일드카드 사용 안함)
3. 포괄적인 메타데이터 포함
4. 최소 PowerShell 버전을 지정하세요.
5. 검색 가능성을 위한 태그 추가
6. 프로젝트 및 라이선스 URL을 포함하세요.
7. 크로스 플랫폼 지원을 위해 CompatiblePSEditions 설정

## 모듈 스크립트

### 기본 모듈 스크립트
```powershell
# MyModule.psm1
$ErrorActionPreference = 'Stop'

# Load public functions
Get-ChildItem -Path "$PSScriptRoot\Public" -Filter "*.ps1" | ForEach-Object {
    . $_.FullName
}

# Load private functions
Get-ChildItem -Path "$PSScriptRoot\Private" -Filter "*.ps1" | ForEach-Object {
    . $_.FullName
}

# Export only public functions
$publicFunctions = Get-ChildItem -Path "$PSScriptRoot\Public" -Filter "*.ps1" | 
                   ForEach-Object { [System.IO.Path]::GetFileNameWithoutExtension($_.FullName) }

Export-ModuleMember -Function $publicFunctions
```
## 공개 함수

### 함수 템플릿
```powershell
# Public/Get-Item.ps1
<#
.SYNOPSIS
    Retrieves items from the system
.DESCRIPTION
    Detailed description of the Get-Item function
.PARAMETER Name
    The name of the item to retrieve
.PARAMETER Id
    The ID of the item to retrieve
.EXAMPLE
    Get-Item -Name "MyItem"
.EXAMPLE
    Get-Item -Id 123
.INPUTS
    None
.OUTPUTS
    System.Management.Automation.PSObject
.NOTES
    Additional information
#>

function Get-Item {
    [CmdletBinding(DefaultParameterSetName='Name')]
    param(
        [Parameter(Mandatory=$true, ParameterSetName='Name')]
        [ValidateNotNullOrEmpty()]
        [string]$Name,
        
        [Parameter(Mandatory=$true, ParameterSetName='Id')]
        [ValidateRange(1, [int]::MaxValue)]
        [int]$Id,
        
        [Parameter(Mandatory=$false)]
        [switch]$IncludeDetails
    )
    
    begin {
        Write-Verbose "Starting Get-Item"
    }
    
    process {
        try {
            Write-Verbose "Processing request"
            
            # Implementation
            $result = [PSCustomObject]@{
                Name = $Name
                Id = $Id
                Details = if ($IncludeDetails) { "Detailed information" } else { $null }
            }
            
            return $result
        }
        catch {
            Write-Error "Error in Get-Item: $_"
            throw
        }
    }
    
    end {
        Write-Verbose "Completing Get-Item"
    }
}
```
### 함수 모범 사례

1. 항상 사용하세요`CmdletBinding()`2. 포괄적인 설명 기반 도움말 포함
3. 매개변수 검증 사용
4. 적절한 오류 처리 구현
5. 디버깅을 위해 자세한 출력을 사용하세요.
6. PowerShell 동사-명사 명명을 따릅니다.
7. 기능에 집중하고 단일 목적으로 유지하세요.
8. 텍스트가 아닌 객체를 반환합니다.

## 비공개 기능

### 도우미 함수 예
```powershell
# Private/Helper-Function.ps1
function Invoke-ApiCall {
    [CmdletBinding()]
    param(
        [string]$Endpoint,
        [string]$Method = 'GET',
        [hashtable]$Headers = @{}
    )
    
    try {
        $params = @{
            Uri = $Endpoint
            Method = $Method
            Headers = $Headers
            ErrorAction = 'Stop'
        }
        
        return Invoke-RestMethod @params
    }
    catch {
        Write-Error "API call failed: $_"
        throw
    }
}
```
## 수업

### PowerShell 클래스
```powershell
# Classes/MyClass.ps1
class MyClass {
    [string]$Name
    [int]$Id
    [bool]$Active
    
    # Constructor
    MyClass([string]$name, [int]$id) {
        $this.Name = $name
        $this.Id = $id
        $this.Active = $true
    }
    
    # Method
    [void] Activate() {
        $this.Active = $true
    }
    
    [void] Deactivate() {
        $this.Active = $false
    }
    
    [string] ToString() {
        return "$($this.Name) ($($this.Id))"
    }
}
```
## 형식 사양

### 사용자 정의 형식
```xml
<!-- Formats/MyModule.format.ps1xml -->
<Configuration>
    <ViewDefinitions>
        <View>
            <Name>MyModuleItem</Name>
            <ViewSelectedBy>
                <TypeName>MyModule.Item</TypeName>
            </ViewSelectedBy>
            <TableControl>
                <TableRowEntries>
                    <TableRowEntry>
                        <TableColumnItems>
                            <TableColumnItem>
                                <PropertyName>Id</PropertyName>
                            </TableColumnItem>
                            <TableColumnItem>
                                <PropertyName>Name</PropertyName>
                            </TableColumnItem>
                            <TableColumnItem>
                                <PropertyName>Active</PropertyName>
                            </TableColumnItem>
                        </TableColumnItems>
                    </TableRowEntry>
                </TableRowEntries>
            </TableControl>
        </View>
    </ViewDefinitions>
</Configuration>
```
## 유형 확장

### 유형 멤버 추가
```xml
<!-- Types/MyModule.types.ps1xml -->
<Types>
    <Type>
        <Name>MyModule.Item</Name>
        <Members>
            <ScriptMethod>
                <Name>ToJson</Name>
                <ScriptBlock>
                    $this | ConvertTo-Json -Depth 10
                </ScriptBlock>
            </ScriptMethod>
        </Members>
    </Type>
</Types>
```
## 포장

### NuGet 패키지 생성
```powershell
# Update module manifest version
$manifestPath = "MyModule.psd1"
Update-ModuleManifest -Path $manifestPath -ModuleVersion "1.1.0"

# Build module
# Ensure all files are in place

# Test module
Import-Module ".\MyModule.psd1"
Get-Command -Module MyModule

# Create NuGet package
# The module directory is ready for distribution
```
### PowerShellGet 사용
```powershell
# Publish to PowerShell Gallery
Publish-Module -Path ".\MyModule" -NuGetApiKey "your-api-key" -Repository PSGallery

# Install from PowerShell Gallery
Install-Module -Name MyModule

# Update module
Update-Module -Name MyModule
```
## 테스트

### 페스터 테스트
```powershell
# Tests/Unit/Get-Item.Tests.ps1
Describe "Get-Item" {
    BeforeAll {
        Import-Module "$PSScriptRoot\..\..\MyModule.psd1"
    }
    
    It "Should import successfully" {
        $module = Get-Module MyModule
        $module | Should -Not -BeNullOrEmpty
    }
    
    It "Should export functions" {
        $functions = Get-Command -Module MyModule
        $functions.Count | Should -BeGreaterThan 0
    }
    
    It "Should retrieve item by name" {
        $result = Get-Item -Name "Test"
        $result.Name | Should -Be "Test"
    }
    
    It "Should throw error for invalid name" {
        { Get-Item -Name "" } | Should -Throw
    }
}
```
## 문서

### 주제 정보
```text
# en-US/about_MyModule.help.txt
TOPIC
    about_MyModule

SHORT DESCRIPTION
    A brief description of the MyModule module

LONG DESCRIPTION
    Detailed description of what the module does

EXAMPLES
    Example 1: Basic usage
    PS C:\> Get-Item -Name "Test"

NOTES
    Additional notes and references
```
## 모범 사례 요약

1. **구조**: 표준 모듈 레이아웃을 따릅니다.
2. **매니페스트**: 의미론적 버전 관리를 사용하고 필요한 멤버만 내보내기
3. **함수**: 주석 기반 도움말 포함, 매개변수 확인 사용
4. **테스팅**: 포괄적인 Pester 테스트 작성
5. **문서**: README, 주제 및 예제에 대한 내용을 포함합니다.
6. **버전 제어**: 소스 제어를 위해 Git 사용
7. **CI/CD**: 자동화된 테스트 및 배포 구현
8. **종속성**: 종속성을 올바르게 지정하고 관리합니다.
9. **오류 처리**: 강력한 오류 처리 구현
10. **성능**: 성능 및 리소스 사용량 최적화

## 리소스

- [PowerShell 모듈 개발](https://docs.microsoft.com/en-us/powershell/scripting/developer/module/how-to-write-a-powershell-module)
- [Pester 테스트 프레임워크](https://pester.dev/)
- [PowerShellGet](https://docs.microsoft.com/en-us/powershell/module/powershellget/)
- [PSScriptAnalyzer](https://github.com/PowerShell/PSScriptAnalyzer)