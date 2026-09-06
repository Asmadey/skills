# Axum Patterns

Detailed patterns for Axum web framework.

---

## Table of Contents

1. [Handlers](#handlers)
2. [Extractors](#extractors)
3. [State Management](#state-management)
4. [Middleware](#middleware)
5. [Error Handling](#error-handling)
6. [Authentication](#authentication)
7. [Testing](#testing)

---

## Handlers

### Basic Handler

```rust
use axum::{response::Json, http::StatusCode};
use serde::{Deserialize, Serialize};

#[derive(Serialize)]
struct User {
    id: i64,
    name: String,
}

async fn get_user() -> Json<User> {
    Json(User { id: 1, name: "Alice".into() })
}
```

### Handler with Path Parameters

```rust
use axum::extract::Path;

async fn get_user_by_id(Path(user_id): Path<i64>) -> Json<User> {
    Json(User { id: user_id, name: "Alice".into() })
}

// Route: .route("/users/:id", get(get_user_by_id))
```

### Handler with Query Parameters

```rust
use axum::extract::Query;

#[derive(Deserialize)]
struct Pagination {
    page: Option<u32>,
    limit: Option<u32>,
}

async fn list_users(Query(params): Query<Pagination>) -> Json<Vec<User>> {
    let page = params.page.unwrap_or(1);
    let limit = params.limit.unwrap_or(10);
    // ...
}
```

### Handler with JSON Body

```rust
#[derive(Deserialize)]
struct CreateUser {
    name: String,
    email: String,
}

async fn create_user(Json(payload): Json<CreateUser>) -> (StatusCode, Json<User>) {
    let user = User { id: 1, name: payload.name };
    (StatusCode::CREATED, Json(user))
}
```

---

## Extractors

### Multiple Extractors

```rust
async fn update_user(
    Path(id): Path<i64>,
    State(db): State<DbPool>,
    Json(payload): Json<UpdateUser>,
) -> Result<Json<User>, AppError> {
    // Order matters! State should come before body extractors
}
```

### Custom Extractor

```rust
use axum::{
    async_trait,
    extract::FromRequestParts,
    http::{request::Parts, StatusCode},
};

struct AuthUser {
    user_id: i64,
}

#[async_trait]
impl<S> FromRequestParts<S> for AuthUser
where
    S: Send + Sync,
{
    type Rejection = (StatusCode, &'static str);

    async fn from_request_parts(parts: &mut Parts, _state: &S) -> Result<Self, Self::Rejection> {
        // Extract from headers, validate JWT, etc.
        let auth_header = parts.headers
            .get("Authorization")
            .ok_or((StatusCode::UNAUTHORIZED, "Missing auth header"))?;
        
        // Validate and extract user_id...
        Ok(AuthUser { user_id: 1 })
    }
}
```

---

## State Management

### Shared State

```rust
use std::sync::Arc;
use tokio::sync::RwLock;

#[derive(Clone)]
struct AppState {
    db: DbPool,
    cache: Arc<RwLock<HashMap<String, String>>>,
}

#[tokio::main]
async fn main() {
    let state = AppState {
        db: create_pool().await,
        cache: Arc::new(RwLock::new(HashMap::new())),
    };

    let app = Router::new()
        .route("/users", get(list_users))
        .with_state(state);
}

async fn list_users(State(state): State<AppState>) -> Json<Vec<User>> {
    let users = state.db.fetch_users().await;
    Json(users)
}
```

---

## Middleware

### Tower Middleware

```rust
use tower_http::{
    cors::CorsLayer,
    trace::TraceLayer,
    compression::CompressionLayer,
};

let app = Router::new()
    .route("/", get(root))
    .layer(TraceLayer::new_for_http())
    .layer(CompressionLayer::new())
    .layer(CorsLayer::permissive());
```

### Custom Middleware

```rust
use axum::middleware::{self, Next};
use axum::http::Request;
use axum::response::Response;

async fn logging_middleware<B>(
    request: Request<B>,
    next: Next<B>,
) -> Response {
    let method = request.method().clone();
    let uri = request.uri().clone();
    
    let response = next.run(request).await;
    
    tracing::info!("{} {} -> {}", method, uri, response.status());
    response
}

let app = Router::new()
    .route("/", get(root))
    .layer(middleware::from_fn(logging_middleware));
```

---

## Error Handling

### App Error Type

```rust
use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde_json::json;

pub struct AppError {
    status: StatusCode,
    message: String,
}

impl AppError {
    pub fn not_found(msg: impl Into<String>) -> Self {
        Self { status: StatusCode::NOT_FOUND, message: msg.into() }
    }
    
    pub fn internal(msg: impl Into<String>) -> Self {
        Self { status: StatusCode::INTERNAL_SERVER_ERROR, message: msg.into() }
    }
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let body = Json(json!({
            "error": self.message
        }));
        (self.status, body).into_response()
    }
}

// Usage in handlers
async fn get_user(Path(id): Path<i64>) -> Result<Json<User>, AppError> {
    let user = db.find_user(id)
        .await
        .map_err(|_| AppError::internal("Database error"))?
        .ok_or_else(|| AppError::not_found("User not found"))?;
    
    Ok(Json(user))
}
```

---

## Authentication

### JWT Authentication

```rust
use jsonwebtoken::{decode, encode, DecodingKey, EncodingKey, Header, Validation};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct Claims {
    sub: i64,  // user_id
    exp: usize,
}

fn create_token(user_id: i64, secret: &[u8]) -> Result<String, jsonwebtoken::errors::Error> {
    let expiration = chrono::Utc::now()
        .checked_add_signed(chrono::Duration::hours(24))
        .unwrap()
        .timestamp() as usize;

    let claims = Claims { sub: user_id, exp: expiration };
    
    encode(&Header::default(), &claims, &EncodingKey::from_secret(secret))
}

fn validate_token(token: &str, secret: &[u8]) -> Result<Claims, jsonwebtoken::errors::Error> {
    let token_data = decode::<Claims>(
        token,
        &DecodingKey::from_secret(secret),
        &Validation::default(),
    )?;
    Ok(token_data.claims)
}
```

---

## Testing

### Integration Tests

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use axum::{
        body::Body,
        http::{Request, StatusCode},
    };
    use tower::ServiceExt;

    #[tokio::test]
    async fn test_get_user() {
        let app = create_app();

        let response = app
            .oneshot(
                Request::builder()
                    .uri("/users/1")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);
    }

    #[tokio::test]
    async fn test_create_user() {
        let app = create_app();

        let response = app
            .oneshot(
                Request::builder()
                    .method("POST")
                    .uri("/users")
                    .header("content-type", "application/json")
                    .body(Body::from(r#"{"name":"Alice","email":"alice@example.com"}"#))
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::CREATED);
    }
}
```
