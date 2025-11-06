# Sistema de Cotizaciones Automatizado - Ejecutable

## 📦 Información del Ejecutable

### Archivo Generado
- **Nombre:** `Sistema_Cotizaciones.exe`
- **Versión:** 2.1.0
- **Tamaño:** ~38 MB
- **Tipo:** Ejecutable independiente (standalone)
- **Plataforma:** Windows 64-bit
- **Fecha de generación:** 5 de Noviembre, 2025
- **Última actualización:** 5 de Noviembre, 2025

### 🚀 Cómo Usar el Ejecutable

#### Instalación
1. **No requiere instalación** - Es un ejecutable independiente
2. Simplemente haz doble clic en `Sistema_Cotizaciones.exe`
3. La aplicación se ejecutará directamente

#### Requisitos del Sistema
- **Sistema Operativo:** Windows 10 o superior
- **Arquitectura:** 64-bit
- **Memoria RAM:** Mínimo 4 GB (recomendado 8 GB)
- **Espacio en disco:** 100 MB para el ejecutable + espacio para cotizaciones generadas

#### Primera Ejecución
1. Ejecutar `Sistema_Cotizaciones.exe`
2. La interfaz gráfica se abrirá automáticamente
3. Completar los datos en las pestañas correspondientes
4. Generar la primera cotización de prueba

### 📁 Estructura de Archivos Generados

Cuando uses el ejecutable, se crearán automáticamente:

```
[Directorio del ejecutable]/
├── cotizaciones/
│   └── [nombre_cliente]/
│       └── to_upload/
│           ├── index.html
│           └── assets/
│               ├── css/
│               ├── js/
│               ├── images/
│               └── fonts/
└── (archivos temporales del sistema)
```

### ⚙️ Características Incluidas

✅ **Interfaz Gráfica Completa**
- Pestañas organizadas para fácil navegación
- Validación automática de campos
- Modo claro/oscuro con toggle
- Cálculo automático de precios con descuento
- **NUEVO:** Botón para abrir carpeta generada directamente

✅ **Generación Automática**
- Crear estructura completa de archivos
- HTML responsive listo para web
- Copia automática de recursos (CSS, JS, imágenes)
- Organización por cliente
- **NUEVO:** Mensaje de éxito con acceso directo a la carpeta

✅ **Funcionalidades Avanzadas**
- Cálculo inverso de precios (precio final → precio original)
- Formateo automático de números colombianos
- Sanitización de nombres de archivos
- Validación de datos de entrada
- **NUEVO:** Apertura automática del explorador de archivos

✅ **Compatibilidad Multiplataforma**
- **NUEVO:** Detección automática del sistema operativo
- **NUEVO:** Soporte para Windows, macOS y Linux
- **NUEVO:** Apertura de carpetas nativa en cada plataforma

### 🔧 Configuración y Personalización

#### Modificar Templates
El ejecutable incluye el template HTML integrado. Para personalizaciones avanzadas:
1. Mantén una copia del proyecto fuente Python
2. Modifica `template.html` según necesidades
3. Regenera el ejecutable con PyInstaller

#### Servicios Disponibles
- ✅ Desarrollo Web (E-commerce)
- ✅ Redes Sociales (Marketing Digital)
- ✅ Bot WhatsApp (Automatización)
- ✅ Campañas Facebook (Publicidad Pagada)
- ✅ Capacitación IA (Formación)

### 🐛 Solución de Problemas

#### Problema: "El ejecutable no inicia"
**Soluciones:**
- Ejecutar como administrador
- Verificar que no esté bloqueado por antivirus
- Asegurar que Windows esté actualizado

#### Problema: "No se crean las carpetas"
**Soluciones:**
- Verificar permisos de escritura en el directorio
- Ejecutar desde una ubicación con permisos completos
- Revisar que el nombre del cliente no tenga caracteres especiales

#### Problema: "Error al abrir archivos HTML"
**Soluciones:**
- Verificar que se creó la carpeta `assets`
- Abrir `index.html` desde la carpeta `to_upload`
- Verificar conexión a internet para fuentes externas

### 📊 Rendimiento

#### Tiempo de Inicio
- **Primera ejecución:** 3-5 segundos
- **Ejecuciones posteriores:** 1-2 segundos

#### Tiempo de Generación
- **Cotización simple:** <1 segundo
- **Cotización completa:** 1-2 segundos
- **Múltiples cotizaciones:** Variable según cantidad

### 🔒 Seguridad

#### Antivirus
- El ejecutable puede ser marcado como "desconocido" por algunos antivirus
- Es seguro - generado con PyInstaller oficial
- Agregar excepción si es necesario

#### Datos del Cliente
- Los datos NO se envían a internet
- Todo se procesa localmente
- Archivos generados permanecen en tu computadora

### 📞 Soporte Técnico

#### Información de Contacto
**Desarrollador:** Daniel Araque Studios  
**Versión:** 2.0.0  
**Fecha:** Septiembre 2025  

#### Para Actualizaciones
- Contactar al desarrollador para nuevas versiones
- Mantener backup de cotizaciones importantes
- Revisar periódicamente si hay actualizaciones

### 🎯 Casos de Uso Recomendados

#### Uso Diario
1. **Cotizaciones Rápidas:** Clientes nuevos con servicios estándar
2. **Presentaciones:** Generar HTML para mostrar en reuniones
3. **Seguimiento:** Mantener historial organizado por cliente

#### Uso Avanzado
1. **Personalización:** Adaptar precios según mercado
2. **Análisis:** Revisar cotizaciones anteriores para tendencias
3. **Automatización:** Generar múltiples versiones para comparación

---

### 📝 Notas Importantes

- **Ejecutable Portable:** No requiere instalación, puede ejecutarse desde USB
- **Sin Dependencias:** Incluye todas las librerías necesarias
- **Multiplataforma:** Esta versión es específica para Windows
- **Backup Recomendado:** Mantener copias de seguridad del ejecutable

---

*Ejecutable generado automáticamente con PyInstaller 6.16.0*  
*Python 3.13.2 | PyQt6 | Daniel Araque Studios*