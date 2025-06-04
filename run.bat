@echo off
echo Starting application...

set VENV_DIR=venv

REM Check if virtual environment directory exists
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Error: Virtual environment directory '%VENV_DIR%' not found.
    echo Please run the setup script first: setup.bat
    goto :eof
)

REM Activate virtual environment
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

REM Check if the main script exists in its new location
if not exist "src\tgju\currency_service.py" (
    echo Error: Main script 'src\tgju\currency_service.py' not found.
    call "%VENV_DIR%\Scripts\deactivate.bat"
    goto :eof
)

echo Setting PYTHONPATH to include src directory
set "PYTHONPATH=.\src;%PYTHONPATH%"

echo Running the application...
python -B src\tgju\currency_service.py

REM Deactivate virtual environment (optional, good practice for consistency)
REM echo Deactivating virtual environment.
REM call "%VENV_DIR%\Scripts\deactivate.bat"
REM Similar to the .sh script, deactivation is implicitly handled when the script ends.

echo Application finished.
