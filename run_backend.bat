@echo off
setlocal
cd /d "%~dp0"
echo ========================================================
echo Starting Swachh.ai Backend (FastAPI + ChromaDB)...
echo ========================================================
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else if exist "..\.venv\Scripts\activate.bat" (
    cd ..
    call .venv\Scripts\activate.bat
) else (
    echo Virtual environment not found! Please ensure .venv exists.
)

python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
pause
