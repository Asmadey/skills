---
name: Rust Development
description: Comprehensive Rust programming skill covering web development (Axum/Actix/Rocket), systems programming, memory management, async/await, and FFI. Use when building REST APIs, CLI tools, high-performance services, or systems-level code in Rust. Includes error handling patterns, Cloud deployment (GCP/Docker), and effective prompts for AI-assisted Rust development. Note - Rust compiler gives very clear errors; agents fix them with 95% probability.
created: 2026-02-08
last_updated: 2026-02-18
---

# Rust Development

Expert guidance for Rust systems programming, web development, and AI-assisted coding.

**Key insight:** Rust compiler errors are VERY clear. Agents fix them with ~95% probability.

---

## Quick Reference

### Framework Selection

| Use Case | Framework | Why |
|----------|-----------|-----|
| **General Web API** | **Axum** ⭐ | Best overall choice, tower ecosystem |
| High-throughput API | Actix Web | Maximum performance |
| Rapid prototyping | Rocket | Ergonomic, less boilerplate |
| Static sites | Rocket + Askama | Simple templating |

### Essential Crates

```toml
[dependencies]
# Web
axum = "0.7"
tokio = { version = "1", features = ["full"] }

# Serialization
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"

# Database
sqlx = { version = "0.7", features = ["runtime-tokio", "postgres"] }

# Error handling
anyhow = "1.0"      # Application errors
thiserror = "1.0"   # Library errors

# Auth
jsonwebtoken = "9"
argon2 = "0.5"
```

---

## Web Development

### Axum Hello World

```rust
use axum::{routing::get, Router};

async fn hello() -> &'static str {
    "Hello, World!"
}

#[tokio::main]
async fn main() {
    let app = Router::new().route("/", get(hello));
    
    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

### Actix Web Hello World

```rust
use actix_web::{web, App, HttpServer, Responder};

async fn hello() -> impl Responder {
    "Hello, World!"
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new().route("/", web::get().to(hello))
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}
```

For detailed patterns, see:
- **[references/axum-patterns.md](references/axum-patterns.md)** — Axum handlers, extractors, middleware
- **[references/actix-patterns.md](references/actix-patterns.md)** — Actix patterns
- **[references/database.md](references/database.md)** — SQLx/Diesel integration

---

## Systems Programming

See **[references/systems.md](references/systems.md)** for:
- Memory management (Box, Rc, Arc, Cell, RefCell)
- Unsafe Rust patterns
- FFI with C libraries
- OS interaction
- Concurrency primitives

### Memory Quick Reference

| Type | When to Use |
|------|-------------|
| `Box<T>` | Heap allocation, single owner |
| `Rc<T>` | Multiple owners, single thread |
| `Arc<T>` | Multiple owners, multiple threads |
| `RefCell<T>` | Interior mutability, single thread |
| `Mutex<T>` | Interior mutability, multi-thread |
| `Cow<T>` | Clone-on-write optimization |

---

## Error Handling

### The Rules

```rust
// ❌ NEVER in production
.unwrap()
.expect("should work")

// ✅ ALWAYS use
?     // Propagate errors
anyhow::Result<T>   // For applications
thiserror::Error    // For libraries
```

### Application Error Pattern

```rust
use anyhow::{Context, Result};

async fn get_user(id: i64) -> Result<User> {
    let user = db.fetch_user(id)
        .await
        .context("Failed to fetch user from database")?;
    
    Ok(user)
}
```

### Library Error Pattern

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ApiError {
    #[error("User not found: {0}")]
    NotFound(i64),
    
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),
    
    #[error("Validation failed: {0}")]
    Validation(String),
}
```

---

## Effective AI Prompts

### For Architecture

```
Act as a Senior Rust Engineer. Review my SPEC.md. 
Suggest idiomatic Rust project structure using 'Clean Architecture'. 
Define the traits for the Repository pattern needed for User management.
```

### For Code Generation

```
Implement the handler for 'POST /users'. 
Use 'anyhow' for error handling. 
Ensure all database calls are async. 
Do not unwrap() results, use '?' operator and map errors appropriately.
```

### For Borrow Checker Errors

```
I am getting a borrow checker error: 
[PASTE ERROR]

Explain why ownership is violated here and rewrite the code using 
.clone() only if necessary, or suggest using Arc/Mutex if sharing 
across threads is required.
```

### For Refactoring

```
Refactor this function to be more idiomatic. 
Replace the imperative loop with functional iterators (map, filter, collect). 
Use pattern matching instead of if-else chains where possible.
```

---

## Required Skills

| Skill | Why Important | How to Learn |
|-------|---------------|--------------|
| Ownership & Borrowing | Avoid memory bugs | Rust Book Ch. 4-5 |
| Async Programming | High-throughput servers | Tokio docs |
| Error Handling | Robust apps | anyhow + thiserror |
| Type Reading | Understand `Arc<Mutex<T>>` vs `&T` | Practice |
| Trait Bounds | `T: Serialize + Clone` | Rust Book Ch. 10 |

---

## Cloud Deployment

### Dockerfile

```dockerfile
FROM rust:1.75 as builder
WORKDIR /app
COPY . .
RUN cargo build --release

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/target/release/my_app /usr/local/bin/
CMD ["my_app"]
```

### Cloud Run Deployment

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/my-app

# Deploy
gcloud run deploy my-app \
  --image gcr.io/PROJECT_ID/my-app \
  --platform managed \
  --allow-unauthenticated
```

---

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|---------|--------------|
| `.unwrap()` everywhere | Use `?` and proper error types |
| `clone()` to fix borrow errors | Understand ownership first |
| Ignore compiler warnings | Treat warnings as errors |
| `Arc<Mutex<T>>` by default | Start with simpler types |
| Block async with `block_on` | Stay async end-to-end |

---

## Project Structure

```
my-api/
├── Cargo.toml
├── src/
│   ├── main.rs           # Entry point
│   ├── lib.rs            # Library root
│   ├── config.rs         # Configuration
│   ├── error.rs          # Error types
│   ├── handlers/         # HTTP handlers
│   │   ├── mod.rs
│   │   └── users.rs
│   ├── models/           # Domain models
│   │   ├── mod.rs
│   │   └── user.rs
│   ├── repositories/     # Data access
│   │   ├── mod.rs
│   │   └── user_repo.rs
│   └── services/         # Business logic
│       ├── mod.rs
│       └── user_service.rs
├── tests/
│   └── integration/
└── migrations/
```
