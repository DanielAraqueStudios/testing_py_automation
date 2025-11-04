# ========================================================
# INSTALADOR INTELIGENTE - SISTEMA DE COTIZACIONES
# Daniel Araque Studios - Version 2.0.0
# PowerShell Script con detección y instalación automática
# ========================================================

# Configurar ventana
$host.UI.RawUI.WindowTitle = "Instalador Sistema de Cotizaciones"
$host.UI.RawUI.BackgroundColor = "Black"
$host.UI.RawUI.ForegroundColor = "Green"
Clear-Host

# Función para escribir con colores
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Banner de inicio
Write-ColorOutput "`n╔═══════════════════════════════════════════════════════════╗" "Cyan"
Write-ColorOutput "║                                                           ║" "Cyan"
Write-ColorOutput "║    SISTEMA DE COTIZACIONES AUTOMATIZADO                  ║" "Cyan"
Write-ColorOutput "║    Instalador Inteligente con Detección de Python        ║" "Cyan"
Write-ColorOutput "║    Daniel Araque Studios - v2.0.0                        ║" "Cyan"
Write-ColorOutput "║                                                           ║" "Cyan"
Write-ColorOutput "╚═══════════════════════════════════════════════════════════╝`n" "Cyan"

# ========================================================
# PASO 1: Verificar Python
# ========================================================
Write-ColorOutput "[1/5] Verificando instalación de Python..." "Yellow"
Write-Host ""

$pythonInstalled = $false
$pythonVersion = $null

try {
    $pythonCheck = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $pythonInstalled = $true
        $pythonVersion = ($pythonCheck -split " ")[1]
        Write-ColorOutput "✅ Python detectado en el sistema" "Green"
        Write-ColorOutput "   Versión instalada: $pythonVersion" "Gray"
    }
} catch {
    Write-ColorOutput "⚠️  Python NO detectado en el sistema" "Red"
}

Write-Host ""
Start-Sleep -Seconds 2

# ========================================================
# PASO 2: Información importante
# ========================================================
Write-ColorOutput "[2/5] Análisis de requisitos..." "Yellow"
Write-Host ""

if (-not $pythonInstalled) {
    Write-ColorOutput "╔═══════════════════════════════════════════════════════════╗" "Magenta"
    Write-ColorOutput "║  NOTA IMPORTANTE:                                         ║" "Magenta"
    Write-ColorOutput "║                                                           ║" "White"
    Write-ColorOutput "║  El ejecutable Sistema_Cotizaciones.exe es PORTABLE      ║" "White"
    Write-ColorOutput "║  y NO NECESITA Python instalado para funcionar.          ║" "White"
    Write-ColorOutput "║                                                           ║" "White"
    Write-ColorOutput "║  Python solo es necesario si planeas:                    ║" "White"
    Write-ColorOutput "║  • Modificar el código fuente                            ║" "Gray"
    Write-ColorOutput "║  • Ejecutar scripts personalizados                       ║" "Gray"
    Write-ColorOutput "║  • Desarrollo o debugging avanzado                       ║" "Gray"
    Write-ColorOutput "║                                                           ║" "White"
    Write-ColorOutput "╚═══════════════════════════════════════════════════════════╝" "Magenta"
    Write-Host ""
    
    $installPython = Read-Host "¿Deseas instalar Python de todas formas? (S/N)"
    
    if ($installPython -notmatch '^[Ss]$') {
        Write-ColorOutput "`n⏭️  Instalación de Python omitida" "Yellow"
        $pythonInstalled = $true  # Continuar sin Python
    }
} else {
    Write-ColorOutput "✅ Python ya está instalado - No se requiere acción" "Green"
}

Write-Host ""
Start-Sleep -Seconds 1

