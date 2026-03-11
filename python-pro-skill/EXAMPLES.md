# Python Pro - 예제 및 패턴

## 안티 패턴

### 안티 패턴: 유형 힌트 무시

**모습:**```python
def process_users(users):  # No type hints
    return [u['name'] for u in users]  # Runtime error if wrong type

result = process_users("not a list")  # No warning until runtime
```

**실패하는 이유:**
- IDE 자동 완성 기능 없음
- 개발이 아닌 런타임에 오류가 발생합니다.
- 안전하게 리팩토링하기가 더 어렵습니다.

**올바른 접근 방식:**```python
from typing import List, Dict

def process_users(users: List[Dict[str, str]]) -> List[str]:
    return [u['name'] for u in users]

# mypy catches error at development time
result = process_users("not a list")  # mypy error!
```

---

### 안티 패턴: 이벤트 루프 차단

**모습:**```python
import time
import asyncio

async def slow_handler():
    time.sleep(5)  # BLOCKS the entire event loop!
    return {"status": "done"}

# All other requests wait 5 seconds
```

**실패하는 이유:**
- 비동기 이점이 완전히 무효화되었습니다.
- 모든 동시 요청 차단
- 서버가 중단된 것처럼 보입니다.

**올바른 접근 방식:**```python
import asyncio

async def slow_handler():
    await asyncio.sleep(5)  # Non-blocking
    return {"status": "done"}

# For CPU-bound work, use executor
async def cpu_intensive_handler():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,  # Use default executor
        expensive_computation
    )
    return result
```

---

### 안티 패턴: 컨텍스트 관리자를 사용하지 않음

**모습:**```python
# Manual resource management
file = open("data.txt", "r")
data = file.read()
file.close()  # Easy to forget, especially with exceptions

conn = psycopg2.connect(...)
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
# If exception here, connection leaks!
conn.close()
```

**올바른 접근 방식:**```python
# Context manager handles cleanup automatically
with open("data.txt", "r") as file:
    data = file.read()
# File automatically closed, even on exception

async with asyncpg.create_pool(DATABASE_URL) as pool:
    async with pool.acquire() as conn:
        result = await conn.fetch("SELECT * FROM users")
# Connection automatically returned to pool
```

---

### 안티 패턴: 변경 가능한 기본 인수

**모습:**```python
def append_to_list(item, items=[]):  # Shared across calls!
    items.append(item)
    return items

print(append_to_list(1))  # [1]
print(append_to_list(2))  # [1, 2] - Unexpected!
print(append_to_list(3))  # [1, 2, 3] - Bug!
```

**올바른 접근 방식:**```python
from typing import Optional, List

def append_to_list(item: int, items: Optional[List[int]] = None) -> List[int]:
    if items is None:
        items = []
    items.append(item)
    return items

print(append_to_list(1))  # [1]
print(append_to_list(2))  # [2] - Correct!
```

---

## 테스트 패턴

