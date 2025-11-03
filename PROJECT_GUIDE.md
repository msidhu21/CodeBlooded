# COSC 310 Project Guide

## 🔑 Key Commands

### Server Management
```powershell
# Start server
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Run tests
cd backend
pytest -q --cov=app --cov-report=term

# Run tests with coverage XML
pytest -q --cov=app --cov-report=term --cov-report=xml:../evidence/coverage.xml
```

### Database
```powershell
# SQLite database location
backend/cosc310.db

# View database (if you have sqlite3)
sqlite3 backend/cosc310.db
.tables
SELECT * FROM users;
SELECT * FROM items;
```

### API Testing
```powershell
# Test root endpoint
curl http://127.0.0.1:8000/

# Test with admin token
curl -X POST http://127.0.0.1:8000/admin/items `
  -H "Authorization: Bearer admin" `
  -H "Content-Type: application/json" `
  -d '{"sku":"TEST","name":"Test","category":"tools","available":true,"description":""}'

# Search items
curl "http://127.0.0.1:8000/items?q=test&page=1&size=10"
```

---

## 📐 Architecture & Process Flow

### Layered Architecture

```
Request → API Router → Service → Repository → Database
         (FastAPI)    (Business)  (Data Access) (SQLite)
```

### 1. **API Layer** (`backend/app/api/`)
- **Purpose**: HTTP endpoints, request/response handling
- **Files**: `admin.py`, `auth.py`, `items.py`, `export.py`, `profile.py`
- **Process**:
  1. Receives HTTP request
  2. Validates input (Pydantic models)
  3. Calls service layer
  4. Returns response

**Example Flow (Admin Create Item):**
```python
# admin.py
@router.post("/admin/items")
def create_item(payload: ItemCreate, _=Depends(require_admin), db: Session = Depends(get_db)):
    # 1. Validate payload (ItemCreate DTO)
    # 2. Check admin auth (require_admin dependency)
    # 3. Get database session
    # 4. Call repository directly (or service if needed)
    obj = ItemRepo(db).create(**payload.model_dump())
    return ItemOut.model_validate(obj)
```

### 2. **Service Layer** (`backend/app/services/`)
- **Purpose**: Business logic, orchestration
- **Files**: `auth_service.py`, `catalog_service.py`, `export_service.py`, `profile_service.py`
- **Process**:
  1. Receives DTOs from API
  2. Applies business rules
  3. Calls repository methods
  4. Transforms data

**Example Flow (Export Service):**
```python
# export_service.py
class ExportService:
    def export_selection(self, req: ExportSelectionRequest) -> ExportPayload:
        # 1. Get items by IDs from repository
        items = self.repo.get_many(req.ids)
        # 2. Transform to DTOs
        out = [ItemOut.model_validate(i) for i in items]
        # 3. Return structured payload
        return ExportPayload(count=len(out), items=out)
```

### 3. **Repository Layer** (`backend/app/repos/`)
- **Purpose**: Database operations, SQL queries
- **Files**: `item_repo.py`, `user_repo.py`
- **Process**:
  1. Receives parameters
  2. Builds SQL queries (SQLAlchemy)
  3. Executes queries
  4. Returns entities

**Example Flow (Item Repository):**
```python
# item_repo.py
def search(self, *, q: str | None, category: str | None, available: bool | None, page: int, size: int):
    # 1. Build base query
    stmt = select(Item)
    # 2. Add filters
    if q:
        stmt = stmt.where((Item.name.like(f"%{q}%")) | (Item.description.like(f"%{q}%")))
    if category:
        stmt = stmt.where(Item.category == category)
    # 3. Add pagination
    stmt = stmt.offset((page - 1) * size).limit(size)
    # 4. Execute and return
    return list(self.db.execute(stmt).scalars())
```

### 4. **Model Layer** (`backend/app/models/`)
- **Purpose**: Data structures
- **Files**: 
  - `entities.py` - SQLAlchemy ORM models (database tables)
  - `dto.py` - Pydantic models (API request/response)

**Entities vs DTOs:**
```python
# entities.py - Database model
class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sku: Mapped[str] = mapped_column(String(64))
    # ... maps to database table

