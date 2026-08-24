"""Pattern metadata, catalog definitions, and architectural descriptions for Go (Golang)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from pattern_detector.domain.value_objects import PatternCategory, PatternType


@dataclass(frozen=True)
class PatternCatalogEntry:
    """Catalog entry describing a design pattern, idiom, or principle in Go."""

    pattern_type: PatternType
    category: PatternCategory
    name: str
    description: str
    idiomatic_example: str


PATTERN_CATALOG: Mapping[PatternType, PatternCatalogEntry] = {
    # Creational
    PatternType.FUNCTIONAL_OPTIONS: PatternCatalogEntry(
        pattern_type=PatternType.FUNCTIONAL_OPTIONS,
        category=PatternCategory.CREATIONAL,
        name="Functional Options Pattern",
        description="Idiomatic Go creational pattern using first-class functions (type Option func(*Config)) to configure structs cleanly with sensible defaults.",
        idiomatic_example="type Option func(*Server)\nfunc WithPort(p int) Option { return func(s *Server) { s.port = p } }\nfunc NewServer(opts ...Option) *Server { ... }",
    ),
    PatternType.BUILDER: PatternCatalogEntry(
        pattern_type=PatternType.BUILDER,
        category=PatternCategory.CREATIONAL,
        name="Builder Pattern",
        description="Separates the construction of a complex struct from its representation through fluent method chaining ending in Build().",
        idiomatic_example="type QueryBuilder struct { ... }\nfunc (b *QueryBuilder) Where(...) *QueryBuilder { ... }\nfunc (b *QueryBuilder) Build() (Query, error) { ... }",
    ),
    PatternType.FACTORY_METHOD: PatternCatalogEntry(
        pattern_type=PatternType.FACTORY_METHOD,
        category=PatternCategory.CREATIONAL,
        name="Factory Method",
        description="Encapsulates struct instantiation within constructor functions (New..., NewFromConfig, Open).",
        idiomatic_example="func NewClient(addr string) (*Client, error) { ... }",
    ),
    PatternType.ABSTRACT_FACTORY: PatternCatalogEntry(
        pattern_type=PatternType.ABSTRACT_FACTORY,
        category=PatternCategory.CREATIONAL,
        name="Abstract Factory",
        description="Defines interfaces with factory methods producing families of related interfaces without specifying concrete structs.",
        idiomatic_example="type DatabaseFactory interface { CreateConnection() Connection; CreateTx() Transaction }",
    ),
    PatternType.SINGLETON: PatternCatalogEntry(
        pattern_type=PatternType.SINGLETON,
        category=PatternCategory.CREATIONAL,
        name="Singleton Pattern",
        description="Ensures a struct has only one global instance safely initialized via sync.Once (once.Do).",
        idiomatic_example="var (instance *Registry; once sync.Once)\nfunc GetRegistry() *Registry { once.Do(func() { instance = &Registry{} }); return instance }",
    ),
    PatternType.PROTOTYPE: PatternCatalogEntry(
        pattern_type=PatternType.PROTOTYPE,
        category=PatternCategory.CREATIONAL,
        name="Prototype Pattern",
        description="Clones existing struct instances via explicit Clone() methods or deep copy mechanisms.",
        idiomatic_example="func (c *Config) Clone() *Config { copy := *c; return &copy }",
    ),

    # Structural
    PatternType.ADAPTER: PatternCatalogEntry(
        pattern_type=PatternType.ADAPTER,
        category=PatternCategory.STRUCTURAL,
        name="Adapter Pattern",
        description="Converts the interface of a struct into another expected interface (e.g. adapting legacy structs to io.Reader or http.Handler).",
        idiomatic_example="type ReaderAdapter struct { src CustomBuffer }\nfunc (a *ReaderAdapter) Read(p []byte) (int, error) { ... }",
    ),
    PatternType.DECORATOR: PatternCatalogEntry(
        pattern_type=PatternType.DECORATOR,
        category=PatternCategory.STRUCTURAL,
        name="Decorator / Middleware Pattern",
        description="Dynamically wraps an interface implementation to add behavior (logging, metrics, authentication) while preserving the same interface.",
        idiomatic_example="type LoggingHandler struct { next http.Handler }\nfunc (h *LoggingHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) { log(); h.next.ServeHTTP(w, r) }",
    ),
    PatternType.FACADE: PatternCatalogEntry(
        pattern_type=PatternType.FACADE,
        category=PatternCategory.STRUCTURAL,
        name="Facade Pattern",
        description="Provides a simplified high-level struct interface over a complex subsystem of packages and clients.",
        idiomatic_example="type EngineFacade struct { decoder Decoder; audio AudioSystem; video VideoSystem }",
    ),
    PatternType.COMPOSITE: PatternCatalogEntry(
        pattern_type=PatternType.COMPOSITE,
        category=PatternCategory.STRUCTURAL,
        name="Composite Pattern",
        description="Composes objects into tree structures to represent part-whole hierarchies (slices of component interfaces []Component).",
        idiomatic_example="type Branch struct { children []Component }\nfunc (b *Branch) Execute() { for _, c := range b.children { c.Execute() } }",
    ),
    PatternType.PROXY: PatternCatalogEntry(
        pattern_type=PatternType.PROXY,
        category=PatternCategory.STRUCTURAL,
        name="Proxy Pattern",
        description="Provides a surrogate placeholder for an interface to control access, lazy load, cache, or perform RPC calls.",
        idiomatic_example="type CachingServiceProxy struct { real Service; cache Cache }",
    ),
    PatternType.BRIDGE: PatternCatalogEntry(
        pattern_type=PatternType.BRIDGE,
        category=PatternCategory.STRUCTURAL,
        name="Bridge Pattern",
        description="Decouples an abstraction struct from its implementation interface so that the two can vary independently.",
        idiomatic_example="type Window struct { backend BackendDriver }",
    ),
    PatternType.FLYWEIGHT: PatternCatalogEntry(
        pattern_type=PatternType.FLYWEIGHT,
        category=PatternCategory.STRUCTURAL,
        name="Flyweight Pattern",
        description="Reuses shared instances efficiently using sync.Pool or string interning caches.",
        idiomatic_example="var bufPool = sync.Pool{New: func() any { return new(bytes.Buffer) }}",
    ),

    # Behavioral
    PatternType.STRATEGY: PatternCatalogEntry(
        pattern_type=PatternType.STRATEGY,
        category=PatternCategory.BEHAVIORAL,
        name="Strategy Pattern",
        description="Defines a family of interchangeable algorithms through interfaces or function types (type SortFunc func(a, b int) bool).",
        idiomatic_example="type CompressionStrategy interface { Compress(data []byte) []byte }",
    ),
    PatternType.OBSERVER: PatternCatalogEntry(
        pattern_type=PatternType.OBSERVER,
        category=PatternCategory.BEHAVIORAL,
        name="Observer / Event Emitter Pattern",
        description="Notifies multiple subscribers of state changes via channel broadcasting (chan Event) or callback slices.",
        idiomatic_example="type EventHub struct { listeners []chan Event }\nfunc (h *EventHub) Publish(e Event) { for _, ch := range h.listeners { ch <- e } }",
    ),
    PatternType.COMMAND: PatternCatalogEntry(
        pattern_type=PatternType.COMMAND,
        category=PatternCategory.BEHAVIORAL,
        name="Command Pattern",
        description="Encapsulates a request as an object (interface with Execute() error or type CommandFunc func() error).",
        idiomatic_example="type Command interface { Execute(ctx context.Context) error; Undo() error }",
    ),
    PatternType.TEMPLATE_METHOD: PatternCatalogEntry(
        pattern_type=PatternType.TEMPLATE_METHOD,
        category=PatternCategory.BEHAVIORAL,
        name="Template Method",
        description="Defines the skeleton of an algorithm in a base struct method, delegating specific steps to embedded interface methods.",
        idiomatic_example="type Pipeline struct { Stepper }\nfunc (p *Pipeline) Run() { p.Extract(); p.Transform(); p.Load() }",
    ),
    PatternType.CHAIN_OF_RESPONSIBILITY: PatternCatalogEntry(
        pattern_type=PatternType.CHAIN_OF_RESPONSIBILITY,
        category=PatternCategory.BEHAVIORAL,
        name="Chain of Responsibility",
        description="Passes requests along a chain of handlers (onion middleware func(http.Handler) http.Handler).",
        idiomatic_example="type Middleware func(http.Handler) http.Handler",
    ),
    PatternType.ITERATOR: PatternCatalogEntry(
        pattern_type=PatternType.ITERATOR,
        category=PatternCategory.BEHAVIORAL,
        name="Iterator Pattern",
        description="Sequential traversal over collections via Iter() func() (T, bool), channels, or Go 1.22+ range-over-func (iter.Seq[V]).",
        idiomatic_example="type Iterator interface { HasNext() bool; Next() Item }",
    ),
    PatternType.MEDIATOR: PatternCatalogEntry(
        pattern_type=PatternType.MEDIATOR,
        category=PatternCategory.BEHAVIORAL,
        name="Mediator Pattern",
        description="Coordinates and orchestrates communication channels between multiple independent goroutines / workers.",
        idiomatic_example="type ChatMediator struct { users map[string]chan Message }",
    ),
    PatternType.MEMENTO: PatternCatalogEntry(
        pattern_type=PatternType.MEMENTO,
        category=PatternCategory.BEHAVIORAL,
        name="Memento Pattern",
        description="Captures and externalizes internal struct state for later restoration (SaveSnapshot() / Restore()).",
        idiomatic_example="func (e *Editor) CreateSnapshot() Snapshot { ... }\nfunc (e *Editor) Restore(s Snapshot) { ... }",
    ),
    PatternType.VISITOR: PatternCatalogEntry(
        pattern_type=PatternType.VISITOR,
        category=PatternCategory.BEHAVIORAL,
        name="Visitor Pattern",
        description="Separates operations from AST elements through a Visitor interface (Walk(v Visitor), Visit(n Node)).",
        idiomatic_example="type Visitor interface { Visit(node Node) Visitor }\nfunc Walk(v Visitor, node Node) { ... }",
    ),
    PatternType.INTERPRETER: PatternCatalogEntry(
        pattern_type=PatternType.INTERPRETER,
        category=PatternCategory.BEHAVIORAL,
        name="Interpreter Pattern",
        description="Evaluates grammar rules and expressions across AST node interfaces (Eval(ctx Context) Value).",
        idiomatic_example="type Expr interface { Eval(env map[string]float64) float64 }",
    ),
    PatternType.STATE: PatternCatalogEntry(
        pattern_type=PatternType.STATE,
        category=PatternCategory.BEHAVIORAL,
        name="State Pattern",
        description="Allows an object to alter behavior when its internal state changes using interface-based state polymorphism.",
        idiomatic_example="type State interface { Handle(c *Context) }",
    ),

    # Go Concurrency & Idioms
    PatternType.PIPELINE: PatternCatalogEntry(
        pattern_type=PatternType.PIPELINE,
        category=PatternCategory.CONCURRENCY,
        name="Pipeline Pattern",
        description="Sequential stages connected by channels where each stage is a group of goroutines running the same function.",
        idiomatic_example="func gen(nums ...int) <-chan int { ... }\nfunc sq(in <-chan int) <-chan int { ... }",
    ),
    PatternType.FAN_OUT_FAN_IN: PatternCatalogEntry(
        pattern_type=PatternType.FAN_OUT_FAN_IN,
        category=PatternCategory.CONCURRENCY,
        name="Fan-Out / Fan-In Pattern",
        description="Spawns multiple worker goroutines to process a channel in parallel (Fan-Out), then merges their results into a single channel (Fan-In).",
        idiomatic_example="func merge(cs ...<-chan int) <-chan int { var wg sync.WaitGroup; ... }",
    ),
    PatternType.WORKER_POOL: PatternCatalogEntry(
        pattern_type=PatternType.WORKER_POOL,
        category=PatternCategory.CONCURRENCY,
        name="Worker Pool Pattern",
        description="Fixed number of goroutines reading from a shared jobs channel to bound resource consumption.",
        idiomatic_example="for w := 1; w <= numWorkers; w++ { go worker(w, jobs, results) }",
    ),
    PatternType.GENERATOR: PatternCatalogEntry(
        pattern_type=PatternType.GENERATOR,
        category=PatternCategory.CONCURRENCY,
        name="Generator Pattern",
        description="Function spawning a producer goroutine and returning a read-only channel (<-chan T).",
        idiomatic_example="func Range(start, end int) <-chan int { out := make(chan int); go func() { ... close(out) }(); return out }",
    ),
    PatternType.CONTEXT_PROPAGATION: PatternCatalogEntry(
        pattern_type=PatternType.CONTEXT_PROPAGATION,
        category=PatternCategory.IDIOM,
        name="Context Propagation",
        description="Idiomatic propagation of context.Context as the first parameter across functions for cancellation and timeouts.",
        idiomatic_example="func DoOperation(ctx context.Context, id string) error { ... }",
    ),
    PatternType.ERRGROUP_CONCURRENCY: PatternCatalogEntry(
        pattern_type=PatternType.ERRGROUP_CONCURRENCY,
        category=PatternCategory.CONCURRENCY,
        name="ErrGroup Concurrency",
        description="Synchronizes multiple goroutines with automatic error handling and cancellation using golang.org/x/sync/errgroup.",
        idiomatic_example="g, ctx := errgroup.WithContext(ctx)\ng.Go(func() error { return task1(ctx) })",
    ),
    PatternType.STRUCT_EMBEDDING: PatternCatalogEntry(
        pattern_type=PatternType.STRUCT_EMBEDDING,
        category=PatternCategory.IDIOM,
        name="Struct Embedding (Composition)",
        description="Idiomatic Go composition over inheritance via anonymous struct embedding.",
        idiomatic_example="type AdminUser struct { User; Role string }",
    ),
    PatternType.CIRCULAR_DEPENDENCY: PatternCatalogEntry(
        pattern_type=PatternType.CIRCULAR_DEPENDENCY,
        category=PatternCategory.IDIOM,
        name="Circular Package Dependency",
        description="Detects cyclic import dependencies between Go packages.",
        idiomatic_example="package a -> import b -> import a",
    ),

    # Principles & Quality
    PatternType.SINGLE_RESPONSIBILITY: PatternCatalogEntry(
        pattern_type=PatternType.SINGLE_RESPONSIBILITY,
        category=PatternCategory.PRINCIPLE,
        name="Single Responsibility (SRP)",
        description="God Struct detection: structs with excessive methods (≥15) or fields (≥12) mixing multiple domains.",
        idiomatic_example="Decompose monolithic structs into cohesive sub-structs.",
    ),
    PatternType.INTERFACE_POLLUTION: PatternCatalogEntry(
        pattern_type=PatternType.INTERFACE_POLLUTION,
        category=PatternCategory.PRINCIPLE,
        name="Interface Pollution (ISP Violation)",
        description="Flags Fat Interfaces (≥8 methods); idiomatic Go favors small, focused 1-2 method interfaces (io.Reader, io.Writer).",
        idiomatic_example="Break large interfaces into small composable interfaces.",
    ),
    PatternType.OPEN_CLOSED: PatternCatalogEntry(
        pattern_type=PatternType.OPEN_CLOSED,
        category=PatternCategory.PRINCIPLE,
        name="Open/Closed Principle (OCP)",
        description="Identifies rigid type switch cascades that should use interface polymorphism.",
        idiomatic_example="Replace type switch cascades with interface method dispatch.",
    ),
    PatternType.LISKOV_SUBSTITUTION: PatternCatalogEntry(
        pattern_type=PatternType.LISKOV_SUBSTITUTION,
        category=PatternCategory.PRINCIPLE,
        name="Liskov Substitution (LSP)",
        description="Detects interface method implementations that panic() or return unimplemented errors unconditionally.",
        idiomatic_example="Avoid panic('unimplemented') in interface methods.",
    ),
    PatternType.DEPENDENCY_INVERSION: PatternCatalogEntry(
        pattern_type=PatternType.DEPENDENCY_INVERSION,
        category=PatternCategory.PRINCIPLE,
        name="Dependency Inversion (DIP)",
        description="Functions accepting interface parameters rather than concrete struct pointers.",
        idiomatic_example="func Process(r io.Reader) instead of func Process(f *os.File)",
    ),
    PatternType.LAW_OF_DEMETER: PatternCatalogEntry(
        pattern_type=PatternType.LAW_OF_DEMETER,
        category=PatternCategory.PRINCIPLE,
        name="Law of Demeter",
        description="Flags deep getter method call chains violating the principle of least knowledge (a.GetB().GetC().GetD()).",
        idiomatic_example="Avoid a.GetB().GetC().GetD(); provide helper methods on intermediate structs.",
    ),
    PatternType.HIGH_COHESION_LOW_COUPLING: PatternCatalogEntry(
        pattern_type=PatternType.HIGH_COHESION_LOW_COUPLING,
        category=PatternCategory.PRINCIPLE,
        name="High Cohesion / Low Coupling",
        description="Flags structs with high fan-out coupling to numerous external package types.",
        idiomatic_example="Minimize dependencies across disparate package boundaries.",
    ),
    PatternType.KISS: PatternCatalogEntry(
        pattern_type=PatternType.KISS,
        category=PatternCategory.PRINCIPLE,
        name="Keep It Simple, Stupid (KISS)",
        description="Flags functions with high cyclomatic complexity (≥10) or long parameter lists (≥5).",
        idiomatic_example="Decompose complex routines into smaller helpers or use Functional Options.",
    ),
    PatternType.DRY: PatternCatalogEntry(
        pattern_type=PatternType.DRY,
        category=PatternCategory.PRINCIPLE,
        name="Don't Repeat Yourself (DRY)",
        description="Identifies duplicate function and method implementations across packages.",
        idiomatic_example="Extract common logic into shared utility packages.",
    ),

    # Safety
    PatternType.GOROUTINE_LEAK_RISK: PatternCatalogEntry(
        pattern_type=PatternType.GOROUTINE_LEAK_RISK,
        category=PatternCategory.SAFETY,
        name="Goroutine Leak Risk",
        description="Flags goroutines running unbounded loops or blocking on unbuffered channels without ctx.Done() or quit channel checks.",
        idiomatic_example="Always listen to ctx.Done() or provide quit channels in long-running goroutines.",
    ),
    PatternType.UNCHECKED_ERROR: PatternCatalogEntry(
        pattern_type=PatternType.UNCHECKED_ERROR,
        category=PatternCategory.SAFETY,
        name="Unchecked Error Risk",
        description="Flags calls ignoring return errors (e.g. _ = fn() on error-returning functions).",
        idiomatic_example="Handle every returned error explicitly: if err != nil { return err }",
    ),
}
