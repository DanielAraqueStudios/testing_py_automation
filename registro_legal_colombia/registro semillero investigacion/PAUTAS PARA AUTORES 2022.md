# Pautas para Autores y Mantenimiento
## Sistema de Cotizaciones HTML Automatizado

### 1. Proposito
Definir reglas para documentar, mantener y validar el proyecto de cotizaciones basado en Python y HTML.

### 2. Alcance
Aplica a:
- Scripts de consola y GUI.
- Plantilla template.html.
- Documentacion tecnica y funcional del repositorio.

### 3. Estructura recomendada para documentos
Todo documento nuevo debe incluir:
1. Titulo y fecha
2. Objetivo
3. Alcance
4. Flujo funcional
5. Reglas de negocio
6. Validaciones
7. Historial de cambios

### 4. Reglas para Python
- Validar entradas antes de convertir a float.
- Mantener funciones pequenas y claras.
- Evitar duplicar bloques HTML en varias partes.
- Conservar el punto de entrada en main().

### 5. Reglas para template.html
- Usar placeholders compatibles con string.Template.
- No mezclar sintaxis de otros motores de plantillas.
- Mantener un solo footer y un solo cierre body/html.
- Mostrar solo bloques de servicios seleccionados.

### 6. Servicios soportados
- Desarrollo web
- Redes sociales
- Bot de WhatsApp
- Campanas de Facebook
- Capacitacion en IA

### 7. Checklist antes de publicar cambios
- [ ] El script ejecuta sin excepciones.
- [ ] No hay IndentationError.
- [ ] No hay footer duplicado en la salida.
- [ ] Los servicios visibles coinciden con seleccion.
- [ ] El enlace de WhatsApp incluye nombre de empresa.

### 8. Pruebas manuales minimas
Caso A: seleccionar solo Desarrollo web.
Caso B: seleccionar Redes + Bot.
Caso C: ingresar precio invalido y verificar reintento.

### 9. Evolucion recomendada
- Agregar pruebas automaticas para validar HTML final.
- Externalizar textos comerciales por servicio.
- Reducir logica de render en strings grandes dentro de Python.
