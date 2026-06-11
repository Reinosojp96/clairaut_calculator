# ui/main_window.py (versión simplificada sin estilos duplicados)

import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QSplitter, QMessageBox,
                             QStatusBar, QProgressBar)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from utils.constants import APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT
from utils.error_handler import error_handler
from ui.input_widget import InputWidget
from ui.results_display import ResultsDisplay
from ui.graph_widget import GraphWidget
from controllers.clairaut_controller import ClairautController


class MainWindow(QMainWindow):
    """
    Ventana principal de la aplicación.
    Integra todos los widgets y maneja la comunicación con el controlador.
    """

    def __init__(self):
        super().__init__()
        
        # Inicializar controlador
        self.controller = ClairautController()
        
        # Configurar ventana
        self.setWindowTitle(APP_TITLE)
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Configurar widgets
        self._setup_ui()
        
        # Conectar señales
        self._connect_signals()
        
        # Configurar barra de estado
        self._setup_statusbar()
        
        error_handler.info("MainWindow", "Ventana principal inicializada")

    def _setup_ui(self):
        """Configura la interfaz de usuario"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Crear splitter para redimensionamiento
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Panel izquierdo (entrada y resultados)
        left_panel = self._create_left_panel()
        left_panel.setMinimumWidth(320)
        splitter.addWidget(left_panel)
        
        # Panel derecho (gráfica)
        right_panel = self._create_right_panel()
        splitter.addWidget(right_panel)
        
        # Configurar proporciones y comportamiento de redimensionamiento
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        splitter.setSizes([int(WINDOW_WIDTH * 0.35), int(WINDOW_WIDTH * 0.65)])
        
        main_layout.addWidget(splitter)

    def _create_left_panel(self) -> QWidget:
        """Crea el panel izquierdo con input y resultados."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        self.input_widget = InputWidget()
        layout.addWidget(self.input_widget)
        
        self.results_widget = ResultsDisplay()
        layout.addWidget(self.results_widget)
        
        layout.addStretch()
        return panel

    def _create_right_panel(self) -> QWidget:
        """Crea el panel derecho con la gráfica."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.graph_widget = GraphWidget()
        layout.addWidget(self.graph_widget)
        
        return panel

    def _connect_signals(self):
        """Conecta las señales entre widgets y controlador"""
        self.input_widget.function_submitted.connect(self._on_function_submitted)
        self.controller.function_loaded.connect(self._on_function_loaded)
        self.controller.error_occurred.connect(self._on_error)
        self.controller.plotting_data_ready.connect(self._on_plotting_data_ready)
        self.controller.processing_started.connect(self._on_processing_started)
        self.controller.processing_finished.connect(self._on_processing_finished)

    def _setup_statusbar(self):
        """Configura la barra de estado"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Listo. Ingrese una función f(p) y presione Calcular")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(150)
        self.progress_bar.setMaximumHeight(15)
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)

    def _on_function_submitted(self, f_expr: str):
        # Primero mostrar estado de carga
        self.results_widget.set_loading(True)
        # Luego limpiar gráfica
        self.graph_widget.clear()
        # Finalmente cargar función
        self.controller.load_function(f_expr)

    def _on_function_loaded(self, results: dict):
        self.results_widget.set_loading(False)
        self.results_widget.display_results(results)
        has_singular = results.get('singular', '') != 'No existe solución singular explícita'
        if has_singular:
            self.status_bar.showMessage("Función cargada. Solución singular encontrada.")
        else:
            self.status_bar.showMessage("Función cargada. No hay solución singular explícita.")

    def _on_plotting_data_ready(self, plot_data: dict):
        self.graph_widget.plot_all_solutions(
            general_data=plot_data.get('general', {}),
            singular_data=plot_data.get('singular', None),
            y_limits=plot_data.get('y_limits', None)
        )
        n_curves = len(plot_data.get('general', {}))
        has_singular = plot_data.get('has_singular', False)
        msg = f"Graficadas {n_curves} curvas de solución general"
        if has_singular:
            msg += " + envolvente"
        self.status_bar.showMessage(msg)

    def _on_error(self, title: str, message: str):
        QMessageBox.critical(self, title, message)
        self.status_bar.showMessage(f"Error: {message}", 5000)
        self._on_processing_finished()

    def _on_processing_started(self):
        self.input_widget.set_loading(True)
        self.results_widget.set_loading(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.status_bar.showMessage("Procesando...")

    def _on_processing_finished(self):
        self.input_widget.set_loading(False)
        self.progress_bar.setVisible(False)
        if not self.status_bar.currentMessage().startswith("Error"):
            self.status_bar.showMessage("Listo")

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Salir", "¿Está seguro de que desea salir?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            error_handler.info("MainWindow", "Aplicación cerrada por el usuario")
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F5:
            self._reset_application()
        else:
            super().keyPressEvent(event)

    def _reset_application(self):
        reply = QMessageBox.question(
            self, "Reiniciar", "¿Desea limpiar todo y reiniciar la aplicación?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.graph_widget.clear()
            self.results_widget.clear()
            self.input_widget.clear_input()
            self.controller.clear()
            self.status_bar.showMessage("Aplicación reiniciada")
            error_handler.info("MainWindow", "Aplicación reiniciada por el usuario")

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(100, self.input_widget.focus_input)