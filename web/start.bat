@echo off
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"

set "PY="
where py >nul 2>&1
if not errorlevel 1 set "PY=py -3"
if not defined PY (
  where python >nul 2>&1
  if not errorlevel 1 set "PY=python"
)
if not defined PY (
  echo [ERROR] Python not found. Install Python 3.10+ and check "Add python.exe to PATH".
  echo.
  pause
  exit /b 1
)

echo ========================================
echo   juicePans local search
echo   URL: http://127.0.0.1:8765/
echo   Close this window to stop
echo ========================================
echo.

start "" /b cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:8765/"

%PY% server.py
set ERR=%ERRORLEVEL%
echo.
if not "%ERR%"=="0" (
  echo [ERROR] Server exited with code %ERR%.
  echo If port 8765 is busy, kill that process or set JUICEPANS_PORT=8766.
  echo.
  pause
  exit /b %ERR%
)
echo Stopped.
pause
