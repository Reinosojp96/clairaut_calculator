# controllers/clairaut_controller.py
# Controlador principal que orquesta la comunicación entre UI y Core

import sympy as sp
from typing import Dict, Any, Optional, List, Tuple
from PyQt6.QtCore import QObject, pyqtSignal

from utils.error_handler import error_handler, ErrorSeverity
from controllers.dependency_container import container


class ClairautController(QObject):
    """
    Controlador para la ecuación de Clairaut.
    Maneja la comunicación entre la UI y el motor matemático.
    """

    # Señales para comunicar con la UI
    function_loaded = pyqtSignal(dict)  # Resultados cargados
    error_occurred = pyqtSignal(str, str)  # (titulo, mensaje)
    plotting_data_ready = pyqtSignal(dict)  # Datos para graficar
    processing_started = pyqtSignal()
    processing_finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.container = container
        self.current_f_expr = None
        self.current_results = None
        
        # Suscribir el controlador a errores globales
        error_handler.subscribe(self._on_global_error)
        
        error_handler.info("ClairautController", "Controlador inicializado")

    def _on_global_error(self, report):
        """Maneja errores globales y los envía a la UI"""
        if report.severity in [ErrorSeverity.ERROR, ErrorSeverity.CRITICAL]:
            self.error_occurred.emit(
                f"Error {report.severity.value}",
                f"{report.module}: {report.message}"
            )

    def load_function(self, f_expr_str: str) -> bool:
        """
        Carga una función f(p) en el motor.

        Args:
            f_expr_str: String con la expresión (ej: "p**2", "sin(p)")

        Returns:
            bool: True si se cargó correctamente, False en caso contrario
        """
        self.processing_started.emit()
        
        try:
            # 1. Validar la expresión
            is_valid, message, f_expr = self.container.validator.validate(f_expr_str)
            
            if not is_valid:
                self.error_occurred.emit("Función inválida", message)
                self.processing_finished.emit()
                return False

            # 2. Reiniciar el motor para la nueva función
            self.container.reset_engine()
            
            # 3. Cargar la función en el motor
            self.container.engine.set_f_function(f_expr)
            
            # 4. Guardar resultados
            self.current_f_expr = f_expr
            self.current_results = self.container.engine.format_results_for_display()
            
            # 5. Notificar a la UI
            self.function_loaded.emit(self.current_results)
            
            # 6. Generar datos para graficar automáticamente
            self.generate_plotting_data()
            
            error_handler.info("ClairautController", 
                f"Función cargada exitosamente: {f_expr_str}")
            
            self.processing_finished.emit()
            return True
            
        except Exception as e:
            error_handler.error("ClairautController", 
                f"Error al cargar función: {str(e)}", 
                details=str(e))
            self.error_occurred.emit("Error de procesamiento", str(e))
            self.processing_finished.emit()
            return False

    def generate_plotting_data(self) -> Optional[Dict]:
        """
        Genera los datos para graficar la familia de soluciones y la envolvente.

        Returns:
            Dict con los datos para graficar o None si hay error
        """
        try:
            plotting = self.container.plotting_utils
            
            # Generar datos para todas las soluciones generales
            general_data = plotting.generate_all_general_solutions_data()
            
            # Generar datos para solución singular (si existe)
            singular_data = plotting.generate_singular_solution_data()
            
            # Calcular límites automáticos del eje Y
            y_limits = plotting.get_y_limits(general_data, singular_data)
            
            # Preparar datos para la UI
            plot_data = {
                'general': {},
                'singular': singular_data,
                'y_limits': y_limits,
                'has_singular': plotting.has_singular_solution()
            }
            
            # Convertir datos numpy a listas para serialización (por si acaso)
            for C, (x_vals, y_vals) in general_data.items():
                plot_data['general'][C] = {
                    'x': x_vals.tolist(),
                    'y': y_vals.tolist()
                }
            
            if singular_data is not None:
                x_vals, y_vals = singular_data
                plot_data['singular'] = {
                    'x': x_vals.tolist(),
                    'y': y_vals.tolist()
                }
            
            # Notificar a la UI
            self.plotting_data_ready.emit(plot_data)
            
            error_handler.info("ClairautController", "Datos de graficación generados")
            return plot_data
            
        except Exception as e:
            error_handler.error("ClairautController", 
                f"Error al generar datos de gráfica: {str(e)}",
                details=str(e))
            self.error_occurred.emit("Error de graficación", str(e))
            self.processing_finished.emit()
            return None

    def get_general_solution_for_display(self) -> str:
        """Retorna la solución general formateada para mostrar"""
        if self.current_results:
            return self.current_results.get('general', 'No disponible')
        return 'No hay función cargada'

    def get_singular_solution_for_display(self) -> str:
        """Retorna la solución singular formateada para mostrar"""
        if self.current_results:
            return self.current_results.get('singular', 'No disponible')
        return 'No hay función cargada'

    def get_f_prime_for_display(self) -> str:
        """Retorna f'(p) formateada para mostrar"""
        if self.current_results:
            return self.current_results.get('f_prime', 'No disponible')
        return 'No hay función cargada'

    def get_singular_condition_for_display(self) -> str:
        """Retorna la condición singular formateada para mostrar"""
        if self.current_results:
            return self.current_results.get('singular_condition', 'No disponible')
        return 'No hay función cargada'

    def clear(self):
        """Limpia el estado actual del controlador"""
        self.current_f_expr = None
        self.current_results = None
        self.container.reset_engine()
        error_handler.info("ClairautController", "Estado del controlador limpiado")

    def __del__(self):
        """Limpiar suscripciones al destruir"""
        try:
            error_handler.unsubscribe(self._on_global_error)
        except:
            pass