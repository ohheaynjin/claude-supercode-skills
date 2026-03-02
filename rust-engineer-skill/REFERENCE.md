# Rust 엔지니어 - 기술 참조

이 문서에는 Rust 개발을 위한 자세한 작업 흐름, 기술 사양 및 고급 패턴이 포함되어 있습니다.

## 작업 흐름: Tokio 채널로 배우 모델 구현

**목표:** 메시지 전달을 통한 상태 저장 처리를 위한 동시 행위자 시스템을 구축합니다.

### 1단계: 행위자 메시지 정의
```rust
use tokio::sync::oneshot;
use uuid::Uuid;

pub enum OrderMessage {
    Create {
        request: CreateOrderRequest,
        response: oneshot::Sender<Result<OrderResponse, OrderError>>,
    },
    Get {
        id: Uuid,
        response: oneshot::Sender<Result<OrderResponse, OrderError>>,
    },
    UpdateStatus {
        id: Uuid,
        status: String,
        response: oneshot::Sender<Result<(), OrderError>>,
    },
}
```
### 2단계: 액터 구현
```rust
use tokio::sync::mpsc;
use std::collections::HashMap;

pub struct OrderActor {
    receiver: mpsc::UnboundedReceiver<OrderMessage>,
    db: PgPool,
    cache: HashMap<Uuid, OrderResponse>,
}

impl OrderActor {
    pub fn new(receiver: mpsc::UnboundedReceiver<OrderMessage>, db: PgPool) -> Self {
        Self {
            receiver,
            db,
            cache: HashMap::new(),
        }
    }
    
    pub async fn run(mut self) {
        while let Some(message) = self.receiver.recv().await {
            self.handle_message(message).await;
        }
    }
    
    async fn handle_message(&mut self, message: OrderMessage) {
        match message {
            OrderMessage::Create { request, response } => {
                let result = service::create_order(&self.db, request).await;
                if let Ok(ref order) = result {
                    self.cache.insert(order.id, order.clone());
                }
                let _ = response.send(result);
            }
            OrderMessage::Get { id, response } => {
                let result = if let Some(cached) = self.cache.get(&id) {
                    Ok(cached.clone())
                } else {
                    service::get_order(&self.db, id).await
                };
                let _ = response.send(result);
            }
            OrderMessage::UpdateStatus { id, status, response } => {
                let result = update_order_status(&self.db, id, &status).await;
                if result.is_ok() {
                    if let Some(order) = self.cache.get_mut(&id) {
                        order.status = status;
                    }
                }
                let _ = response.send(result);
            }
        }
    }
}
```
### 3단계: 클라이언트 핸들 생성
```rust
#[derive(Clone)]
pub struct OrderClient {
    sender: mpsc::UnboundedSender<OrderMessage>,
}

impl OrderClient {
    pub fn new(sender: mpsc::UnboundedSender<OrderMessage>) -> Self {
        Self { sender }
    }
    
    pub async fn create_order(
        &self,
        request: CreateOrderRequest,
    ) -> Result<OrderResponse, OrderError> {
        let (tx, rx) = oneshot::channel();
        self.sender
            .send(OrderMessage::Create { request, response: tx })
            .map_err(|_| OrderError::InvalidData("Actor dropped".to_string()))?;
        rx.await
            .map_err(|_| OrderError::InvalidData("Response dropped".to_string()))?
    }
    
    pub async fn get_order(&self, id: Uuid) -> Result<OrderResponse, OrderError> {
        let (tx, rx) = oneshot::channel();
        self.sender
            .send(OrderMessage::Get { id, response: tx })
            .map_err(|_| OrderError::InvalidData("Actor dropped".to_string()))?;
        rx.await
            .map_err(|_| OrderError::InvalidData("Response dropped".to_string()))?
    }
}
```
### 4단계: 메인에 액터 생성
```rust
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let db = PgPool::connect(&database_url).await?;
    
    let (tx, rx) = mpsc::unbounded_channel();
    let actor = OrderActor::new(rx, db.clone());
    
    // Spawn actor task
    tokio::spawn(async move {
        actor.run().await;
    });
    
    let client = OrderClient::new(tx);
    
    // Use client in handlers
    let app = Router::new()
        .route("/orders", post(handlers::create_order))
        .with_state(client);
    
    // ...
}
```
**예상 결과:**
- 메시지 기반 API를 사용하는 스레드로부터 안전한 상태 저장 액터
- 자동 무효화를 통한 인메모리 캐싱
- HTTP 레이어에서 비즈니스 로직을 분리했습니다.
- 채널 드롭을 통한 정상적인 종료

