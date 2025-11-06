# 📋 Historial de Cambios - Sistema de Cotizaciones

## Versión 2.1.0 - 5 de Noviembre, 2025

### 🎉 Nuevas Características

#### 📂 Botón "Abrir Carpeta"
- **Descripción:** Nuevo botón en el mensaje de éxito que abre directamente la carpeta generada
- **Beneficio:** Acceso instantáneo a los archivos sin buscar manualmente
- **Ubicación:** Aparece después de generar una cotización exitosamente
- **Compatibilidad:** Funciona en Windows, macOS y Linux

#### 🖥️ Detección Multiplataforma
- **Windows:** Usa `os.startfile()` para abrir el Explorador de Windows
- **macOS:** Usa comando `open` para abrir el Finder
- **Linux:** Usa comando `xdg-open` para abrir el gestor de archivos predeterminado

### 🐛 Correcciones de Bugs

#### ❌ Bug Crítico: Sección de Facebook Campaigns Vacía
- **Problema:** Al seleccionar "Campañas Facebook", la sección aparecía vacía en el HTML generado
- **Causa:** Línea 779 en `generate_quote.py` tenía lógica invertida: `'' if not services['facebook'] else ''`
- **Solución:** Reemplazada con el contenido HTML completo de la sección
- **Impacto:** Ahora aparecen correctamente las 3 características de las campañas de Facebook

#### ❌ Bug Crítico: Sección de Capacitación IA Vacía
- **Problema:** Al seleccionar "Capacitación IA", la sección aparecía vacía en el HTML generado
- **Causa:** Línea 780 en `generate_quote.py` tenía la misma lógica invertida
- **Solución:** Reemplazada con el contenido HTML completo de la sección
- **Impacto:** Ahora aparecen correctamente las 3 características de la capacitación

### 📝 Contenido Agregado

#### Sección Facebook Campaigns
```
✅ Videos que Conectan y Convierten
✅ Inteligencia Artificial al Servicio de tu Marca
✅ Segmentación y Resultados Medibles
```

#### Sección Capacitación IA
```
✅ Formación Práctica y Aplicada
✅ Herramientas Avanzadas de IA
✅ Soporte Continuo y Material Completo
```

### 🔧 Mejoras Técnicas

- **Importaciones nuevas:** `subprocess` y `platform`
- **Método nuevo:** `open_folder_in_explorer(folder_path)`
- **Botón personalizado:** "📂 Abrir Carpeta" en QMessageBox
- **Manejo de errores:** Try-catch para apertura de carpetas

### 📊 Impacto en el Usuario

| Característica | Antes | Ahora |
|----------------|-------|-------|
| **Acceso a carpeta** | Buscar manualmente | 1 clic en botón |
| **Sección Facebook** | ❌ Vacía | ✅ 3 características |
| **Sección IA** | ❌ Vacía | ✅ 3 características |
| **Multiplataforma** | Solo Windows | Windows + Mac + Linux |
| **Experiencia UX** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## Versión 2.0.0 - 22 de Septiembre, 2025

### 🎉 Características Iniciales

#### 🎨 Interfaz Gráfica Moderna
- Diseño con PyQt6
- Modo claro/oscuro con toggle
- Paleta de colores personalizada (#6622CC, #0E0F19, #EFE9E7)
- Pestañas organizadas (Información, Servicios, Precios)

#### 💰 Sistema de Precios Inteligente
- Cálculo automático de precio original desde precio final
- Selector de porcentaje de descuento (0-99%)
- Formateo automático de números colombianos
- Validación de hasta 20 dígitos en campos de precio

#### 📁 Generación de Estructura
- Carpetas organizadas por cliente
- Estructura `/cotizaciones/[cliente]/to_upload/`
- Copia automática de assets (CSS, JS, imágenes, fuentes)
- Generación de HTML responsive listo para web

#### ✅ Servicios Disponibles
- Desarrollo Web (E-commerce)
- Redes Sociales (Marketing Digital)
- Bot WhatsApp (Automatización)
- Campañas Facebook (Publicidad Pagada)
- Capacitación IA (Formación)

#### 🔒 Características de Seguridad
- Validación de campos obligatorios
- Sanitización de nombres de archivos
- Prevención de caracteres especiales
- Validación de formato de correos

#### 📦 Distribución
- Ejecutable independiente (.exe)
- No requiere Python instalado
- Portable (funciona desde USB)
- Tamaño optimizado (~38 MB)

---

## 🚀 Roadmap Futuro

### Versión 2.2.0 (Planeada)
- [ ] Exportar cotización a PDF
- [ ] Plantillas personalizables
- [ ] Historial de cotizaciones
- [ ] Búsqueda de clientes anteriores
- [ ] Copiar cotización existente

### Versión 2.3.0 (Planeada)
- [ ] Base de datos SQLite para clientes
- [ ] Estadísticas de ventas
- [ ] Gráficos de cotizaciones generadas
- [ ] Backup automático
- [ ] Sincronización en la nube

### Versión 3.0.0 (Futuro)
- [ ] Versión web responsive
- [ ] API REST para integraciones
- [ ] Multi-usuario con roles
- [ ] Autenticación y seguridad avanzada
- [ ] Firma digital de cotizaciones

---

## 📞 Reporte de Bugs

Si encuentras algún problema:
1. Anota la versión del software (2.1.0)
2. Describe los pasos para reproducir el error
3. Incluye capturas de pantalla si es posible
4. Contacta al desarrollador: Daniel Araque Studios

---

## 🙏 Agradecimientos

Gracias a todos los usuarios que reportaron los bugs de las secciones vacías de Facebook y IA. Sus comentarios ayudan a mejorar el sistema continuamente.

---

*Changelog actualizado el 5 de Noviembre, 2025*  
*Sistema de Cotizaciones Automatizado v2.1.0*  
*Daniel Araque Studios - Todos los derechos reservados*