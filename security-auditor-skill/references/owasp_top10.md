# OWASP 상위 10대 보안 위험

## 개요
OWASP Top 10은 가장 중요한 웹 애플리케이션 보안 위험을 나타냅니다. 이 참조 자료는 각각에 대한 탐지 패턴과 해결 전략을 제공합니다.

## OWASP 상위 10위(2021)

### 1. 손상된 액세스 제어(A01:2021)

**설명:** 인증된 사용자에게 허용된 작업에 대한 제한이 제대로 적용되지 않습니다.

**탐지 패턴:**
- 민감한 엔드포인트에 대한 승인 확인 누락
- IDOR(안전하지 않은 직접 개체 참조)
- URL 조작을 통한 접근통제 점검 우회
- 무단 액세스를 허용하는 CORS 구성 오류

**해결:**```python
# Secure pattern - always verify authorization
from functools import wraps

def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.has_permission(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/documents/<doc_id>')
@require_permission('read_document')
def get_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    if doc.owner_id != current_user.id:
        abort(403)
    return jsonify(doc.to_dict())
```

**도구:** OWASP ZAP, Burp Suite, 수동 코드 검토

### 2. 암호화 오류(A02:2021)

**설명:** 암호화가 잘못 구현되어 민감한 데이터가 노출되는 경우가 많습니다.

**탐지 패턴:**
- 취약한 암호화 알고리즘(DES, MD5, SHA1)
- 하드코딩된 암호화 키
- TLS/SSL 누락
- 비밀번호를 일반 텍스트로 저장

**해결:**```python
# Secure encryption pattern
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

def generate_key(password: bytes, salt: bytes = None) -> bytes:
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def encrypt_data(data: str, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(encrypted_data: bytes, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()

# Password hashing with bcrypt
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
```

**도구:** OpenSSL, bcrypt, 암호화 라이브러리, SSL Labs

### 3. 주입(A03:2021)

**설명:** 사용자가 제공한 데이터는 애플리케이션에 의해 검증, 필터링 또는 삭제되지 않습니다.

**탐지 패턴:**
- SQL 인젝션
- NoSQL 주입
- OS 명령 주입
- LDAP 주입
- XPath 주입

**해결:**```python
# Secure database queries - use parameterized queries
import psycopg2
from psycopg2 import sql

def get_user_by_id(user_id: int):
    conn = psycopg2.connect("dbname=test user=postgres")
    cursor = conn.cursor()
    
    # Safe - parameterized query
    query = sql.SQL("SELECT * FROM users WHERE id = {}").format(
        sql.Literal(user_id)
    )
    cursor.execute(query)
    return cursor.fetchall()

# Using SQLAlchemy with ORM
from sqlalchemy.orm import Session
from sqlalchemy import text

def get_user_by_email(email: str, session: Session):
    # Safe - ORM handles escaping
    return session.query(User).filter(User.email == email).first()

# Using SQLAlchemy Core with bind parameters
def get_users_by_name(name: str):
    stmt = text("SELECT * FROM users WHERE name = :name")
    result = session.execute(stmt, {"name": name})
    return result.fetchall()

# Safe command execution with shlex
import shlex
import subprocess

def safe_exec_command(command_parts: list):
    # Validate and escape command parts
    safe_parts = []
    for part in command_parts:
        safe_parts.append(shlex.quote(part))
    
    return subprocess.run(' '.join(safe_parts), shell=False, check=True)
```

**도구:** SQLMap, OWASP ZAP, Burp Suite, 정적 분석 도구

### 4. 안전하지 않은 디자인(A04:2021)

**설명:** 설계 결함으로 인해 구현만으로는 해결할 수 없는 보안 취약성이 발생합니다.

**탐지 패턴:**
- 위협 모델링 누락
- 안전하지 않은 비즈니스 로직
- 속도 제한 없음
- 보안 기본값 누락
- 클라이언트측 컨트롤을 신뢰함

