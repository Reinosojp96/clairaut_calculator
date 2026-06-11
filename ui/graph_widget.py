# ui/graph_widget.py
# Widget para visualización de gráficas con matplotlib embebido

import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from utils.constants import (
    X_LABEL, Y_LABEL, APP_TITLE,
    DEFAULT_LINEWIDTH, SINGULAR_LINEWIDTH, SINGULAR_COLOR,
    GENERAL_LINESTYLE, GENERAL_COLORMAP,
    X_MIN, X_MAX, Y_MANUAL_MIN, Y_MANUAL_MAX, Y_MIN_AUTO
)


class GraphWidget(QWidget):
    """
    Widget que contiene una figura de matplotlib con su toolbar.
    Permite graficar la familia de soluciones y la envolvente.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Crear la figura y el canvas
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumSize(600, 400)
        
        # Agregar toolbar de navegación (zoom, pan, guardar, etc.)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        # Crear layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        # Referencias a los ejes y líneas
        self.ax = self.figure.add_subplot(111)
        self.general_lines = {}  # {C_value: line_object}
        self.singular_line = None
        
        # Configuración inicial del gráfico
        self._setup_axes()
        
    def _setup_axes(self):
        """Configura los ejes y la apariencia inicial"""
        self.ax.set_xlabel(X_LABEL, fontsize=12)
        self.ax.set_ylabel(Y_LABEL, fontsize=12)
        self.ax.set_title(APP_TITLE, fontsize=14, fontweight='bold')
        self.ax.grid(True, linestyle=':', alpha=0.6)
        self.ax.axhline(y=0, color='black', linewidth=0.8, linestyle='-')
        self.ax.axvline(x=0, color='black', linewidth=0.8, linestyle='-')
        self.ax.set_xlim(X_MIN, X_MAX)
        
        # Colores para las líneas de la solución general
        self.cmap = plt.get_cmap(GENERAL_COLORMAP)
        
    def clear(self):
        """Limpia todas las líneas del gráfico"""
        # Eliminar líneas de solución general
        for line in self.general_lines.values():
            line.remove()
        self.general_lines.clear()
        
        # Eliminar línea de solución singular
        if self.singular_line is not None:
            self.singular_line.remove()
            self.singular_line = None
        
        # Actualizar leyenda
        self._update_legend()
        
        # Refrescar canvas
        self.canvas.draw_idle()
        
    def plot_general_solution(self, C_value: float, x_vals: np.ndarray, y_vals: np.ndarray):
        """
        Grafica una curva de la solución general para un valor específico de C.

        Args:
            C_value: Valor de la constante C
            x_vals: Array de valores de x
            y_vals: Array de valores de y
        """
        # Obtener color basado en C_value (normalizado entre -3 y 3)
        norm_c = (C_value + 3) / 6  # Mapea -3..3 a 0..1
        color = self.cmap(norm_c)
        
        # Crear línea
        line, = self.ax.plot(x_vals, y_vals, 
                             linestyle=GENERAL_LINESTYLE,
                             linewidth=DEFAULT_LINEWIDTH,
                             color=color,
                             label=f'C = {C_value}')
        
        # Guardar referencia
        self.general_lines[C_value] = line
        
        # Actualizar leyenda
        self._update_legend()
        
        # Refrescar canvas
        self.canvas.draw_idle()
        
    def plot_singular_solution(self, x_vals: np.ndarray, y_vals: np.ndarray):
        """
        Grafica la solución singular (envolvente).

        Args:
            x_vals: Array de valores de x
            y_vals: Array de valores de y
        """
        # Eliminar línea anterior si existe
        if self.singular_line is not None:
            self.singular_line.remove()
        
        # Crear nueva línea
        self.singular_line, = self.ax.plot(x_vals, y_vals,
                                            linestyle='-',
                                            linewidth=SINGULAR_LINEWIDTH,
                                            color=SINGULAR_COLOR,
                                            label='Solución singular (envolvente)')
        
        # Actualizar leyenda
        self._update_legend()
        
        # Refrescar canvas
        self.canvas.draw_idle()
        
    # ui/graph_widget.py - Modificar plot_all_solutions

    def plot_all_solutions(self, general_data: dict, singular_data: dict = None, y_limits: tuple = None):
        """
        Grafica todas las soluciones de una vez.

        Args:
            general_data: Diccionario {C_value: {'x': list, 'y': list}}
            singular_data: Diccionario {'x': list, 'y': list} o None
            y_limits: Tupla (y_min, y_max) para ajustar el eje Y
        """
        self.clear()
        
        # Graficar soluciones generales
        for C_value, data in general_data.items():
            x_vals = np.array(data['x']) if isinstance(data, dict) else data[0]
            y_vals = np.array(data['y']) if isinstance(data, dict) else data[1]
            
            # Asegurar dimensiones correctas
            if len(y_vals) != len(x_vals):
                continue
                
            self.plot_general_solution(C_value, x_vals, y_vals)
        
        # Graficar solución singular si existe
        if singular_data is not None:
            if isinstance(singular_data, dict):
                x_vals = np.array(singular_data['x'])
                y_vals = np.array(singular_data['y'])
            else:
                x_vals, y_vals = singular_data
            
            if len(y_vals) == len(x_vals):
                self.plot_singular_solution(x_vals, y_vals)
        
        # Ajustar límites del eje Y
        self.set_y_limits(y_limits)
        
    def set_y_limits(self, y_limits: tuple = None):
        """
        Ajusta los límites del eje Y.

        Args:
            y_limits: Tupla (y_min, y_max) o None para automático
        """
        if y_limits is not None:
            y_min, y_max = y_limits
            # Limitar a valores razonables para evitar gráficas extremas
            y_min = max(y_min, -50) if not np.isinf(y_min) else Y_MANUAL_MIN
            y_max = min(y_max, 50) if not np.isinf(y_max) else Y_MANUAL_MAX
            self.ax.set_ylim(y_min, y_max)
        elif not Y_MIN_AUTO:
            self.ax.set_ylim(Y_MANUAL_MIN, Y_MANUAL_MAX)
        # Si es automático, matplotlib ajusta automáticamente
        
        self.canvas.draw_idle()
        
    def _update_legend(self):
        """Actualiza la leyenda del gráfico"""
        # Obtener líneas actuales que tienen label
        lines_with_labels = []
        for line in self.general_lines.values():
            if line.get_label() and line.get_visible():
                lines_with_labels.append(line)
        
        if self.singular_line is not None and self.singular_line.get_visible():
            lines_with_labels.append(self.singular_line)
        
        if lines_with_labels:
            self.ax.legend(loc='best', fontsize=9, title='Soluciones')
        else:
            # Ocultar leyenda si no hay líneas
            legend = self.ax.get_legend()
            if legend:
                legend.remove()
                
    def set_title(self, title: str):
        """Cambia el título del gráfico"""
        self.ax.set_title(title, fontsize=14, fontweight='bold')
        self.canvas.draw_idle()
        
    def set_x_limits(self, x_min: float, x_max: float):
        """Ajusta los límites del eje X"""
        self.ax.set_xlim(x_min, x_max)
        self.canvas.draw_idle()
        
    def save_figure(self, filename: str):
        """Guarda la figura actual como imagen"""
        self.figure.savefig(filename, dpi=150, bbox_inches='tight')
        
    def get_current_limits(self) -> dict:
        """Obtiene los límites actuales de los ejes"""
        x_lim = self.ax.get_xlim()
        y_lim = self.ax.get_ylim()
        return {'x_min': x_lim[0], 'x_max': x_lim[1], 
                'y_min': y_lim[0], 'y_max': y_lim[1]}


# Importar matplotlib.pyplot para el colormap
import matplotlib.pyplot as plt