# ---------------------------------------------------------------------------
# Restaurant Vision Analytics — developer Makefile
# Cross-platform note: targets assume a POSIX shell. On Windows use Git Bash,
# WSL, or run the underlying commands directly (see docs/GettingStarted.md).
# ---------------------------------------------------------------------------

PYTHON ?= python
PIP ?= $(PYTHON) -m pip
BACKEND_HOST ?= 0.0.0.0
BACKEND_PORT ?= 8000

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: install-backend install-frontend ## Install backend + frontend dependencies

.PHONY: install-backend
install-backend: ## Install backend (editable) with dev extras
	$(PIP) install -e ".[dev]"

.PHONY: install-frontend
install-frontend: ## Install frontend dependencies
	npm --prefix frontend install

.PHONY: backend
backend: ## Run the FastAPI backend (http://localhost:8000)
	$(PYTHON) -m uvicorn app.main:app --reload --host $(BACKEND_HOST) --port $(BACKEND_PORT) --app-dir backend

.PHONY: frontend
frontend: ## Run the Vite dev server (http://localhost:5173)
	npm --prefix frontend run dev

.PHONY: demo
demo: ## Run backend in demo mode (synthetic, anonymous data — no camera needed)
	ENABLE_DEMO_MODE=true $(PYTHON) -m uvicorn app.main:app --host $(BACKEND_HOST) --port $(BACKEND_PORT) --app-dir backend

.PHONY: test
test: ## Run backend test suite
	$(PYTHON) -m pytest

.PHONY: lint
lint: ## Lint backend with ruff
	$(PYTHON) -m ruff check backend

.PHONY: format
format: ## Auto-format backend with ruff
	$(PYTHON) -m ruff format backend

.PHONY: build-frontend
build-frontend: ## Build the production frontend bundle
	npm --prefix frontend run build

.PHONY: docker-up
docker-up: ## Build and start the full stack with Docker Compose
	docker compose up --build

.PHONY: docker-down
docker-down: ## Stop and remove Docker Compose services
	docker compose down

.PHONY: synthetic
synthetic: ## Generate a synthetic customer-flow event file for demos
	$(PYTHON) demo/synthetic/generate_synthetic_flow.py