# dto.py - API model
class ItemOut(BaseModel):
    id: int
    sku: str
    # ... used for JSON serialization
    class Config:
        from_attributes = True  # Allows conversion from entity
```

---

## 🔐 Authentication Flow

### Admin Token Check
```python
# Step 1: Header extraction
authorization: str | None = Header(default=None)

# Step 2: Token parsing
token = (authorization or "").split(" ")[-1]  # "Bearer admin" → "admin"

# Step 3: Validation
def is_admin_token(token: str | None) -> bool:
    return token == "admin"

# Step 4: Dependency injection
def require_admin(authorization: ...):
    if not is_admin_token(token):
        raise Forbidden("Admin role required")
```

**Usage in endpoint:**
```python
@router.post("/admin/items")
def create_item(..., _=Depends(require_admin), ...):
    # require_admin runs FIRST, blocks if not admin
    # Only proceeds if admin token is valid
```

---

## 📊 Database Connection Flow

### Database Session Management
```python
# core/db.py
engine = create_engine("sqlite:///./cosc310.db")
SessionLocal = sessionmaker(bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db  # Provides session to endpoint
        db.commit()  # Commits on success
    except:
        db.rollback()  # Rolls back on error
        raise
    finally:
        db.close()  # Always closes connection
```

**Dependency Injection:**
```python
# FastAPI automatically calls get_db() for each request
def create_item(..., db: Session = Depends(get_db)):
    # db is automatically provided by FastAPI
    # Session is created, used, committed, closed automatically
```

---

## 🧪 Testing Architecture

### Test Structure
```
backend/tests/
  ├── unit/          # Test individual functions
  │   └── test_export_service.py
  └── integration/   # Test full API endpoints
      └── test_admin_api.py
```

### Integration Test Flow
```python
# 1. Create test database (in-memory SQLite)
engine = create_engine(f"sqlite:///{tmp_path/'t.db'}")

# 2. Override dependency
app.dependency_overrides[core_db.get_db] = _get_db

# 3. Create test client
client = TestClient(app)

# 4. Test endpoints
response = client.post("/admin/items", json={...}, headers={...})
assert response.status_code == 201
```

---

## 🔄 Request Flow Example

### Complete Request: Create Item (Admin)

```
1. HTTP Request
   POST http://127.0.0.1:8000/admin/items
   Headers: Authorization: Bearer admin
   Body: {"sku":"TEST","name":"Test","category":"tools",...}

2. FastAPI Router (admin.py)
   - Receives request
   - Validates ItemCreate DTO
   - Calls require_admin dependency

3. Security Check (require_admin)
   - Extracts token from header
   - Validates token == "admin"
   - Raises Forbidden if invalid

4. Database Dependency (get_db)
   - Creates SQLAlchemy session
   - Yields session to endpoint

5. Repository (ItemRepo)
   - Checks for duplicate SKU
   - Creates Item entity
   - Saves to database
   - Returns entity

6. Response
   - Converts Item entity → ItemOut DTO
   - Returns JSON: {"id":1,"sku":"TEST",...}
   - Status: 201 Created

7. Database Cleanup
   - Commits transaction
   - Closes session
```

---

## ❓ Important Questions & Answers

### Q1: Why separate layers (API → Service → Repo)?
**A:** Separation of concerns:
- **API**: Handles HTTP, validation, routing
- **Service**: Business logic, complex operations
- **Repo**: Simple database queries

**Benefit**: Easy to test, maintain, modify each layer independently.

### Q2: What's the difference between Entity and DTO?
**A:**
- **Entity** (`entities.py`): Database model, has SQLAlchemy mappings
- **DTO** (`dto.py`): API model, has Pydantic validation

**Example:**
```python
# Entity - from database
item = Item(id=1, sku="TEST", ...)  # SQLAlchemy object

# DTO - for API response
item_out = ItemOut.model_validate(item)  # Pydantic object → JSON
```

### Q3: How does dependency injection work?
**A:** FastAPI's `Depends()`:
```python
def get_db() -> Session:
    # This function runs for each request
    db = SessionLocal()
    yield db  # Provides db to endpoint
    db.close()  # Runs after endpoint finishes

# Usage
def endpoint(db: Session = Depends(get_db)):
    # db is automatically provided
```

### Q4: Why use `yield` in get_db?
**A:** Ensures cleanup happens:
- Code before `yield` runs before endpoint
- Code after `yield` runs after endpoint (cleanup)
- Works even if endpoint raises an error

### Q5: How does search filtering work?
**A:** Dynamic SQL query building:
```python
stmt = select(Item)  # Start with base query

# Add filters conditionally
if q:
    stmt = stmt.where(Item.name.like(f"%{q}%"))
if category:
    stmt = stmt.where(Item.category == category)

# Execute once with all filters
results = db.execute(stmt).scalars()
```

### Q6: What happens when you create an item?
**A:**
1. API validates `ItemCreate` DTO
2. Repository checks for duplicate SKU
3. Creates `Item` entity object
4. `db.add(obj)` - adds to session
5. `db.flush()` - executes INSERT (but doesn't commit yet)
6. Returns entity
7. FastAPI commits transaction (via `get_db` dependency)
8. Database saves permanently

### Q7: How does pagination work?
**A:**
```python
# Offset = skip N records
# Limit = take M records
offset = (page - 1) * size  # Page 1: skip 0, Page 2: skip 10, etc.
limit = size  # Take 10 records

stmt = stmt.offset(offset).limit(limit)
```

### Q8: Why use Pydantic models?
**A:**
- Automatic validation (type checking, required fields)
- Automatic JSON serialization
- Documentation generation (Swagger/OpenAPI)
- Type safety

### Q9: What's the difference between flush() and commit()?
**A:**
- **flush()**: Executes SQL but doesn't commit transaction (can rollback)
- **commit()**: Permanently saves changes (can't rollback)

**Why flush() in repo?**
- Gets auto-generated ID (needed for response)
- But keeps transaction open (allows rollback on error)

### Q10: How does error handling work?
**A:**
```python
# Custom exceptions (core/errors.py)
class NotFound(HTTPException):
    status_code = 404

# Usage
if not item:
    raise NotFound("Item not found")

# FastAPI automatically converts to HTTP response
```

---

## 🛠️ Common Operations

### Add a new endpoint
1. Create DTO in `models/dto.py`
2. Add route in `api/your_module.py`
3. Add service method if needed (optional)
4. Add repo method if new DB operation needed

### Add a new field to Item
1. Update `Item` entity in `models/entities.py`
2. Update `ItemOut` DTO in `models/dto.py`
3. Update `ItemCreate`/`ItemUpdate` DTOs
4. Run migration or recreate DB

### Debug a request
```python
# Add print statements
print(f"Received: {payload}")
print(f"Database: {db}")

# Check logs
# FastAPI shows request/response in console
```

---

## 📝 Key Files Overview

| File | Purpose | Key Concepts |
|------|---------|--------------|
| `main.py` | App initialization | Router registration, FastAPI app creation |
| `api/*.py` | HTTP endpoints | Routing, dependencies, request/response |
| `services/*.py` | Business logic | Data transformation, orchestration |
| `repos/*.py` | Database access | SQL queries, entity operations |
| `models/entities.py` | Database models | SQLAlchemy ORM, table definitions |
| `models/dto.py` | API models | Pydantic validation, serialization |
| `core/db.py` | Database setup | Connection, session management |
| `core/security.py` | Auth utilities | Password hashing, token validation |
| `core/errors.py` | Custom exceptions | HTTP error handling |

---

## 🎯 Quick Reference

**Start server:**
```powershell
cd backend
python -m uvicorn app.main:app --reload
```

**Test endpoint:**
```powershell
curl http://127.0.0.1:8000/items
```

**Admin endpoint:**
```powershell
curl -H "Authorization: Bearer admin" http://127.0.0.1:8000/admin/items
```

**View docs:**
```
http://127.0.0.1:8000/docs
```

**Check database:**
```powershell
sqlite3 backend/cosc310.db "SELECT * FROM items;"
```

