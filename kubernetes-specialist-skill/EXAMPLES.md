# Kubernetes 전문가 - 코드 예제 및 패턴

## 블루-그린 배포 패턴

**사용 시기:** 즉각적인 롤백 기능을 갖춘 다운타임 없는 배포

### 블루 배포(현재 생산)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
  namespace: production
spec:
  replicas: 5
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
      - name: myapp
        image: myregistry.com/myapp:v1.0.0
        ports:
        - containerPort: 8080
```
### 서비스(파란색과 녹색 간 전환)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  namespace: production
spec:
  selector:
    app: myapp
    version: blue  # Change to 'green' to cutover
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer
```
### 배포 프로세스
```bash
# Step 1: Deploy green (new version) alongside blue
kubectl apply -f green-deployment.yaml

# Step 2: Wait for green to be ready
kubectl wait --for=condition=available --timeout=300s \
  deployment/myapp-green -n production

# Step 3: Test green deployment (internal testing)
kubectl port-forward deployment/myapp-green -n production 9000:8080
curl http://localhost:9000/health

# Step 4: Cutover traffic to green (instant switch)
kubectl patch service myapp-service -n production \
  -p '{"spec":{"selector":{"version":"green"}}}'

# Step 5: Monitor for issues (5-10 minutes)
kubectl logs -f deployment/myapp-green -n production

# If successful: Delete blue
kubectl delete deployment myapp-blue -n production

# If issues: Instant rollback
kubectl patch service myapp-service -n production \
  -p '{"spec":{"selector":{"version":"blue"}}}'
```
## 안티 패턴 1: 리소스 요청/제한 없음

### 외관(나쁨):
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
  - name: app
    image: myapp:latest
    # No resources defined - pod can consume entire node!
```
### 실패 이유:
- 용량 확인 없이 노드에 예약된 포드(다른 포드에서 OOMKilled 발생)
- QoS 클래스 없음(BestEffort - 리소스 부족 시 먼저 종료됨)
- HPA는 확장할 수 없습니다(사용률을 계산하려면 리소스 요청이 필요함).

### 올바른 접근 방식:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
  - name: app
    image: myapp:latest
    resources:
      requests:  # Minimum guaranteed resources
        cpu: "500m"     # 0.5 CPU cores
        memory: "512Mi" # 512 MB
      limits:    # Maximum allowed resources
        cpu: "1000m"    # 1 CPU core
        memory: "1Gi"   # 1 GB
    # QoS class: Guaranteed (requests == limits)
```
## 안티 패턴 2: 상태 프로브 누락

### 외관(나쁨):
```yaml
containers:
- name: app
  image: myapp:latest
  # No liveness or readiness probes!
```
### 실패 이유:
- Kubernetes는 즉시 Pod에 트래픽을 보냅니다(앱이 준비되지 않은 경우에도).
- 충돌한 포드가 자동으로 다시 시작되지 않음
- 롤링 업데이트는 새 포드가 정상 상태가 될 때까지 기다리지 않습니다.

### 올바른 접근 방식:
```yaml
containers:
- name: app
  image: myapp:latest
  ports:
  - containerPort: 8080
  
  livenessProbe:  # Restart pod if this fails
    httpGet:
      path: /health
      port: 8080
    initialDelaySeconds: 30  # Wait for app to start
    periodSeconds: 10        # Check every 10 seconds
    timeoutSeconds: 5
    failureThreshold: 3      # Restart after 3 failures
  
  readinessProbe:  # Remove from service if this fails
    httpGet:
      path: /ready
      port: 8080
    initialDelaySeconds: 10
    periodSeconds: 5
    failureThreshold: 2
```
## 네트워크 정책 예
```yaml
# Default deny all ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress

---
# Allow traffic from specific namespace
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-frontend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: frontend
    ports:
    - protocol: TCP
      port: 8080
```
## HorizonPodAutoscaler 예
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max
```
## PodDisruptionBudget 예
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
  namespace: production
spec:
  minAvailable: 2  # Or use maxUnavailable: 1
  selector:
    matchLabels:
      app: myapp
```
## 데이터베이스용 StatefulSet
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: database
spec:
  serviceName: postgres
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: gp3
      resources:
        requests:
          storage: 100Gi
```
