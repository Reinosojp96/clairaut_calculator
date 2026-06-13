# ui/input_widget.py
# Widget para ingresar la ecuación de Clairaut en dos modos:
#   Modo 1: ingresar f(p) directamente
#   Modo 2: ingresar la ecuación completa y = xp + f(p)

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton,
                             QFrame, QMessageBox, QTabWidget)
from PyQt6.QtCore import Qt, pyqtSignal


class InputWidget(QWidget):
    """
    Widget de entrada con dos modos:
      - Pestaña 'f(p)': ingreso directo de la función f(p)
      - Pestaña 'Ecuación completa': ingreso de y = xp + algo
    Emite function_submitted(str) con la f(p) detectada en ambos casos.
    """

    function_submitted = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self._create_title()
        self._create_tabs()
        self._create_buttons()
        self._create_examples_section()
        self._create_info_section()
        self._setup_shortcuts()

    # ------------------------------------------------------------------ #
    #  Título                                                              #
    # ------------------------------------------------------------------ #

    def _create_title(self):
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

        subtitle_label = QLabel("y = x·y' + f(y')")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-style: italic;
                color: #666;
                padding-bottom: 6px;
            }
        """)
        self.main_layout.addWidget(subtitle_label)

    # ------------------------------------------------------------------ #
    #  Pestañas de modo                                                    #
    # ------------------------------------------------------------------ #

    def _create_tabs(self):
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 8px;
            }
            QTabBar::tab {
                padding: 6px 14px;
                font-size: 10px;
            }
            QTabBar::tab:selected {
                background: #4CAF50;
                color: white;
                font-weight: bold;
                border-radius: 3px;
            }
        """)

        # --- Pestaña 1: f(p) directa ---
        tab_fp = QWidget()
        layout_fp = QVBoxLayout(tab_fp)
        layout_fp.setSpacing(6)

        note_fp = QLabel("Ingrese solo la parte f(p) de la ecuación:")
        note_fp.setStyleSheet("color: #555; font-size: 10px;")
        layout_fp.addWidget(note_fp)

        form_fp = QLabel("y = x·p  +  f(p)")
        form_fp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_fp.setStyleSheet("""
            font-size: 12px; font-style: italic;
            color: #1a6fbf; padding: 4px;
        """)
        layout_fp.addWidget(form_fp)

        self.input_fp = QLineEdit()
        self.input_fp.setPlaceholderText("Ejemplo: p**2   |   sin(p)   |   1/p")
        self._style_input(self.input_fp)
        self.input_fp.returnPressed.connect(self._on_submit)
        layout_fp.addWidget(self.input_fp)

        self.tabs.addTab(tab_fp, "  Ingresar f(p)  ")

        # --- Pestaña 2: Ecuación completa ---
        tab_eq = QWidget()
        layout_eq = QVBoxLayout(tab_eq)
        layout_eq.setSpacing(6)

        note_eq = QLabel(
            "Ingrese la ecuación completa despejada en y.\n"
            "El programa detectará f(p) automáticamente."
        )
        note_eq.setWordWrap(True)
        note_eq.setStyleSheet("color: #555; font-size: 10px;")
        layout_eq.addWidget(note_eq)

        form_eq = QLabel("y  =  ...")
        form_eq.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_eq.setStyleSheet("""
            font-size: 12px; font-style: italic;
            color: #1a6fbf; padding: 4px;
        """)
        layout_eq.addWidget(form_eq)

        self.input_eq = QLineEdit()
        self.input_eq.setPlaceholderText(
            "Ejemplo: p*x - p**2   |   p*x + sqrt(1+p**2)   |   x*p - exp(p)"
        )
        self._style_input(self.input_eq)
        self.input_eq.returnPressed.connect(self._on_submit)
        layout_eq.addWidget(self.input_eq)

        # Resultado de la detección (feedback visual)
        self.detected_label = QLabel("")
        self.detected_label.setWordWrap(True)
        self.detected_label.setStyleSheet("font-size: 10px; color: #388e3c; padding-top: 4px;")
        layout_eq.addWidget(self.detected_label)

        self.tabs.addTab(tab_eq, "  Ecuación completa  ")

        # Actualizar feedback al escribir
        self.input_eq.textChanged.connect(self._update_detected_label)

        self.main_layout.addWidget(self.tabs)

    def _style_input(self, field: QLineEdit):
        field.setMinimumHeight(35)
        field.setStyleSheet("""
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

    def _update_detected_label(self, text: str):
        """Muestra en tiempo real la f(p) detectada al escribir la ecuación completa."""
        text = text.strip()
        if not text:
            self.detected_label.setText("")
            return
        try:
            f_expr = self._extract_fp_from_equation(text)
            self.detected_label.setStyleSheet(
                "font-size: 10px; color: #388e3c; padding-top: 4px;"
            )
            self.detected_label.setText(f"✔ f(p) detectada: {f_expr}")
        except Exception as e:
            self.detected_label.setStyleSheet(
                "font-size: 10px; color: #c62828; padding-top: 4px;"
            )
            self.detected_label.setText(f"✘ {e}")

    # ------------------------------------------------------------------ #
    #  Botones                                                             #
    # ------------------------------------------------------------------ #

    def _create_buttons(self):
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        self.calculate_btn = QPushButton("Calcular y Graficar")
        self.calculate_btn.setMinimumHeight(35)
        self.calculate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; color: white;
                border: none; border-radius: 4px;
                padding: 8px; font-weight: bold;
            }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:pressed { background-color: #3d8b40; }
        """)
        self.calculate_btn.clicked.connect(self._on_submit)

        self.clear_btn = QPushButton("Limpiar")
        self.clear_btn.setMinimumHeight(35)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336; color: white;
                border: none; border-radius: 4px; padding: 8px;
            }
            QPushButton:hover { background-color: #da190b; }
            QPushButton:pressed { background-color: #b71c1c; }
        """)
        self.clear_btn.clicked.connect(self.clear_input)

        buttons_layout.addWidget(self.calculate_btn)
        buttons_layout.addWidget(self.clear_btn)
        self.main_layout.addLayout(buttons_layout)

    # ------------------------------------------------------------------ #
    #  Ejemplos                                                            #
    # ------------------------------------------------------------------ #

    def _create_examples_section(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.main_layout.addWidget(separator)

        # Ejemplos para modo f(p)
        label_fp = QLabel("Ejemplos f(p):")
        label_fp.setStyleSheet("font-weight: bold; margin-top: 4px; font-size: 10px;")
        self.main_layout.addWidget(label_fp)

        row_fp = QHBoxLayout()
        row_fp.setSpacing(5)
        for lbl, expr in [("p²", "p**2"), ("p³", "p**3"), ("1/p", "1/p"),
                           ("p²+1", "p**2+1"), ("sin(p)", "sin(p)"), ("exp(p)", "exp(p)")]:
            btn = self._mini_btn(lbl)
            btn.clicked.connect(lambda _, e=expr: self._set_example_fp(e))
            row_fp.addWidget(btn)
        row_fp.addStretch()
        self.main_layout.addLayout(row_fp)

        # Ejemplos para modo ecuación completa
        label_eq = QLabel("Ejemplos ecuación completa:")
        label_eq.setStyleSheet("font-weight: bold; margin-top: 4px; font-size: 10px;")
        self.main_layout.addWidget(label_eq)

        row_eq = QHBoxLayout()
        row_eq.setSpacing(5)
        for lbl, expr in [
            ("px-p²",    "p*x - p**2"),
            ("px+√1+p²", "p*x + sqrt(1+p**2)"),
            ("xp-eᵖ",   "x*p - exp(p)"),
        ]:
            btn = self._mini_btn(lbl)
            btn.clicked.connect(lambda _, e=expr: self._set_example_eq(e))
            row_eq.addWidget(btn)
        row_eq.addStretch()
        self.main_layout.addLayout(row_eq)

    def _mini_btn(self, text: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setMaximumWidth(80)
        btn.setMaximumHeight(25)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0; border: 1px solid #ccc;
                border-radius: 3px; font-size: 10px;
            }
            QPushButton:hover { background-color: #d0d0d0; }
        """)
        return btn

    def _set_example_fp(self, expr: str):
        self.tabs.setCurrentIndex(0)
        self.input_fp.setText(expr)
        self.input_fp.setFocus()

    def _set_example_eq(self, expr: str):
        self.tabs.setCurrentIndex(1)
        self.input_eq.setText(expr)
        self.input_eq.setFocus()

    # ------------------------------------------------------------------ #
    #  Info de sintaxis                                                    #
    # ------------------------------------------------------------------ #

    def _create_info_section(self):
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5; border: 1px solid #ddd;
                border-radius: 4px; padding: 5px; margin-top: 6px;
            }
            QLabel { font-size: 10px; color: #666; }
        """)
        info_layout = QVBoxLayout(info_frame)

        title = QLabel("📐 Sintaxis válida:")
        title.setStyleSheet("font-weight: bold; color: #333;")
        info_layout.addWidget(title)

        info = QLabel(
            "• Operadores: +, -, *, /, **\n"
            "• Funciones: sin(p), cos(p), exp(p), log(p), sqrt(p)\n"
            "• Constantes: pi, E\n"
            "• Variable: p (minúscula)"
        )
        info.setWordWrap(True)
        info_layout.addWidget(info)

        self.main_layout.addWidget(info_frame)

    # ------------------------------------------------------------------ #
    #  Atajos                                                              #
    # ------------------------------------------------------------------ #

    def _setup_shortcuts(self):
        self.calculate_btn.setShortcut("Ctrl+Return")
        self.calculate_btn.setToolTip("Calcular y graficar (Ctrl+Enter)")
        self.clear_btn.setShortcut("Ctrl+L")
        self.clear_btn.setToolTip("Limpiar campo (Ctrl+L)")

    # ------------------------------------------------------------------ #
    #  Lógica de extracción de f(p) desde ecuación completa               #
    # ------------------------------------------------------------------ #

    def _extract_fp_from_equation(self, equation_str: str) -> str:
        """
        Dado 'y = expr(x, p)' o directamente 'expr(x, p)',
        extrae f(p) = expr - x*p usando SymPy.
        Lanza ValueError si la expresión no es válida.
        """
        import sympy as sp

        x, p = sp.symbols('x p')

        # Permitir que el usuario escriba con o sin 'y ='
        clean = equation_str.strip()
        if '=' in clean:
            parts = clean.split('=', 1)
            clean = parts[1].strip()

        try:
            expr = sp.sympify(clean, locals={'x': x, 'p': p})
        except Exception:
            raise ValueError("No se pudo interpretar la expresión.")

        # f(p) = expr - x*p
        f_expr = sp.simplify(expr - x * p)

        # Verificar que no quede x en f(p)
        if x in f_expr.free_symbols:
            raise ValueError("La ecuación no tiene forma y = xp + f(p): queda 'x' en f(p).")

        return str(f_expr)

    # ------------------------------------------------------------------ #
    #  Envío                                                               #
    # ------------------------------------------------------------------ #

    def _on_submit(self):
        mode = self.tabs.currentIndex()

        if mode == 0:
            # Modo f(p) directo
            f_expr = self.input_fp.text().strip()
            if not f_expr:
                QMessageBox.warning(self, "Entrada vacía",
                    "Por favor ingrese f(p).\n\nEjemplo: p**2")
                return
            self.function_submitted.emit(f_expr)

        else:
            # Modo ecuación completa
            equation = self.input_eq.text().strip()
            if not equation:
                QMessageBox.warning(self, "Entrada vacía",
                    "Por favor ingrese la ecuación completa.\n\nEjemplo: p*x - p**2")
                return
            try:
                f_expr = self._extract_fp_from_equation(equation)
            except ValueError as e:
                QMessageBox.critical(self, "Error al detectar f(p)", str(e))
                return
            self.function_submitted.emit(f_expr)

    # ------------------------------------------------------------------ #
    #  API pública                                                         #
    # ------------------------------------------------------------------ #

    def get_function(self) -> str:
        if self.tabs.currentIndex() == 0:
            return self.input_fp.text().strip()
        return self.input_eq.text().strip()

    def set_function(self, f_expr: str):
        """Establece f(p) en la pestaña de modo directo."""
        self.tabs.setCurrentIndex(0)
        self.input_fp.setText(f_expr)
        self.input_fp.setFocus()

    def clear_input(self):
        self.input_fp.clear()
        self.input_eq.clear()
        self.detected_label.setText("")
        if self.tabs.currentIndex() == 0:
            self.input_fp.setFocus()
        else:
            self.input_eq.setFocus()

    def set_loading(self, loading: bool = True):
        self.calculate_btn.setEnabled(not loading)
        self.clear_btn.setEnabled(not loading)
        self.calculate_btn.setText("Calculando..." if loading else "Calcular y Graficar")

    def focus_input(self):
        if self.tabs.currentIndex() == 0:
            self.input_fp.setFocus()
            self.input_fp.selectAll()
        else:
            self.input_eq.setFocus()
            self.input_eq.selectAll()
