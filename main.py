# main.py
# Punto de entrada de la aplicación - Visualizador de Clairaut

import sys
import traceback
from pathlib import Path

# Asegurar que el directorio actual esté en el path
sys.path.insert(0, str(Path(__file__).parent))

# Importar PyQt6
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont, QFontDatabase

# Importar utilidades básicas
from utils.constants import APP_TITLE
from utils.error_handler import error_handler

# Importar UI
from ui.main_window import MainWindow


def setup_error_handling():
    """Configurar manejo global de excepciones no capturadas"""
    def global_exception_handler(exc_type, exc_value, exc_traceback):
        """Captura cualquier excepción no manejada"""
        error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        error_handler.critical(
            module="Global",
            message=f"Excepción no capturada: {exc_value}",
            details=error_msg
        )
        print(error_msg)

    sys.excepthook = global_exception_handler


def run_application():
    """Ejecuta la aplicación PyQt6"""
    app = QApplication(sys.argv)
    
    # === CONFIGURACIÓN DE FUENTES UNIVERSAL ===
    # Probar fuentes en orden de prioridad hasta encontrar una que funcione
    font_families = [
        "Arial",           # Windows, Mac, Linux
        "Microsoft Sans Serif",  # Windows
        "DejaVu Sans",     # Linux
        "Helvetica",       # Mac
        "SansSerif",       # Fallback genérico
        "sans-serif"       # Fallback final
    ]
    
    selected_font = None
    for family in font_families:
        if family in QFontDatabase.families():
            selected_font = QFont(family, 9)
            break
    
    if selected_font is None:
        selected_font = QFont("Arial", 9)  # Fallback
    
    app.setFont(selected_font)
    
    # Aplicar hoja de estilos simple y robusta
    app.setStyleSheet("""
        * {
            font-family: "Arial", "Microsoft Sans Serif", "DejaVu Sans", "Helvetica", sans-serif;
            font-size: 9pt;
        }
        QLineEdit, QTextEdit {
            font-family: "Courier New", "Consolas", monospace;
            font-size: 10pt;
        }
        QPushButton {
            font-weight: bold;
        }
        QGroupBox {
            font-weight: bold;
            margin-top: 12px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
    """)
    
    app.setApplicationName(APP_TITLE)
    app.setOrganizationName("ClairautVisualizer")
    
    # Crear y mostrar ventana principal
    window = MainWindow()
    window.show()
    
    # Ejecutar loop de eventos
    sys.exit(app.exec())


def main():
    """Función principal - punto de entrada"""
    # Configurar manejo de errores
    setup_error_handling()
    
    # Mostrar mensaje de inicio
    print(f"🚀 Iniciando {APP_TITLE}...")
    print("📐 Versión: Completa con UI PyQt6")
    print("💡 La interfaz gráfica se abrirá en una ventana nueva")
    print("=" * 60)
    
    # Ejecutar aplicación
    run_application()


if __name__ == "__main__":
    main()