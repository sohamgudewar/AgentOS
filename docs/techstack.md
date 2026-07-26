# Technology Stack

## Purpose

This document explains the technologies used in AgentOS and the reasoning behind each architectural decision.

The goal is to select tools that are production-ready, scalable, and widely adopted in enterprise AI systems.

---

# Frontend

| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| Next.js | Frontend Framework | Server-side rendering, routing, and production-ready React framework |
| React | UI Library | Component-based architecture with a large ecosystem |
| TypeScript | Programming Language | Static typing improves maintainability and developer experience |
| Tailwind CSS | Styling | Utility-first styling with excellent productivity |
| shadcn/ui | UI Components | Modern, customizable components without vendor lock-in |
| React Flow | Workflow Visualization | Interactive visualization of LangGraph workflows |
| TanStack Query | Data Fetching | Efficient server-state management and caching |
| Zustand | State Management | Lightweight global state management |
| Recharts | Data Visualization | Dashboards and monitoring charts |

---

# Backend

| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| Python 3.12 | Programming Language | Excellent ecosystem for AI and backend development |
| FastAPI | Web Framework | High performance, async support, automatic OpenAPI generation |
| Pydantic v2 | Data Validation | Type-safe request and configuration validation |
| SQLAlchemy | ORM | Mature ORM with excellent PostgreSQL support |
| Alembic | Database Migrations | Version-controlled schema management |
| Uvicorn | ASGI Server | Fast production-grade ASGI server |

---

# AI Framework

| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| LangGraph | Agent Orchestration | Stateful workflow engine for enterprise AI agents |
| LangChain | Integrations | Used only where it simplifies integrations |
| MCP SDK | Tool Integration | Standard protocol for connecting external tools |
| OpenAI SDK | LLM Provider | Primary model provider during development |
| Azure OpenAI SDK | Enterprise Deployment | Production-ready enterprise AI services |

---

# Databases

## PostgreSQL

Purpose

- User management
- Agent configuration
- Conversations
- Evaluations
- Audit logs

Reason

Reliable relational database with strong ACID guarantees.

---

## Redis

Purpose

- Caching
- Session storage
- Temporary workflow state

Reason

Extremely fast in-memory data store suitable for real-time systems.

---

## Qdrant

Purpose

- Embedding storage
- Semantic search
- Enterprise RAG

Reason

Purpose-built vector database with excellent performance and developer experience.

---

# Storage

## Azure Blob Storage

Purpose

Store uploaded enterprise documents.

Reason

Scalable object storage with strong Azure ecosystem integration.

---

# Authentication

| Technology | Purpose |
|------------|---------|
| JWT | Stateless authentication |
| bcrypt | Password hashing |
| RBAC | Role-based access control |

---

# Monitoring

| Technology | Purpose |
|------------|---------|
| OpenTelemetry | Distributed tracing |
| Prometheus | Metrics collection |
| Grafana | Metrics visualization |

---

# DevOps

| Technology | Purpose |
|------------|---------|
| Docker | Containerization |
| Docker Compose | Local development environment |
| GitHub Actions | CI/CD automation |
| Terraform | Infrastructure as Code |

---

# Cloud Platform

## Microsoft Azure

Services

- Azure OpenAI
- Azure Container Apps
- Azure Blob Storage
- Azure Key Vault
- Azure Monitor

Reason

Azure provides a strong ecosystem for enterprise AI workloads and aligns closely with production deployments used by many organizations.

---

# Development Tools

| Technology | Purpose |
|------------|---------|
| uv | Python package and project management |
| Git | Version control |
| GitHub | Source code hosting and collaboration |
| VS Code | Primary development environment |

---

# Why This Stack?

The selected technologies were chosen based on the following principles:

- Production readiness
- Scalability
- Strong community support
- Enterprise adoption
- Maintainability
- Performance
- Excellent AI ecosystem
- Cloud-native deployment

The architecture also emphasizes abstraction layers, allowing components such as LLM providers, vector databases, and storage providers to be replaced with minimal changes to the application.