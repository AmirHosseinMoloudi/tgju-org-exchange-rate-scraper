@echo off
echo Starting project setup for Windows...

set VENV_DIR=venv

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not found in PATH. Please install Python 3 and try again.
    goto :eof
)
echo Python found.

REM Create virtual environment if it doesn't exist
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Creating Python virtual environment in '%VENV_DIR%'...
    python -m venv "%VENV_DIR%"
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment.
        goto :eof
    )
) else (
    echo Virtual environment '%VENV_DIR%' already exists.
)

REM Activate virtual environment and install dependencies
echo Activating virtual environment and installing dependencies...
call "%VENV_DIR%\Scripts\activate.bat"

if not exist "requirements.txt" (
    echo Error: requirements.txt not found. Cannot install dependencies.
    call "%VENV_DIR%\Scripts\deactivate.bat"
    goto :eof
)

pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies from requirements.txt.
    call "%VENV_DIR%\Scripts\deactivate.bat"
    goto :eof
)

echo Dependencies installed successfully.
echo Setup complete! To activate the virtual environment in your current command prompt, run: %VENV_DIR%\Scripts\activate.bat
echo You can then run the application using: run.bat or python currency_service.py

REM Deactivate is implicitly handled when the script ends for the dependencies installation part.
REM The user needs to activate it in their own cmd window.
