MCG – Fast-Moving Consumer Goods Platform

(Working Title)

Table of Contents

Project Overview

Key Features

Architecture & Tech Stack

Getting Started

Prerequisites

Installation

Configuration

Running Locally

Directory Structure

Usage

Frontend

Backend

Model / Database

Deployment

Testing

Contributing

License

Contact

Project Overview

The FMCG platform is designed to serve as a comprehensive solution for managing fast‐moving consumer goods (FMCG) supply-chains, tendering, and procurement workflows. It supports integration of government e-marketplaces, e-tenders, and database management for tenders and RFPs.

Key Features

A frontend web application (UI) for users: browsing tenders, submitting bids, tracking status.

A backend API server handling business logic, authentication, data processing.

A model/database layer: storing tender data, RFPs, user data, bidding history, analytics.

Data ingestion from external sources (e.g., government portals) into a unified database.

Reporting dashboards for monitoring tender activity, win-rates, vendor performance.

Architecture & Tech Stack

Frontend: TypeScript, JavaScript, CSS – likely using a modern framework (React/Vue/Angular) based on code.

Backend: Python (or another language) – handling API endpoints, business logic, data access.

Database: SQLite (evidenced by rfp_database.db in repo) for local/dev; can be swapped for Postgres/MySQL in production.

Model: A module/folder (model/) where domain models and business schema reside.

Data ingestion/CSV: tenders.csv hints at CSV import capability for tender data.

Overall layered architecture: Frontend → Backend API → Model/Database.

Getting Started
Prerequisites

Node.js (version ≥ X) and npm/yarn for frontend.

Python (version ≥ X) for backend (if applicable).

SQLite3 (or equivalent) installed locally.

Git for version control.

Installation

Clone the repository:

git clone https://github.com/Yashbhu/fmcg.git
cd fmcg


Navigate to sub-modules:

cd frontend
npm install
cd ../backend
pip install -r requirements.txt

Configuration

Create a .env file in backend/ with necessary environment variables (e.g., DATABASE_URL, SECRET_KEY, API_PORT).

In frontend/, adjust config.js or similar with backend API base URL.

Running Locally

Start backend:

cd backend
python app.py


Start frontend:

cd frontend
npm start


Open http://localhost:3000 (or configured port) in your browser.
```
Directory Structure
fmcg/
├── frontend/        # UI application
├── backend/         # API server & business logic
├── database/        # database-related files (e.g., SQLite DB, migrations)
├── model/           # domain/model definitions, schema, modules
├── tenders.csv      # sample data ingestion file
└── README.md        # this readme
```

Adjust folders and names as your repo reflects.

Usage
Frontend

Browse list of tenders.

Filter/search tenders by date, category, status.

Register/login as vendor.

Submit bids, view bid status.

Backend

RESTful endpoints:

GET /api/tenders → list all tenders

POST /api/bids → submit a bid

GET /api/vendors/:vendorId → vendor profile & activity
(Fill in actual endpoint definitions)

Authentication (JWT or session‐based) for protected routes.

Model / Database

Data schema includes tables/collections: Tenders, Vendors, Bids, RFPs.

Sample CSV file tenders.csv can be imported using a script in database/.

Example script:

python database/import_tenders.py --file tenders.csv

Deployment

Use environment variables to configure production database (e.g., Postgres) and services.

Build frontend for production:

cd frontend
npm run build


Deploy backend on a cloud provider or container (Docker, AWS, Azure).

Serve built frontend as static assets or via CDN.

Ensure HTTPS, logging, monitoring are configured.

Testing

Backend tests: in backend/tests/ – run via pytest.

Frontend tests: in frontend/tests/ – run via npm test.

CI/CD configuration (GitHub Actions) to run tests on every PR.

Contributing

Contributions are very welcome! To contribute:

Fork the repository

Create a new branch: git checkout -b feature/YourFeature

Commit your changes with clear messages

Push your branch and create a Pull Request (PR)

Ensure your changes include tests where applicable and pass existing tests

Please adhere to the code style and add documentation/comments for new features.

License

Specify your license here (e.g., MIT License).

MIT License
