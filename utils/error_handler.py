# utils/error_handler.py
# Manejo centralizado de errores y logging

from enum import Enum
from typing import Callable, Optional
from dataclasses import dataclass
from datetime import datetime


class ErrorSeverity(Enum):
    """Niveles de severidad de errores"""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class ErrorReport:
    """Estructura de un reporte de error"""
    severity: ErrorSeverity
    module: str
    message: str
    details: Optional[str] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def __str__(self):
        return f"[{self.timestamp.strftime('%H:%M:%S')}] {self.severity.value} [{self.module}]: {self.message}"


class ErrorHandler:
    """
    Manejador global de errores.
    Soporta múltiples callbacks para notificar a la UI.
    """

    _instance = None
    _callbacks: list[Callable[[ErrorReport], None]] = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._callbacks = []
        return cls._instance

    def subscribe(self, callback: Callable[[ErrorReport], None]):
        """
        Suscribir un callback (ej: función de UI para mostrar error en ventana)
        """
        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def unsubscribe(self, callback: Callable[[ErrorReport], None]):
        """Desuscribir callback"""
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def _notify(self, report: ErrorReport):
        """Notificar a todos los callbacks suscritos"""
        for callback in self._callbacks:
            try:
                callback(report)
            except Exception as e:
                print(f"Error en callback: {e}")

    def log(self, severity: ErrorSeverity, module: str, message: str, details: Optional[str] = None):
        """
        Registrar un error y notificar a los suscriptores

        Args:
            severity: Nivel de severidad
            module: Nombre del módulo que reporta (ej: "ClairautEngine")
            message: Mensaje corto para el usuario
            details: Detalles técnicos (opcional)
        """
        report = ErrorReport(
            severity=severity,
            module=module,
            message=message,
            details=details
        )

        # Siempre imprimir en consola
        print(report)
        if details:
            print(f"    Detalles: {details}")

        # Notificar a UI
        self._notify(report)

    def info(self, module: str, message: str):
        self.log(ErrorSeverity.INFO, module, message)

    def warning(self, module: str, message: str, details: Optional[str] = None):
        self.log(ErrorSeverity.WARNING, module, message, details)

    def error(self, module: str, message: str, details: Optional[str] = None):
        self.log(ErrorSeverity.ERROR, module, message, details)

    def critical(self, module: str, message: str, details: Optional[str] = None):
        self.log(ErrorSeverity.CRITICAL, module, message, details)

    def clear(self):
        """Limpiar todos los callbacks"""
        self._callbacks.clear()


# Singleton global para fácil acceso
error_handler = ErrorHandler()