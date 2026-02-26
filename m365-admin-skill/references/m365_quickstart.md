# Microsoft 365 관리자 - 빠른 시작 가이드

이 가이드는 M365 관리 기술의 스크립트 및 도구를 시작하는 데 도움이 됩니다.

## 전제 조건

- Node.js 16+ 설치
- 전역 관리자 액세스 권한이 있는 Microsoft 365 테넌트
- 필요한 권한으로 Azure AD에 등록된 앱
- TypeScript가 전역적으로 설치됨

## Azure AD 앱 등록

1. **앱 등록 생성:**
```bash
   # Go to Azure Portal → App registrations → New registration
   # Name: M365 Admin Script
   # Supported account types: Accounts in this organizational directory only
   ```
2. **API 권한 추가:**
   - 마이크로소프트 그래프 → User.ReadWrite.All
   - 마이크로소프트 그래프 → Group.ReadWrite.All
   - 마이크로소프트 그래프 → Team.Create
   - Microsoft Graph → TeamSettings.ReadWrite.All

3. **클라이언트 비밀번호 생성:**
```bash
   # Go to Certificates & secrets → New client secret
   # Copy the secret value (you won't see it again)
   ```
4. **관리자 동의 부여:**
```bash
   # Go to API permissions → Click Grant admin consent for your organization
   ```
## 설치
```bash
npm install @azure/identity @microsoft/microsoft-graph-client @azure/msal-node isomorphic-fetch
npm install -D typescript @types/node
```
## 인증

스크립트는 Azure AD 앱 인증을 사용합니다.
```typescript
const userManager = new M365UserManager(
  'client-id',
  'client-secret',
  'tenant-id'
);
```
또는 환경 변수를 사용하십시오.
```bash
export AZURE_CLIENT_ID='your-client-id'
export AZURE_CLIENT_SECRET='your-client-secret'
export AZURE_TENANT_ID='your-tenant-id'
```
## 빠른 예

### 사용자 관리
```typescript
import { M365UserManager } from './scripts/create_m365_users';

const userManager = new M365UserManager(
  'client-id',
  'client-secret',
  'tenant-id'
);

// Create a new user
const userResult = await userManager.createUser({
  displayName: 'John Doe',
  mailNickname: 'jdoe',
  userPrincipalName: 'jdoe@yourdomain.com',
  password: 'SecurePassword123!',
  accountEnabled: true,
  usageLocation: 'US',
  licenses: ['LICENSE-ID-HERE']
});

if (userResult.success) {
  console.log(`User created with ID: ${userResult.userId}`);
}

// List users
const users = await userManager.listUsers();
console.log(users.map(u => u.displayName));

// Block a user
await userManager.blockUser('user-id');

// Reset password
await userManager.resetPassword('user-id', 'NewPassword123!');
```
### 팀 구성
```typescript
import { TeamsManager } from './scripts/configure_teams';

const teamsManager = new TeamsManager(
  'client-id',
  'client-secret',
  'tenant-id'
);

// Create a new team
const teamResult = await teamsManager.createTeam({
  displayName: 'Project Alpha Team',
  description: 'Team for Project Alpha development'
});

if (teamResult.success) {
  console.log(`Team created with ID: ${teamResult.teamId}`);

  // Create channels
  const channelId = await teamsManager.createChannel(teamResult.teamId!, {
    displayName: 'General',
    description: 'General discussions',
    isFavoriteByDefault: true
  });

  // Add members
  await teamsManager.addMember(teamResult.teamId!, {
    userId: 'user-id',
    role: 'Owner'
  });
}

// List all teams
const teams = await teamsManager.listTeams();
console.log(teams.map(t => t.displayName));

// Create group chat
const chatId = await teamsManager.createGroupChat(['user1-id', 'user2-id', 'user3-id']);
```
### Exchange Online 관리
```typescript
import { ExchangeManager } from './scripts/setup_exchange';

const exchangeManager = new ExchangeManager(
  'client-id',
  'client-secret',
  'tenant-id'
);

// Create mailbox for user
const mailboxResult = await exchangeManager.createMailbox('user-id');

// Configure auto-reply
await exchangeManager.configureAutoReply(
  'user-id',
  'Internal: I am out of office',
  'External: I am out of office',
  '2024-01-01T00:00:00Z',
  '2024-01-15T00:00:00Z'
);

// Create distribution group
await exchangeManager.createDistributionGroup({
  displayName: 'All Employees',
  mailNickname: 'all-employees',
  description: 'Distribution list for all employees',
  members: ['user-id-1', 'user-id-2']
});

// Get inbox messages
const messages = await exchangeManager.getInboxMessages('user-id', 20);
console.log(messages);

// Send email
await exchangeManager.sendMessage(
  'user-id',
  ['recipient@example.com'],
  'Subject',
  '<p>Email body in HTML</p>'
);

// Create calendar event
const eventId = await exchangeManager.createCalendarEvent('user-id', {
  subject: 'Team Meeting',
  body: 'Weekly team sync',
  start: '2024-01-15T10:00:00Z',
  end: '2024-01-15T11:00:00Z',
  attendees: ['attendee1@example.com', 'attendee2@example.com'],
  location: 'Conference Room A',
  isOnlineMeeting: true
});
```
## 일반적인 패턴

