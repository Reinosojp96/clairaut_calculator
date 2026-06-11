# ui/__init__.py
# Puerta de entrada para módulos de interfaz gráfica

from .graph_widget import GraphWidget
from .results_display import ResultsDisplay
from .input_widget import InputWidget
from .main_window import MainWindow

__all__ = [
    'GraphWidget',
    'ResultsDisplay',
    'InputWidget',
    'MainWindow',
]