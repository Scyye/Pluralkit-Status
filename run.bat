@echo off
setlocal

if not exist "%~dp0.venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv "%~dp0.venv"
)

call "%~dp0.venv\Scripts\activate.bat"
python -m pip install --upgrade pip
python -m pip install -r "%~dp0requirements.txt"

echo Dependencies installed.
python.exe "%~dp0main.py"
pause
