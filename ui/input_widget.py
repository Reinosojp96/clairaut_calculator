# ui/input_widget.py
# Widget para ingresar la función f(p) de la ecuación de Clairaut

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, 
                             QComboBox, QFrame, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal


class InputWidget(QWidget):
    """
    Widget para ingresar la función f(p).
    Incluye campo de texto, botón de cálculo y botones de ejemplo.
    """

    # Señal que emite la función ingresada como string
    function_submitted = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configurar layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Título
        self._create_title()
        
        # Campo de entrada
        self._create_input_field()
        
        # Botones de acción
        self._create_buttons()
        
        # Ejemplos rápidos
        self._create_examples_section()
        
        # Información adicional
        self._create_info_section()
        
        # Configurar atajos de teclado
        self._setup_shortcuts()
        
    def _create_title(self):
        """Crea el título del widget"""
        title_label = QLabel("Ecuación de Clairaut")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        self.main_layout.addWidget(title_label)
        
        # Subtítulo
        subtitle_label = QLabel("y = x·y' + f(y')")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-style: italic;
                color: #666;
                padding-bottom: 10px;
            }
        """)
        self.main_layout.addWidget(subtitle_label)
        
    def _create_input_field(self):
        """Crea el campo de entrada para f(p)"""
        input_layout = QVBoxLayout()
        
        # Etiqueta
        label = QLabel("Ingrese f(p):")
        label.setStyleSheet("font-weight: bold;")
        input_layout.addWidget(label)
        
        # Campo de texto
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ejemplo: p**2, p**3, sin(p), 1/p, exp(p)")
        self.input_field.setMinimumHeight(35)
        self.input_field.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                font-size: 11px;
                font-family: monospace;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        
        # Conectar evento Enter
        self.input_field.returnPressed.connect(self._on_submit)
        
        input_layout.addWidget(self.input_field)
        
        # Añadir al layout principal
        self.main_layout.addLayout(input_layout)
        
    def _create_buttons(self):
        """Crea los botones de acción"""
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        # Botón Calcular
        self.calculate_btn = QPushButton("Calcular y Graficar")
        self.calculate_btn.setMinimumHeight(35)
        self.calculate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.calculate_btn.clicked.connect(self._on_submit)
        
        # Botón Limpiar
        self.clear_btn = QPushButton("Limpiar")
        self.clear_btn.setMinimumHeight(35)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #b71c1c;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_input)
        
        buttons_layout.addWidget(self.calculate_btn)
        buttons_layout.addWidget(self.clear_btn)
        
        self.main_layout.addLayout(buttons_layout)
        
    def _create_examples_section(self):
        """Crea una sección con ejemplos rápidos"""
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.main_layout.addWidget(separator)
        
        # Título de ejemplos
        examples_label = QLabel("Ejemplos rápidos:")
        examples_label.setStyleSheet("font-weight: bold; margin-top: 5px;")
        self.main_layout.addWidget(examples_label)
        
        # Botones de ejemplos
        examples_layout = QHBoxLayout()
        examples_layout.setSpacing(5)
        
        examples = [
            ("p²", "p**2"),
            ("p³", "p**3"),
            ("1/p", "1/p"),
            ("p²+1", "p**2 + 1"),
            ("sin(p)", "sin(p)"),
            ("exp(p)", "exp(p)"),
        ]
        
        for label_text, expr in examples:
            btn = QPushButton(label_text)
            btn.setMaximumWidth(60)
            btn.setMaximumHeight(25)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #e0e0e0;
                    border: 1px solid #ccc;
                    border-radius: 3px;
                    font-size: 10px;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
            """)
            # Usar lambda con argumento por defecto para capturar expr
            btn.clicked.connect(lambda checked, e=expr: self.set_function(e))
            examples_layout.addWidget(btn)
        
        examples_layout.addStretch()
        self.main_layout.addLayout(examples_layout)
        
    def _create_info_section(self):
        """Crea una sección con información de sintaxis"""
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
                margin-top: 10px;
            }
            QLabel {
                font-size: 10px;
                color: #666;
            }
        """)
        
        info_layout = QVBoxLayout(info_frame)
        
        info_title = QLabel("📐 Sintaxis válida:")
        info_title.setStyleSheet("font-weight: bold; color: #333;")
        info_layout.addWidget(info_title)
        
        info_text = QLabel(
            "• Operadores: +, -, *, /, **\n"
            "• Funciones: sin(p), cos(p), exp(p), log(p), sqrt(p)\n"
            "• Constantes: pi, E\n"
            "• Variable: p (minúscula)"
        )
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        
        self.main_layout.addWidget(info_frame)
        
    def _setup_shortcuts(self):
        """Configura atajos de teclado"""
        # Ctrl+Enter para calcular
        self.calculate_btn.setShortcut("Ctrl+Return")
        self.calculate_btn.setToolTip("Calcular y graficar (Ctrl+Enter)")
        
        # Ctrl+L para limpiar
        self.clear_btn.setShortcut("Ctrl+L")
        self.clear_btn.setToolTip("Limpiar campo (Ctrl+L)")
        
        # Tooltip para el campo de entrada
        self.input_field.setToolTip(
            "Ingrese f(p) usando 'p' como variable.\n"
            "Ejemplos: p**2, p**3, sin(p), 1/p, exp(p)\n"
            "Presione Enter o Ctrl+Enter para calcular"
        )
        
    def _on_submit(self):
        """Maneja el envío de la función"""
        f_expr = self.input_field.text().strip()
        
        if not f_expr:
            QMessageBox.warning(
                self, 
                "Entrada vacía", 
                "Por favor ingrese una función f(p).\n\nEjemplo: p**2, p**3, sin(p)"
            )
            return
            
        # Emitir señal con la función ingresada
        self.function_submitted.emit(f_expr)
        
    def get_function(self) -> str:
        """Retorna la función ingresada actualmente"""
        return self.input_field.text().strip()
        
    def set_function(self, f_expr: str):
        """
        Establece la función en el campo de texto.

        Args:
            f_expr: Expresión de f(p) (ej: "p**2")
        """
        self.input_field.setText(f_expr)
        self.input_field.setFocus()
        
    def clear_input(self):
        """Limpia el campo de entrada"""
        self.input_field.clear()
        self.input_field.setFocus()
        
    def set_loading(self, loading: bool = True):
        """
        Habilita/deshabilita botones durante procesamiento.

        Args:
            loading: True si está procesando
        """
        self.calculate_btn.setEnabled(not loading)
        self.clear_btn.setEnabled(not loading)
        
        if loading:
            self.calculate_btn.setText("Calculando...")
        else:
            self.calculate_btn.setText("Calcular y Graficar")
            
    def focus_input(self):
        """Pone el foco en el campo de entrada"""
        self.input_field.setFocus()
        self.input_field.selectAll()