# ========================================================
# PASO 3: Descargar Python si es necesario
# ========================================================
if (-not $pythonInstalled) {
    Write-ColorOutput "[3/5] Descargando Python 3.13.2..." "Yellow"
    Write-Host ""
    
    $pythonUrl = "https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe"
    $installerPath = "$env:TEMP\python_installer.exe"
    
    try {
        Write-ColorOutput "⏳ Descargando desde python.org..." "Cyan"
        Write-ColorOutput "   URL: $pythonUrl" "Gray"
        Write-Host ""
        
        # Descargar con barra de progreso
        $ProgressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath -UseBasicParsing
        $ProgressPreference = 'Continue'
        
        Write-ColorOutput "✅ Descarga completada" "Green"
        $fileSize = [math]::Round((Get-Item $installerPath).Length / 1MB, 2)
        Write-ColorOutput "   Tamaño: $fileSize MB" "Gray"
        
    } catch {
        Write-ColorOutput "❌ ERROR: No se pudo descargar Python" "Red"
        Write-ColorOutput "   Verifica tu conexión a internet" "Red"
        Write-Host ""
        Read-Host "Presiona Enter para continuar sin Python"
        goto SkipPythonInstall
    }
    
    Write-Host ""
    Start-Sleep -Seconds 2
    
    # ========================================================
    # PASO 4: Instalar Python
    # ========================================================
    Write-ColorOutput "[4/5] Instalando Python 3.13.2..." "Yellow"
    Write-Host ""
    Write-ColorOutput "⏳ Este proceso puede tardar varios minutos..." "Cyan"
    Write-ColorOutput "   Por favor espera sin cerrar esta ventana" "Gray"
    Write-Host ""
    
    try {
        # Instalar Python silenciosamente con todas las opciones
        $installArgs = @(
            "/quiet",
            "InstallAllUsers=1",
            "PrependPath=1",
            "Include_test=0",
            "Include_doc=0",
            "Include_pip=1",
            "Include_tcltk=0"
        )
        
        $process = Start-Process -FilePath $installerPath -ArgumentList $installArgs -Wait -PassThru
        
        if ($process.ExitCode -eq 0) {
            Write-ColorOutput "✅ Python instalado exitosamente" "Green"
            
            # Refrescar las variables de entorno
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
            
            # Verificar instalación
            Start-Sleep -Seconds 3
            try {
                $pythonCheck = python --version 2>&1
                Write-ColorOutput "   Versión: $pythonCheck" "Gray"
            } catch {
                Write-ColorOutput "⚠️  Python instalado correctamente" "Yellow"
                Write-ColorOutput "   NOTA: Es posible que necesites reiniciar la terminal" "Yellow"
            }
            
        } else {
            Write-ColorOutput "⚠️  Instalación completada con advertencias" "Yellow"
            Write-ColorOutput "   Código de salida: $($process.ExitCode)" "Gray"
        }
        
        # Limpiar instalador
        Remove-Item $installerPath -Force -ErrorAction SilentlyContinue
        
    } catch {
        Write-ColorOutput "❌ ERROR durante la instalación de Python" "Red"
        Write-ColorOutput "   $($_.Exception.Message)" "Red"
    }
    
    Write-Host ""
    Start-Sleep -Seconds 2
}

# ========================================================
# PASO 5: Verificar y ejecutar el sistema
# ========================================================
:SkipPythonInstall
Write-ColorOutput "[5/5] Verificando Sistema de Cotizaciones..." "Yellow"
Write-Host ""

$exePath = Join-Path $PSScriptRoot "Sistema_Cotizaciones.exe"

if (-not (Test-Path $exePath)) {
    Write-ColorOutput "❌ ERROR: No se encontró Sistema_Cotizaciones.exe" "Red"
    Write-ColorOutput "   Ruta esperada: $exePath" "Gray"
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-ColorOutput "✅ Ejecutable encontrado" "Green"
$exeSize = [math]::Round((Get-Item $exePath).Length / 1MB, 2)
Write-ColorOutput "   Tamaño: $exeSize MB" "Gray"
Write-ColorOutput "   Ubicación: $exePath" "Gray"

Write-Host ""
Start-Sleep -Seconds 1

# ========================================================
# Resumen final
# ========================================================
Write-ColorOutput "`n╔═══════════════════════════════════════════════════════════╗" "Green"
Write-ColorOutput "║                                                           ║" "Green"
Write-ColorOutput "║    ✅ INSTALACIÓN COMPLETADA EXITOSAMENTE                ║" "Green"
Write-ColorOutput "║                                                           ║" "Green"
Write-ColorOutput "╚═══════════════════════════════════════════════════════════╝" "Green"

Write-Host ""
Write-ColorOutput "📊 RESUMEN:" "Cyan"
if ($pythonVersion) {
    Write-ColorOutput "   • Python: Instalado (v$pythonVersion)" "Gray"
} else {
    Write-ColorOutput "   • Python: No requerido (ejecutable independiente)" "Gray"
}
Write-ColorOutput "   • Ejecutable: Listo para usar" "Gray"
Write-ColorOutput "   • Tamaño: $exeSize MB" "Gray"

Write-Host ""
Write-ColorOutput "🚀 Presiona cualquier tecla para iniciar el sistema..." "Yellow"
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Ejecutar el sistema
try {
    Start-Process -FilePath $exePath
    Write-Host ""
    Write-ColorOutput "✅ Sistema iniciado correctamente" "Green"
    Write-Host ""
    Write-ColorOutput "La aplicación se está ejecutando." "White"
    Write-ColorOutput "Puedes cerrar esta ventana de manera segura." "Gray"
    Write-Host ""
} catch {
    Write-ColorOutput "❌ ERROR al iniciar el sistema" "Red"
    Write-ColorOutput "   $($_.Exception.Message)" "Red"
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Start-Sleep -Seconds 3
exit 0