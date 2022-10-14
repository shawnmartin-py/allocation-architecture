Four key design patterns:
- **Repository pattern** - an abstraction over the idea of persistent storage
- **Service Layer patterm** - to clearly define where our use cases begin and end
- **Unit of Work pattern** - to provide atomic operations
- **Aggregate pattern** - to enforce the integrity of our data

Event-Driven Architecture
- **Domain Events** - trigger workflows that cross consistency boundaries
- **Message Bus** - provide a unified way of invoking use cases from any endpoint
- **CQRS** - separating reads and writes avoids awkward compromises in an
event-driven architecture and enables performance and scalability improvements