# Quick endpoint tests for COSC 310 Backend

Write-Host "Testing server endpoints..." -ForegroundColor Cyan

# Test root
Write-Host "`n1. Testing root endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/" -Method GET
    Write-Host "✓ Root: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "  Response: $($response.Content)"
} catch {
    Write-Host "✗ Root failed: $_" -ForegroundColor Red
}

# Test docs
Write-Host "`n2. Testing /docs endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/docs" -Method GET
    Write-Host "✓ Docs: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "  Open http://127.0.0.1:8000/docs in your browser"
} catch {
    Write-Host "✗ Docs failed: $_" -ForegroundColor Red
}

# Test auth/me
Write-Host "`n3. Testing /auth/me..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/auth/me" -Method GET
    Write-Host "✓ Auth/me: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "  Response: $($response.Content)"
} catch {
    Write-Host "✗ Auth/me failed: $_" -ForegroundColor Red
}

# Test items
Write-Host "`n4. Testing /items..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/items" -Method GET
    Write-Host "✓ Items: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "  Response: $($response.Content)"
} catch {
    Write-Host "✗ Items failed: $_" -ForegroundColor Red
}

# Test admin create (with auth)
Write-Host "`n5. Testing /admin/items (create)..." -ForegroundColor Yellow
try {
    $headers = @{
        "Authorization" = "Bearer admin"
        "Content-Type" = "application/json"
    }
    $body = @{
        sku = "TEST001"
        name = "Test Item"
        category = "tools"
        available = $true
        description = "Test description"
    } | ConvertTo-Json
    
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/admin/items" -Method POST -Headers $headers -Body $body
    Write-Host "✓ Admin create: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "  Response: $($response.Content)"
} catch {
    Write-Host "✗ Admin create failed: $_" -ForegroundColor Red
}

Write-Host "`n=== Server is running at http://127.0.0.1:8000 ===" -ForegroundColor Green
Write-Host "Open http://127.0.0.1:8000/docs in your browser for interactive API docs" -ForegroundColor Cyan

