@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

:: ========================================================
:: INSTALADOR INTELIGENTE - SISTEMA DE COTIZACIONES
:: Daniel Araque Studios - Version 2.0.0
:: ========================================================

color 0A
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║    SISTEMA DE COTIZACIONES AUTOMATIZADO                  ║
echo ║    Instalador Inteligente con Detección de Python        ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: ========================================================
:: PASO 1: Verificar si Python está instalado
:: ========================================================
echo [1/4] Verificando Python en el sistema...
echo.

python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python detectado en el sistema
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo    Versión instalada: !PYTHON_VERSION!
    set PYTHON_INSTALLED=1
) else (
    echo ⚠️  Python NO detectado en el sistema
    set PYTHON_INSTALLED=0
)

echo.
pause
echo.

:: ========================================================
:: PASO 2: Decisión de instalación
:: ========================================================
if !PYTHON_INSTALLED! equ 0 (
    echo [2/4] Python no está instalado
    echo.
    echo ╔═══════════════════════════════════════════════════════════╗
    echo ║  NOTA IMPORTANTE:                                         ║
    echo ║                                                           ║
    echo ║  El ejecutable Sistema_Cotizaciones.exe NO NECESITA      ║
    echo ║  Python instalado para funcionar.                        ║
    echo ║                                                           ║
    echo ║  ¿Deseas instalar Python de todas formas?                ║
    echo ║  (Útil para desarrollo o scripts personalizados)         ║
    echo ╚═══════════════════════════════════════════════════════════╝
    echo.
    
    choice /C SN /M "¿Instalar Python 3.13.2?"
    if errorlevel 2 goto :SKIP_PYTHON_INSTALL
    if errorlevel 1 goto :INSTALL_PYTHON
) else (
    echo [2/4] Python ya está instalado - Omitiendo instalación
    goto :CHECK_EXECUTABLE
)

:: ========================================================
:: PASO 3: Instalación de Python (si se solicitó)
:: ========================================================
:INSTALL_PYTHON
echo.
echo [3/4] Descargando e instalando Python 3.13.2...
echo.
echo ⏳ Este proceso puede tardar varios minutos...
echo.

:: URL de descarga de Python 3.13.2
set PYTHON_URL=https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe
set INSTALLER_PATH=%TEMP%\python_installer.exe

:: Descargar Python usando PowerShell
echo Descargando Python desde python.org...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%INSTALLER_PATH%'}"

if not exist "%INSTALLER_PATH%" (
    echo ❌ ERROR: No se pudo descargar Python
    echo    Verifica tu conexión a internet
    pause
    exit /b 1
)

:: Instalar Python silenciosamente
echo.
echo Instalando Python 3.13.2...
echo (Instalación silenciosa con opciones recomendadas)
echo.

"%INSTALLER_PATH%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

:: Esperar a que termine la instalación
timeout /t 10 /nobreak >nul

:: Verificar instalación
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python instalado exitosamente
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do echo    Versión: %%i
) else (
    echo ⚠️  Python instalado pero requiere reiniciar la consola
    echo    Cierra y vuelve a abrir esta ventana
)

:: Limpiar instalador temporal
del "%INSTALLER_PATH%" >nul 2>&1

goto :CHECK_EXECUTABLE

:SKIP_PYTHON_INSTALL
echo.
echo [3/4] Instalación de Python omitida por el usuario
echo.

:: ========================================================
:: PASO 4: Verificar y ejecutar el sistema
:: ========================================================
:CHECK_EXECUTABLE
echo.
echo [4/4] Verificando ejecutable del sistema...
echo.

if not exist "Sistema_Cotizaciones.exe" (
    echo ❌ ERROR: No se encontró Sistema_Cotizaciones.exe
    echo    Asegúrate de que este archivo está en la misma carpeta
    pause
    exit /b 1
)

echo ✅ Ejecutable encontrado
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║    INSTALACIÓN COMPLETADA                                ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo Presiona cualquier tecla para iniciar el Sistema de Cotizaciones...
pause >nul

:: Ejecutar el sistema
start "" "Sistema_Cotizaciones.exe"

echo.
echo ✅ Sistema iniciado correctamente
echo.
echo La aplicación se está ejecutando en segundo plano.
echo Puedes cerrar esta ventana de manera segura.
echo.
timeout /t 5
exit /b 0