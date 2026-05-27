# Social App - Connecto

## Project Overview

A modern social web application built with React, FastAPI, and DevSecOps practices. This project focuses on continuous integration, automated testing, and secure deployment.

### Prerequisites

## Project Structure

```text
/
backend/
|
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── auth.py         # Autentisering
│   │           ├── circles.py      # Circle CRUD
│   │           ├── circle_members.py
│   │           ├── posts.py        # Inlägg CRUD
│   │           └── users.py        # Användarsökning
│   │  
│   ├── core/
│   │   ├── config.py              # Konfiguration
│   │   ├── security.py            # JWT, hashing
│   │   └── db.py                  # DB connection
│   │  
│   ├── db/
│   │   ├── models.py              # SQLAlchemy models
│   │   └── database.py            # Session management
│   ├── schemas/
│   │   ├── auth.py                # Pydantic schemas
│   │   └── social.py
│   └── main.py                    # FastAPI app
│   
├── tests/
│   ├── unit/                      # Enhetstester
│   ├── integration/               # Integrationstester
│   ├── e2e/                       # End-to-end tester
│   │   └── step_defs/              
│   │       ├── test_user_dashboard.py  
│   │       ├── test_login.py
│   │       ├── test_registration.py
│   │       └── test_ui.py
│   └── conftest.py                # Shared fixtures (Database, etc.)
│   

|
├── pyproject.toml                 # Dependencies
├── uv.lock
│
docs                               # General project documentation and guides
├── features/                      # BDD Gherkin files
│   ├── login.feature   
|   └── etc...
├── BDD_CONFIGURATION.md
├── etc...
|    
frontend/
|
├── src/
│   ├── components/         # Återanvändbara komponenter
│   ├── pages/              # Sidor (LoginPage, RegisterPage, etc.)
│   ├── services/           # API-kommunikation
│   │   └── auth.service.js
│   ├── hooks/              # Custom React hooks
│   ├── context/            # React Context för state
│   ├── utils/              # Hjälpfunktioner
│   └── App.jsx             # Huvudkomponent
├── public/                 # Statiska filer
├── index.html
├── package.json            # Dependencies
├── vite.config.js          # Build-konfiguration
│
├── Makefile 
└── README.md                     # This file
```

## Standardizing Execution with Makefile

- Single Source of Truth: I use a Makefile to define all our complex build, test, and run commands.
- Local Parity: The exact same commands I type on our laptops (like make test-backend) are the ones GitHub Actions uses.
- Abstracted Complexity: Developers don't need to memorize long Pytest arguments or Playwright flags; the Makefile handles it.

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

# Run end-2-end tests
make run-test-backend
make run-frontend
make test-e2e

```


## Frontend Tech Stack

- **React 19** with Vite
- **React Router DOM** v6
- **Axios** for HTTP requests
- **Vitest** + Testing Library (unit/integration)

## Backend Technology Stack

- **Dependency Manager:** uv (replaces pip/poetry)
- **Framework:** FastAPI 
- **Server:** Uvicorn
- **Authentication:** PyJWT (Modern replacement for python-jose)
- **Password Hashing:** pwdlib + argon2 (Modern replacement for passlib)
- **Validation:** Pydantic 
- **Database:** SQLAlchemy, PostgreSQL 
- **Testing:** pytest
- **Code Quality:** Ruff (replaces black/flake8/isort) + mypy
- **Security:** bandit


## 🎯 Example Development Workflow using GitHub Flow

1. **Create feature branch** from main
2. **Implement feature** with tests, run tests
3. **Check code quality:** e.g. make lint-backend
4. **Security scan:** e.g. make security-backend
5. **Commit and push** to feature branch
6. **Create Pull Request** (CI will run automatically)
7. **Code review** by team
8. **Merge** to main

## 🧪 Testing Architecture

Our project utilizes a comprehensive, multi-layered testing strategy to ensure reliability across the entire stack. I divide our tests into specific domains to maximize execution speed and maintain clean database states.

### 🐍 Backend Testing (Pytest)

Our backend testing suite focuses on the FastAPI server and database logic, emphasizing speed and transaction safety.
- **Unit Testing:** Tests individual functions, utilities, and isolated business logic. I mock external dependencies and avoid database interactions to provide immediate developer feedback.
- **Integration Testing:** Tests API endpoints, database queries, and SQLAlchemy models natively using `@pytest.mark.asyncio`.
- * **Data Strategy:** We use a highly optimized `db_session` fixture. Instead of wiping the database, this fixture wraps every test in a safe transaction and strictly rolls it back when the test completes.
- * **Execution:** Run via `make test-backend`.

### ⚛️ Frontend Testing (Vitest & React Testing Library)

Our frontend unit and component tests are powered by **Vitest**, chosen for its blazing-fast execution and native integration with our Vite build pipeline.
* **Component Testing:** I use `@testing-library/react` to render components in isolation. We focus on testing how a user interacts with the UI (e.g., finding elements by accessible roles) rather than testing internal React state.
* **DOM Assertions:** Extended with `@testing-library/jest-dom` for highly readable matchers like `toBeInTheDocument()`.
* **Browser Simulation:** We use `jsdom` to simulate a browser environment inside Node.js, allowing us to test clicks and renders in milliseconds without launching a real browser.
* **Structure:** Tests are located in `frontend/src/tests/` or colocated directly next to the components they test (e.g., `Button.test.jsx`).
* **Execution:** Run via `make test-frontend-unit` (or `npm run test:watch` for active development).

## CI/CD Pipeline

GitHub Actions workflow located in .github/workflows/:

Runs on push to main/develop branches and pull requests

### Common Setup Steps (Run for both jobs)

- Checkout code: Fetches the repository code so the runner can access it.

- Initialize CodeQL: Prepares the GitHub Advanced Security scanner for either Python or JavaScript depending on the matrix target.

- Install uv: Sets up the Python package manager and caches dependencies based on the backend/uv.lock file.

- Setup Backend Environment: Creates a .env file with database credentials populated from GitHub Secrets and installs backend dependencies.

- Setup Test Database & Start Server: Seeds the shared PostgreSQL database and boots up the backend server in the background.

#### Backend Job Steps (Python)

- Lint, Format, Security: Runs static analysis and basic security checks on the Python code.

- Run Tests: Executes the backend unit and integration tests.

#### Frontend Job Steps (Node.js)

- Setup Node.js: Initializes Node version 20 and caches npm packages.

- Install & Audit: Installs frontend dependencies, runs a security audit, and performs linting checks.

- Unit Tests: Executes the frontend unit tests via Vitest.

- Playwright Setup: Caches browser binaries using the uv.lock key, and intelligently downloads either the full browsers or just the system dependencies based on whether the cache was hit.

- Run E2E Tests: Starts the frontend React server, waits for port 3000 to become available, and executes the Playwright end-to-end suite.

#### Teardown & Security Analysis

- Cleanup: An "always-run" step that safely kills any lingering background npm, node, and uvicorn processes to free up the runner.

- CodeQL Analysis: Finalizes the security scan and guarantees the results are uploaded to the GitHub Security tab, regardless of whether tests passed or failed.

## Clone the repository

git clone <https://github.com/DiscSecOps/DiscSecOps>

## Important Links

### Frontend App

- [http://localhost:3000]

### API documentation

- [http://localhost:8000/docs]

- [http://localhost:8000/redoc]

## Notes

- The project follows DevSecOps principles with security integrated from the start

- Feature development uses slicing methodology for incremental delivery

## Contributors

- Camelia Ciuca

## License

MIT
