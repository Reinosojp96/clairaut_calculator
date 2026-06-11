@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Instalacion - Clairaut Calculator
echo ========================================
echo.

REM Verificar si Python esta instalado
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    echo Descargalo desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] Creando entorno virtual...
if exist venv (
    echo El entorno virtual ya existe
) else (
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Fallo al crear el entorno virtual
        pause
        exit /b 1
    )
)

echo [2/3] Activando entorno...
call venv\Scripts\activate.bat

echo [3/3] Instalando dependencias...
venv\Scripts\python.exe -m pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Fallo al instalar dependencias
    pause
    exit /b 1
)

echo.
echo ========================================
echo Instalacion completada!
echo ========================================
echo.
echo Para ejecutar la aplicacion:
echo   1. Abre PowerShell en esta carpeta
echo   2. Ejecuta: .\venv\Scripts\Activate.ps1
echo   3. Ejecuta: python main.py
echo.
echo O simplemente ejecuta iniciar.bat
echo.

pause

