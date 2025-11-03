# Quick script to start the COSC 310 backend server
Write-Host "Starting COSC 310 Backend Server..." -ForegroundColor Cyan

cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

