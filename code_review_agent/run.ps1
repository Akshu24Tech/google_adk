# Run ADK Web — Launch from the PARENT directory (E:\Projects\google adk\)
# This script must be run from: E:\Projects\google adk\
# NOT from inside the agent folder

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

Write-Host "Starting Code Review Agent (ADK Web)..." -ForegroundColor Cyan
Write-Host "Open: http://127.0.0.1:8000" -ForegroundColor Green
adk web
