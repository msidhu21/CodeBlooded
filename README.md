
# CodeBlooded 
# modifcation try1
# Olamipo modification

# COSC 310 Backend (M3)

FastAPI backend with SQLite, layered architecture.

## Setup

```bash
pip install -r requirements.txt
```

Or with venv:
```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

## Run
#this is a test
```bash
python -m uvicorn backend.app.main:app --reload
```

Open http://127.0.0.1:8000/docs for interactive API docs.

## Tests

```bash
cd backend
pytest -q --cov=app --cov-report=term --cov-report=xml:../evidence/coverage.xml
```

## Docker

```bash
docker compose up --build
```

## API Endpoints

### Auth
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login
- `GET /auth/me` - Demo user info

### Items
- `GET /items?q=search&category=tools&page=1&size=10` - Search items
- `GET /items/{id}` - Get item details

### Admin (requires `Authorization: Bearer admin`)
- `POST /admin/items` - Create item
- `PATCH /admin/items/{id}` - Update item
- `DELETE /admin/items/{id}` - Delete item

### Export (requires `Authorization: Bearer admin`)
- `POST /export/selection` - Export selected items as JSON

### Profile
- `PATCH /profile` - Update profile

## Example Requests

```powershell
# Create item
curl -X POST http://127.0.0.1:8000/admin/items -H "Authorization: Bearer admin" -H "Content-Type: application/json" -d '{"sku":"TEST001","name":"Test Item","category":"tools","available":true,"description":"Test"}'

# Get item
curl http://127.0.0.1:8000/items/1

# Search items
curl "http://127.0.0.1:8000/items?q=test&page=1&size=10"

# Update item
curl -X PATCH http://127.0.0.1:8000/admin/items/1 -H "Authorization: Bearer admin" -H "Content-Type: application/json" -d '{"name":"Updated Name"}'

# Export selection
curl -X POST http://127.0.0.1:8000/export/selection -H "Authorization: Bearer admin" -H "Content-Type: application/json" -d '{"ids":[1,2]}'

# Register
curl -X POST http://127.0.0.1:8000/auth/register -H "Content-Type: application/json" -d '{"email":"user@test.com","password":"pass123","name":"User"}'

# Login
curl -X POST http://127.0.0.1:8000/auth/login -H "Content-Type: application/json" -d '{"email":"user@test.com","password":"pass123"}'
```

## Features

- Auth: register, login, user profile
- Catalog: search items, view details
- Admin: CRUD operations for items
- Export: JSON export for selected items
- SQLite database with SQLAlchemy ORM
- Layered architecture: routers → services → repos → models


