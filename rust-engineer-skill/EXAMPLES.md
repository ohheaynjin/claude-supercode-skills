# Rust 엔지니어 - 코드 예제 및 패턴

이 문서에는 Rust 개발을 위한 코드 예제, 안티 패턴, 실제 구현 패턴이 포함되어 있습니다.

## 안티 패턴 1: .unwrap()을 사용한 오류 처리 무시

**모습:**```rust
// WRONG: Unwrap everywhere
fn load_config() -> Config {
    let content = std::fs::read_to_string("config.toml").unwrap(); // Panic on missing file!
    toml::from_str(&content).unwrap() // Panic on parse error!
}

// WRONG: Ignoring Results
async fn save_user(db: &PgPool, user: &User) {
    sqlx::query!("INSERT INTO users (name) VALUES ($1)", user.name)
        .execute(db)
        .await; // Result ignored! Error silently discarded
}
```

**실패하는 이유:**
- **런타임 패닉**: `.unwrap()`이 `Err` 또는 `None`에서 프로그램을 충돌시킵니다.
- **자동 오류**: `Result`을 무시하면 데이터베이스 오류, 네트워크 오류가 숨겨집니다.
- **복구 없음**: 비동기 컨텍스트에서는 패닉을 안전하게 포착할 수 없습니다.
- **나쁜 UX**: 사용자에게 유용한 오류 메시지 대신 "스레드 패닉"이 표시됩니다.

**올바른 접근 방식:**```rust
// CORRECT: Proper error propagation
fn load_config() -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string("config.toml")
        .map_err(|e| ConfigError::FileRead(e))?;
    toml::from_str(&content)
        .map_err(|e| ConfigError::Parse(e))
}

// CORRECT: Handle errors explicitly
async fn save_user(db: &PgPool, user: &User) -> Result<(), sqlx::Error> {
    sqlx::query!("INSERT INTO users (name) VALUES ($1)", user.name)
        .execute(db)
        .await?;
    Ok(())
}

// CORRECT: Use expect() only for truly impossible cases
let port: u16 = std::env::var("PORT")
    .expect("PORT env var required") // Only if this is a startup requirement
    .parse()
    .expect("PORT must be a valid u16");
```

**.unwrap()이 허용되는 경우:**
- 테스트(실패하면 테스트에 실패해야 함)
- 프로토타입 및 예시
- 정말 불가능한 경우(수학적으로 증명됨)
- 명시적인 검증 후(`if let Some(x) = ... { x.unwrap() }`)

---

## 안티 패턴 2: 복제가 많은 코드(불필요한 할당)

**모습:**```rust
// WRONG: Cloning on every function call
fn process_orders(orders: Vec<Order>) -> Vec<OrderSummary> {
    orders
        .iter()
        .map(|order| calculate_summary(order.clone())) // Unnecessary clone!
        .collect()
}

// WRONG: Cloning to satisfy borrow checker
async fn handle_request(state: AppState) {
    let db = state.db.clone(); // Clone entire connection pool!
    let config = state.config.clone(); // Clone large config!
    
    process_data(db, config).await;
}

// WRONG: String clones in hot path
fn generate_ids(count: usize) -> Vec<String> {
    (0..count)
        .map(|i| format!("ID-{}", i).clone()) // format! already returns String!
        .collect()
}
```

**실패하는 이유:**
- **성능 저하**: 할당 비용이 많이 듭니다.
- **메모리 부족**: 불필요한 복제로 인해 메모리 사용량이 증가합니다.
- **캐시 누락**: 더 많은 할당 = 더 많은 포인터 추적
- **소유권 버그 숨기기**: 복제 마스크 디자인 문제