---

## 패턴: 결과 기반 오류 처리

**사용 사례:** 다음을 사용한 명시적 오류 전파`?`깨끗한 비동기 코드를 위한 연산자입니다.
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ServiceError {
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),
    
    #[error("Not found: {resource} with id {id}")]
    NotFound { resource: String, id: String },
    
    #[error("Validation failed: {0}")]
    Validation(String),
}

pub async fn process_order(
    db: &PgPool,
    order_id: Uuid,
) -> Result<OrderResponse, ServiceError> {
    // ? operator propagates errors automatically
    let order = fetch_order(db, order_id).await?;
    let payment = process_payment(&order).await?;
    update_order_status(db, order_id, "completed").await?;
    
    Ok(OrderResponse {
        id: order.id,
        status: "completed".to_string(),
        payment_id: payment.id,
    })
}

async fn fetch_order(db: &PgPool, id: Uuid) -> Result<Order, ServiceError> {
    sqlx::query_as!(Order, "SELECT * FROM orders WHERE id = $1", id)
        .fetch_optional(db)
        .await?
        .ok_or(ServiceError::NotFound {
            resource: "Order".to_string(),
            id: id.to_string(),
        })
}
```
**맞춤 설정 포인트:**
- 컨텍스트 추가`anyhow::Context`더 풍부한 오류 메시지를 위해
- 커스텀 구현`From`타사 오류 유형에 대한 암시
- 사용`eyre`역추적이 있는 오류 보고서의 경우

---

## 패턴: 안전한 FFI 래퍼

**사용 사례:** 안전한 Rust 인터페이스로 C 라이브러리를 호출합니다.
```rust
use std::ffi::{CStr, CString};
use std::os::raw::{c_char, c_int};

// Unsafe FFI declarations
#[link(name = "z")]
extern "C" {
    fn compress(
        dest: *mut u8,
        dest_len: *mut usize,
        source: *const u8,
        source_len: usize,
    ) -> c_int;
}

// Safe wrapper
pub struct CompressionError {
    pub code: i32,
}

pub fn compress_data(data: &[u8]) -> Result<Vec<u8>, CompressionError> {
    let max_size = (data.len() as f64 * 1.1) as usize + 12; // zlib bound
    let mut compressed = vec![0u8; max_size];
    let mut compressed_size = max_size;
    
    let result = unsafe {
        compress(
            compressed.as_mut_ptr(),
            &mut compressed_size,
            data.as_ptr(),
            data.len(),
        )
    };
    
    if result != 0 {
        return Err(CompressionError { code: result });
    }
    
    compressed.truncate(compressed_size);
    Ok(compressed)
}

// Usage: fully safe API
let data = b"Hello, world!";
let compressed = compress_data(data).expect("Compression failed");
```
**맞춤 설정 포인트:**
- 사용`bindgen`C 헤더에서 FFI 바인딩을 자동 생성합니다.
- 구현`Drop`C 리소스(malloc 포인터, 파일 핸들)의 경우
- 사용`safer-ffi`메모리 안전을 보장하면서 Rust를 C로 내보내는 경우

---

## 패턴: 특성 기반 종속성 주입

**사용 사례:** 모의 가능한 종속성이 있는 테스트 가능한 코드입니다.
```rust
use async_trait::async_trait;
use uuid::Uuid;

#[async_trait]
pub trait OrderRepository: Send + Sync {
    async fn find_by_id(&self, id: Uuid) -> Result<Option<Order>, sqlx::Error>;
    async fn create(&self, order: &CreateOrder) -> Result<Order, sqlx::Error>;
}

// Production implementation
pub struct SqlxOrderRepository {
    pool: PgPool,
}

