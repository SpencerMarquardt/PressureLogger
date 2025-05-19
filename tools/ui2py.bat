@echo off
setlocal

REM Define paths
set SCRIPT_DIR=%~dp0
set UI_DIR=%SCRIPT_DIR%..\app\ui
set VENV_PYTHON=S:\repos\PressureLogger\.venv\Scripts\python.exe

REM Navigate to the UI directory
cd /d "%UI_DIR%"

REM Debugging information
echo Current directory: %cd%
dir *.ui

REM Iterate through all .ui files in the directory
for %%f in (*.ui) do (
    echo Processing UI file: %%f
    "%VENV_PYTHON%" -m PyQt6.uic.pyuic -o "ui_%%~nf.py" "%%f"
)

echo Conversion complete! All processed files are prefixed with ui_
@REM pause
