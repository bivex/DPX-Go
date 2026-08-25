# 🐹 DPX-Go: Hexagonal Go Pattern Scanner & Architecture Engine

<p align="center">
  <strong>High-Performance Static Analysis & Software Design Pattern Detection for Go (Golang 1.18 - 1.24+)</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Language-Go%201.18--1.24+-00ADD8.svg?style=for-the-badge&logo=go" alt="Go" />
  <img src="https://img.shields.io/badge/Architecture-Hexagonal%20DDD-10B981.svg?style=for-the-badge" alt="Hexagonal DDD" />
  <img src="https://img.shields.io/badge/Rules%20Catalog-40%20Rules-8B5CF6.svg?style=for-the-badge" alt="Rules" />
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="License" />
</p>

---

## 🌟 Overview

**DPX-Go** is a next-generation static analysis and software design pattern detection engine designed specifically for **Go (Golang)** codebases. Built following strict **Hexagonal Architecture (Ports & Adapters)** and **Domain-Driven Design (DDD)** principles, DPX-Go detects Gang of Four (GoF) design patterns, idiomatic Go concurrency idioms (Channels, Pipelines, Fan-Out/Fan-In, Worker Pools, `sync.Once`), and architectural code smells (God Structs, Fat Interfaces, Goroutine Leaks).

### 🚀 Key Highlights

- **⚡ Zero External Binaries / Blazing Fast:** Native streaming Go lexer and balanced-delimiter parser capable of scanning thousands of Go files in sub-second speeds.
- **🛠️ Idiomatic Go Concurrency & Options:** Specialized detection for Functional Options (`WithPort()`), Channel Pipelines, Fan-Out/Fan-In, Worker Pools, `errgroup`, and `context.Context` propagation.
- **🛡️ Safety & Resource Auditing:** Detects Goroutine Leaks (unbounded loops without `ctx.Done()`) and unchecked errors (`_ = fn()`).
- **📊 Rich Multi-Format Reporting:** Generates interactive dark Semantic UI HTML Dashboards, OASIS SARIF v2.1.0 (for GitHub Security Scanning), JSON, Markdown, and AI / LLM Architectural Context Maps.

---

## 🏗️ Architecture

```
                               ┌────────────────────────────────────────────────────────┐
                               │                    DPX-Go CLI                          │
                               └───────────────────────────┬────────────────────────────┘
                                                           │
                                                           ▼ (ScanOptions)
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                             APPLICATION LAYER                                                    │
│                                                                                                                  │
│   ┌──────────────────────────────────────────────┐              ┌────────────────────────────────────────────┐   │
│   │               ScanningService                │─────────────▶│              DetectionService              │   │
│   └──────────────────────┬───────────────────────┘              └─────────────────────┬──────────────────────┘   │
└──────────────────────────┼────────────────────────────────────────────────────────────┼──────────────────────────┘
                           │ (CodeModel)                                                │ (Rules Execution)
                           ▼                                                            ▼
┌───────────────────────────────────────────────────────┐  ┌───────────────────────────────────────────────────────┐
│                    OUTBOUND PORTS                     │  │                     DOMAIN RULES                      │
│                                                       │  │                                                       │
│ • NativeGoParserAdapter (Go 1.18+ AST / CST)          │  │ • Creational: Functional Options, Builder, Factory    │
│ • FileSourceProvider (.go files)                      │  │ • Structural: Adapter, Decorator, Facade, Composite   │
│ • HtmlReportFormatter (Dark Semantic UI Dashboard)    │  │ • Behavioral: Strategy, Observer, Command, Visitor    │
│ • SarifReportFormatter (OASIS SARIF v2.1.0)           │  │ • Concurrency: Pipeline, Fan-In, Worker Pool, errgroup│
│ • Json / Markdown / LLM Context Formatters            │  │ • SOLID & Safety: SRP, ISP, Goroutine Leaks, DRY     │
└───────────────────────────────────────────────────────┘  └───────────────────────────────────────────────────────┘
```

---

## 📦 Installation & Quick Start

```bash
# Clone the repository
git clone https://github.com/bivex/DPX-Go.git
cd DPX-Go

# Install dependencies using uv
uv sync

# Run the pattern scanner on any Go project
uv run dpx scan /path/to/your/go/project

# Generate an interactive HTML dashboard
uv run dpx scan /path/to/your/go/project -H report.html

# Generate GitHub SARIF for CI/CD
uv run dpx scan /path/to/your/go/project -S results.sarif
```

---

## 📋 Catalog of Supported Patterns & Rules (40 Rules)

