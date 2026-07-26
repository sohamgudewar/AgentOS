# Folder Structure

## Purpose

This document explains the directory structure of the AgentOS project and the responsibility of each folder.

The project follows a **feature-first**, **modular**, and **Clean Architecture** approach to ensure scalability, maintainability, and separation of concerns.

---

# Root Directory

```text
AgentOS/
│
├── backend/
├── frontend/
├── docs/
├── docker/
├── terraform/
├── scripts/
├── .github/
│
├── docker-compose.yml
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

---

# Directory Overview

| Directory | Responsibility |
|------------|----------------|
| `backend/` | FastAPI application, AI orchestration, APIs, business logic |
| `frontend/` | Next.js web application and dashboard |
| `docs/` | Architecture, system design, roadmap, and technical documentation |
| `docker/` | Dockerfiles and container configuration |
| `terraform/` | Infrastructure as Code (Azure) |
| `scripts/` | Development and deployment helper scripts |
| `.github/` | GitHub Actions CI/CD workflows |

---

# Backend Structure

```text
backend/
│
├── app/
├── tests/
├── pyproject.toml
├── uv.lock
├── .python-version
└── README.md
```

---

## app/

Contains the entire backend application.

```text
app/
│
├── api/
├── core/
├── database/
├── auth/
├── users/
├── agents/
├── rag/
├── mcp/
├── guardrails/
├── evaluation/
├── monitoring/
├── approvals/
├── providers/
├── workers/
├── shared/
└── main.py
```

> **Note:** Only `api/`, `core/`, and `database/` exist initially. Other modules will be added incrementally as development progresses.

---

# Module Responsibilities

## api/

Contains all REST API endpoints.

Responsibilities:

- API routing
- Request validation
- Response models
- API versioning

---

## core/

Contains application-wide components.

Responsibilities:

- Configuration
- Logging
- Security
- Constants
- Custom exceptions

---

## database/

Responsible for database management.

Responsibilities:

- Database connection
- SQLAlchemy Base
- Session management
- Alembic migrations

---

## auth/

Authentication and authorization.

Responsibilities:

- JWT
- Refresh Tokens
- RBAC
- Password hashing

---

## users/

User management.

Responsibilities:

- User CRUD
- Roles
- Permissions

---

## agents/

Core AI agent management.

Responsibilities:

- Agent creation
- Prompt management
- Workflow configuration
- Tool assignment

---

## rag/

Enterprise Retrieval-Augmented Generation.

Responsibilities:

- Document ingestion
- Chunking
- Embeddings
- Retrieval
- Context generation

---

## mcp/

Model Context Protocol integrations.

Responsibilities:

- GitHub
- Filesystem
- PostgreSQL
- Browser
- Email

---

## guardrails/

AI safety and validation.

Responsibilities:

- Prompt injection detection
- Jailbreak detection
- PII detection
- Output validation

---

## evaluation/

LLM evaluation framework.

Responsibilities:

- Faithfulness
- Relevancy
- Latency
- Cost tracking
- Token usage

---

## monitoring/

System observability.

Responsibilities:

- Metrics
- Tracing
- Logging
- Health monitoring

---

## approvals/

Human-in-the-loop workflows.

Responsibilities:

- Approval requests
- Workflow interruption
- Resume execution

---

## providers/

External service abstractions.

Examples:

- OpenAI
- Azure OpenAI
- Embedding providers
- Storage providers

---

## workers/

Background task execution.

Examples:

- Embedding generation
- Evaluation jobs
- Document processing

---

## shared/

Reusable components shared across modules.

Examples:

- Utilities
- Base classes
- Common schemas
- Helper functions

---

# Frontend Structure

The frontend will be built using Next.js and organized by feature.

Example structure:

```text
frontend/
│
├── app/
├── components/
├── features/
├── hooks/
├── services/
├── store/
├── types/
└── public/
```

---

# Design Principles

The project follows these architectural principles:

- Feature-first organization
- Modular architecture
- Clean Architecture
- SOLID principles
- Dependency Injection
- Repository Pattern
- Provider abstraction
- Async-first programming

---

# Why This Structure?

This organization provides several advantages:

- Easy to navigate
- Highly modular
- Supports team collaboration
- Scales as new features are added
- Reduces coupling between modules
- Encourages clean separation of responsibilities

As the project grows, each major module can be extracted into its own microservice with minimal refactoring.