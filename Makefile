PYTHON_BIN ?= $(shell if command -v python3.12 >/dev/null 2>&1; then command -v python3.12; else command -v python3; fi)
BACKEND_VENV := backend/.venv
BACKEND_PYTHON := $(BACKEND_VENV)/bin/python
BACKEND_PIP := $(BACKEND_VENV)/bin/pip

.PHONY: backend-install frontend-install install test build smoke dev-backend dev-frontend

backend-install:
	$(PYTHON_BIN) -m venv $(BACKEND_VENV)
	$(BACKEND_PIP) install --upgrade pip setuptools wheel
	$(BACKEND_PIP) install -e './backend[dev]'

frontend-install:
	cd frontend && npm ci

install: backend-install frontend-install

test:
	cd backend && .venv/bin/python -m pytest tests

build:
	cd frontend && npm run build

smoke:
	bash scripts/full_health_check.sh

dev-backend:
	cd backend && .venv/bin/uvicorn app.main:app --reload

dev-frontend:
	cd frontend && npm run dev