#[async_trait]
impl OrderRepository for SqlxOrderRepository {
    async fn find_by_id(&self, id: Uuid) -> Result<Option<Order>, sqlx::Error> {
        sqlx::query_as!(Order, "SELECT * FROM orders WHERE id = $1", id)
            .fetch_optional(&self.pool)
            .await
    }
    
    async fn create(&self, order: &CreateOrder) -> Result<Order, sqlx::Error> {
        // ... SQLx implementation
    }
}

// Mock for testing
pub struct MockOrderRepository {
    pub orders: HashMap<Uuid, Order>,
}

#[async_trait]
impl OrderRepository for MockOrderRepository {
    async fn find_by_id(&self, id: Uuid) -> Result<Option<Order>, sqlx::Error> {
        Ok(self.orders.get(&id).cloned())
    }
    
    async fn create(&self, order: &CreateOrder) -> Result<Order, sqlx::Error> {
        // Mock implementation
    }
}

// Service uses trait
pub struct OrderService<R: OrderRepository> {
    repository: R,
}

impl<R: OrderRepository> OrderService<R> {
    pub async fn get_order(&self, id: Uuid) -> Result<Order, ServiceError> {
        self.repository
            .find_by_id(id)
            .await?
            .ok_or(ServiceError::NotFound {
                resource: "Order".to_string(),
                id: id.to_string(),
            })
    }
}

// Testing
#[tokio::test]
async fn test_get_order() {
    let mock_repo = MockOrderRepository {
        orders: HashMap::from([(order_id, order)]),
    };
    
    let service = OrderService { repository: mock_repo };
    let result = service.get_order(order_id).await.unwrap();
    
    assert_eq!(result.id, order_id);
}
```
**맞춤 설정 포인트:**
- 사용`mockall`자동 모의 생성을 위한 상자
- 모든 외부 종속성에 대한 저장소 패턴 구현
- 사용`Arc<dyn Trait>`컴파일 타임 제네릭이 필요하지 않은 경우 런타임 다형성을 위해

---

## Axum 애플리케이션 구조
```rust
// main.rs
use axum::{
    routing::{get, post},
    Router,
};
use sqlx::postgres::PgPoolOptions;
use std::sync::Arc;
use tower_http::trace::TraceLayer;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::init();
    
    let database_url = std::env::var("DATABASE_URL")?;
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(&database_url)
        .await?;
    
    let app_state = Arc::new(AppState { db: pool });
    
    let app = Router::new()
        .route("/health", get(health_check))
        .route("/api/orders", post(create_order))
        .route("/api/orders/:id", get(get_order))
        .layer(TraceLayer::new_for_http())
        .with_state(app_state);
    
    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
    axum::serve(listener, app).await?;
    
    Ok(())
}

// handlers.rs
use axum::{
    extract::{Path, State},
    http::StatusCode,
    Json,
};

pub async fn create_order(
    State(state): State<Arc<AppState>>,
    Json(request): Json<CreateOrderRequest>,
) -> Result<(StatusCode, Json<OrderResponse>), AppError> {
    let order = service::create_order(&state.db, request).await?;
    Ok((StatusCode::CREATED, Json(order)))
}

pub async fn get_order(
    State(state): State<Arc<AppState>>,
    Path(id): Path<Uuid>,
) -> Result<Json<OrderResponse>, AppError> {
    let order = service::get_order(&state.db, id).await?;
    Ok(Json(order))
}
```
---

## 소유권 지침

| 패턴 | 사용 시기 | 메모리 동작 |
|---------|----------|----|
|`T`(소유) | 소유권 이전 | 발신자가 액세스할 수 없음 |
|`&T`(공유 참조) | 읽기 전용 액세스 | 비용 제로, 할당 없음 |
|`&mut T`(변경 가능한 참조) | 내부 수정 | 독점 액세스 필요 |
|`Box<T>`| 힙 할당 | 단일 소유자 |
|`Rc<T>`| 공유 소유권(단일 스레드) | 참조 횟수 |
|`Arc<T>`| 공유 소유권(멀티스레드) | 원자 참조 계산 |
|`Cow<'a, T>`| 쓰기 중 복제 | 가능하면 할당을 피하세요 |