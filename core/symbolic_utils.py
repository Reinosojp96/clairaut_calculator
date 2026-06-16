# core/symbolic_utils.py
# Utilidades simbólicas para operaciones con sympy

import sympy as sp
import numpy as np
from typing import List, Optional
from utils.error_handler import error_handler


class SymbolicUtils:
    """
    Clase de utilidades para operaciones simbólicas con sympy.
    """

    def __init__(self):
        self.x = sp.Symbol('x', real=True)
        self.p = sp.Symbol('p', real=True)
        self.C = sp.Symbol('C', real=True)

    def derivative(self, expr, var='p'):
        """
        Calcula la derivada de una expresión.
        """
        try:
            if var == 'p':
                result = sp.diff(expr, self.p)
            else:
                result = sp.diff(expr, self.x)
            return sp.simplify(result)
        except Exception as e:
            error_handler.error("SymbolicUtils", f"Error en derivada: {e}", str(e))
            return None

    def solve_equation(self, equation, variable):
        """
        Resuelve ecuación equation = 0.
        """
        try:
            solutions = sp.solve(equation, variable)
            if not solutions:
                return []
            if isinstance(solutions, list):
                return solutions
            return [solutions]
        except Exception as e:
            error_handler.error("SymbolicUtils", f"Error al resolver: {e}", str(e))
            return []

    def simplify(self, expr):
        """
        Simplifica una expresión.
        """
        try:
            return sp.simplify(expr)
        except:
            return expr

    def to_lambda(self, expr: sp.Expr, variables: List[sp.Symbol]) -> Optional[callable]:
        """
        Convierte una expresión sympy en una función numérica segura.

        - Detecta zoo (ComplexInfinity), oo, -oo y nan.
        - Simplifica expresiones problemáticas.
        - Maneja números complejos convirtiendo la parte imaginaria a NaN.
        - Devuelve NaN ante errores de evaluación.
        """
        try:
            if expr is None:
                raise ValueError("La expresión es None")

            # Simplificación agresiva
            expr_simplified = sp.simplify(expr)

            try:
                expr_simplified = sp.powsimp(expr_simplified, force=True)
                expr_simplified = sp.powdenest(expr_simplified, force=True)
                expr_simplified = sp.cancel(expr_simplified)
                expr_simplified = sp.factor(expr_simplified)
            except Exception:
                pass

            # Detectar infinitos simbólicos
            invalid_symbols = (
                sp.zoo,
                sp.oo,
                -sp.oo,
                sp.nan
            )

            if any(expr_simplified.has(item) for item in invalid_symbols):
                raise ValueError(
                    f"La expresión contiene valores inválidos: {expr_simplified}"
                )

            # Crear función numérica
            raw_func = sp.lambdify(
                variables,
                expr_simplified,
                modules=["numpy"]
            )

            # Validar con un valor de prueba
            try:
                test_args = [1.0] * len(variables)
                raw_func(*test_args)
            except Exception as test_e:
                error_handler.warning(
                    module="SymbolicUtils",
                    message="La función requiere evaluación protegida",
                    details=str(test_e)
                )

            # Wrapper seguro con manejo de números complejos
            def safe_func(*args):
                try:
                    result = raw_func(*args)

                    # Escalar
                    if np.isscalar(result):
                        result = float(result)
                        if not np.isfinite(result):
                            return np.nan
                        return result

                    # Array: manejar posibles números complejos
                    result = np.asarray(result)
                    
                    # Convertir complejos a reales (parte imaginaria -> NaN)
                    if np.iscomplexobj(result):
                        # Parte real donde la imaginaria es insignificante
                        real_part = np.real(result)
                        imag_part = np.imag(result)
                        result = np.where(np.abs(imag_part) < 1e-10, real_part, np.nan)
                    else:
                        result = result.astype(float)
                    
                    # Limpiar valores no finitos
                    result = np.where(
                        np.isfinite(result),
                        result,
                        np.nan
                    )

                    return result

                except Exception:
                    if len(args) > 0:
                        try:
                            return np.full_like(
                                np.asarray(args[0]),
                                np.nan,
                                dtype=float
                            )
                        except Exception:
                            pass

                    return np.nan

            return safe_func

        except Exception as e:
            error_handler.error(
                module="SymbolicUtils",
                message="Error al convertir expresión a función",
                details=str(e)
            )

            def fallback_func(*args):
                if len(args) > 0:
                    try:
                        return np.full_like(
                            np.asarray(args[0]),
                            np.nan,
                            dtype=float
                        )
                    except Exception:
                        pass

                return np.nan

            return fallback_func

    def format_expression(self, expr):
        """
        Formatea expresión para mostrar en la UI.
        Usa str() de SymPy que es legible pero compacto (una sola línea).
        Ejemplo: -x**2/4 en vez de LaTeX o multi-línea.
        """
        try:
            # Convertir a string de SymPy
            expr_str = str(expr)
            
            # Reemplazos simples para mejorar legibilidad
            expr_str = expr_str.replace('**', '^ ')  # x**2 -> x^ 2
            expr_str = expr_str.replace('sqrt(', '√(')  # sqrt -> √
            expr_str = expr_str.replace('pi', 'π')
            expr_str = expr_str.replace('E', 'e')  # Constante de Euler
            
            return expr_str
        except Exception:
            return ""