# controllers/__init__.py
# Puerta de entrada para controladores

from .dependency_container import DependencyContainer, container
from .clairaut_controller import ClairautController

__all__ = [
    'DependencyContainer',
    'container',
    'ClairautController',
]