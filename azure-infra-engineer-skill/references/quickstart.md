# Azure 인프라 엔지니어 - 빠른 시작 가이드

이 가이드는 Azure 인프라 엔지니어 기술의 스크립트 및 도구를 시작하는 데 도움이 됩니다.

## 전제 조건

- Node.js 16+ 설치
- Azure CLI가 설치 및 구성되었습니다(`az login`)
- 적절한 권한이 있는 Azure 구독
- TypeScript가 전역적으로 설치됨

## 설치
```bash
npm install @azure/arm-resources @azure/arm-network @azure/arm-monitor @azure/identity
npm install -D typescript @types/node
```
## 인증

스크립트는 여러 인증 방법을 지원하는 Azure DefaultAzureCredential을 사용합니다.

1. **Azure CLI**(로컬 개발에 권장):
```bash
   az login
   ```
2. **서비스 주체**(CI/CD용):
```bash
   export AZURE_CLIENT_ID=<client-id>
   export AZURE_CLIENT_SECRET=<client-secret>
   export AZURE_TENANT_ID=<tenant-id>
   ```
3. **관리 ID**(Azure 리소스용):
   - 시스템 할당 또는 사용자 할당 관리 ID를 자동으로 사용합니다.

## 빠른 예

### 가상 네트워크 배포
```typescript
import { deployVNet } from './scripts/deploy_azure_resources';

const config = {
  subscriptionId: 'your-subscription-id',
  name: 'my-vnet',
  addressSpace: ['10.0.0.0/16'],
  subnets: [
    {
      name: 'subnet-1',
      addressPrefix: '10.0.1.0/24'
    },
    {
      name: 'subnet-2',
      addressPrefix: '10.0.2.0/24'
    }
  ],
  location: 'eastus',
  resourceGroupName: 'my-resource-group'
};

const result = await deployVNet(config);
if (result.success) {
  console.log(`VNet deployed: ${result.vnetId}`);
} else {
  console.error(`Errors: ${result.errors?.join(', ')}`);
}
```
### Bicep 템플릿 배포
```typescript
import { deployBicepTemplate } from './scripts/configure_bicep_template';

const config = {
  subscriptionId: 'your-subscription-id',
  resourceGroupName: 'my-resource-group',
  deploymentName: 'app-deployment',
  templatePath: './templates/main.bicep',
  parameters: {
    location: 'eastus',
    vmSize: 'Standard_DS2_v2'
  },
  location: 'eastus'
};

const result = await deployBicepTemplate(config);
if (result.success) {
  console.log(`Deployment successful: ${result.deploymentId}`);
  console.log(`Outputs: ${JSON.stringify(result.outputs, null, 2)}`);
}
```
### 모니터링 설정
```typescript
import { createActionGroup, createMetricAlert } from './scripts/setup_monitoring';

const actionGroupConfig = {
  subscriptionId: 'your-subscription-id',
  resourceGroupName: 'my-resource-group',
  name: 'devops-alerts',
  location: 'eastus',
  emailReceivers: [
    {
      name: 'DevOps Team',
      emailAddress: 'devops@example.com'
    }
  ]
};

const actionGroupId = await createActionGroup(actionGroupConfig);

if (actionGroupId) {
  const alertConfig = {
    subscriptionId: 'your-subscription-id',
    resourceGroupName: 'my-resource-group',
    name: 'cpu-alert',
    targetResourceId: '/subscriptions/.../resourceGroups/.../providers/Microsoft.Compute/virtualMachines/my-vm',
    criteria: {
      metricName: 'Percentage CPU',
      threshold: 80,
      operator: 'GreaterThan',
      timeAggregation: 'Average',
      windowSize: 'PT5M',
      evaluationFrequency: 'PT1M'
    },
    actionGroups: [actionGroupId]
  };

  const alertCreated = await createMetricAlert(alertConfig);
  console.log(`Alert created: ${alertCreated}`);
}
```
## 일반적인 패턴

### 주소 접두사 확인 중
```typescript
import { validateAddressPrefix } from './scripts/deploy_azure_resources';

const isValid = validateAddressPrefix('10.0.1.0/24');
console.log(`Valid CIDR: ${isValid}`);
```
### 비행 전 확인
```typescript
import { validateDeployment } from './scripts/configure_bicep_template';

const isValid = await validateDeployment(config);
if (isValid) {
  console.log('Template validation passed');
} else {
  console.log('Template validation failed');
  process.exit(1);
}
```
## 모범 사례

1. **배포하기 전에 항상 검증** - 사용`validateDeployment()` before running deployments
2. **Use what-if** - Run `whatIfDeployment()` to preview changes
3. **Implement proper error handling** - Check `result.errors` for detailed error messages
4. **Use naming conventions** - Follow Azure naming conventions for resources
5. **Tag resources** - Add tags for cost tracking and resource organization
6. **Monitor deployments** - Set up alerts for critical resources
7. **Use resource groups** - Group related resources together
8. **Implement RBAC** - Grant least privilege access to resources

## Troubleshooting

### Authentication Errors

```
Error: DefaultAzureCredential: Authentication failed
```


**Solution**: Run `az login` to authenticate with Azure CLI

### Permission Errors

```
Error: AuthorizationFailed: The client has permission to perform action
```


**Solution**: Ensure your account has Contributor or Owner role on the resource group

### Template Validation Failures

```
Error: Template validation failed
```


**Solution**:
1. Check the Bicep template syntax
2. Verify all required parameters are provided
3. Use `az bicep build` to compile Bicep to JSON first
4. Review the detailed error message

### Resource Not Found Errors

```
Error: ResourceNotFound: The resource with id could not be found
```


**Solution**:
1. Verify the resource ID is correct
2. Check if the resource exists
3. Ensure you're using the correct subscription

### Network Deployment Timeouts

```
Error: Deployment operation timed out
```


**Solution**:
1. Increase timeout values in the deployment configuration
2. Check Azure service health
3. Verify network connectivity to Azure endpoints

## Additional Resources

- [Azure Documentation](https://docs.microsoft.com/azure)
- [Azure CLI Reference](https://docs.microsoft.com/cli/azure)
- [Bicep Documentation](https://docs.microsoft.com/azure/azure-resource-manager/bicep)
- [Azure SDK for TypeScript](https://github.com/Azure/azure-sdk-for-js)
- [Azure Best Practices](https://docs.microsoft.com/azure/architecture/best-practices)
