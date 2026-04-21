@echo off
start /B uvicorn app.main:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1
timeout /t 2 /nobreak > nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do echo %%a > uvicorn.pid & goto :done
:done
echo API started. PID saved to uvicorn.pid
exit