**올바른 접근 방식:**```rust
// CORRECT: Borrow instead of clone
fn process_orders(orders: &[Order]) -> Vec<OrderSummary> {
    orders
        .iter()
        .map(|order| calculate_summary(order)) // Pass reference
        .collect()
}

fn calculate_summary(order: &Order) -> OrderSummary {
    OrderSummary {
        id: order.id,
        total: order.items.iter().map(|i| i.price).sum(),
    }
}

// CORRECT: Share with Arc only when needed
#[derive(Clone)]
struct AppState {
    db: PgPool, // PgPool is already Arc internally, cheap to clone
    config: Arc<Config>, // Wrap large struct in Arc
}

async fn handle_request(state: AppState) {
    // Cloning state is cheap: PgPool = Arc clone, config = Arc clone
    process_data(state.db, state.config).await;
}

// CORRECT: Avoid redundant operations
fn generate_ids(count: usize) -> Vec<String> {
    (0..count)
        .map(|i| format!("ID-{}", i)) // format! returns String, no .clone()
        .collect()
}

// CORRECT: Use Cow for conditional cloning
use std::borrow::Cow;

fn normalize_string(s: &str) -> Cow<str> {
    if s.contains(char::is_uppercase) {
        Cow::Owned(s.to_lowercase()) // Clone only if needed
    } else {
        Cow::Borrowed(s) // No allocation if already lowercase
    }
}
```

**가이드라인:**
- 소유권 이전이 필요한 경우를 제외하고 **기본값은 차용**(`&T`)입니다.
- **스레드 간에 공유된 불변 데이터의 경우 `Arc<T>`**을 사용하세요.
- **단일 스레드 컨텍스트에서 공유 데이터에는 `Rc<T>`**를 사용하세요.
- **최적화 전 프로필**: `cargo flamegraph`을 사용하여 핫 클론을 찾습니다.
- **저렴한 복제도 괜찮습니다**: `Arc`, `Rc`, `PgPool`, 작은 복사 유형

---

## 예: 완전한 Axum REST API

```rust
// main.rs
use axum::{
    extract::{Path, Query, State},
    http::StatusCode,
    response::IntoResponse,
    routing::{delete, get, post, put},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use sqlx::postgres::PgPoolOptions;
use std::sync::Arc;
use uuid::Uuid;

#[derive(Clone)]
struct AppState {
    db: sqlx::PgPool,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let database_url = std::env::var("DATABASE_URL")?;
    
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(&database_url)
        .await?;
    
    let state = AppState { db: pool };
    
    let app = Router::new()
        .route("/api/products", get(list_products).post(create_product))
        .route(
            "/api/products/:id",
            get(get_product).put(update_product).delete(delete_product),
        )
        .with_state(state);
    
    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
    println!("Server running on http://localhost:3000");
    axum::serve(listener, app).await?;
    
    Ok(())
}

// Models
#[derive(Debug, Serialize, Deserialize, sqlx::FromRow)]
struct Product {
    id: Uuid,
    name: String,
    price: f64,
    created_at: chrono::DateTime<chrono::Utc>,
}

#[derive(Debug, Deserialize)]
struct CreateProduct {
    name: String,
    price: f64,
}

#[derive(Debug, Deserialize)]
struct ListParams {
    limit: Option<i64>,
    offset: Option<i64>,
}

// Handlers
async fn list_products(
    State(state): State<AppState>,
    Query(params): Query<ListParams>,
) -> Result<Json<Vec<Product>>, AppError> {
    let limit = params.limit.unwrap_or(20);
    let offset = params.offset.unwrap_or(0);
    
    let products = sqlx::query_as!(
        Product,
        r#"SELECT id, name, price, created_at FROM products 
           ORDER BY created_at DESC LIMIT $1 OFFSET $2"#,
        limit,
        offset
    )
    .fetch_all(&state.db)
    .await?;
    
    Ok(Json(products))
}

async fn get_product(
    State(state): State<AppState>,
    Path(id): Path<Uuid>,
) -> Result<Json<Product>, AppError> {
    let product = sqlx::query_as!(
        Product,
        "SELECT id, name, price, created_at FROM products WHERE id = $1",
        id
    )
    .fetch_optional(&state.db)
    .await?
    .ok_or(AppError::NotFound)?;
    
    Ok(Json(product))
}

async fn create_product(
    State(state): State<AppState>,
    Json(input): Json<CreateProduct>,
) -> Result<(StatusCode, Json<Product>), AppError> {
    let product = sqlx::query_as!(
        Product,
        r#"INSERT INTO products (id, name, price, created_at) 
           VALUES ($1, $2, $3, NOW()) 
           RETURNING id, name, price, created_at"#,
        Uuid::new_v4(),
        input.name,
        input.price
    )
    .fetch_one(&state.db)
    .await?;
    
    Ok((StatusCode::CREATED, Json(product)))
}

// Error handling
#[derive(Debug)]
enum AppError {
    Database(sqlx::Error),
    NotFound,
}

impl From<sqlx::Error> for AppError {
    fn from(err: sqlx::Error) -> Self {
        AppError::Database(err)
    }
}

impl IntoResponse for AppError {
    fn into_response(self) -> axum::response::Response {
        let (status, message) = match self {
            AppError::Database(e) => {
                tracing::error!("Database error: {:?}", e);
                (StatusCode::INTERNAL_SERVER_ERROR, "Database error")
            }
            AppError::NotFound => (StatusCode::NOT_FOUND, "Not found"),
        };
        
        (status, Json(serde_json::json!({ "error": message }))).into_response()
    }
}
```

