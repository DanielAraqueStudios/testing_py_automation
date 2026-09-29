# Sistema de Cotizaciones - Guía de Usuario

## 🚀 Descripción

Sistema profesional para generar cotizaciones HTML personalizadas con dos interfaces disponibles:

1. **Versión Consola** - `generate_quote.py` (Original)
2. **Versión GUI Moderna** - `quote_gui.py` (Nueva interfaz gráfica)

## 📋 Servicios Disponibles

- 🌐 **Desarrollo Web**: Página web ecommerce completa
- 📱 **Redes Sociales**: Estrategia integral de redes sociales
- 🤖 **Bot de WhatsApp**: Automatización inteligente 24/7
- 📢 **Campañas Facebook**: Publicidad pagada y estrategias
- 🧠 **Capacitación IA**: Formación en herramientas de IA

## 🖥️ Interfaz Gráfica (GUI) - RECOMENDADO

### Características
- ✨ Diseño moderno con tema oscuro
- 📑 Interfaz por pestañas organizadas
- ⚡ Validación en tiempo real de precios
- 🎯 Vista previa de cotizaciones
- 📊 Barra de progreso para generación
- 🔄 Threading para mejor rendimiento

### Uso
```bash
# Ejecutar la interfaz gráfica
python quote_gui.py

# O usar el launcher
python run_gui.py
```

### Flujo de Trabajo
1. **Información** - Complete datos del cliente y empresa
2. **Servicios** - Seleccione los servicios a incluir
3. **Precios** - Configure precios originales y con descuento
4. **Generar** - Cree la cotización HTML

## 🖥️ Interfaz de Consola (Original)

### Uso
```bash
python generate_quote.py
```

### Flujo de Trabajo
1. Ingrese información del cliente
2. Seleccione servicios (s/n)
3. Configure precios para servicios seleccionados
4. Defina términos de la oferta
5. La cotización se genera automáticamente

## 📁 Archivos del Sistema

- `generate_quote.py` - Versión consola original
- `quote_gui.py` - Interfaz gráfica moderna
- `run_gui.py` - Launcher para la GUI
- `template.html` - Plantilla HTML base
- `cotizacion_generada.html` - Archivo de salida
- `README.md` - Esta guía

## 🛠️ Requisitos

```bash
pip install PyQt6
```

## 🎨 Características de la GUI

### Diseño Visual
- **Tema Oscuro Profesional**: Colores #2c3e50, #34495e, #3498db
- **Tipografía Moderna**: Fuentes optimizadas para lectura
- **Iconos Intuitivos**: Emojis para mejor identificación
- **Animaciones Suaves**: Transiciones y hover effects

### Validación de Datos
- ✅ Campos obligatorios marcados
- ✅ Formato de precios automático (1.234.567)
- ✅ Validación de servicios seleccionados
- ✅ Mensajes de error descriptivos

### Experiencia de Usuario
- 🎯 Navegación por pestañas
- 🔄 Habilitación/deshabilitación dinámica
- 📊 Progreso visual de generación
- 👁️ Vista previa antes de generar
- 💾 Generación en hilo separado (no bloquea UI)

## 🚀 Ventajas de la GUI vs Consola

| Característica | GUI | Consola |
|---------------|-----|---------|
| Usabilidad | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Validación | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Diseño Visual | ⭐⭐⭐⭐⭐ | ⭐ |
| Eficiencia | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Facilidad | ⭐⭐⭐⭐⭐ | ⭐⭐ |

## 🔧 Solución de Problemas

### Error de PyQt6
```bash
pip install --upgrade pip
pip install PyQt6
```

### Error de Template
- Verifique que `template.html` existe
- Revise permisos de escritura

### Error de Generación
- Complete todos los campos obligatorios
- Seleccione al menos un servicio
- Verifique formato de precios

## 📞 Soporte

Para problemas técnicos o mejoras, contacte al desarrollador.

---
*Sistema desarrollado con PyQt6 y Python - Interfaz moderna para generación profesional de cotizaciones*