### 1. 🏗️ Creational Patterns (6)
| Pattern | Detection Criteria |
|---|---|
| **Functional Options** | Idiomatic Go creational pattern: `type Option func(*Server)`, `WithPort()`, variadic `...Option`. |
| **Builder** | Fluent chaining setters returning `*Builder` with terminal `Build()` / `Create()` methods. |
| **Factory Method** | Encapsulated constructor functions (`New...()`, `NewFromConfig()`, `Open()`). |
| **Abstract Factory** | Interfaces declaring families of product creation methods (`CreateConnection()`, `CreateTx()`). |
| **Singleton** | Thread-safe lazy global initialization via `sync.Once` (`once.Do(func() { ... })`). |
| **Prototype** | Deep object cloning via explicit `Clone()` / `DeepCopy()` methods. |

### 2. 🧩 Structural Patterns (7)
| Pattern | Detection Criteria |
|---|---|
| **Adapter** | Structs wrapping adaptees (`src`, `inner`) implementing target interfaces (`io.Reader`, `http.Handler`). |
| **Decorator / Middleware** | Wrapping inner interfaces/handlers to layer cross-cutting concerns (logging, auth, metrics). |
| **Facade** | Aggregator structs simplifying access across 3+ subsystem packages behind a unified API. |
| **Composite** | Part-whole tree hierarchies with slices of component interfaces (`[]Component`, `[]Node`). |
| **Proxy** | Surrogate objects holding target references to control access, caching, or remote RPC calls. |
| **Bridge** | Decoupling struct abstraction from backend driver interfaces (`driver.Driver`, `backend.Engine`). |
| **Flyweight** | Shared memory allocation reuse via `sync.Pool` or string interning caches. |

### 3. 🎯 Behavioral Patterns (11)
| Pattern | Detection Criteria |
|---|---|
| **Strategy** | Polymorphic algorithm interfaces or first-class function strategy types (`type MatcherFunc func(...)`). |
| **Observer / Event Hub** | Multi-subscriber channel dispatchers (`chan Event`, `map[string][]chan Event`, `Publish()`). |
| **Command** | Encapsulating requests as executable interfaces with `Execute(ctx)` / `Undo()`. |
| **Template Method** | Base struct workflows calling embedded interface steps in fixed template sequence. |
| **Chain of Responsibility** | Onion middleware chains (`func(http.Handler) http.Handler`, handler successors). |
| **Iterator** | Collection traversal via `Next()` / `HasNext()`, channels, or range-over-func. |
| **Mediator** | Central coordinator managing communication channels between independent goroutines. |
| **Memento** | Capturing internal struct state snapshots for restoration (`SaveSnapshot()` / `Restore()`). |
| **Visitor** | AST traversal protocol via `Visitor` interfaces (`Walk(v Visitor)`, `Visit(node Node)`). |
| **Interpreter** | Grammatical expression evaluation over AST nodes (`Eval(ctx Context) Value`). |
| **State** | Interface-based state machines and polymorphic state handlers. |

### 4. ⚡ Go Concurrency & Idioms (8)
| Pattern / Idiom | Detection Criteria |
|---|---|
| **Pipeline** | Channel stages taking `<-chan T` input and streaming transformed items to `<-chan T` output. |
| **Fan-Out / Fan-In** | Merging multiple channel inputs into a single output channel using `sync.WaitGroup`. |
| **Worker Pool** | Fixed number of worker goroutines consuming tasks from a shared jobs channel. |
| **Generator** | Spawning a producer goroutine and returning a read-only receive channel (`<-chan T`). |
| **Context Propagation** | Idiomatic passing of `ctx context.Context` as the first parameter for cancellations and timeouts. |
| **ErrGroup Concurrency** | Coordinating concurrent subtasks with `golang.org/x/sync/errgroup` for automatic error handling. |
| **Struct Embedding** | Idiomatic Go composition over inheritance via anonymous struct embedding. |
| **Circular Dependency** | Detecting cross-package import cycles. |

### 5. 🛡️ SOLID Principles & Safety (8)
| Principle / Smell | Detection Criteria |
|---|---|
| **Single Responsibility (SRP)** | God Structs: Structs with excessive methods (≥15) or fields (≥12). |
| **Interface Pollution (ISP)** | Fat Interfaces: Interfaces with ≥8 methods (idiomatic Go prefers 1-2 method interfaces). |
| **Open/Closed Principle (OCP)** | Rigid type switch cascades (`switch v.(type)`) with ≥5 cases that should use polymorphism. |
| **Liskov Substitution (LSP)** | Methods calling `panic("unimplemented")` or unconditional errors in interface methods. |
| **Dependency Inversion (DIP)** | Functions depending on interface abstractions (`io.Reader`, `io.Writer`) rather than struct pointers. |
| **Keep It Simple (KISS)** | Functions with high cyclomatic complexity (≥10) or long parameter lists (≥5). |
| **Don't Repeat Yourself (DRY)**| Identical function implementation logic duplicated across multiple locations. |
| **Goroutine Leak Risk** | Goroutines running infinite loops or blocking channels without `ctx.Done()` or quit channels. |
| **Unchecked Error Risk** | Explicitly ignored returned errors (`_ = fn()`). |

