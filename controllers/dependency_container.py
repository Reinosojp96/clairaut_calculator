# controllers/dependency_container.py
# Contenedor de inyección de dependencias

from core.clairaut_engine import ClairautEngine
from core.plotting_utils import PlottingUtils
from utils.validators import ClairautValidator
from utils.error_handler import error_handler


class DependencyContainer:
    """
    Contenedor de dependencias para toda la aplicación.
    Centraliza la creación y acceso a todas las instancias.
    Patrón Singleton para evitar múltiples instancias.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._engine = None
        self._plotting_utils = None
        self._validator = None
        
        error_handler.info("DependencyContainer", "Contenedor de dependencias inicializado")

    @property
    def engine(self) -> ClairautEngine:
        """Obtiene o crea la instancia del motor de Clairaut"""
        if self._engine is None:
            self._engine = ClairautEngine()
            error_handler.info("DependencyContainer", "Motor de Clairaut instanciado")
        return self._engine

    @property
    def plotting_utils(self) -> PlottingUtils:
        """Obtiene o crea la instancia de PlottingUtils"""
        if self._plotting_utils is None:
            self._plotting_utils = PlottingUtils(self.engine)
            error_handler.info("DependencyContainer", "PlottingUtils instanciado")
        return self._plotting_utils

    @property
    def validator(self) -> ClairautValidator:
        """Obtiene o crea la instancia del validador"""
        if self._validator is None:
            self._validator = ClairautValidator()
            error_handler.info("DependencyContainer", "Validador instanciado")
        return self._validator

    def reset_engine(self) -> None:
        """
        Reinicia el motor para una nueva función.
        Crea una nueva instancia limpia.
        """
        self._engine = ClairautEngine()
        self._plotting_utils = None  # Se recreará automáticamente con el nuevo engine
        error_handler.info("DependencyContainer", "Motor reiniciado para nueva función")

    def get_all_dependencies(self) -> dict:
        """Retorna todas las dependencias como diccionario (útil para debugging)"""
        return {
            'engine': self.engine,
            'plotting_utils': self.plotting_utils,
            'validator': self.validator
        }


# Instancia global única
container = DependencyContainer()