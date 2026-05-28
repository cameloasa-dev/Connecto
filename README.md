# Social App - Connecto

Connecto is a full‑stack social application built with FastAPI, React, and a complete DevSecOps pipeline.
The project emphasizes clean architecture, automated testing, security‑first development, and reproducible workflows through a unified Makefile.

## Prerequisites

To run the project locally, ensure you have:

Python 3.12+

uv (Python package manager)

Node.js 20+

npm 10+

PostgreSQL 15+

Make

Git

## Project Structure

```text
backend/
│
├── app/
│   ├── api/endpoints/         # API routes (auth, circles, posts, users)
│   ├── core/                  # Config, security, DB connection
│   ├── db/                    # SQLAlchemy models & session
│   ├── schemas/               # Pydantic models
│   └── main.py                # FastAPI entrypoint
│
├── tests/
│   ├── unit/                  # Unit tests
│   ├── integration/           # API + DB integration tests
│    
├── pyproject.toml
├── uv.lock
│
frontend/
│
├── src/
│   ├── components/            # Reusable UI components
│   ├── pages/                 # Page‑level views
│   ├── services/              # API communication
│   ├── hooks/                 # Custom hooks
│   ├── context/               # Global state
│   ├── utils/                 # Helpers
│   └── App.jsx
├── tests/
│   ├── unit/                  # Unit tests
│   ├── integration/ 
│
├── public/
├── package.json
├── vite.config.js
│
├── Makefile
└── README.md                  # This file
```

## ⚙️ Standardizing Execution with Makefile

The Makefile acts as the single source of truth for all development, testing, and CI commands.

### Select Make commands

Note that these commands should all be run from the root folder of the project.

``` bash
# Show all Make commands
make help

# Install backend and fronted dependencies
make install

# Start development server backend (FastAPI)
# API docs available here: API Docs: http://localhost:8000/docs
make run-backend

# Start development server frontend (requires backend to be running also)
# access at http://localhost:3000
make run-backend
make run-frontend

```

## 🖥️ Frontend Tech Stack

React 19 (Vite-powered)

React Router DOM 7

Axios for HTTP requests

Vitest + React Testing Library

jsdom for browser simulation

ESLint + Prettier for code quality

## 🐍 Backend Technology Stack

FastAPI (async Python framework)

uv for dependency management

SQLAlchemy ORM

PyJWT for authentication

pwdlib + argon2 for secure password hashing

Pydantic for validation

pytest for testing

Ruff for linting/formatting

mypy for static typing

## 🧪 Testing Strategy

Connecto uses a layered testing approach to ensure reliability across the entire stack.

Backend Testing (pytest)
Unit tests: Pure logic, no DB.

Integration tests: API + DB using async fixtures.

Database strategy:  
Each test runs inside a transaction that is rolled back automatically — no DB resets needed.

Run with:

``` bash
make test-backend
```

Frontend Testing (Vitest)
Component tests: Render components in isolation.

DOM assertions: via @testing-library/jest-dom

Browser simulation: using jsdom

Test locations: colocated or under src/tests/

Run with:

``` bash
make test-frontend-unit
```

## 🚀 CI/CD Pipeline (GitHub Actions)

The pipeline runs on every push and pull request.

Shared Setup
Checkout repository

Initialize CodeQL (security scanning)

Install uv + Python dependencies

Install Node.js + npm dependencies

Start backend server + test database

Backend Job
Ruff linting

mypy type checking

bandit security scan

pytest (unit + integration)

Frontend Job
npm audit

ESLint

Vitest unit tests

Teardown
Clean up background processes

Upload CodeQL results

## 🔗 Local Development URLs

Frontend:  
[http://localhost:3000]

API Docs (Swagger):  
[http://localhost:8000/docs]

API Docs (ReDoc):  
[http://localhost:8000/redoc]
