# System Design

## Purpose

This document describes the high-level system design of AgentOS, including component interactions, request lifecycle, data flow, and infrastructure.

The goal of AgentOS is to provide a modular, scalable, and production-ready platform for building and managing enterprise AI agents.

---

# System Overview

AgentOS follows a modular monolithic architecture.

Each major module is isolated behind well-defined interfaces, allowing future migration to microservices with minimal refactoring.

```
                        User
                          │
                  Next.js Dashboard
                          │
                 HTTPS / WebSocket
                          │
                  FastAPI Backend
                          │
      ┌───────────────────┼───────────────────┐
      │                   │                   │
 Authentication      Agent Engine         Monitoring
      │             (LangGraph)               │
      │                   │                   │
      ├──────────────┬────┴───────┬───────────┤
      │              │            │
 Enterprise RAG   Guardrails   Evaluation
      │              │            │
      └──────────────┼────────────┘
                     │
                 MCP Client
                     │
      ┌──────────────┼──────────────┐
      │              │              │
   GitHub       PostgreSQL      Filesystem
                     │
          PostgreSQL  Redis  Qdrant
```

---

# System Components

## Frontend

Technology:

- Next.js
- React
- TypeScript

Responsibilities:

- User Interface
- Dashboard
- Authentication
- Chat Interface
- Agent Builder
- Monitoring Dashboard

---

## Backend

Technology:

- FastAPI

Responsibilities:

- REST APIs
- Business Logic
- Authentication
- Agent Management
- Workflow Execution
- Monitoring

---

## LangGraph Engine

Responsible for orchestrating AI workflows.

Functions:

- Planning
- Routing
- Tool Calling
- Memory
- State Management
- Conditional Execution
- Human Approval Interrupts

---

## Enterprise RAG

Responsible for enterprise knowledge retrieval.

Pipeline

```
Upload Document

↓

Extract Text

↓

Chunk Document

↓

Generate Embeddings

↓

Store in Qdrant

↓

Semantic Search

↓

Context Builder

↓

LLM
```

---

## MCP Layer

The Model Context Protocol (MCP) provides a standardized interface between AI agents and external systems.

Supported integrations:

- GitHub
- PostgreSQL
- Filesystem
- Browser
- Email

Future integrations can be added without modifying agent logic.

---

## Guardrails

Every request passes through guardrails.

Input

- Prompt Injection Detection
- Jailbreak Detection
- PII Detection
- Secret Detection

Output

- JSON Validation
- Citation Validation
- Policy Enforcement
- Sensitive Data Filtering

---

## Evaluation

Every generated response is evaluated automatically.

Metrics

- Faithfulness
- Relevancy
- Context Precision
- Context Recall
- Latency
- Token Usage
- Cost

Evaluation results are stored for monitoring and regression testing.

---

## Monitoring

The platform continuously records:

- API Requests
- Response Times
- Tool Usage
- Agent Executions
- Graph Execution Time
- Errors
- Cost

---

# Request Lifecycle

Example request:

```
User

↓

Authentication

↓

Authorization

↓

Agent Selection

↓

LangGraph Execution

↓

Need RAG?

↓

Retrieve Documents

↓

Need Tool?

↓

Execute MCP Tool

↓

Need Approval?

↓

Pause Workflow

↓

Human Approval

↓

Continue

↓

LLM Response

↓

Evaluation

↓

Audit Logging

↓

Return Response
```

---

# Data Flow

## Authentication

User

↓

JWT Validation

↓

RBAC

↓

API Access

---

## Document Processing

Upload

↓

Blob Storage

↓

Parser

↓

Chunker

↓

Embeddings

↓

Qdrant

---

## Agent Execution

Prompt

↓

Planner

↓

Retriever

↓

Tool

↓

LLM

↓

Evaluator

↓

Response

---

# Database Responsibilities

## PostgreSQL

Stores

- Users
- Agents
- Conversations
- Evaluations
- Audit Logs
- Approval Requests

---

## Redis

Stores

- Cache
- Sessions
- Temporary Workflow State

---

## Qdrant

Stores

- Embeddings
- Document Chunks
- Vector Metadata

---

# Deployment Architecture

```
Next.js

↓

Azure Container Apps

↓

FastAPI

↓

Azure OpenAI

↓

Azure Blob Storage

↓

PostgreSQL

↓

Redis

↓

Qdrant

↓

Azure Monitor
```

---

# Design Principles

- Modular Architecture
- Clean Architecture
- SOLID Principles
- Repository Pattern
- Dependency Injection
- Provider Abstraction
- Async-first Programming
- Security by Default
- Observability by Default

---

# Future Evolution

Although AgentOS begins as a modular monolith, every major module is designed so it can later be extracted into an independent microservice with minimal changes.