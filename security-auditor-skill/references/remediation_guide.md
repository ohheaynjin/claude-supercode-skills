# 보안 개선 가이드

## 개요
일반적인 보안 취약점을 해결하고 보안 모범 사례를 구현하기 위한 종합 가이드입니다.

## 문제 해결 우선순위 지정

### 심각도 기반 우선순위 지정
1. **중요** - 즉각적인 해결(24시간 이내)
2. **높음** - 긴급 수정(1주 이내)
3. **중간** - 계획된 수정(1개월 이내)
4. **낮음** - 백로그 수정(3개월 이내)

### 위험 기반 접근 방식
다음을 고려하십시오:
- Exploitability (악용의 용이성)
- 영향(사업상의 피해)
- 자산 가치(영향을 받는 시스템의 중요성)
- 노출(공개 vs. 내부)

## 일반적인 취약점 해결

### SQL 주입

**발각:**```sql
-- Vulnerable pattern (detected by scanners)
SELECT * FROM users WHERE id = $user_input
```

**해결:**```python
# Using parameterized queries with SQLAlchemy
from sqlalchemy import text

def get_user(user_id):
    # Safe - parameterized query
    query = text("SELECT * FROM users WHERE id = :id")
    result = db.session.execute(query, {"id": user_id})
    return result.fetchone()

# Using psycopg2 with proper binding
import psycopg2

def get_user(user_id):
    conn = psycopg2.connect(...)
    cursor = conn.cursor()
    
    # Safe - parameterized query
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    return cursor.fetchone()

# Using ORM
from models import User

def get_user(user_id):
    # Safe - ORM handles escaping
    return User.query.filter_by(id=user_id).first()
```

**확인:**```bash
# Use SQLMap to test remediation
sqlmap -u "http://example.com/user?id=1" --level=5 --risk=3
```

### 교차 사이트 스크립팅(XSS)

**발각:**```html
<!-- Vulnerable pattern -->
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
```

**해결:**```python
# Input validation with bleach
import bleach

def sanitize_user_input(content):
    # Strip all HTML tags
    return bleach.clean(content, tags=[], strip=True)

# Whitelist approach with allowed tags
def sanitize_rich_text(content):
    allowed_tags = ['b', 'i', 'u', 'em', 'strong', 'a']
    allowed_attrs = {'a': ['href', 'title']}
    return bleach.clean(
        content,
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True
    )

# Template escaping (automatically done in modern frameworks)
# Jinja2 example
from jinja2 import Environment, select_autoescape

env = Environment(
    autoescape=select_autoescape(['html', 'xml'])
)

# Output context-aware encoding
@app.route('/comment')
def show_comment(comment_text):
    return render_template('comment.html', comment=comment_text)
```

**HTTP 헤더:**```python
# Content Security Policy
@app.after_request
def add_csp_header(response):
    csp = "default-src 'self'; script-src 'self' https://trusted.cdn.com;"
    response.headers['Content-Security-Policy'] = csp
    return response
```

### 인증 우회

**발각:**```python
# Vulnerable pattern
if password == stored_password:  # Weak comparison
```

**해결:**```python
# Secure password hashing
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed.encode('utf-8')
    )

# Secure login with rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and verify_password(password, user.password_hash):
        login_user(user)
        return redirect(url_for('dashboard'))
    
    # Use constant-time comparison to prevent timing attacks
    return 'Invalid credentials', 401
```

### 안전하지 않은 IDOR(직접 개체 참조)

**발각:**```python
# Vulnerable pattern
@app.route('/documents/<doc_id>')
def get_document(doc_id):
    doc = Document.query.get(doc_id)
    return doc.content  # No authorization check
```

**해결:**```python
# Add authorization checks
@app.route('/documents/<doc_id>')
@login_required
def get_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    
    # Authorization check
    if doc.owner_id != current_user.id:
        if not current_user.has_permission('read_all_documents'):
            abort(403)
    
    return doc.content

# Alternative: use UUID instead of sequential IDs
import uuid

# Document model
class Document(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Generate secure URLs
document_url = url_for('get_document', document_id=document.id)
```

### 하드코딩된 자격 증명

**발각:**```python
# Vulnerable pattern
API_KEY = "sk_live_1234567890abcdef"
DB_PASSWORD = "admin123"
```

**해결:**```python
# Use environment variables
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Use secret management for production
# AWS Secrets Manager example
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# HashiCorp Vault example
import hvac

client = hvac.Client(url='https://vault.example.com')
client.auth.approle.login(
    role_id=os.getenv('VAULT_ROLE_ID'),
    secret_id=os.getenv('VAULT_SECRET_ID')
)

secret = client.read_secret(path='secret/database')['data']['password']
```

### 안전하지 않은 역직렬화

**발각:**```python
# Vulnerable pattern
import pickle

def load_data(data):
    return pickle.loads(data)  # Dangerous!
```

**해결:**```python
# Use JSON instead of pickle
import json

def load_data(data):
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        raise ValueError("Invalid data format")

# If pickle must be used, sign the data
import hmac
import hashlib
import pickle

def secure_serialize(data, secret_key):
    pickled = pickle.dumps(data)
    signature = hmac.new(secret_key.encode(), pickled, hashlib.sha256).digest()
    return signature + pickled

def secure_deserialize(data, secret_key):
    signature = data[:32]
    pickled = data[32:]
    
    expected_sig = hmac.new(secret_key.encode(), pickled, hashlib.sha256).digest()
    
    if not hmac.compare_digest(signature, expected_sig):
        raise ValueError("Invalid signature")
    
    return pickle.loads(pickled)
```

## 구성 강화

### 웹 서버 보안