### 대량 사용자 생성
```typescript
const users = [
  {
    displayName: 'User One',
    mailNickname: 'userone',
    userPrincipalName: 'user1@domain.com',
    password: 'Password123!',
    accountEnabled: true,
    usageLocation: 'US'
  },
  {
    displayName: 'User Two',
    mailNickname: 'usertwo',
    userPrincipalName: 'user2@domain.com',
    password: 'Password123!',
    accountEnabled: true,
    usageLocation: 'US'
  }
];

const { successes, failures } = await bulkCreateUsers(userManager, users);
console.log(`Created: ${successes.length}, Failed: ${failures.length}`);
```
### 팀 온보딩 워크플로
```typescript
async function onboardNewTeam(teamName: string, ownerIds: string[], memberIds: string[]) {
  // Create team
  const team = await teamsManager.createTeam({ displayName: teamName });

  if (team.success && team.teamId) {
    // Create standard channels
    await teamsManager.createChannel(team.teamId, {
      displayName: 'General',
      description: 'General discussions'
    });

    await teamsManager.createChannel(team.teamId, {
      displayName: 'Announcements',
      description: 'Important announcements'
    });

    await teamsManager.createChannel(team.teamId, {
      displayName: 'Documents',
      description: 'Shared documents'
    });

    // Add owner
    for (const ownerId of ownerIds) {
      await teamsManager.addMember(team.teamId, {
        userId: ownerId,
        role: 'Owner'
      });
    }

    // Add members
    for (const memberId of memberIds) {
      await teamsManager.addMember(team.teamId, {
        userId: memberId,
        role: 'Member'
      });
    }
  }
}
```
### 사용자 오프보딩 워크플로
```typescript
async function offboardUser(userId: string) {
  // Block user account
  await userManager.blockUser(userId);

  // Reset password
  await userManager.resetPassword(userId, generateRandomPassword());

  // Remove from all Teams (would require listing teams)
  const teams = await teamsManager.listTeams();

  for (const team of teams) {
    const members = await teamsManager.listMembers(team.id);

    for (const member of members) {
      if (member.id === userId) {
        await teamsManager.removeMember(team.id, member.id);
      }
    }
  }

  // Remove from distribution groups (would require listing groups)
  const groups = await exchangeManager.getDistributionGroups();

  for (const group of groups) {
    await exchangeManager.removeMemberFromDistributionGroup(group.id, userId);
  }
}
```
## 모범 사례

