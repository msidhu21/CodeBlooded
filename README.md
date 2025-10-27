# COSC 310 Project - M3 Backend Slice

## Overview
This project implements the M3 backend slice for the COSC 310 project, featuring Admin CRUD operations and JSON export functionality with a layered/MVC architecture.

## Directory Structure
```
310groupwork/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── admin.py          # Admin CRUD endpoints
│   │   │   └── export.py         # Export endpoint
│   │   ├── core/
│   │   │   ├── deps.py           # Dependencies (DB session, admin auth)
│   │   │   └── errors.py         # Custom exceptions
│   │   ├── models/
│   │   │   ├── entities.py       # SQLAlchemy models
│   │   │   └── dto.py            # Pydantic DTOs
│   │   ├── repos/
│   │   │   └── item_repo.py      # Data access layer
│   │   ├── services/
│   │   │   └── export_service.py # Business logic
│   │   └── main.py               # FastAPI app entry point
│   └── tests/
│       ├── unit/
│       │   └── test_export_service.py
│       └── integration/
│           └── test_admin_api.py
└── requirements.txt

```

## Installation

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

## Running the Application

1. **Start the FastAPI server:**
```bash
cd backend
uvicorn app.main:app --reload
```

The API will be available at:
- Main: http://localhost:8000
- Documentation: http://localhost:8000/docs
- OpenAPI Spec: http://localhost:8000/openapi.json

2. **Test the API:**
Admin endpoints require the header: `Authorization: Bearer admin`

Example using curl:
```bash
# Create an item
curl -X POST "http://localhost:8000/admin/items" \
  -H "Authorization: Bearer admin" \
  -H "Content-Type: application/json" \
  -d '{"sku":"A100","name":"Alpha","category":"tools","available":true,"description":"Test item"}'

# Export items
curl -X POST "http://localhost:8000/export/selection" \
  -H "Authorization: Bearer admin" \
  -H "Content-Type: application/json" \
  -d '{"ids":[1,2,3]}'
```

## Running Tests

1. **Run all tests:**
```bash
cd backend
pytest -q
```

2. **Run with coverage:**
```bash
cd backend
pytest -q --cov=app --cov-report=term --cov-report=xml:../evidence/coverage.xml
cd ..
```

3. **Run specific test files:**
```bash
cd backend
pytest tests/unit/test_export_service.py -v
pytest tests/integration/test_admin_api.py -v
```

## API Endpoints

### Admin CRUD Operations

- `POST /admin/items` - Create a new item (201)
- `PATCH /admin/items/{item_id}` - Update an item (200)
- `DELETE /admin/items/{item_id}` - Delete an item (204)

### Export Operations

- `POST /export/selection` - Export selected items as JSON

### Error Responses

- `403` - Missing or invalid admin token
- `404` - Item not found
- `409` - Duplicate SKU conflict

## Architecture

This implementation follows a layered/MVC architecture:

1. **Routers** (`api/`) - Handle HTTP requests and responses
2. **Services** (`services/`) - Business logic and orchestration
3. **Repositories** (`repos/`) - Data access layer with domain rules
4. **Models** (`models/`) - Data entities (SQLAlchemy) and DTOs (Pydantic)

### Domain Rules Enforced

1. **Unique SKU**: Each item must have a unique SKU (enforced at repository level)
2. **Transactional Safety**: Database sessions use commit/rollback for ACID compliance
3. **Admin-Only Actions**: All admin and export endpoints require valid admin token

## Testing Strategy

- **Unit Tests**: Test individual service logic with mocked dependencies
- **Integration Tests**: Test full HTTP request/response cycle with test database
- **Coverage**: Aim for comprehensive coverage of business logic paths

## Git Workflow

To prepare for PR:

```bash
git checkout -b feature/m3-admin-export
git add backend/ requirements.txt README.md
git commit -m "feat(cosc310): admin CRUD + JSON export with unit+integration tests (M3)"
git push -u origin feature/m3-admin-export
```

## M3 Evidence

After running tests, the following evidence will be generated:

- `evidence/coverage.xml` - Coverage report
- `evidence/screenshots/coverage_admin_export.png` (optional)
- `evidence/screenshots/docs_admin_export.png` (optional)

## Notes

- Admin authentication is simplified for M3 demo purposes (Bearer token)
- SQLite database file: `cosc310.db`
- All database operations are transactional (commit/rollback)

