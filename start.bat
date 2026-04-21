@echo off
powershell -Command "Start-Process python -ArgumentList '-m uvicorn app.main:app --host 0.0.0.0 --port 8000' -WindowStyle Hidden -PassThru | Select-Object -ExpandProperty Id | Out-File uvicorn.pid -Encoding ASCII"
echo API started. PID saved to uvicorn.pid
exit
