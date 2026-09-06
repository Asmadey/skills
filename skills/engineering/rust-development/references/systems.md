# Rust Systems Programming

Low-level systems programming patterns in Rust.

---

## Table of Contents

1. [Memory Management](#memory-management)
2. [Unsafe Rust](#unsafe-rust)
3. [FFI (Foreign Function Interface)](#ffi)
4. [OS Interaction](#os-interaction)
5. [Concurrency Primitives](#concurrency-primitives)
6. [Performance Optimization](#performance-optimization)

---

## Memory Management

### Stack vs Heap

```rust
// Stack allocation (fast, automatic cleanup)
let x = 5;
let arr = [1, 2, 3, 4, 5];

// Heap allocation (flexible size, manual control)
let boxed = Box::new(5);
let vec = Vec::new();
```

### Box<T> — Single Owner Heap Allocation

```rust
// Use when:
// - Need heap allocation with single owner
// - Recursive types
// - Large data that shouldn't be copied

// Recursive type
enum List {
    Cons(i32, Box<List>),
    Nil,
}

let list = List::Cons(1, Box::new(List::Cons(2, Box::new(List::Nil))));
```

### Rc<T> — Reference Counting (Single Thread)

```rust
use std::rc::Rc;

// Use when:
// - Multiple owners needed
// - Single-threaded only

let data = Rc::new(vec![1, 2, 3]);
let clone1 = Rc::clone(&data);  // Increments count
let clone2 = Rc::clone(&data);

println!("Count: {}", Rc::strong_count(&data)); // 3
```

### Arc<T> — Atomic Reference Counting (Multi Thread)

```rust
use std::sync::Arc;
use std::thread;

// Use when:
// - Multiple owners across threads

let data = Arc::new(vec![1, 2, 3]);

let handles: Vec<_> = (0..3).map(|_| {
    let data = Arc::clone(&data);
    thread::spawn(move || {
        println!("{:?}", data);
    })
}).collect();

for handle in handles {
    handle.join().unwrap();
}
```

### Interior Mutability

```rust
use std::cell::{Cell, RefCell};
use std::sync::Mutex;

// Cell<T> - Copy types, single thread
let cell = Cell::new(5);
cell.set(10);
let value = cell.get();

// RefCell<T> - Runtime borrow checking, single thread
let refcell = RefCell::new(vec![1, 2, 3]);
refcell.borrow_mut().push(4);

// Mutex<T> - Multi-thread
let mutex = Mutex::new(vec![1, 2, 3]);
{
    let mut guard = mutex.lock().unwrap();
    guard.push(4);
} // Lock released here
```

### Cow<T> — Clone-on-Write

```rust
use std::borrow::Cow;

fn process(input: Cow<str>) -> Cow<str> {
    if input.contains("bad") {
        // Only clones if modification needed
        Cow::Owned(input.replace("bad", "good"))
    } else {
        input  // No allocation
    }
}

let borrowed: Cow<str> = Cow::Borrowed("hello");
let owned: Cow<str> = Cow::Owned(String::from("world"));
```

---

## Unsafe Rust

### When to Use Unsafe

```rust
// 1. Dereference raw pointers
// 2. Call unsafe functions (including FFI)
// 3. Implement unsafe traits
// 4. Access mutable statics
```

### Safe Abstractions

```rust
/// # Safety
/// 
/// The caller must ensure that:
/// - `ptr` is valid and aligned
/// - `ptr` points to initialized memory
/// - No other references to this memory exist
pub unsafe fn dangerous_function(ptr: *mut i32) {
    *ptr = 42;
}

// Safe wrapper
pub fn safe_wrapper(value: &mut i32) {
    // SAFETY: We have exclusive access via &mut
    unsafe {
        dangerous_function(value as *mut i32);
    }
}
```

### Raw Pointers

```rust
let mut x = 5;

// Create raw pointers (safe)
let raw_const: *const i32 = &x;
let raw_mut: *mut i32 = &mut x;

// Dereference (unsafe)
unsafe {
    println!("raw_const: {}", *raw_const);
    *raw_mut = 10;
}
```

### Miri for Verification

```bash
# Install Miri
rustup +nightly component add miri

# Run tests with Miri
cargo +nightly miri test
```

---

## FFI

### Calling C from Rust

```rust
// Link against C library
#[link(name = "c")]
extern "C" {
    fn puts(s: *const libc::c_char) -> libc::c_int;
    fn strlen(s: *const libc::c_char) -> libc::size_t;
}

fn main() {
    let msg = std::ffi::CString::new("Hello from Rust!").unwrap();
    unsafe {
        puts(msg.as_ptr());
    }
}
```

### Exposing Rust to C

```rust
// No name mangling for C compatibility
#[no_mangle]
pub extern "C" fn rust_function(x: i32) -> i32 {
    x * 2
}

// Generate C header with cbindgen
// cbindgen --output bindings.h
```

### Using bindgen

```bash
# Install
cargo install bindgen-cli

# Generate bindings
bindgen wrapper.h -o src/bindings.rs
```

```rust
// src/lib.rs
#![allow(non_upper_case_globals)]
#![allow(non_camel_case_types)]
#![allow(non_snake_case)]

include!(concat!(env!("OUT_DIR"), "/bindings.rs"));
```

---

## OS Interaction

### File System

```rust
use std::fs::{self, File};
use std::io::{Read, Write, BufReader, BufWriter};

// Read entire file
let content = fs::read_to_string("file.txt")?;

// Write file
fs::write("output.txt", "Hello, World!")?;

// Buffered reading
let file = File::open("file.txt")?;
let reader = BufReader::new(file);
for line in reader.lines() {
    println!("{}", line?);
}

// Buffered writing
let file = File::create("output.txt")?;
let mut writer = BufWriter::new(file);
writer.write_all(b"Hello!")?;
```

### Process Management

```rust
use std::process::{Command, Stdio};

// Run command
let output = Command::new("ls")
    .arg("-la")
    .output()?;

println!("stdout: {}", String::from_utf8_lossy(&output.stdout));

// Piped commands
let echo = Command::new("echo")
    .arg("hello")
    .stdout(Stdio::piped())
    .spawn()?;

let grep = Command::new("grep")
    .arg("ell")
    .stdin(echo.stdout.unwrap())
    .output()?;
```

### Environment Variables

```rust
use std::env;

// Get
let path = env::var("PATH")?;
let home = env::var("HOME").unwrap_or_else(|_| String::from("/tmp"));

// Set (current process only)
env::set_var("MY_VAR", "value");

// Remove
env::remove_var("MY_VAR");
```

---

## Concurrency Primitives

### Atomics

```rust
use std::sync::atomic::{AtomicUsize, Ordering};

static COUNTER: AtomicUsize = AtomicUsize::new(0);

fn increment() {
    COUNTER.fetch_add(1, Ordering::SeqCst);
}

fn get_count() -> usize {
    COUNTER.load(Ordering::SeqCst)
}
```

### Mutex and RwLock

```rust
use std::sync::{Mutex, RwLock, Arc};

// Mutex - exclusive access
let data = Arc::new(Mutex::new(vec![]));
{
    let mut guard = data.lock().unwrap();
    guard.push(1);
}

// RwLock - multiple readers OR single writer
let data = Arc::new(RwLock::new(vec![]));

// Reading (multiple allowed)
{
    let guard = data.read().unwrap();
    println!("{:?}", *guard);
}

// Writing (exclusive)
{
    let mut guard = data.write().unwrap();
    guard.push(1);
}
```

### Channels

```rust
use std::sync::mpsc;
use std::thread;

// Multiple producer, single consumer
let (tx, rx) = mpsc::channel();

let tx1 = tx.clone();
thread::spawn(move || {
    tx1.send("from thread 1").unwrap();
});

thread::spawn(move || {
    tx.send("from thread 2").unwrap();
});

for received in rx {
    println!("Got: {}", received);
}
```

---

## Performance Optimization

### Memory Layout

```rust
// C-compatible layout
#[repr(C)]
struct CCompatible {
    a: u8,
    b: u32,
    c: u8,
}

// Packed (no padding, careful with alignment!)
#[repr(packed)]
struct Packed {
    a: u8,
    b: u32,
    c: u8,
}

// Check sizes
println!("Normal: {}", std::mem::size_of::<CCompatible>()); // 12
println!("Packed: {}", std::mem::size_of::<Packed>());      // 6
```

### SIMD

```rust
#[cfg(target_arch = "x86_64")]
use std::arch::x86_64::*;

#[cfg(target_arch = "x86_64")]
unsafe fn add_simd(a: &[f32; 4], b: &[f32; 4]) -> [f32; 4] {
    let va = _mm_loadu_ps(a.as_ptr());
    let vb = _mm_loadu_ps(b.as_ptr());
    let vc = _mm_add_ps(va, vb);
    
    let mut result = [0.0f32; 4];
    _mm_storeu_ps(result.as_mut_ptr(), vc);
    result
}
```

### Minimize Allocations

```rust
// Pre-allocate
let mut vec = Vec::with_capacity(1000);

// Reuse allocations
vec.clear();  // Keeps capacity

// Use references instead of cloning
fn process(data: &[u8]) { }  // Not fn process(data: Vec<u8>)

// Use iterators (zero-cost abstraction)
let sum: i32 = (0..1000).filter(|x| x % 2 == 0).sum();
```