---

## 🌐 The DPX Suite Family

Cross-language architectural static analysis across all modern programming languages:

| Repository | Language / Ecosystem | Primary Paradigms & Focus |
|---|---|---|
| **[`DPX-Gleam`](https://github.com/bivex/DPX-Gleam)** | **Gleam** (1.0 - 1.8+) | **Type-Safe OTP Actors, Algebraic Data Types, Railway Monads, GoF 23** |
| **[`DPX-Mojo`](https://github.com/bivex/DPX-Mojo)** | **Mojo** (24.x - 25.x+) | **SIMD Vectorization, Ownership, Memory Safety, GoF 23, AI Acceleration** |
| **[`DPX-Julia`](https://github.com/bivex/DPX-Julia)** | **Julia** (1.6 - 1.11+) | **Multiple Dispatch, Holy Traits, Metaprogramming, Tasks, GoF 23** |
| **[`DPX-Kotlin`](https://github.com/bivex/DPX-Kotlin)** | **Kotlin** (1.8 - 2.0+) | **Coroutines, Flow, Jetpack Compose, Multiplatform, GoF 23** |
| **[`DPX-Swift`](https://github.com/bivex/DPX-Swift)** | **Swift** (5.5 - 6.0+) | **Protocol-Oriented, Actor Concurrency, SwiftUI, ARC Safety** |
| **[`DPX-CSharp`](https://github.com/bivex/DPX-CSharp)** | **C#** (10 - 13 / .NET 8-9) | **Clean Architecture, CQRS MediatR, Channel Pipelines** |
| **[`DPX-TypeScript`](https://github.com/bivex/DPX-TypeScript)** | **TypeScript / JavaScript** | **Hexagonal DI, Decorator Meta, Reactive Streams, React/NestJS** |
| **[`DPX-Rust`](https://github.com/bivex/DPX-Rust)** | **Rust** (Edition 2021/2024) | **Zero-Cost Abstractions, RAII Lifetimes, Typestate Pattern** |
| **[`DPX-Go`](https://github.com/bivex/DPX-Go)** | **Go** (1.18 - 1.24+) | **Goroutine Channels, CSP Concurrency, Pipeline Streaming** |
| **[`DPX-Py`](https://github.com/bivex/DPX-Py)** | **Python** (3.8 - 3.13+) | **Multi-Paradigm Hexagonal, Data Flow Engine, AsyncIO** |
| **[`DPX-Php`](https://github.com/bivex/DPX-Php)** | **PHP** (8.1 - 8.4+) | **Attribute-driven DDD, Fiber Concurrency, Laravel/Symfony** |
| **[`DPX-Haskell`](https://github.com/bivex/DPX-Haskell)** | **Haskell** (GHC 9.2 - 9.12+) | **Category Theory, Monad Transformers, Free Monads, Optics** |
| **[`DPX-OCaml`](https://github.com/bivex/DPX-OCaml)** | **OCaml** (4.14 - 5.3+ Multicore) | **Functor Modules, Effect Handlers, GADTs, Railway Monads** |
| **[`DPX-Elixir`](https://github.com/bivex/DPX-Elixir)** | **Elixir** (OTP 25 - 27+) | **GenServer, DynamicSupervisor, Actor Fault Tolerance** |
| **[`DPX-Erlang`](https://github.com/bivex/DPX-Erlang)** | **Erlang/OTP** (24 - 27+) | **OTP Behaviors, Supervision Trees, Message Passing** |
| **[`DPX-C`](https://github.com/bivex/DPX-C)** | **C** (C99 - C23) | **Opaque Structs, VTables, MISRA/CERT Safety, Arena Allocators** |
| **[`DPX-Cpp`](https://github.com/bivex/DPX-Cpp)** | **C++** (C++14 - C++20) | **CRTP, Policy-Based Design, RAII Memory Safety, ANTLR4 AST** |
| **[`DPX-Java`](https://github.com/bivex/DPX-Java)** | **Java** (17 - 23+) | **Virtual Threads, Spring Boot / Jakarta EE, GoF Patterns** |
| **[`DPX`](https://github.com/bivex/DPX)** | **Clojure** / Meta Engine | **Pure Functional, Multimethods, Homoiconic Macro Architecture** |
---

## 📄 License

MIT License © 2026 Bivex Team
