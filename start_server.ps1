# PillBuddy 서버 시작 스크립트
Write-Host "Starting PillBuddy Server..." -ForegroundColor Green
Write-Host ""

Set-Location backend

Write-Host "Backend will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend will be available at: http://localhost:8000/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

