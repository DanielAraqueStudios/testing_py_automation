# Build Information - Sistema de Cotizaciones

## 📊 Información de Compilación

### Detalles del Build
- **Fecha de compilación:** 22 de Septiembre, 2025 - 11:30 PM
- **Herramienta:** PyInstaller 6.16.0
- **Python Version:** 3.13.2
- **Plataforma objetivo:** Windows 64-bit
- **Tipo de build:** Release (Producción)

### Especificaciones Técnicas
- **Ejecutable:** Sistema_Cotizaciones.exe
- **Tamaño:** 39,731,663 bytes (~38 MB)
- **Tipo:** Aplicación Windows independiente
- **Bootloader:** Windows-64bit-intel\runw.exe
- **Compresión:** Activada (archivo único)

### Dependencias Incluidas
- **PyQt6:** Framework de interfaz gráfica
- **python-docx:** Procesamiento de documentos Word
- **reportlab:** Generación de archivos PDF
- **shutil:** Utilidades de archivos del sistema
- **pathlib:** Manejo moderno de rutas de archivos
- **datetime:** Procesamiento de fechas y horas
- **re:** Expresiones regulares
- **os:** Funciones del sistema operativo

### Assets Integrados
- **template.html:** Plantilla HTML principal
- **assets/:** Carpeta completa de recursos
  - CSS: Bootstrap, Font Awesome, estilos personalizados
  - JavaScript: jQuery, plugins, funcionalidades interactivas
  - Imágenes: Logos, iconos, elementos gráficos
  - Fuentes: Tipografías personalizadas y iconos

### Configuración de PyInstaller
```bash
pyinstaller --onefile --windowed --name="Sistema_Cotizaciones" 
           --add-data="template.html;." 
           --add-data="assets;assets" 
           quote_gui.py
```

### Parámetros Utilizados
- `--onefile`: Generar un solo archivo ejecutable
- `--windowed`: Aplicación de ventana (sin consola)
- `--name`: Nombre personalizado del ejecutable
- `--add-data`: Incluir archivos de datos necesarios

### Archivos Fuente
- **quote_gui.py:** Interfaz gráfica principal
- **generate_quote.py:** Lógica de backend (importado)
- **template.html:** Plantilla HTML para cotizaciones
- **assets/:** Recursos web completos

### Testing
- ✅ Compilación exitosa sin errores
- ✅ Inclusión correcta de dependencias
- ✅ Assets integrados correctamente
- ✅ Ejecutable funcional verificado
- ✅ Tamaño optimizado para distribución

### Distribución
El ejecutable es completamente portable y puede:
- Ejecutarse sin instalación
- Copiarse a cualquier ubicación
- Ejecutarse desde medios removibles (USB)
- Distribuirse como archivo único

### Notas de Desarrollo
1. **Hooks personalizados:** PyInstaller detectó automáticamente PyQt6
2. **DLL incluidas:** Todas las librerías Qt6 necesarias
3. **Optimización:** Compilación con optimización para tamaño
4. **Compatibilidad:** Windows 10/11 64-bit

### Hash del Archivo
Para verificación de integridad, generar hash con:
```powershell
Get-FileHash -Path "Sistema_Cotizaciones.exe" -Algorithm SHA256
```

---
*Build completado exitosamente por Daniel Araque Studios*
*PyInstaller 6.16.0 | Python 3.13.2 | Windows Build Environment*