
# Webhook Delivery & Event Processing Platform

A backend platform for registering webhook endpoints, ingesting events,
tracking deliveries, and handling retries reliably.

## Tech Stack

- Python 3.14
- FastAPI
- Uvicorn
- Pytest
- PostgreSQL, RabbitMQ, and Celery (planned)

## Current Features

- FastAPI application setup
- Health endpoint: `GET /health/live`
- Interactive API documentation at `/docs`

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project and development dependencies:

```powershell
python -m pip install -e ".[dev]"
```

Run the application:

```powershell
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the API.

## Project Status

Day 1: Initial setup and health endpoint completed.