### 비동기 테스트를 사용한 Pytest

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_user(async_client: AsyncClient):
    response = await async_client.post(
        "/users/",
        json={"email": "test@example.com", "password": "secure123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_user_not_found(async_client: AsyncClient):
    response = await async_client.get("/users/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
```

### 외부 서비스 모의

```python
from unittest.mock import AsyncMock, patch
import pytest

@pytest.mark.asyncio
async def test_fetch_external_data():
    mock_response = {"data": "mocked"}
    
    with patch("app.services.external_api.fetch") as mock_fetch:
        mock_fetch.return_value = mock_response
        
        result = await fetch_external_data()
        
        assert result == mock_response
        mock_fetch.assert_called_once()


@pytest.mark.asyncio
async def test_database_operation():
    mock_session = AsyncMock()
    mock_session.execute.return_value.scalar_one_or_none.return_value = User(
        id=1, email="test@example.com"
    )
    
    repo = UserRepository(mock_session)
    user = await repo.get(1)
    
    assert user.email == "test@example.com"
```

---

## Pydantic 고급 패턴

### 검증이 포함된 중첩 모델

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional
from datetime import datetime

class Address(BaseModel):
    street: str
    city: str
    country: str = "USA"
    zip_code: str = Field(..., pattern=r'^\d{5}(-\d{4})?$')


class OrderItem(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, le=100)
    unit_price: float = Field(..., gt=0)
    
    @property
    def total(self) -> float:
        return self.quantity * self.unit_price


class Order(BaseModel):
    id: Optional[int] = None
    customer_email: str
    items: List[OrderItem] = Field(..., min_length=1)
    shipping_address: Address
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    @field_validator('customer_email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower()
    
    @model_validator(mode='after')
    def validate_order(self) -> 'Order':
        if self.total > 10000:
            # Business rule: large orders need approval
            pass
        return self
    
    @property
    def total(self) -> float:
        return sum(item.total for item in self.items)


# Usage
order = Order(
    customer_email="John@Example.com",
    items=[
        OrderItem(product_id=1, quantity=2, unit_price=29.99),
        OrderItem(product_id=2, quantity=1, unit_price=49.99)
    ],
    shipping_address=Address(
        street="123 Main St",
        city="New York",
        zip_code="10001"
    )
)
print(order.customer_email)  # "john@example.com" (lowercased)
print(order.total)  # 109.97
```

---

## 비동기 생성기 패턴

```python
from typing import AsyncGenerator
import asyncpg

async def stream_users(
    pool: asyncpg.Pool, 
    batch_size: int = 100
) -> AsyncGenerator[User, None]:
    """Stream users from database in batches"""
    offset = 0
    
    while True:
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM users ORDER BY id LIMIT $1 OFFSET $2",
                batch_size,
                offset
            )
        
        if not rows:
            break
        
        for row in rows:
            yield User(**dict(row))
        
        offset += batch_size


# Usage
async def process_all_users():
    async for user in stream_users(pool):
        await process_user(user)
```

---

## 의존성 주입 패턴

```python
from typing import Protocol, runtime_checkable
from functools import lru_cache

@runtime_checkable
class EmailService(Protocol):
    async def send(self, to: str, subject: str, body: str) -> bool: ...


class SMTPEmailService:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
    
    async def send(self, to: str, subject: str, body: str) -> bool:
        # Actual SMTP implementation
        return True


class MockEmailService:
    async def send(self, to: str, subject: str, body: str) -> bool:
        print(f"Mock: Would send to {to}")
        return True


# Dependency provider
@lru_cache
def get_email_service() -> EmailService:
    if settings.TESTING:
        return MockEmailService()
    return SMTPEmailService(settings.SMTP_HOST, settings.SMTP_PORT)


# FastAPI dependency injection
@app.post("/notify")
async def notify_user(
    user_id: int,
    email_service: EmailService = Depends(get_email_service)
):
    user = await get_user(user_id)
    await email_service.send(
        to=user.email,
        subject="Notification",
        body="Hello!"
    )
    return {"status": "sent"}
```

---

## 캐싱 패턴

```python
from functools import lru_cache
from typing import Optional
import asyncio
from datetime import datetime, timedelta

# Simple in-memory cache with TTL
class TTLCache:
    def __init__(self, ttl_seconds: int = 300):
        self._cache: dict = {}
        self._ttl = ttl_seconds
    
    def get(self, key: str) -> Optional[any]:
        if key in self._cache:
            value, expires_at = self._cache[key]
            if datetime.utcnow() < expires_at:
                return value
            del self._cache[key]
        return None
    
    def set(self, key: str, value: any) -> None:
        expires_at = datetime.utcnow() + timedelta(seconds=self._ttl)
        self._cache[key] = (value, expires_at)


cache = TTLCache(ttl_seconds=300)

async def get_user_cached(user_id: int) -> User:
    cache_key = f"user:{user_id}"
    
    # Try cache first
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    # Fetch from database
    user = await db.fetch_user(user_id)
    
    # Store in cache
    cache.set(cache_key, user)
    
    return user
```
