import sys
import re
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QFormLayout, QLabel, 
                             QLineEdit, QCheckBox, QPushButton, QTextEdit, 
                             QScrollArea, QFrame, QSpacerItem, QSizePolicy,
                             QMessageBox, QProgressBar, QTabWidget)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPixmap, QPalette, QColor, QIcon
from string import Template

class QuoteGenerator(QThread):
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self):
        try:
            # Import the backend functions
            from generate_quote import get_variables_from_data, generate_html, format_price
            
            self.progress_updated.emit(25)
            
            # Convert GUI data to backend format
            variables = get_variables_from_data(self.data)
            
            self.progress_updated.emit(50)
            
            # Use the existing backend generation logic
            current_dir = os.path.dirname(os.path.abspath(__file__))
            template_path = os.path.join(current_dir, 'template.html')
            output_path = os.path.join(current_dir, 'cotizacion_generada.html')
            
            self.progress_updated.emit(75)
            
            # Generate using the original backend function
            success = generate_html(template_path, output_path, variables)
            
            self.progress_updated.emit(100)
            
            if success:
                self.finished.emit(output_path)
            else:
                self.error_occurred.emit("Error generating HTML file")
            
        except Exception as e:
            self.error_occurred.emit(str(e))

class PriceInputWidget(QWidget):
    def __init__(self, service_name, parent=None):
        super().__init__(parent)
        self.service_name = service_name
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Original price
        self.original_input = QLineEdit()
        self.original_input.setPlaceholderText("Precio original (ej: 5000000)")
        self.original_input.setMaxLength(25)  # Allow up to 25 characters including dots
        self.original_input.textChanged.connect(self.validate_price)
        
        # Discounted price
        self.discounted_input = QLineEdit()
        self.discounted_input.setPlaceholderText("Precio con descuento (ej: 4500000)")
        self.discounted_input.setMaxLength(25)  # Allow up to 25 characters including dots
        self.discounted_input.textChanged.connect(self.validate_price)
        
        layout.addWidget(QLabel("Original:"))
        layout.addWidget(self.original_input)
        layout.addWidget(QLabel("Descuento:"))
        layout.addWidget(self.discounted_input)
    
    def validate_price(self):
        sender = self.sender()
        if not isinstance(sender, QLineEdit):
            return
        text = sender.text()
        
        # Allow up to 20 digits - remove all non-numeric characters except dots and commas
        cleaned = re.sub(r'[^\d,.-]', '', text)
        
        # Handle different decimal separator formats
        if ',' in cleaned and '.' in cleaned:
            # Format: 1,234,567.89 - remove commas (thousand separators)
            cleaned = cleaned.replace(',', '')
        elif ',' in cleaned and '.' not in cleaned:
            # Format: 1,89 - treat comma as decimal separator
            cleaned = cleaned.replace(',', '.')
        else:
            # Remove any remaining commas
            cleaned = cleaned.replace(',', '')
        
        # Remove multiple dots (keep only the first one)
        parts = cleaned.split('.')
        if len(parts) > 2:
            cleaned = parts[0] + '.' + ''.join(parts[1:])
        
        # Limit to 20 digits maximum (before decimal point)
        if '.' in cleaned:
            integer_part, decimal_part = cleaned.split('.', 1)
            if len(integer_part) > 20:
                integer_part = integer_part[:20]
            cleaned = integer_part + '.' + decimal_part
        else:
            if len(cleaned) > 20:
                cleaned = cleaned[:20]
        
        # Format for display (only if it's a valid number)
        try:
            if cleaned and cleaned != '.' and cleaned != '':
                # Check if it's a valid number first
                value = float(cleaned)
                # Format with dots as thousand separators (Colombian format)
                if value >= 1000:
                    formatted = "{:,.0f}".format(value).replace(",", ".")
                else:
                    formatted = str(int(value))
                
                # Only update if the formatted version is different
                if sender.text() != formatted:
                    cursor_pos = sender.cursorPosition()
                    sender.blockSignals(True)
                    sender.setText(formatted)
                    # Try to maintain cursor position
                    sender.setCursorPosition(min(cursor_pos, len(formatted)))
                    sender.blockSignals(False)
        except (ValueError, OverflowError):
            # If it's not a valid number, just allow the input as-is for now
            pass
    
    def get_prices(self):
        try:
            # Remove dots (thousand separators) and convert to float
            original_text = self.original_input.text().replace('.', '')
            discounted_text = self.discounted_input.text().replace('.', '')
            
            # Handle empty fields
            if not original_text.strip() or not discounted_text.strip():
                return None, None
            
            original = float(original_text)
            discounted = float(discounted_text)
            return original, discounted
        except (ValueError, OverflowError):
            return None, None
    
    def set_enabled(self, enabled):
        self.original_input.setEnabled(enabled)
        self.discounted_input.setEnabled(enabled)

class ModernQuoteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize dictionaries first
        self.services = {}
        self.price_widgets = {}
        self.setup_ui()
        self.apply_dark_theme()
        
    def setup_ui(self):
        self.setWindowTitle("Sistema de Cotizaciones - Moderno")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # Central widget with scroll area
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        self.create_header(main_layout)
        
        # Content area with tabs
        self.create_content_tabs(main_layout)
        
        # Footer with action buttons
        self.create_footer(main_layout)
    
    def create_header(self, parent_layout):
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2c3e50, stop:1 #3498db);
                border: none;
            }
        """)
        
        header_layout = QHBoxLayout(header)
        
        title_label = QLabel("Sistema de Cotizaciones")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
            }
        """)
        
        subtitle_label = QLabel("Generador profesional de propuestas")
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #ecf0f1;
                font-size: 14px;
                background: transparent;
            }
        """)
        
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        title_layout.setContentsMargins(20, 10, 10, 10)
        
        header_layout.addWidget(title_container)
        header_layout.addStretch()
        
        parent_layout.addWidget(header)
    
    def create_content_tabs(self, parent_layout):
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #34495e;
                background-color: #2c3e50;
            }
            QTabBar::tab {
                background-color: #34495e;
                color: #ecf0f1;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #4a6741;
            }
        """)
        
        # Client Information Tab
        self.create_client_tab()
        
        # Services Selection Tab
        self.create_services_tab()
        
        # Pricing Tab
        self.create_pricing_tab()
        
        parent_layout.addWidget(self.tab_widget)
    
    def create_client_tab(self):
        tab = QWidget()
        scroll = QScrollArea()
        scroll.setWidget(tab)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Client Information Section
        client_group, client_content = self.create_form_group("Información del Cliente")
        client_form = QFormLayout()
        
        self.client_names = QLineEdit()
        self.client_names.setPlaceholderText("Nombres completos del cliente")
        
        self.client_position = QLineEdit()
        self.client_position.setPlaceholderText("Cargo o posición")
        
        self.company_name = QLineEdit()
        self.company_name.setPlaceholderText("Nombre de la empresa")
        
        client_form.addRow("Cliente:", self.client_names)
        client_form.addRow("Cargo:", self.client_position)
        client_form.addRow("Empresa:", self.company_name)
        
        client_content.setLayout(client_form)
        layout.addWidget(client_group)
        
        # Sender Information Section
        sender_group, sender_content = self.create_form_group("Información del Remitente")
        sender_form = QFormLayout()
        
        self.sender_name = QLineEdit()
        self.sender_name.setPlaceholderText("Su nombre completo")
        
        self.sender_position = QLineEdit()
        self.sender_position.setPlaceholderText("Su cargo o posición")
        
        sender_form.addRow("Nombre:", self.sender_name)
        sender_form.addRow("Cargo:", self.sender_position)
        
        sender_content.setLayout(sender_form)
        layout.addWidget(sender_group)
        
        # Offer Terms Section
        terms_group, terms_content = self.create_form_group("Términos de la Oferta")
        terms_form = QFormLayout()
        
        self.validity_days = QLineEdit()
        self.validity_days.setPlaceholderText("15")
        
        self.payment_terms = QLineEdit()
        self.payment_terms.setPlaceholderText("50% firma de contrato, 50% al finalizar")
        
        terms_form.addRow("Días de validez:", self.validity_days)
        terms_form.addRow("Términos de pago:", self.payment_terms)
        
        terms_content.setLayout(terms_form)
        layout.addWidget(terms_group)
        
        layout.addStretch()
        
        self.tab_widget.addTab(scroll, "📝 Información")
    
    def create_services_tab(self):
        tab = QWidget()
        scroll = QScrollArea()
        scroll.setWidget(tab)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        services_group, services_content = self.create_form_group("Selección de Servicios")
        services_layout = QVBoxLayout()
        
        # Service checkboxes with descriptions
        services_data = [
            ("web", "🌐 Desarrollo Web", "Página web ecommerce completa con diseño responsive"),
            ("social", "📱 Redes Sociales", "Estrategia integral de redes sociales y contenido"),
            ("bot", "🤖 Bot de WhatsApp", "Automatización inteligente para atención 24/7"),
            ("facebook", "📢 Campañas Facebook", "Publicidad pagada y estrategias de tráfico"),
            ("ai", "🧠 Capacitación IA", "Formación en herramientas de inteligencia artificial")
        ]
        
        for service_key, title, description in services_data:
            service_widget = self.create_service_checkbox(service_key, title, description)
            services_layout.addWidget(service_widget)
        
        services_content.setLayout(services_layout)
        layout.addWidget(services_group)
        layout.addStretch()
        
        self.tab_widget.addTab(scroll, "⚙️ Servicios")
    
    def create_pricing_tab(self):
        tab = QWidget()
        scroll = QScrollArea()
        scroll.setWidget(tab)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        pricing_group, pricing_content = self.create_form_group("Configuración de Precios")
        pricing_layout = QVBoxLayout()
        
        # Create price input widgets for each service
        services_data = [
            ("web", "🌐 Desarrollo Web"),
            ("social", "📱 Redes Sociales"),
            ("bot", "🤖 Bot de WhatsApp"),
            ("facebook", "📢 Campañas Facebook"),
            ("ai", "🧠 Capacitación IA")
        ]
        
        for service_key, title in services_data:
            price_section = self.create_price_section(service_key, title)
            pricing_layout.addWidget(price_section)
            
        pricing_content.setLayout(pricing_layout)
        layout.addWidget(pricing_group)
        layout.addStretch()
        
        self.tab_widget.addTab(scroll, "💰 Precios")
    
    def create_form_group(self, title):
        group = QFrame()
        group.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border: 1px solid #4a6741;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        # Create main layout for the group
        main_layout = QVBoxLayout()
        
        # Add title label
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #3498db;
                font-size: 16px;
                font-weight: bold;
                background: transparent;
                border: none;
                padding: 0px 0px 10px 0px;
            }
        """)
        
        main_layout.addWidget(title_label)
        
        # Create a container widget for the form content
        content_widget = QWidget()
        main_layout.addWidget(content_widget)
        
        # Set the main layout on the group
        group.setLayout(main_layout)
        
        # Return both the group and the content widget
        return group, content_widget
    
    def create_service_checkbox(self, key, title, description):
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border: 1px solid #34495e;
                border-radius: 8px;
                padding: 15px;
                margin: 5px 0px;
            }
            QFrame:hover {
                border-color: #3498db;
                background-color: #34495e;
            }
        """)
        
        layout = QHBoxLayout(container)
        
        checkbox = QCheckBox(title)
        checkbox.setStyleSheet("""
            QCheckBox {
                color: #ecf0f1;
                font-size: 14px;
                font-weight: bold;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #7f8c8d;
                border-radius: 4px;
                background-color: transparent;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #3498db;
                border-radius: 4px;
                background-color: #3498db;
            }
        """)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            QLabel {
                color: #bdc3c7;
                font-size: 12px;
                background: transparent;
            }
        """)
        desc_label.setWordWrap(True)
        
        info_layout = QVBoxLayout()
        info_layout.addWidget(checkbox)
        info_layout.addWidget(desc_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # Connect checkbox to enable/disable pricing
        checkbox.toggled.connect(lambda checked, k=key: self.toggle_service_pricing(k, checked))
        self.services[key] = checkbox
        
        return container
    
    def create_price_section(self, key, title):
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border: 1px solid #34495e;
                border-radius: 8px;
                padding: 15px;
                margin: 5px 0px;
            }
        """)
        
        layout = QVBoxLayout(container)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #ecf0f1;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        
        price_widget = PriceInputWidget(key)
        price_widget.set_enabled(False)  # Initially disabled
        
        layout.addWidget(title_label)
        layout.addWidget(price_widget)
        
        self.price_widgets[key] = price_widget
        
        return container
    
    def toggle_service_pricing(self, service_key, enabled):
        if service_key in self.price_widgets:
            self.price_widgets[service_key].set_enabled(enabled)
    
    def create_footer(self, parent_layout):
        footer = QFrame()
        footer.setFixedHeight(80)
        footer.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-top: 1px solid #4a6741;
            }
        """)
        
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(30, 15, 30, 15)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #34495e;
                border-radius: 8px;
                text-align: center;
                color: white;
                background-color: #2c3e50;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 6px;
            }
        """)
        
        # Action buttons
        self.generate_btn = QPushButton("🚀 Generar Cotización")
        self.generate_btn.clicked.connect(self.generate_quote)
        
        self.preview_btn = QPushButton("👁️ Vista Previa")
        self.preview_btn.clicked.connect(self.preview_quote)
        
        # Button styling
        button_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton:disabled {
                background-color: #7f8c8d;
                color: #bdc3c7;
            }
        """
        
        self.generate_btn.setStyleSheet(button_style)
        self.preview_btn.setStyleSheet(button_style.replace("#3498db", "#27ae60").replace("#2980b9", "#229954").replace("#21618c", "#196f3d"))
        
        footer_layout.addWidget(self.progress_bar)
        footer_layout.addStretch()
        footer_layout.addWidget(self.preview_btn)
        footer_layout.addWidget(self.generate_btn)
        
        parent_layout.addWidget(footer)
    
    def apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QWidget {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QLineEdit {
                background-color: #34495e;
                border: 2px solid #4a6741;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                color: #ecf0f1;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
            QLineEdit:disabled {
                background-color: #2c3e50;
                color: #7f8c8d;
                border-color: #34495e;
            }
            QTextEdit {
                background-color: #34495e;
                border: 2px solid #4a6741;
                border-radius: 6px;
                padding: 8px;
                color: #ecf0f1;
            }
            QLabel {
                color: #ecf0f1;
                background: transparent;
            }
            QScrollArea {
                border: none;
                background-color: #2c3e50;
            }
            QScrollBar:vertical {
                background-color: #34495e;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #4a6741;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #3498db;
            }
        """)
    
    def validate_inputs(self):
        errors = []
        
        if not self.client_names.text().strip():
            errors.append("Nombre del cliente es requerido")
        
        if not self.company_name.text().strip():
            errors.append("Nombre de la empresa es requerido")
        
        if not self.sender_name.text().strip():
            errors.append("Nombre del remitente es requerido")
        
        # Check if at least one service is selected
        selected_services = [key for key, checkbox in self.services.items() if checkbox.isChecked()]
        if not selected_services:
            errors.append("Debe seleccionar al menos un servicio")
        
        # Validate pricing for selected services
        for service_key in selected_services:
            original, discounted = self.price_widgets[service_key].get_prices()
            if original is None or discounted is None:
                service_names = {
                    'web': 'Desarrollo Web',
                    'social': 'Redes Sociales',
                    'bot': 'Bot de WhatsApp',
                    'facebook': 'Campañas Facebook',
                    'ai': 'Capacitación IA'
                }
                errors.append(f"Precios inválidos para {service_names[service_key]}")
        
        return errors
    
    def collect_data(self):
        """Collect data from GUI in format expected by backend"""
        # Collect selected services
        selected_services = {}
        for key, checkbox in self.services.items():
            selected_services[key] = checkbox.isChecked()
        
        # Collect prices for selected services only
        prices = {}
        for service_key, checkbox in self.services.items():
            if checkbox.isChecked():
                original, discounted = self.price_widgets[service_key].get_prices()
                prices[f'{service_key}_original'] = original
                prices[f'{service_key}_discounted'] = discounted
        
        # Prepare data structure for backend
        data = {
            'client_names': self.client_names.text().strip(),
            'client_position': self.client_position.text().strip(),
            'company_name': self.company_name.text().strip(),
            'sender_name': self.sender_name.text().strip(),
            'sender_position': self.sender_position.text().strip(),
            'validity_days': self.validity_days.text().strip() or "15",
            'payment_terms': self.payment_terms.text().strip() or "50% firma de contrato, 50% al finalizar",
            'services': selected_services,
            'prices': prices
        }
        
        return data
    
    def generate_quote(self):
        errors = self.validate_inputs()
        if errors:
            QMessageBox.warning(self, "Errores de Validación", "\n".join(errors))
            return
        
        # Show progress
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.generate_btn.setEnabled(False)
        
        # Collect data
        data = self.collect_data()
        
        # Start generation thread with GUI data
        self.generator_thread = QuoteGenerator(data)
        self.generator_thread.progress_updated.connect(self.progress_bar.setValue)
        self.generator_thread.finished.connect(self.on_generation_finished)
        self.generator_thread.error_occurred.connect(self.on_generation_error)
        self.generator_thread.start()
    
    def on_generation_finished(self, output_path):
        self.progress_bar.setVisible(False)
        self.generate_btn.setEnabled(True)
        
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("¡Éxito!")
        msg.setText("Cotización generada exitosamente")
        msg.setInformativeText(f"Archivo guardado en:\n{output_path}")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
    
    def on_generation_error(self, error_message):
        self.progress_bar.setVisible(False)
        self.generate_btn.setEnabled(True)
        
        QMessageBox.critical(self, "Error", f"Error al generar la cotización:\n{error_message}")
    
    def preview_quote(self):
        errors = self.validate_inputs()
        if errors:
            QMessageBox.warning(self, "Errores de Validación", "\n".join(errors))
            return
        
        data = self.collect_data()
        
        # Create preview dialog
        preview_dialog = QMessageBox(self)
        preview_dialog.setWindowTitle("Vista Previa de Cotización")
        preview_dialog.setIcon(QMessageBox.Icon.Information)
        
        # Build services list
        services_list = []
        if data['services']['web']:
            services_list.append("• Desarrollo Web")
        if data['services']['social']:
            services_list.append("• Redes Sociales")
        if data['services']['bot']:
            services_list.append("• Bot de WhatsApp")
        if data['services']['facebook']:
            services_list.append("• Campañas Facebook")
        if data['services']['ai']:
            services_list.append("• Capacitación IA")
        
        preview_text = f"""
Cliente: {data['client_names']}
Empresa: {data['company_name']}

Servicios Seleccionados:
{chr(10).join(services_list)}

Validez: {data['validity_days']} días
Términos: {data['payment_terms']}
        """
        
        preview_dialog.setText(preview_text.strip())
        preview_dialog.exec()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    # Set application properties
    app.setApplicationName("Sistema de Cotizaciones")
    app.setApplicationVersion("2.0")
    
    window = ModernQuoteApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()