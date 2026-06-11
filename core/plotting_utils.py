# core/plotting_utils.py
# Utilidades para generar datos de graficación de soluciones de Clairaut

import numpy as np
import sympy as sp
from typing import List, Tuple, Optional, Dict, Any
from utils.constants import C_VALUES, X_MIN, X_MAX, NUM_POINTS
from utils.error_handler import error_handler
from core.clairaut_engine import ClairautEngine


class PlottingUtils:
    """
    Genera los datos numéricos para graficar:
    - Familia de soluciones generales (para cada C)
    - Solución singular (envolvente)
    """

    def __init__(self, engine: ClairautEngine):
        """
        Args:
            engine: Instancia de ClairautEngine ya configurada con f(p)
        """
        self.engine = engine
        self.x_vals = np.linspace(X_MIN, X_MAX, NUM_POINTS)

    def generate_general_solution_data(
        self,
        C_value: float
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genera datos (x,y) para una solución general.
        Maneja dominios inválidos, infinitos y errores numéricos.
        """

        try:
            # Evitar constantes problemáticas
            if not np.isfinite(C_value):
                return self.x_vals, np.full_like(
                    self.x_vals,
                    np.nan,
                    dtype=float
                )

            lambda_func = self.engine.get_general_solution_lambda(C_value)

            if lambda_func is None:
                return self.x_vals, np.full_like(
                    self.x_vals,
                    np.nan,
                    dtype=float
                )

            y_vals = lambda_func(self.x_vals)

            # Escalar → vector
            if np.isscalar(y_vals):
                y_vals = np.full_like(
                    self.x_vals,
                    float(y_vals),
                    dtype=float
                )

            else:
                y_vals = np.asarray(
                    y_vals,
                    dtype=float
                ).flatten()

            # Ajustar tamaño
            if len(y_vals) != len(self.x_vals):

                if len(y_vals) == 1:
                    y_vals = np.full_like(
                        self.x_vals,
                        y_vals[0],
                        dtype=float
                    )

                else:
                    error_handler.warning(
                        module="PlottingUtils",
                        message=(
                            f"Dimensión inválida para "
                            f"C={C_value}"
                        ),
                        details=(
                            f"x={len(self.x_vals)}, "
                            f"y={len(y_vals)}"
                        )
                    )

                    return (
                        self.x_vals,
                        np.full_like(
                            self.x_vals,
                            np.nan,
                            dtype=float
                        )
                    )

            # Limpiar valores inválidos
            y_vals = np.where(
                np.isfinite(y_vals),
                y_vals,
                np.nan
            )

            # Eliminar explosiones numéricas
            y_vals = np.where(
                np.abs(y_vals) < 1e10,
                y_vals,
                np.nan
            )

            return self.x_vals, y_vals

        except Exception as e:

            error_handler.error(
                module="PlottingUtils",
                message=f"Error generando curva C={C_value}",
                details=str(e)
            )

            return (
                self.x_vals,
                np.full_like(
                    self.x_vals,
                    np.nan,
                    dtype=float
                )
            )

    def generate_all_general_solutions_data(self) -> Dict[float, Tuple[np.ndarray, np.ndarray]]:
        """
        Genera datos para todos los valores de C en C_VALUES.

        Returns:
            Dict: {C_value: (x_vals, y_vals)}
        """
        data = {}
        for C in C_VALUES:
            data[C] = self.generate_general_solution_data(C)
        return data

    def generate_singular_solution_data(
        self
    ) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        """
        Genera los datos de la solución singular.
        Tolera dominios parciales como sqrt(x), log(x), etc.
        """

        try:

            lambda_func = self.engine.get_singular_solution_lambda()

            if lambda_func is None:
                return None

            y_vals = lambda_func(self.x_vals)

            if np.isscalar(y_vals):

                y_vals = np.full_like(
                    self.x_vals,
                    float(y_vals),
                    dtype=float
                )

            else:

                y_vals = np.asarray(
                    y_vals,
                    dtype=float
                ).flatten()

            if len(y_vals) != len(self.x_vals):

                error_handler.warning(
                    module="PlottingUtils",
                    message="Dimensión incorrecta en solución singular",
                    details=(
                        f"x={len(self.x_vals)}, "
                        f"y={len(y_vals)}"
                    )
                )

                return None

            # Reemplazar inf, -inf y nan
            y_vals = np.where(
                np.isfinite(y_vals),
                y_vals,
                np.nan
            )

            # Si toda la curva es inválida
            if np.all(np.isnan(y_vals)):
                return None

            return self.x_vals, y_vals

        except Exception as e:

            error_handler.warning(
                module="PlottingUtils",
                message="No se pudo generar la solución singular",
                details=str(e)
            )

            return None

    def get_y_limits(self, all_data: Dict[float, Tuple[np.ndarray, np.ndarray]], 
                     singular_data: Optional[Tuple[np.ndarray, np.ndarray]] = None) -> Tuple[float, float]:
        """
        Calcula los límites automáticos del eje Y basados en los datos.

        Args:
            all_data: Datos de todas las soluciones generales
            singular_data: Datos de solución singular (opcional)

        Returns:
            Tuple[float, float]: (y_min, y_max)
        """
        all_y = []
        
        for _, (_, y_vals) in all_data.items():
            y_finite = y_vals[np.isfinite(y_vals)]
            if len(y_finite) > 0:
                all_y.extend(y_finite)
        
        if singular_data is not None:
            _, y_sing = singular_data
            y_finite = y_sing[np.isfinite(y_sing)]
            if len(y_finite) > 0:
                all_y.extend(y_finite)
        
        if len(all_y) == 0:
            return -10.0, 10.0
        
        y_min = float(np.min(all_y))
        y_max = float(np.max(all_y))
        
        # Agregar margen del 10%
        margin = (y_max - y_min) * 0.1 if y_max != y_min else 1.0
        return y_min - margin, y_max + margin

    def has_singular_solution(self) -> bool:
        """Retorna True si existe solución singular"""
        return self.engine.singular_solution is not None