**해결:**```python
# Rate limiting implementation
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/login')
@limiter.limit("5 per minute")
def login():
    pass

# Input validation with Pydantic
from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=12, max_length=128)
    username: constr(min_length=3, max_length=50, regex=r'^[a-zA-Z0-9_]+$')
    
    class Config:
        extra = 'forbid'

# Secure defaults configuration
DEFAULT_SECURITY_CONFIG = {
    'password_min_length': 12,
    'session_timeout': 3600,
    'max_login_attempts': 5,
    'enable_csrf': True,
    'require_https': True
}
```

**도구:** 위협 모델링 도구, 설계 검토 체크리스트, 설계 원칙에 따른 보안

### 5. 잘못된 보안 구성(A05:2021)

**설명:** 안전하지 않은 기본 구성, 불완전한 구성, 개방형 클라우드 저장소, 잘못 구성된 HTTP 헤더.

**탐지 패턴:**
- 기본 자격 증명
- 디버그 모드 활성화
- 자세한 오류 메시지
- 보안 헤더 누락
- 불필요한 서비스 실행

**해결:**```python
# Flask security configuration
app = Flask(__name__)
app.config.update({
    'DEBUG': False,
    'TESTING': False,
    'SESSION_COOKIE_SECURE': True,
    'SESSION_COOKIE_HTTPONLY': True,
    'SESSION_COOKIE_SAMESITE': 'Lax',
    'PERMANENT_SESSION_LIFETIME': timedelta(hours=1)
})

# Security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

# Disable verbose errors in production
if not app.debug:
    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify({'error': 'Internal server error'}), 500
```

**도구:** Nmap, SSL Labs, 보안 헤더 검사기, 구성 린터

### 6. 취약하고 오래된 구성 요소(A06:2021)

**설명:** 알려진 취약점이 있는 라이브러리를 사용하거나 구성 요소를 업데이트하지 못합니다.

**탐지 패턴:**
- 오래된 의존성
- 종속성에서 알려진 CVE
- 버려진 도서관
- 프로덕션에서 알파/베타 버전 사용

**해결:**```bash
# Python - pip-audit
pip install pip-audit
pip-audit

# Node.js - npm audit
npm audit
npm audit fix

# Using Dependabot for GitHub
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"

# Poetry dependency management
poetry update
poetry show --tree
```

**도구:** OWASP 종속성 검사, Snyk, npm 감사, pip-audit, WhiteSource

### 7. 식별 및 인증 실패(A07:2021)

**설명:** 사용자 신원 확인, 인증, 세션 관리가 손상되었습니다.

**탐지 패턴:**
- 취약한 비밀번호 정책
- 크리덴셜 스터핑
- 세션 고정
- 무차별 공격
- 다단계 인증 우회

**해결:**```python
# Secure authentication with Flask-Login
from flask_login import LoginManager, UserMixin
from flask_bcrypt import Bcrypt

login_manager = LoginManager()
bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    user = User.query.filter_by(email=email).first()
    
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for('dashboard'))
    
    return 'Invalid credentials', 401

# Rate limiting for authentication
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/auth/login', methods=['POST'])
@limiter.limit("5 per 10 minutes")
def login():
    pass

# Secure session management
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
```

**도구:** OWASP ZAP, Burp Suite, MFA 솔루션, 비밀번호 정책 도구

### 8. 소프트웨어 및 데이터 무결성 오류(A08:2021)

**설명:** 무결성 위반으로부터 보호하지 않는 코드 및 인프라입니다.

**탐지 패턴:**
- 서명되지 않은 코드/패키지
- 무결성 검사 없이 자동 업데이트
- CI/CD 파이프라인 취약점
- 역직렬화 공격

**해결:**```python
# Verify package signatures
import hashlib
import json

def verify_package_integrity(package_path: str, checksums: dict) -> bool:
    with open(package_path, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    
    expected_hash = checksums.get(package_path)
    return file_hash == expected_hash

# Safe deserialization
import json

def safe_deserialize(data: str):
    # Use JSON instead of pickle for security
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON data") from e

# CI/CD security checks
# .github/workflows/security-checks.yml
name: Security Checks
on: [push, pull_request]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run security scan
        run: |
          pip install bandit
          bandit -r ./src
```

**도구:** GPG, 체크섬 확인, SLSA 프레임워크, Sigstore

