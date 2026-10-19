# Webhook Delivery & Event Processing Platform

A backend platform designed to receive application events, manage webhook endpoints, and deliver events reliably to registered destinations. The project focuses on reliable event processing, failure recovery, security, and production-oriented backend engineering.

## Overview

Modern applications often need to notify external services when an event occurs, such as an order being created, a payment being processed, or a user account being updated.

This platform is designed to provide a centralized webhook delivery system that accepts events, matches them with registered endpoints, processes deliveries, tracks delivery attempts, and supports recovery from temporary failures.

The project is being developed incrementally, with an emphasis on clean architecture, testability, reliability, and security.

## Key Features

### Implemented

- FastAPI application foundation
- Health-check endpoint: `GET /health/live`
- Interactive API documentation through Swagger UI
- Python virtual environment and dependency management
- Git-based version control

### Planned Capabilities

- Webhook endpoint registration and event subscriptions
- Event ingestion and persistent event storage
- Delivery status tracking and attempt history
- Asynchronous processing with RabbitMQ and Celery
- Retry scheduling with exponential backoff and jitter
- Idempotency and duplicate-event protection
- HMAC-based webhook signatures
- Authentication and owner-level authorization
- Webhook destination validation and SSRF protection
- Automated unit, API, and integration tests
- Structured logging, metrics, and health monitoring
- Docker-based local development
- Continuous integration with GitHub Actions

Planned capabilities will be documented as implemented only after they have been developed and tested.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | REST API development |
| Pydantic | Request validation and data schemas |
| Uvicorn | ASGI application server |
| PostgreSQL | Persistent data storage |
| SQLAlchemy | Database ORM |
| Alembic | Database migrations |
| HTTPX | Outbound HTTP requests |
| RabbitMQ | Message broker |
| Celery | Background task processing |
| Pytest | Automated testing |
| Ruff | Linting and code quality |
| Docker Compose | Local multi-service environment |
| GitHub Actions | Continuous integration |

Some technologies listed above are planned integrations and may not yet be configured in the application.

## Architecture

The intended architecture follows a modular monolith approach with a separate background worker.

```text
Source Application
        |
        v
    FastAPI API
        |
        v
   Event Storage
   (PostgreSQL)
        |
        v
 Message Broker
   (RabbitMQ)
        |
        v
 Background Worker
      (Celery)
        |
        v
 Registered Webhook Endpoint
        |
        v
 Delivery Status & Attempt History
```

The intended processing flow is:

1. A source application submits an event.
2. The platform validates and persists the event.
3. Matching webhook endpoints are identified.
4. Delivery work is scheduled for background processing.
5. The worker sends an HTTP request with event metadata and a signature.
6. The platform records the delivery outcome and attempt history.
7. Temporary failures are retried according to a bounded retry policy.

This architecture describes the target design; individual components will become operational as they are implemented.

## Project Structure

```text
webhook-delivery-platform/
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── __init__.py
├── docs/
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

The structure will expand as API routes, database models, services, integrations, workers, and tests are introduced.

## Getting Started

### Prerequisites

- Python 3.14 or a compatible Python version
- Git
- Visual Studio Code or another Python editor
- Internet access for installing dependencies

### 1. Clone the Repository

```bash
git clone <repository-url>
cd webhook-delivery-platform
```

Replace `<repository-url>` with the actual GitHub repository URL.

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -e ".[dev]"
```

### 4. Run the Application

```bash
python -m uvicorn app.main:app --reload
```

### 5. Access the API

Once the server is running locally:

- API documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health/live

The health endpoint currently returns:

```json
{
  "status": "alive"
}
```

## Testing

The project uses Pytest for automated testing.

Run the test suite with:

```bash
python -m pytest
```

Lint the project with:

```bash
python -m ruff check .
```

As additional features are implemented, tests will cover API validation, database operations, delivery outcomes, retries, idempotency, security controls, and failure scenarios.

## Reliability and Delivery Semantics

The intended delivery model is **at-least-once delivery**, not exactly-once delivery.

Network failures can occur after a receiver processes an event but before the sender receives the response. Consequently, receivers should use stable event identifiers and idempotent processing to avoid repeating business operations.

The target retry system will use bounded attempts, exponential backoff, and appropriate handling of transient HTTP failures.

## Security Considerations

Security is a core design objective. Planned controls include:

- Authentication and authorization for management APIs
- HMAC signatures for verifying webhook authenticity
- Timestamp validation and replay protection
- Destination URL validation and SSRF mitigation
- Request payload limits and rate limiting
- Secure secret handling and log redaction
- Owner-scoped access to events and delivery records

These controls must be implemented and tested before the platform is considered production-ready.

## Development Principles

- Build features incrementally by topic and concept.
- Keep API, business logic, persistence, and integrations separated.
- Test functionality and failure cases as features are developed.
- Use database migrations for schema changes.
- Keep secrets out of source control.
- Prefer explicit error handling and observable delivery states.
- Document architectural decisions and known limitations.

## Roadmap

The project will evolve toward:

- Persistent event and webhook management
- Reliable asynchronous delivery
- Retry and recovery mechanisms
- Security and idempotency controls
- Comprehensive automated testing
- Containerized development and continuous integration
- Deployment and operational monitoring

Progress is organized by features and concepts rather than a fixed day-by-day schedule.

## Contributing

Contributions and suggestions are welcome. Changes should follow the existing project structure, include relevant tests, and document any new configuration or operational requirements.

## License

No license has been selected yet. A license can be added once the project's distribution and reuse terms have been decided.