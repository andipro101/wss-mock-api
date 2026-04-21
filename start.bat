@echo off
powershell -WindowStyle Hidden -Command "Start-Process uvicorn -ArgumentList 'app.main:app --host 0.0.0.0 --port 8000' -PassThru | Select-Object -ExpandProperty Id | Out-File uvicorn.pid"
echo API started. PID saved to uvicorn.pid
exit
