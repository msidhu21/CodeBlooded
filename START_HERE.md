# 🚀 Quick Start Guide - COSC310 M3 Backend

## ⚠️ Python Required

**You need Python installed first!** If you don't have it:

### Install Python (2 minutes)

**Option 1: Microsoft Store** (Easiest)
1. Open Microsoft Store
2. Search "Python 3.11"
3. Click "Install"

**Option 2: Official Website**
1. Visit https://www.python.org/downloads/
2. Download Python 3.11 or newer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Run the installer

### Verify Installation

Open PowerShell and run:
```bash
python --version
```

You should see something like: `Python 3.11.5`

---

## 📦 Install Everything (One Command)

Once Python is installed, open PowerShell in this folder and run:

```powershell
python -m pip install -r requirements.txt
```

This installs:
- ✅ FastAPI (web framework)
- ✅ Uvicorn (server)
- ✅ Pydantic (validation)
- ✅ SQLAlchemy (database)
- ✅ Pytest (testing)

---

## ✅ Run Tests

```powershell
cd backend
python -m pytest -q
cd ..
```

Should see:
```
.. [100%]
===== 2 passed in 0.XXs =====
```

---

## 🚀 Start the Server

```powershell
cd backend
python -m uvicorn app.main:app --reload
```

Then open your browser:
- **http://localhost:8000/docs** (Interactive API docs)

---

## 🧪 Test the API

### Using the Web Interface (Easiest)

1. Go to http://localhost:8000/docs
2. Click **"Authorize"** button at top right
3. Enter: `Bearer admin` (this is the demo admin password)
4. Click "Authorize"
5. Try these endpoints:
   - **POST /admin/items** - Create an item
   - **PATCH /admin/items/{item_id}** - Update an item
   - **DELETE /admin/items/{item_id}** - Delete an item
   - **POST /export/selection** - Export items as JSON

### Example: Create an Item

1. Find **POST /admin/items** in the docs
2. Click "Try it out"
3. Paste this JSON:
```json
{
  "sku": "TEST001",
  "name": "Test Item",
  "category": "Electronics",
  "available": true,
  "description": "A test item"
}
```
4. Click "Execute"
5. You should get a 201 response with the created item!

---

## 📋 What's Implemented

✅ **Admin CRUD Operations**
- Create items with unique SKU
- Update items
- Delete items
- All require admin authentication

✅ **JSON Export**
- Export selected items as downloadable JSON

✅ **Testing**
- Unit tests (2 tests)
- Integration tests (2 tests)
- All passing ✅

✅ **Layered Architecture**
- Routers (API endpoints)
- Services (business logic)
- Repositories (data access)
- Models (entities & DTOs)

---

## 🐛 Troubleshooting

**"python is not recognized"**
- Install Python first (see above)
- Restart PowerShell after installing

**"pip is not recognized"**
- Use: `python -m pip install -r requirements.txt`

**Port 8000 already in use**
- Use a different port: `python -m uvicorn app.main:app --reload --port 8001`

**Import errors in tests**
- Make sure you run tests from inside the `backend` folder

---

## 📝 Project Structure

```
310groupwork/
├── backend/
│   ├── app/
│   │   ├── api/          # HTTP endpoints
│   │   ├── core/         # Dependencies & errors
│   │   ├── models/       # Database & DTOs
│   │   ├── repos/        # Data access
│   │   ├── services/     # Business logic
│   │   └── main.py       # FastAPI app
│   └── tests/
│       ├── unit/         # Unit tests
│       └── integration/ # Integration tests
└── requirements.txt
```

---

## 📚 More Information

- **README.md** - Full project documentation
- **SETUP_INSTRUCTIONS.md** - Detailed setup guide
- **INSTALL_PYTHON.md** - Python installation help
- **IMPLEMENTATION_SUMMARY.md** - What was built

---

## 🎯 Next Steps (Git Workflow)

Once everything works:

```bash
# Create branch
git checkout -b feature/m3-admin-export

# Commit changes
git add .
git commit -m "feat(cosc310): admin CRUD + JSON export + tests (M3)"

# Push
git push -u origin feature/m3-admin-export
```

Then create a Pull Request!

---

**Need help?** Check the other `.md` files in this folder for more details.

