# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview
Companies microservice for Gondor platform. Python/FastAPI service managing company profiles, business units, branches, and company settings.

## Commands
- `make run` — run with hot reload on port 8019
- `make test` — run pytest
- `make lint` — ruff check + format check
- `make format` — auto-format with ruff
- `make docker` — build Docker image

## Architecture
- `app/main.py` — FastAPI app, lifespan, router registration
- `app/api/v1/` — route handlers
- `app/core/` — config, security (JWT), database engine
- `app/models/` — SQLAlchemy models
- `app/schemas/` — Pydantic request/response schemas
- `app/repositories/` — database access layer
- `app/services/` — business logic layer
- `migrations/` — Alembic migrations

## Key Decisions
- Async everywhere (asyncpg + SQLAlchemy async)
- JWT validated locally (same secret as users-security service)
- All data scoped by company_id (multi-tenancy)
- Soft delete for companies (is_active flag)
- Settings stored as key-value pairs per company
