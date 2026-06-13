# ui/results_display.py
# Widget para mostrar resultados matemáticos de la ecuación de Clairaut

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QGroupBox, QScrollArea, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ResultsDisplay(QWidget):
    """
    Widget que muestra los resultados matemáticos:
    - f(p)
    - f'(p)
    - Solución general
    - Condición singular
    - Solución singular
    - Pasos de resolución
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configurar layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # Contenedor desplazable para resultados
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidget(self.scroll_content)

        # Crear grupos de resultados
        self._create_equation_group()
        self._create_function_group()
        self._create_general_solution_group()
        self._create_singular_solution_group()
        self._create_steps_group()

        self.scroll_layout.addStretch()
        self.main_layout.addWidget(self.scroll_area)
        
        # Inicializar con valores vacíos
        self.clear()
        
    def _create_equation_group(self):
        """Crea el grupo que muestra la ecuación de Clairaut y la notación p = y'"""
        self.equation_group = QGroupBox("Ecuación diferencial de Clairaut")
        self.equation_group.setFont(QFont("Arial", 10, QFont.Weight.Bold))

        layout = QVBoxLayout()

        # Ecuación original con y'
        self.eq_original_label = QLabel("y = x·y' + f(y')")
        self.eq_original_label.setFont(QFont("Arial", 11))
        self.eq_original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.eq_original_label.setStyleSheet("color: #333; padding: 4px;")
        self.eq_original_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        # Separador
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFrameShadow(QFrame.Shadow.Sunken)

        # Nota de notación
        notation_note = QLabel("Usando la notación  p = y'  la ecuación se reescribe como:")
        notation_note.setFont(QFont("Arial", 9))
        notation_note.setStyleSheet("color: #555; font-style: italic;")
        notation_note.setWordWrap(True)

        # Ecuación reescrita con p
        self.eq_p_label = QLabel("y = x·p + f(p)")
        self.eq_p_label.setFont(QFont("Arial", 11))
        self.eq_p_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.eq_p_label.setStyleSheet("color: #1a6fbf; padding: 4px; font-weight: bold;")
        self.eq_p_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        # Ecuación con f(p) sustituida (se actualiza al ingresar función)
        self.eq_substituted_label = QLabel("")
        self.eq_substituted_label.setFont(QFont("Arial", 10))
        self.eq_substituted_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.eq_substituted_label.setStyleSheet("color: #1a6fbf; padding: 2px;")
        self.eq_substituted_label.setWordWrap(True)
        self.eq_substituted_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        layout.addWidget(self.eq_original_label)
        layout.addWidget(sep)
        layout.addWidget(notation_note)
        layout.addWidget(self.eq_p_label)
        layout.addWidget(self.eq_substituted_label)

        self.equation_group.setLayout(layout)
        self.scroll_layout.addWidget(self.equation_group)

    def _create_function_group(self):
        """Crea el grupo para f(p) y f'(p)"""
        self.function_group = QGroupBox("Función y derivada")
        self.function_group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        layout = QVBoxLayout()
        
        # f(p)
        self.f_p_label = QLabel("f(p) = ")
        self.f_p_label.setFont(QFont("Arial", 10))
        self.f_p_label.setWordWrap(True)
        self.f_p_label.setMinimumHeight(30)
        self.f_p_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        # f'(p)
        self.f_prime_label = QLabel("f'(p) = ")
        self.f_prime_label.setFont(QFont("Arial", 10))
        self.f_prime_label.setWordWrap(True)
        self.f_prime_label.setMinimumHeight(30)
        self.f_prime_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        layout.addWidget(self.f_p_label)
        layout.addWidget(self.f_prime_label)
        
        self.function_group.setLayout(layout)
        self.scroll_layout.addWidget(self.function_group)
        
    def _create_general_solution_group(self):
        """Crea el grupo para la solución general"""
        self.general_group = QGroupBox("Solución general")
        self.general_group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        layout = QVBoxLayout()
        
        self.general_label = QLabel("y = ")
        self.general_label.setFont(QFont("Arial", 10))
        self.general_label.setWordWrap(True)
        self.general_label.setMinimumHeight(30)
        self.general_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        layout.addWidget(self.general_label)
        self.general_group.setLayout(layout)
        self.scroll_layout.addWidget(self.general_group)
        
    def _create_singular_solution_group(self):
        """Crea el grupo para la solución singular y condición"""
        self.singular_group = QGroupBox("Solución singular (envolvente)")
        self.singular_group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        layout = QVBoxLayout()
        
        # Condición singular
        self.condition_label = QLabel("Condición: ")
        self.condition_label.setFont(QFont("Arial", 9))
        self.condition_label.setWordWrap(True)
        self.condition_label.setMinimumHeight(25)
        self.condition_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        # Solución singular
        self.singular_label = QLabel("y = ")
        self.singular_label.setFont(QFont("Arial", 10))
        self.singular_label.setWordWrap(True)
        self.singular_label.setMinimumHeight(30)
        self.singular_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        # Línea separadora sutil
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        
        layout.addWidget(self.condition_label)
        layout.addWidget(separator)
        layout.addWidget(self.singular_label)
        
        self.singular_group.setLayout(layout)
        self.scroll_layout.addWidget(self.singular_group)

    def _create_steps_group(self):
        """Crea el grupo para mostrar los pasos de resolución"""
        self.steps_group = QGroupBox("Pasos de resolución")
        self.steps_group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        layout = QVBoxLayout()
        
        self.steps_label = QLabel("Ingrese una función para ver los pasos de resolución.")
        self.steps_label.setFont(QFont("Arial", 9))
        self.steps_label.setWordWrap(True)
        self.steps_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.steps_label.setMinimumHeight(80)
        
        layout.addWidget(self.steps_label)
        self.steps_group.setLayout(layout)
        self.scroll_layout.addWidget(self.steps_group)
        
    def display_results(self, results: dict):
        """
        Muestra los resultados en el widget.

        Args:
            results: Diccionario con los resultados formateados
                    (devuelto por ClairautEngine.format_results_for_display())
        """
        # f(p) y f'(p)
        f_p = results.get('f_p', 'No disponible')
        f_prime = results.get('f_prime', 'No disponible')

        # Actualizar ecuación sustituida en el grupo superior
        if f_p and f_p != 'No disponible':
            self.eq_substituted_label.setText(f"→  y = x·p + ({self._format_expression(f_p)})")
        else:
            self.eq_substituted_label.setText("")

        self.f_p_label.setText(f"f(p) = {self._format_expression(f_p)}")
        self.f_prime_label.setText(f"f'(p) = {self._format_expression(f_prime)}")
        
        # Solución general
        general = results.get('general', 'No disponible')
        self.general_label.setText(f"y = {self._format_expression(general)}")
        
        # Condición singular y solución singular
        condition = results.get('singular_condition', 'No aplica')
        singular = results.get('singular', 'No disponible')
        
        self.condition_label.setText(f"Condición: {condition}")
        self.singular_label.setText(f"y = {self._format_expression(singular)}")

        steps = results.get('steps', [])
        if isinstance(steps, list):
            steps_text = "\n".join(f"• {step}" for step in steps if step)
        else:
            steps_text = str(steps)

        if not steps_text:
            steps_text = "No hay pasos disponibles."

        self.steps_label.setText(steps_text)
        
        # Cambiar estilo del grupo singular si no hay solución
        has_singular = singular != 'No existe solución singular explícita'
        if has_singular and singular != 'No disponible':
            self.singular_group.setStyleSheet("""
                QGroupBox {
                    border: 2px solid #4CAF50;
                    border-radius: 5px;
                    margin-top: 10px;
                }
            """)
        else:
            self.singular_group.setStyleSheet("")
            
    def _format_expression(self, expr_str: str) -> str:
        """
        Formatea una expresión LaTeX para mejor visualización.
        """
        if not expr_str or expr_str == 'No disponible':
            return expr_str
        
        # Limitar longitud para evitar desbordamiento
        if len(expr_str) > 80:
            expr_str = expr_str[:77] + "..."
            
        return expr_str
        
    def clear(self):
        """Limpia todos los campos (sin poner Calculando...)"""
        self.eq_substituted_label.setText("")
        self.f_p_label.setText("f(p) = ")
        self.f_prime_label.setText("f'(p) = ")
        self.general_label.setText("y = ")
        self.condition_label.setText("Condición: ")
        self.singular_label.setText("y = ")
        self.steps_label.setText("Ingrese una función para ver los pasos de resolución.")
        self.singular_group.setStyleSheet("")
        
    def set_loading(self, loading: bool = True):
        """
        Muestra un estado de carga mientras se procesa.
        """
        if loading:
            self.f_p_label.setText("f(p) = Calculando...")
            self.f_prime_label.setText("f'(p) = Calculando...")
            self.general_label.setText("y = Calculando...")
            self.condition_label.setText("Condición: Calculando...")
            self.singular_label.setText("y = Calculando...")
            self.steps_label.setText("Calculando pasos...")
        else:
            # Solo limpiar si estaban en estado "Calculando..."
            if self.f_p_label.text() == "f(p) = Calculando...":
                self.f_p_label.setText("f(p) = ")
            if self.f_prime_label.text() == "f'(p) = Calculando...":
                self.f_prime_label.setText("f'(p) = ")
            if self.general_label.text() == "y = Calculando...":
                self.general_label.setText("y = ")
            if self.condition_label.text() == "Condición: Calculando...":
                self.condition_label.setText("Condición: ")
            if self.singular_label.text() == "y = Calculando...":
                self.singular_label.setText("y = ")
            if self.steps_label.text() == "Calculando pasos...":
                self.steps_label.setText("Ingrese una función para ver los pasos de resolución.")
            
    def set_error(self, message: str):
        """
        Muestra un mensaje de error en los resultados.

        Args:
            message: Mensaje de error a mostrar
        """
        self.f_p_label.setText(f"Error: {message}")
        self.f_prime_label.setText("")
        self.general_label.setText("")
        self.condition_label.setText("")
        self.singular_label.setText("")
        self.steps_label.setText("No hay pasos debido al error.")
        self.singular_group.setStyleSheet("""
            QGroupBox {
                border: 2px solid #f44336;
                border-radius: 5px;
                margin-top: 10px;
            }
        """)