# core/__init__.py
# Puerta de entrada para el núcleo matemático

from .symbolic_utils import SymbolicUtils
from .clairaut_engine import ClairautEngine
from .plotting_utils import PlottingUtils

__all__ = [
    'SymbolicUtils',
    'ClairautEngine',
    'PlottingUtils',
]
