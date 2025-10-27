# Python Installation Guide for Windows

## Quick Installation

You need to install Python 3.9 or later to run this project.

### Option 1: Microsoft Store (Recommended for Windows)

1. Open Microsoft Store
2. Search for "Python 3.11" or "Python 3.12"
3. Click "Install"
4. After installation, open a new PowerShell or Command Prompt
5. Verify installation: `python --version`

### Option 2: Official Python Website

1. Visit https://www.python.org/downloads/
2. Download the latest Python 3.x installer (3.11 or 3.12 recommended)
3. **IMPORTANT**: During installation, check the box "Add Python to PATH"
4. Click "Install Now"
5. After installation, open a new PowerShell or Command Prompt
6. Verify installation: `python --version`
   - Should show something like: `Python 3.11.5` or `Python 3.12.x`

## After Installing Python

### 1. Verify Installation

Open PowerShell or Command Prompt and run:
```bash
python --version
pip --version
```

Both commands should show version numbers.

### 2. Install Project Dependencies

Navigate to the project directory:
```bash
cd C:\Users\thanm\Downloads\310groupwork
pip install -r requirements.txt
```

This will install:
- fastapi
- uvicorn
- pydantic
- sqlalchemy
- pytest
- pytest-cov
- httpx
- alembic

### 3. Run Tests

```bash
cd backend
pytest -q
```

### 4. Start the Server

```bash
cd backend
uvicorn app.main:app --reload
```

### 5. Visit the API Documentation

Open your browser and go to:
http://localhost:8000/docs

## Troubleshooting

**Issue: "Python is not recognized"**
- Make sure you restarted your terminal/PowerShell after installing Python
- Try using `python3` instead of `python`
- Check if Python is in your PATH environment variable

**Issue: "pip is not recognized"**
- Use `python -m pip` instead of just `pip`
- For example: `python -m pip install -r requirements.txt`

**Issue: Installer doesn't offer "Add to PATH" option**
- Install Python with the "Customize installation" option
- On the "Advanced Options" screen, check "Add Python to environment variables"

## Quick Test

After installing Python, run this to install everything:
```bash
cd C:\Users\thanm\Downloads\310groupwork
python -m pip install -r requirements.txt
cd backend
python -m pytest -q
```

If all tests pass, you're ready to go!