1. **입력 유효성 검사** - 내장된 유효성 검사 기능 사용
2. **오류를 적절하게 처리** - 진행하기 전에 result.success를 확인하세요.
3. **최소 권한 사용** - 앱에 꼭 필요한 권한만 부여
4. **모든 작업 기록** - 감사 목적으로 사용자 관리 추적
5. **비프로덕션에서 테스트** - 먼저 테스트 테넌트에서 스크립트를 테스트합니다.
6. **재시도 로직 구현** - 일시적인 오류에 대한 재시도 추가
7. **환경 변수 사용** - 자격 증명을 안전하게 저장
8. **API 제한 모니터링** - 그래프 API 조절 제한에 유의하세요.

## 문제 해결

### 인증 실패
```
Error: Access token request failed
```
**해결책:**
1. 클라이언트 ID, 클라이언트 비밀번호, 테넌트 ID가 올바른지 확인하세요.
2. 앱 등록이 아직 활성화되어 있는지 확인하세요.
3. 관리자 동의가 부여되었는지 확인하세요.
4. API 권한이 올바른지 확인

### 사용자가 이미 존재합니다.
```
Error: Request returned status code 400 with message: Another object with the same value for property userPrincipalName already exists
```
**해결책:**
1. 다음을 사용하여 사용자가 이미 존재하는지 확인하십시오.`getUserByEmail()`2. 사용`updateUser()`새로운 사용자를 생성하는 대신
3. 또는 기존 사용자를 먼저 삭제하세요.

### 권한이 거부되었습니다
```
Error: Access is denied. Check credentials and try again.
```
**해결책:**
1. 앱에 필요한 권한이 있는지 확인
2. 권한에 대한 관리자 동의 부여
3. 올바른 앱 등록을 사용하고 있는지 확인하세요.

### 팀 생성 실패
```
Error: Failed to create team
```
**해결책:**
1. 팀 이름이 아직 존재하지 않는지 확인하세요.
2. 그래프 API 권한이 올바른지 확인하세요.
3. Microsoft Teams 라이선스가 사용자에게 할당되었는지 확인하세요.

### 라이선스 할당 실패
```
Error: Insufficient licenses available
```
**해결책:**
1. Microsoft 365 관리 센터에서 사용 가능한 라이선스 확인
2. 라이선스 SKU ID가 올바른지 확인하세요.
3. 필요한 경우 추가 라이선스를 구매하세요.

## API 제한

Microsoft Graph API에는 제한 한도가 있습니다.

- **분당 요청**: 앱당 최대 100개 요청
- **10초당 요청**: 앱당 최대 15개 요청
- **동시 요청**: 최대 10개 요청

대량 작업의 경우 일괄 처리 및 재시도 논리를 구현합니다.
```typescript
async function bulkOperationWithRetry<T>(
  operation: () => Promise<T>,
  maxRetries = 3
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await operation();
    } catch (error: any) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 2000 * (i + 1)));
    }
  }
  throw new Error('Max retries exceeded');
}
```
## 보안 고려 사항

1. **자격 증명을 하드코딩하지 마세요** - 환경 변수 또는 Key Vault를 사용하세요.
2. **클라이언트 비밀번호를 정기적으로 교체** - 90일마다 비밀번호 업데이트
3. **인증서 기반 인증 사용** - 프로덕션용 클라이언트 비밀번호보다 더 안전합니다.
4. **감사 로그 모니터링** - Microsoft 365 감사 로그를 정기적으로 검토합니다.
5. **조건부 액세스 구현** - 관리 작업에 MFA가 필요합니다.
6. **권한 있는 ID 관리 사용** - 적시 관리자 액세스
7. **정기적으로 권한 검토** - 불필요한 앱 권한 제거

## 추가 리소스

- [Microsoft Graph API 설명서](https://docs.microsoft.com/graph/api)
- [TypeScript용 Microsoft Graph SDK](https://github.com/microsoftgraph/msgraph-sdk-typescript)
- [Microsoft 365 관리 센터](https://admin.microsoft.com/)
- [Azure AD 앱 등록](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade)
- [그래프 API 제한](https://docs.microsoft.com/graph/throttling)