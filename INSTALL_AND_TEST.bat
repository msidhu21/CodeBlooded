@echo off
echo ========================================
echo COSC310 M3 Backend - Install and Test
echo ========================================
echo.

echo Step 1: Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo.

echo Step 2: Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo Step 3: Creating evidence directory...
if not exist "evidence" mkdir evidence
if not exist "evidence\screenshots" mkdir evidence\screenshots
echo.

echo Step 4: Running tests with coverage...
cd backend
python -m pytest -q --cov=app --cov-report=term --cov-report=xml:../evidence/coverage.xml
cd ..
echo.

echo ========================================
echo Tests completed!
echo ========================================
echo.
echo Coverage report saved to: evidence\coverage.xml
echo.
echo To start the server, run:
echo   cd backend
echo   uvicorn app.main:app --reload
echo.
echo Then visit: http://localhost:8000/docs
echo.
pause

