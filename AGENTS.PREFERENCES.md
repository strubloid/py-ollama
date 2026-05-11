# Agent Preferences

Guidance for writing code that is maintainable, scalable, and easy to understand.

---

## Project Structure

### General Guidelines

- Separate concerns: UI, business logic, data access, configuration
- Keep related files together (co-location principle)
- Feature-based structure preferred over type-based for large projects
- Avoid deep nesting (max 3 levels, use flat structures or clear boundaries)
- Use clear, descriptive directory names

### Layer Separation

```
src/
├── features/          # Feature-based modules
│   ├── auth/
│   │   ├── auth.py          # Core logic
│   │   ├── auth_api.py      # API layer
│   │   └── auth_test.py     # Tests co-located
├── shared/            # Cross-cutting concerns
│   ├── database.py
│   ├── logging.py
│   └── exceptions.py
└── config.py
```

---

## SOLID Principles

### S - Single Responsibility Principle

A module should have one reason to change.

- One class, one responsibility
- Functions do one thing well
- When describing a class and you use "and", split it

### O - Open/Closed Principle

Open for extension, closed for modification.

- Add new behavior by adding new code, not changing existing
- Use inheritance, composition, polymorphism
- Strategy pattern for interchangeable behaviors

### L - Liskov Substitution Principle

Subtypes must be substitutable for their base types.

- Child classes must honor contracts of parent classes
- Don't weaken preconditions, don't strengthen postconditions
- If `is-a` doesn't hold, prefer composition over inheritance

### I - Interface Segregation Principle

Prefer small, focused interfaces over large ones.

- Clients shouldn't depend on methods they don't use
- Single-method interfaces are fine (e.g., `Callable`, `Iterable`)
- Role-based interfaces (e.g., `Reader`, `Writer`)

### D - Dependency Inversion Principle

Depend on abstractions, not concretions.

- High-level modules shouldn't depend on low-level modules
- Use interfaces to decouple
- Inject dependencies (constructor injection preferred)

---

## Design Patterns

### Creational Patterns

**Factory Pattern**
Use when: Object creation involves complex logic or different types need to be created based on conditions.

```python
class ParserFactory:
    def create_parser(self, format: str) -> Parser:
        parsers = {
            "json": JSONParser,
            "xml": XMLParser,
            "csv": CSVParser,
        }
        parser_class = parsers.get(format)
        if not parser_class:
            raise ValueError(f"Unknown format: {format}")
        return parser_class()
```

**Builder Pattern**
Use when: Object construction requires many steps or optional parameters.

```python
@dataclass
class QueryBuilder:
    table: str = ""
    conditions: list = field(default_factory=list)
    limit_value: int | None = None

    def select(self, *columns) -> "QueryBuilder":
        return replace(self, columns=columns)

    def where(self, condition) -> "QueryBuilder":
        return replace(self, conditions=[*self.conditions, condition])
```

**Singleton / Dependency Injection**
Prefer DI over Singleton. Use DI container or factory when multiple implementations needed.

```python
# Instead of Singleton
class DatabaseConnection:
    pass

# Use constructor injection
class UserService:
    def __init__(self, db: DatabaseConnection):
        self._db = db
```

### Structural Patterns

**Adapter Pattern**
Use when: Need to make incompatible interfaces work together.

```python
class ExternalServiceAdapter:
    def __init__(self, external_client):
        self._client = external_client

    def get_items(self) -> list[Item]:
        raw = self._client.fetch_data()
        return [Item(id=r["id"], name=r["name"]) for r in raw]
```

**Facade Pattern**
Use when: Complex subsystem needs simplified interface.

```python
class OrderFacade:
    def __init__(self, inventory, payment, shipping):
        self._inventory = inventory
        self._payment = payment
        self._shipping = shipping

    def place_order(self, items, payment_info):
        self._inventory.reserve(items)
        self._payment.charge(payment_info)
        self._shipping.ship(items)
```

**Composition over Inheritance**
Use when: Need shared behavior between unrelated classes.

```python
class Logger:
    def log(self, message):
        print(f"LOG: {message}")

class TimestampLogger(Logger):
    def log(self, message):
        print(f"{datetime.now()}: {message}")

# Use mixins or composition
class WithLogging:
    def __init__(self):
        self._logger = Logger()
```

### Behavioral Patterns

