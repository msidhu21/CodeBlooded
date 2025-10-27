# Setup Instructions for M3 Backend

## Prerequisites

1. **Install Python 3.9+** (if not already installed)
   - Download from https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Verify Python installation:**
```bash
python --version
pip --version
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
cd backend
uvicorn app.main:app --reload
```

The server will start at http://localhost:8000

### 3. View API Documentation

Open your browser to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 4. Test the API

**Using Swagger UI:**
1. Go to http://localhost:8000/docs
2. Click "Authorize" button
3. Enter: `Bearer admin` (this is the admin token for demo purposes)
4. Try the endpoints:
   - POST /admin/items - Create an item
   - PATCH /admin/items/{item_id} - Update an item
   - DELETE /admin/items/{item_id} - Delete an item
   - POST /export/selection - Export items as JSON

**Using curl:**
```bash
# Create an item
curl -X POST "http://localhost:8000/admin/items" \
  -H "Authorization: Bearer admin" \
  -H "Content-Type: application/json" \
  -d '{"sku":"A100","name":"Alpha","category":"tools","available":true,"description":"Test item"}'

# Get the item ID from response, then update it
curl -X PATCH "http://localhost:8000/admin/items/1" \
  -H "Authorization: Bearer admin" \
  -H "Content-Type: application/json" \
  -d '{"name":"Alpha Updated"}'

# Export items
curl -X POST "http://localhost:8000/export/selection" \
  -H "Authorization: Bearer admin" \
  -H "Content-Type: application/json" \
  -d '{"ids":[1]}'
```

## Running Tests

### Run All Tests

```bash
cd backend
pytest -q
```

### Run with Coverage Report

```bash
cd backend
pytest -q --cov=app --cov-report=term --cov-report=xml:../evidence/coverage.xml
cd ..
```

### Run Specific Test Suites

```bash
# Unit tests only
cd backend
pytest tests/unit/ -v

# Integration tests only
cd backend
pytest tests/integration/ -v
```

## Project Structure Summary

```
backend/
├── app/
│   ├── api/           # HTTP endpoints (routers)
│   ├── core/          # Shared dependencies & errors
│   ├── models/        # Database entities & DTOs
│   ├── repos/         # Data access layer
│   ├── services/       # Business logic layer
│   └── main.py        # FastAPI application
└── tests/
    ├── unit/          # Unit tests with mocks
    └── integration/   # Integration tests with test DB
```

## Key Features Implemented

✅ **Admin CRUD Operations**
- Create items with unique SKU validation
- Update items (partial updates supported)
- Delete items
- All operations require admin authentication

✅ **JSON Export**
- Export selected items as JSON
- Downloadable file with proper headers

✅ **Domain Rules Enforcement**
- Unique SKU constraint (409 Conflict if duplicate)
- Transactional safety (rollback on errors)
- Admin-only access (403 Forbidden if not authorized)

✅ **Testing**
- Unit tests for service layer (mocked dependencies)
- Integration tests for full HTTP stack
- Coverage reporting for M3 evidence

## API Response Codes

- `201` - Resource created successfully
- `200` - Request succeeded
- `204` - Deleted successfully (no content)
- `403` - Forbidden (missing/invalid admin token)
- `404` - Item not found
- `409` - Conflict (duplicate SKU)

## Common Issues & Solutions

**Issue: "Module not found" errors**
- Solution: Make sure you're running commands from the project root
- Solution: Verify all `__init__.py` files exist in subdirectories

**Issue: Database locked errors**
- Solution: Close any other connections to `cosc310.db`
- Solution: Delete the database file and let the app recreate it

**Issue: Port 8000 already in use**
- Solution: Use a different port: `uvicorn app.main:app --reload --port 8001`
- Solution: Kill the process using port 8000

**Issue: Import errors in tests**
- Solution: Run tests from the `backend` directory
- Solution: Ensure pytest can find the `app` module

## Next Steps for PR

1. Create branch:
```bash
git checkout -b feature/m3-admin-export
```

2. Add and commit files:
```bash
git add backend/ requirements.txt README.md
git commit -m "feat(cosc310): admin CRUD + JSON export with unit+integration tests (M3)"
```

3. Push and create PR:
```bash
git push -u origin feature/m3-admin-export
```

Then open a Pull Request with:
- Title: `feat(cosc310): admin CRUD + JSON export + tests (M3)`
- Description should reference M1/M2 docs
- Include coverage.xml and any screenshots as evidence

