# COSC 310 Backend (M3)

## Quick Start

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the server:
```bash
cd backend
uvicorn app.main:app --reload
```

Run tests:
```bash
pytest backend/tests/
pytest backend/tests/ --cov=backend/app --cov-report=html
```

## Features

- Auth: register, login, user profile
- Catalog: search items, view details
- Admin: CRUD operations for items
- Export: JSON export for selected items
- SQLite database with SQLAlchemy ORM
- Layered architecture: routers → services → repos → models

