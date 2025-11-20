MCG – Fast-Moving Consumer Goods Platform

(Working Title)
# FMCG — Fast-Moving Consumer Goods (tenders & procurement)

An application to collect, analyze, and present tenders / RFPs data with a React/Next.js frontend, a Python FastAPI backend, and a small model/database layer for data processing and experiments.

This README documents the repo layout, tech stack, setup and local development instructions, and where to find important files.

## Table of contents

- Project overview
- Key features
- Tech stack
- Repository structure and important files
- Quick start (dev)
- Backend setup & run
- Frontend setup & run
- Model / data and database
- Environment variables
- Development notes & tips
- Contributing
- License & contact

## Project overview

This repository collects tools and a UI for working with government and marketplace tenders (RFPs). It contains:

- `frontend/` — Next.js + TypeScript UI built with Tailwind and Radix components for browsing/searching tenders and viewing results.
- `backend/` — FastAPI-based API that provides endpoints for analysis and data operations.
- `model/` — scripts and helpers for data ingestion, pricing logic, and experiments (contains CSVs, DB initialization scripts, and agents/orchestrators).
- `database/` — database files (SQLite) used for quick local development.

This repo is suitable for local development and prototyping; production readiness (scaling, authentication, secure env management) requires additional work.

## Key features

- Ingest tenders from CSV / scraped sources
- Store and query tenders in a local SQLite DB for dev
- Frontend for searching/filtering tenders and viewing analytics
- Backend analysis endpoints (see `backend/routes/`)
- Model code for pricing and workflow orchestration in `model/`

## Tech stack

- Frontend: Next.js 13 (React 18), TypeScript, Tailwind CSS, Radix UI components
- Backend: Python, FastAPI, Uvicorn
- Data: SQLite (local dev), CSV files for sample input
- Tools: Playwright (scraping/testing), BeautifulSoup, pandas

Dependencies (representative):

- frontend/package.json shows Next.js 13.5.1, React 18, Tailwind CSS 3.x, TypeScript
- backend/requirements.txt includes: fastapi, uvicorn, playwright, beautifulsoup4, pandas, groq, python-dotenv

## Repository structure (high-level)

Root
- `frontend/` — Next.js app (UI)
	- `app/` — Next.js app routes and pages
	- `components/` — reusable UI components and primitives
	- `package.json` — frontend dependencies & scripts

- `backend/` — FastAPI server
	- `main.py` — FastAPI app & CORS setup
	- `routes/` — router modules (`analyze.py`, `tenders.py`)
	- `requirements.txt` — Python dependencies

- `model/` — data/modeling scripts
	- `init_db_pricing.py`, `setup_database.py`, `run_workflow.py` — DB init and experimentation scripts
	- `pricing_agent_logic.py`, `sales_agent_logic.py`, `technical_agent_logic.py` — business/agent logic
	- CSVs: `product_database.csv`, `product_prices.csv`, `tenders.csv`, `test_prices.csv`

- `database/` — contains `rfp_database.db` (SQLite) used for local dev
- `tenders.csv` — sample tenders file

## Quick start — development

Prerequisites

- Node.js (≥16) and npm/yarn
- Python 3.9+ (recommended) and pip
- Optionally: SQLite client

1) Clone

		git clone https://github.com/Yashbhu/fmcg.git
		cd fmcg

2) Backend setup

		python -m venv .venv
		source .venv/bin/activate   # macOS / Linux (zsh)
		pip install --upgrade pip
		pip install -r backend/requirements.txt

Notes: Playwright requires an additional install step to download browser binaries:

		playwright install

Run the backend (development):

		# from repo root
		uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

By default the FastAPI app is configured in `backend/main.py`. The app includes CORS settings for localhost:3000.

3) Frontend setup

		cd frontend
		npm install
		npm run dev

Open the frontend at http://localhost:3000. The frontend expects the backend API to be available at `http://localhost:8000` unless configured otherwise.

## Model / data & database

- The repo contains a sample SQLite DB at `database/rfp_database.db` for quick testing. You can open it with `sqlite3 database/rfp_database.db` or any DB browser.
- CSV files live under `model/` and the repo root (`tenders.csv`). Use the scripts in `model/` to import or reinitialize the DB:

		# examples (edit/inspect scripts before running)
		python model/setup_database.py
		python model/init_db_pricing.py

Inspect the scripts to see exact behavior. Back up your DB before re-running initialization scripts.

## Environment variables (example)

Create a `.env` file in `backend/` (or set env vars globally). Example entries:

		DATABASE_URL=sqlite:///./database/rfp_database.db
		SECRET_KEY=replace-with-a-secret
		API_PORT=8000

Load these using `python-dotenv` or your deployment environment.

## Useful endpoints

- The backend includes routers in `backend/routes/`.
- Example (development):
	- Analyze: `GET http://localhost:8000/analyze/...` (see `backend/routes/analyze.py`)

Open the automatic docs when backend runs: `http://localhost:8000/docs` (Swagger) and `http://localhost:8000/redoc`.

## Development notes & tips

- Keep the backend running at port 8000 and the frontend at 3000 for the default CORS setup.
- When updating front/backend contracts, update types in the frontend (if you add API shapes).
- Use small virtual environments for Python work and commit `requirements.txt` changes when dependencies change.

## Testing

- There are no formal tests checked into the repo by default. Add tests under `backend/tests/` using `pytest` and under `frontend/` using your preferred test runner (Jest/React Testing Library).

## Contributing

Contributions welcome. Please:

1. Fork the repo and create a feature branch
2. Run linters and tests locally
3. Open a PR describing your change and include screenshots or sample requests if relevant

If you plan to make breaking changes to the API, document them in this README and create a migration plan for the DB.

## License

Add your chosen license (e.g., MIT). If this repo is private, specify internal usage rules instead.

## Contact / Maintainers

Repo owner: `Yashbhu` (GitHub: Yashbhu)

Questions? Open issues or PRs in the repository.

---
