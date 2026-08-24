# 🐹 DPX-Go: Software Design Pattern & Architecture Report

- **Target Path:** `/Volumes/External/Code/DPX-Go/examples/go_samples`
- **Files Scanned:** `7`
- **Total Patterns & Findings:** `27`
- **Analysis Elapsed Time:** `0.002s`

## 📊 Breakdown by Category

| Category | Count |
|---|:---:|
| **CREATIONAL** | 7 |
| **STRUCTURAL** | 1 |
| **BEHAVIORAL** | 3 |
| **CONCURRENCY** | 5 |
| **IDIOM** | 6 |
| **PRINCIPLE** | 3 |
| **SAFETY** | 2 |

## 📋 Detailed Pattern Findings

### #1 FUNCTIONAL_OPTIONS on `Option`
- **Category:** `creational`
- **Confidence:** **89%** [VERY_HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/options_server.go:15:1`
- **Summary:** Type 'Option' (func(*Server)) defines idiomatic Go Functional Option signature for clean struct configuration

#### Evidence Trail:
- `+60%` **[FUNCTIONAL_OPTION_TYPE_DEF]** Type 'Option' (func(*Server)) defines idiomatic Go Functional Option signature for clean struct configuration -> `/Volumes/External/Code/DPX-Go/examples/go_samples/options_server.go:15:1`
- `+50%` **[FUNCTIONAL_OPTION_WITH_FUNCS]** Provides 3 option generator function(s) (WithPort, WithTimeout, WithTLS) -> `/Volumes/External/Code/DPX-Go/examples/go_samples/options_server.go:17:1`
- `+45%` **[FUNCTIONAL_OPTION_CONSTRUCTOR]** Constructor 'NewServer' accepts variadic functional options (opts ...Option) -> `/Volumes/External/Code/DPX-Go/examples/go_samples/options_server.go:35:1`

### #2 BUILDER on `QueryBuilder`
- **Category:** `creational`
- **Confidence:** **81%** [HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/builder_query.go:10:1`
- **Summary:** Struct 'QueryBuilder' follows Builder naming convention

#### Evidence Trail:
- `+40%` **[BUILDER_NAMING]** Struct 'QueryBuilder' follows Builder naming convention -> `/Volumes/External/Code/DPX-Go/examples/go_samples/builder_query.go:10:1`
- `+45%` **[BUILDER_TERMINAL_METHOD]** Provides terminal construction method 'Build()' returning built instance -> `/Volumes/External/Code/DPX-Go/examples/go_samples/builder_query.go:35:1`
- `+45%` **[BUILDER_FLUENT_SETTERS]** Contains 3 fluent chaining configuration method(s) returning *QueryBuilder (Select, Where, Limit) -> `/Volumes/External/Code/DPX-Go/examples/go_samples/builder_query.go:20:1`

### #3 FACTORY_METHOD on `NewServer`
- **Category:** `creational`
- **Confidence:** **75%** [HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/options_server.go:35:1`
- **Summary:** Factory constructor function 'NewServer()' encapsulates instantiation of '*Server'

#### Evidence Trail:
- `+65%` **[FACTORY_METHOD_CONSTRUCTOR]** Factory constructor function 'NewServer()' encapsulates instantiation of '*Server' -> `/Volumes/External/Code/DPX-Go/examples/go_samples/options_server.go:35:1`
- `+30%` **[FACTORY_METHOD_PARAMETERIZED]** Encapsulates parameterized construction across 2 input parameter(s) -> `/Volumes/External/Code/DPX-Go/examples/go_samples/options_server.go:35:1`

### #4 FACTORY_METHOD on `NewEventHub`
- **Category:** `creational`
- **Confidence:** **65%** [MEDIUM]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/observer_hub.go:12:1`
- **Summary:** Factory constructor function 'NewEventHub()' encapsulates instantiation of '*EventHub'

#### Evidence Trail:
- `+65%` **[FACTORY_METHOD_CONSTRUCTOR]** Factory constructor function 'NewEventHub()' encapsulates instantiation of '*EventHub' -> `/Volumes/External/Code/DPX-Go/examples/go_samples/observer_hub.go:12:1`

### #5 FACTORY_METHOD on `NewQueryBuilder`
- **Category:** `creational`
- **Confidence:** **75%** [HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/builder_query.go:14:1`
- **Summary:** Factory constructor function 'NewQueryBuilder()' encapsulates instantiation of '*QueryBuilder'

#### Evidence Trail:
- `+65%` **[FACTORY_METHOD_CONSTRUCTOR]** Factory constructor function 'NewQueryBuilder()' encapsulates instantiation of '*QueryBuilder' -> `/Volumes/External/Code/DPX-Go/examples/go_samples/builder_query.go:14:1`
- `+30%` **[FACTORY_METHOD_PARAMETERIZED]** Encapsulates parameterized construction across 1 input parameter(s) -> `/Volumes/External/Code/DPX-Go/examples/go_samples/builder_query.go:14:1`

### #6 ABSTRACT_FACTORY on `MegaMonolithicRepository`
- **Category:** `creational`
- **Confidence:** **55%** [MEDIUM]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/principles_and_smells.go:9:1`
- **Summary:** Declares family of 2 product creation method(s) (CreateUser, CreateOrder)

#### Evidence Trail:
- `+55%` **[ABSTRACT_FACTORY_METHODS]** Declares family of 2 product creation method(s) (CreateUser, CreateOrder) -> `/Volumes/External/Code/DPX-Go/examples/go_samples/principles_and_smells.go:9:1`

### #7 SINGLETON on `GetDatabaseInstance`
- **Category:** `creational`
- **Confidence:** **85%** [VERY_HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/singleton_db.go:16:1`
- **Summary:** Thread-safe Singleton accessor 'GetDatabaseInstance()' lazily initializes global instance via sync.Once (once.Do)

#### Evidence Trail:
- `+85%` **[SINGLETON_SYNC_ONCE]** Thread-safe Singleton accessor 'GetDatabaseInstance()' lazily initializes global instance via sync.Once (once.Do) -> `/Volumes/External/Code/DPX-Go/examples/go_samples/singleton_db.go:16:1`

### #8 DECORATOR on `LoggingHandlerDecorator`
- **Category:** `structural`
- **Confidence:** **67%** [MEDIUM]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/middleware_chain.go:18:1`
- **Summary:** Struct 'LoggingHandlerDecorator' follows Decorator / Middleware naming convention

#### Evidence Trail:
- `+35%` **[DECORATOR_NAMING]** Struct 'LoggingHandlerDecorator' follows Decorator / Middleware naming convention -> `/Volumes/External/Code/DPX-Go/examples/go_samples/middleware_chain.go:18:1`
- `+50%` **[DECORATOR_WRAPS_COMPONENT]** Wraps inner component 'next: http.Handler' to decorate behavior -> `/Volumes/External/Code/DPX-Go/examples/go_samples/middleware_chain.go:18:1`

### #9 OBSERVER on `EventHub`
- **Category:** `behavioral`
- **Confidence:** **85%** [VERY_HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/observer_hub.go:8:1`
- **Summary:** Struct 'EventHub' follows Observer / Event Bus naming convention

#### Evidence Trail:
- `+35%` **[OBSERVER_NAMING]** Struct 'EventHub' follows Observer / Event Bus naming convention -> `/Volumes/External/Code/DPX-Go/examples/go_samples/observer_hub.go:8:1`
- `+60%` **[OBSERVER_LISTENER_CHANNELS]** Maintains multi-subscriber dispatch channels/listeners 'listeners: map[string][]chan Event' -> `/Volumes/External/Code/DPX-Go/examples/go_samples/observer_hub.go:8:1`
- `+45%` **[OBSERVER_DISPATCH_METHODS]** Provides observer subscription/broadcast method(s) (Subscribe, Publish) -> `/Volumes/External/Code/DPX-Go/examples/go_samples/observer_hub.go:18:1`

### #10 CHAIN_OF_RESPONSIBILITY on `Middleware`
- **Category:** `behavioral`
- **Confidence:** **75%** [HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/middleware_chain.go:8:1`
- **Summary:** Type 'Middleware' (func(http.Handler) http.Handler) implements Chain of Responsibility middleware pipeline wrapper

#### Evidence Trail:
- `+75%` **[CHAIN_OF_RESPONSIBILITY_MIDDLEWARE_TYPE]** Type 'Middleware' (func(http.Handler) http.Handler) implements Chain of Responsibility middleware pipeline wrapper -> `/Volumes/External/Code/DPX-Go/examples/go_samples/middleware_chain.go:8:1`

### #11 MEDIATOR on `EventHub`
- **Category:** `behavioral`
- **Confidence:** **55%** [MEDIUM]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/observer_hub.go:8:1`
- **Summary:** Maintains decoupled participant registry 'listeners: map[string][]chan Event'

#### Evidence Trail:
- `+55%` **[MEDIATOR_PARTICIPANTS_MAP]** Maintains decoupled participant registry 'listeners: map[string][]chan Event' -> `/Volumes/External/Code/DPX-Go/examples/go_samples/observer_hub.go:8:1`

### #12 PIPELINE on `Squarer`
- **Category:** `concurrency`
- **Confidence:** **85%** [VERY_HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/concurrency_pipeline.go:23:1`
- **Summary:** Function 'Squarer' implements idiomatic Go Pipeline stage streaming data from input channel into output channel

#### Evidence Trail:
- `+85%` **[PIPELINE_CHANNEL_STAGE]** Function 'Squarer' implements idiomatic Go Pipeline stage streaming data from input channel into output channel -> `/Volumes/External/Code/DPX-Go/examples/go_samples/concurrency_pipeline.go:23:1`

### #13 PIPELINE on `MergeFanIn`
- **Category:** `concurrency`
- **Confidence:** **85%** [VERY_HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/concurrency_pipeline.go:38:1`
- **Summary:** Function 'MergeFanIn' implements idiomatic Go Pipeline stage streaming data from input channel into output channel

#### Evidence Trail:
- `+85%` **[PIPELINE_CHANNEL_STAGE]** Function 'MergeFanIn' implements idiomatic Go Pipeline stage streaming data from input channel into output channel -> `/Volumes/External/Code/DPX-Go/examples/go_samples/concurrency_pipeline.go:38:1`

### #14 FAN_OUT_FAN_IN on `MergeFanIn`
- **Category:** `concurrency`
- **Confidence:** **85%** [VERY_HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/concurrency_pipeline.go:38:1`
- **Summary:** Function 'MergeFanIn' implements Fan-In channel multiplexer using sync.WaitGroup to merge multiple concurrent streams into single output channel

#### Evidence Trail:
- `+85%` **[FAN_IN_CHANNEL_MERGE]** Function 'MergeFanIn' implements Fan-In channel multiplexer using sync.WaitGroup to merge multiple concurrent streams into single output channel -> `/Volumes/External/Code/DPX-Go/examples/go_samples/concurrency_pipeline.go:38:1`

### #15 WORKER_POOL on `StartWorkerPool`
- **Category:** `concurrency`
- **Confidence:** **80%** [HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/concurrency_pipeline.go:66:1`
- **Summary:** Function 'StartWorkerPool' implements Worker Pool pattern by spawning a fixed pool of worker goroutines over a shared jobs channel

#### Evidence Trail:
- `+80%` **[WORKER_POOL_SPAWNER]** Function 'StartWorkerPool' implements Worker Pool pattern by spawning a fixed pool of worker goroutines over a shared jobs channel -> `/Volumes/External/Code/DPX-Go/examples/go_samples/concurrency_pipeline.go:66:1`

### #16 GENERATOR on `Generator`
- **Category:** `concurrency`
- **Confidence:** **80%** [HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/concurrency_pipeline.go:8:1`
- **Summary:** Function 'Generator' implements idiomatic Go Generator pattern spawning a producer goroutine and returning receive-only channel '<-chan int'

#### Evidence Trail:
- `+80%` **[GENERATOR_PRODUCER_GOROUTINE]** Function 'Generator' implements idiomatic Go Generator pattern spawning a producer goroutine and returning receive-only channel '<-chan int' -> `/Volumes/External/Code/DPX-Go/examples/go_samples/concurrency_pipeline.go:8:1`

### #17 CONTEXT_PROPAGATION on `Generator`
- **Category:** `idiom`
- **Confidence:** **70%** [HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/concurrency_pipeline.go:8:1`
- **Summary:** Function 'Generator' adheres to idiomatic Go context propagation passing 'ctx: context.Context' as first parameter

#### Evidence Trail:
- `+70%` **[CONTEXT_FIRST_PARAM]** Function 'Generator' adheres to idiomatic Go context propagation passing 'ctx: context.Context' as first parameter -> `/Volumes/External/Code/DPX-Go/examples/go_samples/concurrency_pipeline.go:8:1`

### #18 CONTEXT_PROPAGATION on `Squarer`
- **Category:** `idiom`
- **Confidence:** **70%** [HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/concurrency_pipeline.go:23:1`
- **Summary:** Function 'Squarer' adheres to idiomatic Go context propagation passing 'ctx: context.Context' as first parameter

#### Evidence Trail:
- `+70%` **[CONTEXT_FIRST_PARAM]** Function 'Squarer' adheres to idiomatic Go context propagation passing 'ctx: context.Context' as first parameter -> `/Volumes/External/Code/DPX-Go/examples/go_samples/concurrency_pipeline.go:23:1`

### #19 CONTEXT_PROPAGATION on `MergeFanIn`
- **Category:** `idiom`
- **Confidence:** **70%** [HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/concurrency_pipeline.go:38:1`
- **Summary:** Function 'MergeFanIn' adheres to idiomatic Go context propagation passing 'ctx: context.Context' as first parameter

#### Evidence Trail:
- `+70%` **[CONTEXT_FIRST_PARAM]** Function 'MergeFanIn' adheres to idiomatic Go context propagation passing 'ctx: context.Context' as first parameter -> `/Volumes/External/Code/DPX-Go/examples/go_samples/concurrency_pipeline.go:38:1`

### #20 CONTEXT_PROPAGATION on `StartWorkerPool`
- **Category:** `idiom`
- **Confidence:** **70%** [HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/concurrency_pipeline.go:66:1`
- **Summary:** Function 'StartWorkerPool' adheres to idiomatic Go context propagation passing 'ctx: context.Context' as first parameter

#### Evidence Trail:
- `+70%` **[CONTEXT_FIRST_PARAM]** Function 'StartWorkerPool' adheres to idiomatic Go context propagation passing 'ctx: context.Context' as first parameter -> `/Volumes/External/Code/DPX-Go/examples/go_samples/concurrency_pipeline.go:66:1`

### #21 CONTEXT_PROPAGATION on `Start`
- **Category:** `idiom`
- **Confidence:** **70%** [HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/options_server.go:47:1`
- **Summary:** Function 'Start' adheres to idiomatic Go context propagation passing 'ctx: context.Context' as first parameter

#### Evidence Trail:
- `+70%` **[CONTEXT_FIRST_PARAM]** Function 'Start' adheres to idiomatic Go context propagation passing 'ctx: context.Context' as first parameter -> `/Volumes/External/Code/DPX-Go/examples/go_samples/options_server.go:47:1`

### #22 CONTEXT_PROPAGATION on `ProcessDataStream`
- **Category:** `idiom`
- **Confidence:** **70%** [HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/principles_and_smells.go:57:1`
- **Summary:** Function 'ProcessDataStream' adheres to idiomatic Go context propagation passing 'ctx: context.Context' as first parameter

#### Evidence Trail:
- `+70%` **[CONTEXT_FIRST_PARAM]** Function 'ProcessDataStream' adheres to idiomatic Go context propagation passing 'ctx: context.Context' as first parameter -> `/Volumes/External/Code/DPX-Go/examples/go_samples/principles_and_smells.go:57:1`

### #23 SINGLE_RESPONSIBILITY on `GodManager`
- **Category:** `principle`
- **Confidence:** **85%** [VERY_HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/principles_and_smells.go:23:1`
- **Summary:** SRP Violation (God Struct): Struct 'GodManager' has 16 methods and 13 fields, indicating mixed domain responsibilities

#### Evidence Trail:
- `+85%` **[SRP_GOD_STRUCT]** SRP Violation (God Struct): Struct 'GodManager' has 16 methods and 13 fields, indicating mixed domain responsibilities -> `/Volumes/External/Code/DPX-Go/examples/go_samples/principles_and_smells.go:23:1`

### #24 INTERFACE_POLLUTION on `MegaMonolithicRepository`
- **Category:** `principle`
- **Confidence:** **80%** [HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/principles_and_smells.go:9:1`
- **Summary:** Interface Pollution (ISP Violation): Interface 'MegaMonolithicRepository' declares 10 methods; idiomatic Go encourages small, single-purpose interfaces (1-2 methods)

#### Evidence Trail:
- `+80%` **[INTERFACE_POLLUTION_FAT_INTERFACE]** Interface Pollution (ISP Violation): Interface 'MegaMonolithicRepository' declares 10 methods; idiomatic Go encourages small, single-purpose interfaces (1-2 methods) -> `/Volumes/External/Code/DPX-Go/examples/go_samples/principles_and_smells.go:9:1`

### #25 DEPENDENCY_INVERSION on `ProcessDataStream`
- **Category:** `principle`
- **Confidence:** **75%** [HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/principles_and_smells.go:57:1`
- **Summary:** DIP Adherence: Function 'ProcessDataStream' depends on interface abstraction(s) (ctx context.Context, r io.Reader) rather than concrete struct pointers

#### Evidence Trail:
- `+75%` **[DIP_INTERFACE_PARAMETER]** DIP Adherence: Function 'ProcessDataStream' depends on interface abstraction(s) (ctx context.Context, r io.Reader) rather than concrete struct pointers -> `/Volumes/External/Code/DPX-Go/examples/go_samples/principles_and_smells.go:57:1`

### #26 GOROUTINE_LEAK_RISK on `LeakyBackgroundWorker`
- **Category:** `safety`
- **Confidence:** **80%** [HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/principles_and_smells.go:62:1`
- **Summary:** Safety Audit (Goroutine Leak Risk): Function 'LeakyBackgroundWorker' spawns an infinite goroutine loop without listening for 'ctx.Done()' cancellation or a quit channel

#### Evidence Trail:
- `+80%` **[GOROUTINE_LEAK_RISK]** Safety Audit (Goroutine Leak Risk): Function 'LeakyBackgroundWorker' spawns an infinite goroutine loop without listening for 'ctx.Done()' cancellation or a quit channel -> `/Volumes/External/Code/DPX-Go/examples/go_samples/principles_and_smells.go:62:1`

### #27 UNCHECKED_ERROR on `BadErrorHandler`
- **Category:** `safety`
- **Confidence:** **75%** [HIGH]
- **Primary Location:** `/Volumes/External/Code/DPX-Go/examples/go_samples/principles_and_smells.go:71:1`
- **Summary:** Safety Audit (Unchecked Error): Function 'BadErrorHandler' explicitly ignores returned error(s) (_ = w.Close(...); always check err != nil

#### Evidence Trail:
- `+75%` **[UNCHECKED_ERROR_RETURN]** Safety Audit (Unchecked Error): Function 'BadErrorHandler' explicitly ignores returned error(s) (_ = w.Close(...); always check err != nil -> `/Volumes/External/Code/DPX-Go/examples/go_samples/principles_and_smells.go:71:1`
