import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt6.QtCore import Qt

class SimpleQuoteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quote Generator - Test")
        self.setGeometry(100, 100, 400, 200)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        label = QLabel("PyQt6 GUI is working!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        button = QPushButton("Test Button")
        button.clicked.connect(self.on_button_click)
        
        layout.addWidget(label)
        layout.addWidget(button)
        
        # Dark theme
        self.setStyleSheet("""
            QMainWindow { background-color: #2c3e50; color: white; }
            QLabel { color: white; font-size: 16px; }
            QPushButton { background-color: #3498db; color: white; padding: 10px; }
        """)
    
    def on_button_click(self):
        print("Button clicked! GUI is working correctly.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleQuoteApp()
    window.show()
    sys.exit(app.exec())