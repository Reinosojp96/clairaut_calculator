@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Iniciando Clairaut Calculator...
echo ========================================
echo.

if not exist venv\Scripts\python.exe (
    echo [ERROR] No se encontro el entorno virtual. Ejecuta primero install.bat
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
python main.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Fallo al ejecutar main.py
    echo Verifica que el entorno virtual este activado o ejecuta install.bat nuevamente
) else (
    echo.
    echo ========================================
    echo Aplicacion cerrada correctamente
    echo ========================================
)

pause
