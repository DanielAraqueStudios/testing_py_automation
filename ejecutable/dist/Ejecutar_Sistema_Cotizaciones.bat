@echo off
echo ========================================================
echo    SISTEMA DE COTIZACIONES AUTOMATIZADO
echo    Daniel Araque Studios - Version 2.0.0
echo ========================================================
echo.
echo Iniciando aplicacion...
echo.

REM Verificar si el ejecutable existe
if not exist "Sistema_Cotizaciones.exe" (
    echo ERROR: No se encontro el archivo Sistema_Cotizaciones.exe
    echo Asegurate de que este archivo .bat esta en la misma carpeta que el ejecutable
    pause
    exit /b 1
)

REM Ejecutar la aplicacion
start "" "Sistema_Cotizaciones.exe"

REM Mostrar mensaje de confirmacion
echo ✅ Aplicacion iniciada correctamente
echo.
echo La interfaz grafica deberia aparecer en unos momentos.
echo Si no aparece, revisa que no este bloqueada por el antivirus.
echo.
echo Puedes cerrar esta ventana ahora.
echo.
pause