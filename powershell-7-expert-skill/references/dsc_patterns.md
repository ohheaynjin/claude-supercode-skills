# 원하는 상태 구성(DSC) 패턴

## 개요

DSC(필요한 상태 구성)는 소프트웨어 서비스에 대한 구성 데이터를 배포 및 관리하고 이러한 서비스가 실행되는 환경을 관리할 수 있는 PowerShell의 관리 플랫폼입니다.

## 기본 DSC 구성

### 간단한 구성
```powershell
# Simple Web Server Configuration
Configuration WebServerConfig {
    param(
        [Parameter(Mandatory=$true)]
        [string]$ComputerName,
        
        [Parameter(Mandatory=$true)]
        [string]$WebsitePath
    )
    
    Node $ComputerName {
        WindowsFeature WebServer {
            Ensure = 'Present'
            Name = 'Web-Server'
        }
        
        File WebsiteContent {
            Ensure = 'Present'
            Type = 'Directory'
            DestinationPath = $WebsitePath
        }
        
        File DefaultPage {
            Ensure = 'Present'
            Type = 'File'
            DestinationPath = Join-Path $WebsitePath 'index.html'
            Contents = '<h1>Hello from DSC!</h1>'
        }
    }
}

# Compile configuration
WebServerConfig -ComputerName 'web01' -WebsitePath 'C:\inetpub\wwwroot'
```
## 고급 DSC 패턴

### 복합 리소스
```powershell
# Composite DSC Resource
Configuration CompositeWebsite {
    Import-DscResource -ModuleName PSDesiredStateConfiguration
    
    Node web01 {
        # Install web platform
        WindowsFeature WebServer {
            Ensure = 'Present'
            Name = 'Web-Server'
            IncludeAllSubFeature = $true
        }
        
        # Configure IIS
        Script ConfigureIIS {
            GetScript = {
                @{
                    Result = (Get-Website 'Default Web Site' -ErrorAction SilentlyContinue) -ne $null
                }
            }
            TestScript = {
                (Get-Website 'Default Web Site' -ErrorAction SilentlyContinue) -ne $null
            }
            SetScript = {
                # Configuration logic
            }
        }
    }
}
```
### 구성 데이터
```powershell
# Configuration Data
$configData = @{
    AllNodes = @(
        @{
            NodeName = 'web01'
            Role = 'WebServer'
            WebsitePath = 'C:\inetpub\wwwroot'
        },
        @{
            NodeName = 'web02'
            Role = 'WebServer'
            WebsitePath = 'C:\inetpub\wwwroot'
        },
        @{
            NodeName = 'db01'
            Role = 'Database'
            SqlInstance = 'MSSQLSERVER'
        }
    )
}

# Configuration using data
Configuration RoleBasedConfig {
    Node $AllNodes.NodeName {
        switch ($Node.Role) {
            'WebServer' {
                WindowsFeature WebServer {
                    Ensure = 'Present'
                    Name = 'Web-Server'
                }
                
                File Website {
                    Ensure = 'Present'
                    Type = 'Directory'
                    DestinationPath = $Node.WebsitePath
                }
            }
            
            'Database' {
                WindowsFeature SQLServer {
                    Ensure = 'Present'
                    Name = 'SQL-Server'
                }
            }
        }
    }
}

RoleBasedConfig -ConfigurationData $configData
```
### 부분 구성
```powershell
# Configuration 1: IIS
Configuration IISConfig {
    Node web01 {
        WindowsFeature WebServer {
            Ensure = 'Present'
            Name = 'Web-Server'
        }
    }
}

# Configuration 2: Security
Configuration SecurityConfig {
    Node web01 {
        WindowsFeature Firewall {
            Ensure = 'Present'
            Name = 'Web-Server'
        }
    }
}

# Apply partial configurations
# Compile
IISConfig -OutputPath C:\DSC\IIS
SecurityConfig -OutputPath C:\DSC\Security

# Apply
Start-DscConfiguration -Path C:\DSC\IIS -ComputerName web01 -Wait -Verbose
Start-DscConfiguration -Path C:\DSC\Security -ComputerName web01 -Wait -Verbose
```
## DSC 리소스

