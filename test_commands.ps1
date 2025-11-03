# Admin Auth Tests
Write-Host "=== Admin Auth Tests ===" -ForegroundColor Cyan

# 1. Test WITHOUT auth (should fail with 403)
Write-Host "`n1. Testing WITHOUT auth (should fail):" -ForegroundColor Yellow
Invoke-RestMethod -Uri "http://127.0.0.1:8000/admin/items" -Method Post -Body '{"sku":"TEST","name":"Test","category":"tools","available":true,"description":""}' -ContentType "application/json" -ErrorAction SilentlyContinue

# 2. Test WITH wrong token (should fail with 403)
Write-Host "`n2. Testing WITH wrong token (should fail):" -ForegroundColor Yellow
$headers = @{"Authorization" = "Bearer wrongtoken"}
Invoke-RestMethod -Uri "http://127.0.0.1:8000/admin/items" -Method Post -Headers $headers -Body '{"sku":"TEST","name":"Test","category":"tools","available":true,"description":""}' -ContentType "application/json" -ErrorAction SilentlyContinue

# 3. Test WITH correct token (should work)
Write-Host "`n3. Testing WITH 'Bearer admin' (should work):" -ForegroundColor Yellow
$headers = @{"Authorization" = "Bearer admin"}
$result = Invoke-RestMethod -Uri "http://127.0.0.1:8000/admin/items" -Method Post -Headers $headers -Body '{"sku":"TEST001","name":"Test Item","category":"tools","available":true,"description":"Test"}' -ContentType "application/json"
Write-Host "Created item ID: $($result.id)" -ForegroundColor Green
$itemId = $result.id

# Items Search Tests
Write-Host "`n=== Items Search Tests ===" -ForegroundColor Cyan

# 4. Test with all parameters
Write-Host "`n4. Testing /items with ALL parameters:" -ForegroundColor Yellow
Invoke-RestMethod -Uri "http://127.0.0.1:8000/items?q=test&category=tools&available=true&page=1&size=10"

# 5. Test with partial parameters
Write-Host "`n5. Testing /items with partial params (q only):" -ForegroundColor Yellow
Invoke-RestMethod -Uri "http://127.0.0.1:8000/items?q=test"

# 6. Test with no parameters
Write-Host "`n6. Testing /items with NO parameters:" -ForegroundColor Yellow
Invoke-RestMethod -Uri "http://127.0.0.1:8000/items"

# Cleanup
Write-Host "`n7. Cleaning up test item:" -ForegroundColor Yellow
$headers = @{"Authorization" = "Bearer admin"}
Invoke-RestMethod -Uri "http://127.0.0.1:8000/admin/items/$itemId" -Method Delete -Headers $headers -ErrorAction SilentlyContinue

Write-Host "`n=== Done ===" -ForegroundColor Cyan