---

## 테스트 패턴

### 모의를 이용한 단위 테스트

```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    #[tokio::test]
    async fn test_create_order_success() {
        let mock_repo = MockOrderRepository::new();
        mock_repo.expect_create()
            .returning(|order| Ok(Order { id: Uuid::new_v4(), ..order }));
        
        let service = OrderService::new(mock_repo);
        let result = service.create(CreateOrder { 
            customer_id: Uuid::new_v4(),
            items: vec![],
        }).await;
        
        assert!(result.is_ok());
    }
    
    #[tokio::test]
    async fn test_get_order_not_found() {
        let mock_repo = MockOrderRepository::new();
        mock_repo.expect_find_by_id()
            .returning(|_| Ok(None));
        
        let service = OrderService::new(mock_repo);
        let result = service.get(Uuid::new_v4()).await;
        
        assert!(matches!(result, Err(ServiceError::NotFound { .. })));
    }
}
```

### 통합 테스트

```rust
#[cfg(test)]
mod integration_tests {
    use super::*;
    use sqlx::PgPool;
    
    #[sqlx::test]
    async fn test_product_crud(pool: PgPool) {
        // Create
        let product = create_product(&pool, "Test Product", 10.0).await.unwrap();
        assert_eq!(product.name, "Test Product");
        
        // Read
        let fetched = get_product(&pool, product.id).await.unwrap();
        assert_eq!(fetched.id, product.id);
        
        // Update
        let updated = update_product(&pool, product.id, "Updated", 20.0).await.unwrap();
        assert_eq!(updated.name, "Updated");
        assert_eq!(updated.price, 20.0);
        
        // Delete
        delete_product(&pool, product.id).await.unwrap();
        let result = get_product(&pool, product.id).await;
        assert!(result.is_err());
    }
}
```

---

## Rust 서비스용 Dockerfile

```dockerfile
# Build stage
FROM rust:1.75-alpine AS builder

RUN apk add --no-cache musl-dev

WORKDIR /app
COPY Cargo.toml Cargo.lock ./
COPY src ./src

RUN cargo build --release --target x86_64-unknown-linux-musl

# Runtime stage
FROM alpine:3.19

RUN apk add --no-cache ca-certificates

COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/myapp /usr/local/bin/

EXPOSE 3000
CMD ["myapp"]
```

**빌드 최적화:**
- 더 작은 바이너리의 경우 `Cargo.toml`에서 `lto = true`을 사용하세요.
- 디버그 기호를 제거하려면 `strip = true`를 사용하세요.
- 크기 최적화를 위해 `opt-level = "s"`을(를) 고려하세요.