**엔진엑스:**```nginx
# Disable server tokens
server_tokens off;

# Security headers
add_header X-Frame-Options "DENY";
add_header X-Content-Type-Options "nosniff";
add_header X-XSS-Protection "1; mode=block";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
add_header Content-Security-Policy "default-src 'self'";

# SSL configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
ssl_prefer_server_ciphers off;
```

**아파치:**```apache
# Disable server signature
ServerSignature Off
ServerTokens Prod

# Security headers
Header always set X-Frame-Options "DENY"
Header always set X-Content-Type-Options "nosniff"
Header always set X-XSS-Protection "1; mode=block"
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"

# SSL configuration
SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
SSLCipherSuite HIGH:!aNULL:!MD5
```

### 데이터베이스 보안

**포스트그레SQL:**```sql
-- Remove default test database
DROP DATABASE IF EXISTS test;

-- Create users with least privilege
CREATE USER app_user WITH PASSWORD 'strong_password';
GRANT CONNECT ON DATABASE mydb TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;

-- Enable SSL
ALTER SYSTEM SET ssl = on;
```

**MySQL/MariaDB:**```sql
-- Remove anonymous users
DELETE FROM mysql.user WHERE User='';

-- Remove test database
DROP DATABASE IF EXISTS test;

-- Set password policy
SET GLOBAL validate_password.policy = STRONG;
SET GLOBAL validate_password.length = 12;

-- Enable SSL
ALTER USER 'root'@'localhost' REQUIRE SSL;
```

### 시스템 강화

**우분투/데비안:**```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install and configure firewall
sudo apt install ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw enable

# Disable root login via SSH
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart sshd

# Configure fail2ban
sudo apt install fail2ban
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
```

**RHEL/센트OS:**```bash
# Update system
sudo yum update -y

# Configure firewalld
sudo systemctl start firewalld
sudo systemctl enable firewalld
sudo firewall-cmd --add-service=ssh --permanent
sudo firewall-cmd --reload

# Harden SSH
sudo sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart sshd
```

## 종속성 관리

### 파이썬```bash
# Audit dependencies
pip-audit

# Update dependencies
pip install --upgrade package-name

# Use pip-tools for dependency pinning
pip install pip-tools
pip-compile requirements.in
```

### Node.js```bash
# Audit dependencies
npm audit

# Fix vulnerabilities
npm audit fix

# Update packages
npm update package-name

# Use npm-check-updates
npx npm-check-updates -u
npm install
```

## 컨테이너 보안

### 도커```dockerfile
# Use minimal base image
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Don't run as root
# Don't include secrets in image
# Use multi-stage builds

# Scan image
# docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
#   aquasec/trivy:latest image myapp:latest
```

### 쿠버네티스```yaml
# Security context
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
  containers:
  - name: app
    image: myapp:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
```

## 모니터링 및 로깅

### 보안 이벤트 로깅```python
import structlog

logger = structlog.get_logger()

# Log authentication events
def log_auth_attempt(username, success, ip_address):
    logger.info(
        "auth_attempt",
        username=username,
        success=success,
        ip_address=ip_address,
        timestamp=datetime.utcnow().isoformat()
    )

# Log sensitive operations
def log_data_access(user_id, resource_type, resource_id):
    logger.warning(
        "data_access",
        user_id=user_id,
        resource_type=resource_type,
        resource_id=resource_id,
        timestamp=datetime.utcnow().isoformat()
    )
```

### 침입 탐지```bash
# Install OSSEC
sudo apt install ossec-hids-server

# Configure monitoring
# Monitor critical files
<syscheck>
  <directories check_all="yes">/etc,/usr/bin,/usr/sbin</directories>
</syscheck>

# Configure active response
<active-response>
  <command>host-deny</command>
  <location>local</location>
</active-response>
```

## 테스트 및 검증

### 자동화된 보안 테스트```yaml
# GitHub Actions workflow
name: Security Scan
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Run Bandit
        run: |
          pip install bandit
          bandit -r ./src
      
      - name: Run Safety
        run: |
          pip install safety
          safety check --json
      
      - name: Run Trivy
        run: |
          docker run --rm -v $PWD:/app aquasec/trivy config /app
```

### 침투 테스트```bash
# OWASP ZAP automated scan
zap-cli quick-scan --self-contained --start-options '-config api.disablekey=true' http://localhost:8080

# Nmap vulnerability scan
nmap --script vuln -p- target.example.com

# Nikto web scanner
nikto -h http://target.example.com -C all
```

## 해결 작업 흐름

1. **식별** - 스캔을 통해 취약점을 감지합니다.
2. **우선순위** - 위험 및 비즈니스 영향 평가
3. **수정** - 우선순위에 따라 수정 사항을 적용합니다.
4. **검증** - 수정이 효과적인지 테스트합니다.
5. **문서** - 변경 사항 및 증거 기록
6. **모니터** - 회귀 및 새로운 문제를 관찰합니다.

## 교정 후 검증

### 확인 체크리스트
- [ ] 취약점 스캐너에 더 이상 결과가 표시되지 않습니다.
- [ ] 수동 테스트를 통해 수정 사항이 효과적인지 확인
- [ ] 애플리케이션이 여전히 올바르게 작동함
- [ ] 성능 저하 없음
- [ ] 보안 테스트 통과
- [ ] 문서가 업데이트되었습니다.
- [ ] 팀에 변경 사항이 통보되었습니다.

## 자원

- [OWASP 요약본 시리즈](https://cheatsheetseries.owasp.org/)
- [CWE 상위 25위](https://cwe.mitre.org/top25/)
- [NIST 사이버 보안 프레임워크](https://www.nist.gov/cyberframework)
- [산스열람실](https://www.sans.org/reading-room/)