### 9. 보안 로깅 및 모니터링 오류(A09:2021)

**설명:** 활성 위반에 대한 로깅, 감지, 에스컬레이션 및 대응은 효과적이지 않습니다.

**탐지 패턴:**
- 불충분한 로깅
- 침입 감지 없음
- 감사 추적 누락
- 보호되지 않은 채 저장된 로그

**해결:**```python
# Secure logging with structlog
import structlog
import logging

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Log security events
@app.before_request
def log_request():
    log_data = {
        'method': request.method,
        'path': request.path,
        'ip': request.remote_addr,
        'user_agent': request.user_agent.string
    }
    
    if current_user.is_authenticated:
        log_data['user_id'] = current_user.id
    
    logger.info("api_request", **log_data)

# Alerting on security events
def log_security_event(event_type: str, details: dict):
    log_entry = {
        'event_type': event_type,
        'timestamp': datetime.utcnow().isoformat(),
        'severity': 'high',
        **details
    }
    
    logger.warning("security_event", **log_entry)
    
    # Send alert (example with Sentry)
    # capture_message(f"Security event: {event_type}", extra=log_entry)
```

**도구:** ELK 스택, Splunk, Graylog, SIEM 솔루션, AWS CloudTrail

### 10. 서버측 요청 위조(A10:2021)

**설명:** 서버측 요청 위조는 웹 애플리케이션이 사용자가 제공한 URL을 확인하지 않고 원격 리소스를 가져올 때 발생합니다.

**탐지 패턴:**
- 임의의 URL 가져오기
- 파일 업로드 기능의 SSRF
- 메타데이터 서비스 접근
- 내부 네트워크 스캐닝

**해결:**```python
# Validate and sanitize URLs
from urllib.parse import urlparse
import ipaddress

ALLOWED_DOMAINS = ['api.example.com', 'cdn.example.com']

def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        
        if parsed.scheme not in ['http', 'https']:
            return False
        
        hostname = parsed.hostname
        if not hostname:
            return False
        
        # Block internal IP addresses
        ip = ipaddress.ip_address(hostname)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            return False
        
        # Allow only whitelisted domains
        if hostname not in ALLOWED_DOMAINS:
            return False
        
        return True
    except (ValueError, TypeError):
        return False

@app.route('/api/fetch')
def fetch_url():
    url = request.args.get('url')
    
    if not is_valid_url(url):
        return 'Invalid URL', 400
    
    # Use httpx with timeout and size limits
    import httpx
    with httpx.Client(timeout=10, max_redirects=3) as client:
        response = client.get(url, follow_redirects=True)
        return response.content

# Alternative: Use allowlist approach
ALLOWED_URLS = {
    'user_profile': 'https://api.example.com/v1/users/{id}',
    'product_info': 'https://api.example.com/v1/products/{id}'
}

def fetch_allowed_resource(resource_type: str, resource_id: str):
    template = ALLOWED_URLS.get(resource_type)
    if not template:
        raise ValueError(f"Unknown resource type: {resource_type}")
    
    url = template.format(id=resource_id)
    # Fetch URL...
```

**도구:** OWASP SSRF 테스트 가이드, Burp Suite, 사용자 정의 검증 스크립트

## 추가 OWASP 리소스

- [OWASP 테스트 가이드](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP 요약본 시리즈](https://cheatsheetseries.owasp.org/)
- [OWASP 코드 검토 가이드](https://owasp.org/www-project-code-review-guide/)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)

## 빠른 참조 체크리스트

- [ ] 모든 사용자 입력에 대한 입력 검증
- [ ] 데이터베이스 액세스를 위한 매개변수화된 쿼리
- [ ] 적절한 인증 및 세션 관리
- [ ] 모든 민감한 작업에 대한 승인 확인
- [ ] 안전한 암호화 구현
- [ ] 정보 공개 없이 오류 처리
- [ ] 보안 헤더가 구성됨
- [ ] 종속성 취약점 스캔
- [ ] 로깅 및 모니터링이 실행 중입니다.
- [ ] 정기적인 보안 테스트 및 코드 검토