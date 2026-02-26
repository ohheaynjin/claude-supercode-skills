# AD 보안 검토자 - 빠른 시작 가이드

이 가이드는 AD 보안 검토자 기술의 스크립트 및 도구를 시작하는 데 도움이 됩니다.

## 전제 조건

- Active Directory가 포함된 Windows Server 2016 이상
- RSAT(원격 서버 관리 도구) 설치
- 포괄적인 감사를 위한 도메인 관리자 권한
- 파워셸 5.1 이상
- TypeScript 스크립트의 경우: Node.js 16+, Azure AD 앱 등록

## 필수 모듈 설치
```powershell
# Install RSAT features (PowerShell)
Install-WindowsFeature RSAT-AD-PowerShell -IncludeManagementTools

# Import modules
Import-Module ActiveDirectory
```
## Azure AD 앱 등록(TypeScript 스크립트용)

1. **앱 등록 생성:**
```bash
   # Azure Portal → App registrations → New registration
   # Name: AD Security Reviewer
   # Permissions: Directory.Read.All, AuditLog.Read.All
   ```
2. **클라이언트 비밀번호 생성:**
```bash
   # Certificates & secrets → New client secret
   ```
## 빠른 예

### PowerShell: 권한 있는 그룹 감사
```powershell
# Audit all privileged groups in the domain
.\audit_privileged_groups.ps1 -Domain "example.com" -Threshold 5

# Audit with custom inactive days threshold
.\audit_privileged_groups.ps1 -Domain "example.com" -InactiveDays 60

# Generate report to specific location
.\audit_privileged_groups.ps1 -ReportPath "C:\Reports\privileged_audit.html"
```
### PowerShell: 위임 검토
```powershell
# Review delegation across entire domain
.\review_delegation.ps1 -SearchBase "DC=example,DC=com"

# Review specific OU only
.\review_delegation.ps1 -SearchBase "OU=Users,DC=example,DC=com"

# Set custom report path
.\review_delegation.ps1 -ReportPath "C:\Reports\delegation_review.html"
```
### TypeScript: 보안 평가 실행
```typescript
import { ADSecurityAnalyzer } from './scripts/analyze_ad_security';

const analyzer = new ADSecurityAnalyzer(
  'client-id',
  'client-secret',
  'tenant-id'
);

// Perform comprehensive security assessment
const assessment = await analyzer.performSecurityAssessment();

// Generate report
const report = generateSecurityReport(assessment);
console.log(report);

// Save report to file
const fs = require('fs');
fs.writeFileSync('security_report.md', report);
```
## 일반적인 패턴

### 자동화된 보안 평가
```powershell
# Run all security audits daily
$today = Get-Date -Format "yyyy-MM-dd"
$reportPath = "C:\Reports\$today-security-audit.html"

# Run privileged group audit
.\audit_privileged_groups.ps1 -ReportPath "$reportPath-groupts.html"

# Run delegation review
.\review_delegation.ps1 -ReportPath "$reportPath-delegation.html"

# Run TypeScript assessment
node assess_security.js
```
### 월별 보안 검토
```typescript
import { ADSecurityAnalyzer, generateSecurityReport } from './scripts/analyze_ad_security';
import * as fs from 'fs';

async function monthlySecurityReview() {
  const analyzer = new ADSecurityAnalyzer(
    process.env.AZURE_CLIENT_ID,
    process.env.AZURE_CLIENT_SECRET,
    process.env.AZURE_TENANT_ID
  );

  // Perform assessment
  const assessment = await analyzer.performSecurityAssessment();

  // Generate report
  const report = generateSecurityReport(assessment);

  // Save with timestamp
  const timestamp = new Date().toISOString().split('T')[0];
  const reportPath = `security_report_${timestamp}.md`;
  fs.writeFileSync(reportPath, report);

  console.log(`Report saved to: ${reportPath}`);

  // Alert if critical findings
  if (assessment.summary.critical > 0) {
    console.error(`ALERT: ${assessment.summary.critical} critical findings detected!`);
    // Send alert notification...
  }
}

monthlySecurityReview().catch(console.error);
```
### 표적 위임 감사
```powershell
# Find all delegation from specific user
$targetUser = "jdoe"
$reportPath = "C:\Reports\delegation_${targetUser}.html"

.\review_delegation.ps1 -SearchBase "DC=example,DC=com" | Out-String |
    Select-String -Pattern $targetUser -Context 0, 2 |
    Out-File $reportPath
```
## 보안 평가 구성요소

TypeScript 보안 분석기는 다음 검사를 수행합니다.

1. **특권 그룹 멤버십**
   - 기업 관리자
   - 도메인 관리자
   - 스키마 관리자
   - 관리자
   - 계정 운영자
   - 백업 운영자

2. **부실 계정 감지**
   - 90일 이상 비활성화된 계정
   - 최근 로그인 활동이 없는 사용자

3. **비밀번호 정책 검토**
   - 잠금 임계값 검증
   - 잠금 기간 확인
   - 비밀번호 복잡성 요구 사항

4. **MFA 등록 확인**
   - MFA를 활성화한 사용자 비율
   - MFA 권한이 없는 계정 식별