**Strategy Pattern**
Use when: Multiple algorithms for a task and need to swap at runtime.

```python
class SortStrategy:
    def sort(self, data: list) -> list: ...

class QuickSort(SortStrategy): ...
class MergeSort(SortStrategy): ...

class DataProcessor:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy
```

**Observer Pattern**
Use when: One object needs to notify multiple others of state changes.

```python
class EventBus:
    def __init__(self):
        self._subscribers: dict[str, list[Callable]] = {}

    def subscribe(self, event: str, handler: Callable):
        self._subscribers.setdefault(event, []).append(handler)

    def emit(self, event: str, data):
        for handler in self._subscribers.get(event, []):
            handler(data)
```

**Template Method**
Use when: Algorithm with customizable steps.

```python
class DataPipeline:
    def process(self, data):
        data = self.fetch(data)
        data = self.transform(data)
        data = self.validate(data)
        return self.save(data)

    def fetch(self, data): return data
    def transform(self, data): return data
    def validate(self, data): return data
    def save(self, data): return data
```

**Command Pattern**
Use when: Encapsulate operations as objects, support undo/redo, queue operations.

```python
@dataclass
class Command:
    def execute(self): ...

@dataclass
class CreateOrderCommand(Command):
    order_service: OrderService

    def execute(self):
        self.order_service.create(self.order)
```

---

## Code Organization

### General Rules

- Flat is better than nested
- Colocation: tests near source, config near usage
- Explicit over implicit (explicit imports, explicit types)
- Orthogonal code: one change should affect minimal places

### Functions

- Small: prefer < 20 lines
- Do one thing
- Prefer pure functions (same input → same output, no side effects)
- Return early, avoid flag arguments
- Use keyword arguments for clarity

### Classes

- Keep small: < 200 lines
- Single responsibility
- Use dataclasses for data containers
- Use `@property` for computed attributes
- Private by default (prefix `_`), no pseudoprivate (`__`)

### Modules

- Clear public API (`__all__`)
- Group imports: stdlib, third-party, local
- One module = one concept

### Naming

| Thing          | Convention         | Example           |
| -------------- | ------------------ | ----------------- |
| Files          | snake_case         | `user_service.py` |
| Classes        | PascalCase         | `UserService`     |
| Functions      | snake_case         | `get_user_by_id`  |
| Constants      | SCREAMING_SNAKE    | `MAX_RETRIES`     |
| Private        | leading underscore | `_internal`       |
| Type variables | PascalCase         | `T`, `Result`     |

---

## Error Handling

- Fail fast: validate inputs at boundaries
- Use specific exception types
- Include context in exceptions (message, values)
- Never swallow exceptions silently
- Use result types for expected failures (prevents exceptions for control flow)

```python
@dataclass
class Result[T]:
    value: T | None = None
    error: Error | None = None

    def is_ok(self) -> bool: ...
    def is_err(self) -> bool: ...
```

---

## Async / Concurrency

- Don't mix sync and async
- Use `asyncio` for I/O-bound tasks, `threading` for CPU-bound
- Keep critical sections small
- Use `concurrent.futures` for simple parallelism
- Prefer `async with` for resource management
- Avoid shared mutable state across async tasks

---

## Configuration

- Environment variables for deployment settings
- Config files (YAML, JSON, TOML) for development
- Secrets never in code, never in version control
- Use pydantic/dataclasses for typed config validation

---

## Testing

- Unit tests: one assertion per test concept
- Arrange-Act-Assert pattern
- Mock external dependencies
- Test behavior, not implementation
- Co-locate tests with source
- Use fixtures for shared setup

### Docstring Placement

Docstrings go **directly above** the function/class definition, with no blank lines:

```python
# Correct
"""Description of what this does."""
def my_function():
    pass


# Incorrect (extra blank lines)
def my_function():

    """Description of what this does."""

    pass

# Also incorrect (docstring below def + blank line after)
def my_function():
    """Description."""

    pass
```

This applies to test functions as well.

---

## Refactoring Checklist

When modifying code:

- [ ] Single responsibility maintained or improved?
- [ ] Dependencies injected (not hardcoded)?
- [ ] Can I understand the change without reading unrelated code?
- [ ] Is the change testable in isolation?
- [ ] Is the new code consistent with existing patterns?
- [ ] Can I delete the old code now?