### 내장 리소스
```powershell
# File resource
File ExampleFile {
    Ensure = 'Present'
    Type = 'File'
    DestinationPath = 'C:\Temp\example.txt'
    Contents = 'Example content'
    Force = $true
}

# Registry resource
Registry ExampleRegistry {
    Ensure = 'Present'
    Key = 'HKLM:\SOFTWARE\Example'
    ValueName = 'Setting'
    ValueData = 'Value'
    ValueType = 'String'
}

# Service resource
Service ExampleService {
    Name = 'wuauserv'
    StartupType = 'Automatic'
    State = 'Running'
}

# WindowsFeature resource
WindowsFeature IIS {
    Ensure = 'Present'
    Name = 'Web-Server'
    IncludeAllSubFeature = $true
}

# Script resource
Script CustomScript {
    GetScript = {
        @{
            Result = (Test-Path 'C:\Temp\checkfile.txt')
        }
    }
    TestScript = {
        Test-Path 'C:\Temp\checkfile.txt'
    }
    SetScript = {
        'Created by DSC' | Out-File 'C:\Temp\checkfile.txt'
    }
}
```
### 사용자 지정 DSC 리소스
```powershell
# Custom resource schema (schema.mof)
[ClassVersion("1.0.0"), FriendlyName("CustomFile")]
class CustomFile : OMI_BaseResource
{
    [Key, Description("Path to file")] String Path;
    [Write, Description("File content")] String Content;
    [Write, Description("Ensure")] String Ensure;
};

# Resource implementation (CustomFile.psm1)
function Get-TargetResource {
    param (
        [string]$Path
    )
    
    if (Test-Path $Path) {
        return @{
            Path = $Path
            Content = Get-Content $Path -Raw
            Ensure = 'Present'
        }
    }
    else {
        return @{
            Path = $Path
            Content = $null
            Ensure = 'Absent'
        }
    }
}

function Set-TargetResource {
    param (
        [string]$Path,
        [string]$Content,
        [string]$Ensure
    )
    
    if ($Ensure -eq 'Present') {
        $Content | Out-File $Path -Encoding UTF8
    }
    else {
        Remove-Item $Path -Force
    }
}

function Test-TargetResource {
    param (
        [string]$Path,
        [string]$Content,
        [string]$Ensure
    )
    
    if (-not (Test-Path $Path)) {
        return $Ensure -eq 'Absent'
    }
    
    $actualContent = Get-Content $Path -Raw
    return $actualContent -eq $Content
}
```
## DSC 풀 서버

### 풀 서버 설정
```powershell
# Install DSC Service
Configuration PullServer {
    param(
        [string]$NodeName = 'localhost'
    )
    
    Node $NodeName {
        WindowsFeature DSCService {
            Ensure = 'Present'
            Name = 'DSC-Service'
        }
        
        File DSCModulePath {
            Ensure = 'Present'
            Type = 'Directory'
            DestinationPath = 'C:\Program Files\WindowsPowerShell\DscService\Modules'
        }
        
        File DSCConfigurationPath {
            Ensure = 'Present'
            Type = 'Directory'
            DestinationPath = 'C:\Program Files\WindowsPowerShell\DscService\Configuration'
        }
    }
}

PullServer

# Configure LCM
[DscLocalConfigurationManager()]
Configuration SetLCM {
    Node localhost {
        Settings {
            RefreshMode = 'Pull'
            ConfigurationID = '12345678-1234-1234-1234-123456789012'
        }
        
        ConfigurationRepositoryWeb PullSrv {
            ServerURL = 'http://pullserver:8080/PSDSCPullServer.svc'
            AllowUnsecureConnection = $true
        }
    }
}

SetLCM
```
## JEA(충분한 행정)

### JEA 구성
```powershell
# Create JEA Session Configuration
$sessionConfig = @{
    Path = ".\JEAConfig.pssc"
    SessionType = "RestrictedRemoteServer"
    RunAsVirtualAccount = $true
    RoleDefinitions = @{
        "CONTOSO\\JEA_Admins" = @{
            RoleCapabilityFiles = @(".\\AdminRole.psrc")
        }
    }
    TranscriptDirectory = "C:\\Transcripts"
}

New-PSSessionConfigurationFile @sessionConfig

# Register session configuration
Register-PSSessionConfiguration -Path ".\JEAConfig.pssc" -Name "JEA" -Force
```
### 역할 능력
```powershell
# Create role capability file
$roleParams = @{
    Path = ".\\AdminRole.psrc"
    VisibleCmdlets = "Get-Service", "Restart-Service", "Get-Process"
    VisibleFunctions = "Get-SystemInfo"
    VisibleExternalCommands = "C:\\Windows\\System32\\whoami.exe"
    ModulesToImport = "ActiveDirectory"
}

New-PSRoleCapabilityFile @roleParams
```
## DSC 테스트

### 테스트 구성
```powershell
# Test configuration compliance
Test-DscConfiguration -ComputerName web01

# Get DSC configuration status
Get-DscConfigurationStatus -CimSession web01

# Test specific resource
Invoke-DscResource -Name File -Method Test -ModuleName PSDesiredStateConfiguration -Property @{
    DestinationPath = 'C:\Temp\test.txt'
    Ensure = 'Present'
}
```
## 모범 사례

1. 선언적 언어를 사용하십시오(절차가 아닌 상태를 설명).
2. 데이터와 구성 분리
3. 멱등성 리소스 사용
4. 적절한 오류 처리 구현
5. 배포 전 구성 테스트
6. DSC 구성에 버전 제어 사용
7. 사용자 지정 리소스를 철저하게 문서화하세요.
8. DSC 규정 준수를 정기적으로 모니터링합니다.

## 문제 해결

### 구성 컴파일 오류

**오류:** 잘못된 MOF 파일

**해결책:** 구성 스크립트에서 구문 및 리소스 매개변수를 확인하세요.

### LCM 문제

**오류:** LCM이 비활성화된 상태입니다.

**해결책:** LCM을 활성화하고 새로 고침 모드를 설정합니다.
```powershell
Set-DscLocalConfigurationManager -Enabled $true
```
### 리소스 오류

**오류:** 리소스 실행 실패

**해결책:** 리소스 로그를 확인하고 전제조건을 확인하세요.

## 리소스

- [DSC 설명서](https://docs.microsoft.com/en-us/powershell/dsc/overview)
- [DSC 리소스](https://docs.microsoft.com/en-us/powershell/dsc/resources/resources)
- [JEA 문서](https://docs.microsoft.com/en-us/powershell/scripting/learn/remoting/jea/overview)