5. **의심스러운 로그인 분석**
   - 고위험 로그인 시도
   - 특이한 지리적 위치
   - 비정형적인 기기 사용

6. **조건부 액세스 정책**
   - 정책 유무 확인
   - 관리자를 위한 MFA 요구 사항
   - 지리적 제한

7. **위험한 사용자 감지**
   - 중간 및 고위험 사용자
   - 손상된 계정 표시

## 모범 사례

1. **정기 감사 실행** - 주간 또는 월간 보안 평가
2. **결과를 즉시 검토** - 중요한 문제를 즉시 해결합니다.
3. **문서 수정** - 수정 사항 및 그 효과를 추적합니다.
4. **기준 구현** - 보안 기준을 설정하고 편차를 모니터링합니다.
5. **최소 권한 사용** - 권한 있는 액세스를 정기적으로 검토하고 줄입니다.
6. **변경 사항 모니터링** - 권한 있는 그룹 수정에 대한 알림 설정
7. **사용자 교육** - 보안 모범 사례에 대해 직원 교육
8. **테스트 복구** - 수정 절차가 올바르게 작동하는지 확인합니다.

## 문제 해결

### 모듈 가져오기 오류
```
Error: Active Directory module not available
```
**해결책:**
```powershell
Install-WindowsFeature RSAT-AD-PowerShell -IncludeManagementTools
Import-Module ActiveDirectory
```
### 권한 거부 오류
```
Error: Access is denied
```
**해결책:**
1. 관리자 권한으로 PowerShell을 실행하세요.
2. 도메인 관리자 자격 증명 사용
3. 계정에 필요한 위임 권한이 있는지 확인하세요.

### 그래프 API 인증 실패
```
Error: Access token request failed
```
**해결책:**
1. 클라이언트 ID, 클라이언트 비밀번호, 테넌트 ID 확인
2. 앱 등록이 활성화되어 있는지 확인하세요
3. Directory.Read.All 권한이 부여되었는지 확인하세요.
4. 관리자 동의가 부여되었는지 확인

### 대규모 데이터 세트 시간 초과
```
Error: Operation timed out
```
**해결책:**
1. 더 작은 배치로 처리
2. 스크립트 시간 초과 값을 늘립니다.
3. 전체 도메인 대신 특정 OU를 사용하세요
4. 사용량이 적은 시간에 실행

## 결과 해석

### 심각한 심각도

즉각적인 보안 위험을 초래하는 결과:
- 불필요한 도메인 관리자 멤버십
- 권한이 있는 비활성화된 계정
- 일반모든 위임 권한
- 알 수 없는 위치에서 로그인하는 위험도가 높음

**조치 필요:** 즉각적인 해결

### 높은 심각도

중요한 보안 문제:
- 과도한 권한을 가진 그룹 구성원
- 권한이 있는 상태에서 90일 이상 비활성화된 계정
- 관리자에 대해 MFA가 활성화되지 않았습니다.
- 취약한 비밀번호 정책

**조치 필요:** 24~48시간 이내에 해결

### 중간 심각도

해결해야 할 보안 문제:
- 위임이 있는 비특권 계정
- 비밀번호가 365일 이상 변경되지 않음
- 보통 위험 사용자
- 불완전한 조건부 액세스 적용 범위

**조치 필요:** 1~2주 이내에 해결

### 낮은 심각도

사소한 보안 문제:
- 문서 공백
- 명명 규칙 위반
- 사소한 정책 불일치

**조치 필요:** 다음 유지 관리 기간 중 주소

## 모니터링과의 통합

### 중요한 결과에 대한 이메일 알림
```typescript
import { sendEmail } from './email_utils';

async function alertOnCriticalFindings(assessment: SecurityAssessmentResult) {
  const criticalFindings = assessment.findings.filter(f => f.severity === 'Critical');

  if (criticalFindings.length > 0) {
    const subject = `CRITICAL: ${criticalFindings.length} security findings detected`;
    const body = generateSecurityReport(assessment);

    await sendEmail('security-team@example.com', subject, body);
  }
}
```
### SIEM 통합
```powershell
# Send audit events to SIEM
$events = Get-Content ".\audit_log.log" | ConvertFrom-Csv

foreach ($event in $events) {
    if ($event.Level -eq 'ERROR' -or $event.Level -eq 'CRITICAL') {
        # Send to SIEM (example for Sentinel)
        Invoke-RestMethod -Uri "https://siem.example.com/api/events" `
            -Method Post `
            -Body ($event | ConvertTo-Json) `
            -ContentType "application/json"
    }
}
```
## 추가 리소스

- [Active Directory 보안 모범 사례](https://docs.microsoft.com/windows-server/identity/ad-ds/plan/security-best-practices)
- [Microsoft Graph 보안 API](https://docs.microsoft.com/graph/api/resources/security-overview)
- [Azure ID 보호](https://docs.microsoft.com/azure/active-directory/identity-protection/overview)
- [권한 있는 ID 관리](https://docs.microsoft.com/azure/active-directory/privileged-identity-management/)
- [조건부 액세스 정책](https://docs.microsoft.com/azure/active-directory/conditional-access/)