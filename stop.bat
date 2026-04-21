@echo off
if not exist uvicorn.pid (
    echo No running API found.
    exit /b
)
set /p PID=<uvicorn.pid
set PID=%PID: =%
taskkill /PID %PID% /F
del uvicorn.pid
echo API stopped.
