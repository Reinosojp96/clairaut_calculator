# core/clairaut_engine.py
# Motor principal para ecuaciones diferenciales de Clairaut

import sympy as sp
from typing import Dict, Any, Tuple, Optional, List
from utils.error_handler import error_handler
from core.symbolic_utils import SymbolicUtils


class ClairautEngine:
    """
    Motor de resolución de ecuaciones diferenciales de Clairaut.
    Forma: y = x*y' + f(y')
    """

    def __init__(self):
        self.sym_utils = SymbolicUtils()
        self.x = self.sym_utils.x
        self.p = self.sym_utils.p
        self.C = self.sym_utils.C
        
        self.f_p = None
        self.f_prime = None
        self.general_solution = None
        self.singular_solution = None
        self.singular_p_expr = None

    def set_f_function(self, f_expr: sp.Expr) -> None:
        """
        Establece la función f(p).
        IMPORTANTE: f_expr debe usar el símbolo self.p, no un símbolo externo.
        """
        # Reescribir f_expr usando self.p si es necesario
        f_expr_rewritten = f_expr.subs(sp.Symbol('p'), self.p)
        self.f_p = f_expr_rewritten
        
        self._calculate_derivative()
        self._calculate_general_solution()
        self._calculate_singular_solution()
        
        error_handler.info(
            module="ClairautEngine",
            message=f"Función f(p) = {self.sym_utils.format_expression(self.f_p)} cargada correctamente"
        )

    def _calculate_derivative(self) -> None:
        """Calcula f'(p)"""
        if self.f_p is not None:
            self.f_prime = sp.diff(self.f_p, self.p)
            self.f_prime = sp.simplify(self.f_prime)
            error_handler.info(
                module="ClairautEngine",
                message=f"f'(p) = {self.sym_utils.format_expression(self.f_prime)}"
            )

    def _calculate_general_solution(self) -> None:
        """Solución general: y = C*x + f(C)"""
        if self.f_p is not None:
            f_at_C = self.f_p.subs(self.p, self.C)
            self.general_solution = self.C * self.x + f_at_C
            self.general_solution = sp.simplify(self.general_solution)

    def _calculate_singular_solution(self) -> None:
        """Solución singular: x + f'(p) = 0"""
        if self.f_prime is None:
            self.singular_solution = None
            self.singular_p_expr = None
            return

        try:
            condition = self.x + self.f_prime
            solutions = sp.solve(condition, self.p)
            
            if not solutions:
                error_handler.warning(
                    module="ClairautEngine",
                    message="No se pudo despejar p de la condición singular",
                    details=f"Condición: {condition} = 0"
                )
                self.singular_solution = None
                self.singular_p_expr = None
                return

            p_expr = solutions[0]
            self.singular_p_expr = p_expr
            
            y_expr = self.x * p_expr + self.f_p.subs(self.p, p_expr)
            self.singular_solution = sp.simplify(y_expr)
            
            error_handler.info(
                module="ClairautEngine",
                message=f"Solución singular: y = {self.sym_utils.format_expression(self.singular_solution)}"
            )
            
        except Exception as e:
            error_handler.error(
                module="ClairautEngine",
                message="Error al calcular solución singular",
                details=str(e)
            )
            self.singular_solution = None
            self.singular_p_expr = None

    def get_general_solution_for_C(self, C_value: float) -> Optional[sp.Expr]:
        """
        Obtiene la solución general para un valor específico de C.
        Retorna None si la expresión es inválida (singularidad).
        """
        if self.general_solution is None:
            return None
        
        try:
            expr = self.general_solution.subs(self.C, C_value)
            expr = sp.simplify(expr)
            
            # Detectar singularidades inmediatas
            if expr.has(sp.zoo, sp.oo, -sp.oo, sp.nan):
                return None
                
            return expr
            
        except Exception:
            return None

    def get_general_solution_lambda(self, C_value: float) -> Optional[callable]:
        """
        Convierte la solución general para un C específico en función lambda.
        Si C_value causa una singularidad (ej: C=0 en 1/C), retorna None.
        """
        expr = self.get_general_solution_for_C(C_value)
        if expr is None:
            return None
        
        # Verificar si la expresión tiene singularidad para este C
        try:
            # Intentar evaluar en un punto de prueba
            test_x = 1.0
            test_result = expr.subs(self.x, test_x).evalf()
            
            # Detectar zoo (ComplexInfinity), oo, -oo
            if test_result in (sp.zoo, sp.oo, -sp.oo, sp.nan):
                error_handler.warning(
                    module="ClairautEngine",
                    message=f"Saltando C={C_value}: causa singularidad",
                    details=f"Expresión: {expr}"
                )
                return None
                
        except Exception as e:
            error_handler.warning(
                module="ClairautEngine",
                message=f"Posible singularidad para C={C_value}",
                details=str(e)
            )
            return None
        
        return self.sym_utils.to_lambda(expr, [self.x])

    def get_singular_solution_lambda(self) -> Optional[callable]:
        """
        Convierte la solución singular en función lambda.
        Maneja casos donde la expresión no es válida para todos los x.
        """
        if self.singular_solution is None:
            return None
        
        # Verificar que la expresión no tenga problemas críticos
        try:
            # Probar con un valor de x
            test_x = 1.0
            test_result = self.singular_solution.subs(self.x, test_x).evalf()
            if test_result in (sp.zoo, sp.oo, -sp.oo, sp.nan):
                error_handler.warning(
                    module="ClairautEngine",
                    message="La solución singular no es finita para x=1",
                    details="La gráfica puede mostrar solo parte del dominio"
                )
        except:
            pass
        
        return self.sym_utils.to_lambda(self.singular_solution, [self.x])

    def get_results_dict(self) -> Dict[str, Any]:
        """Retorna un diccionario con todos los resultados."""
        return {
            'f_p': self.f_p,
            'f_prime': self.f_prime,
            'general_solution': self.general_solution,
            'singular_solution': self.singular_solution,
            'singular_p_expr': self.singular_p_expr,
            'has_singular': self.singular_solution is not None
        }

    def _generate_step_descriptions(self) -> List[str]:
        """Genera una lista de pasos texto para explicar el cálculo."""
        steps = []

        steps.append(f"f(p) = {self.sym_utils.format_expression(self.f_p)}")
        steps.append(f"f'(p) = {self.sym_utils.format_expression(self.f_prime)}")
        steps.append("Solución general: y = C·x + f(C)")
        steps.append(
            f"Reemplazando C en f(p), la solución general es: y = {self.sym_utils.format_expression(self.general_solution)}"
        )

        if self.singular_solution is not None:
            steps.append("Condición singular: x + f'(p) = 0")
            steps.append(
                f"Resolviendo para p, se obtiene: p = {self.sym_utils.format_expression(self.singular_p_expr)}"
            )
            steps.append(
                f"Solución singular: y = {self.sym_utils.format_expression(self.singular_solution)}"
            )
        else:
            steps.append("No hay solución singular explícita para esta función.")

        return steps

    def format_results_for_display(self) -> Dict[str, str]:
        """Formatea los resultados para mostrar en la UI."""
        results = {}
        
        if self.f_p is not None:
            results['f_p'] = self.sym_utils.format_expression(self.f_p)
            results['f_prime'] = self.sym_utils.format_expression(self.f_prime) if self.f_prime is not None else "No disponible"
            results['general'] = self.sym_utils.format_expression(self.general_solution) if self.general_solution else "No disponible"
            results['steps'] = self._generate_step_descriptions()
            
            if self.singular_solution is not None:
                results['singular'] = self.sym_utils.format_expression(self.singular_solution)
                results['singular_condition'] = f"x + f'(p) = 0  →  p = {self.sym_utils.format_expression(self.singular_p_expr)}"
            else:
                results['singular'] = "No existe solución singular explícita"
                results['singular_condition'] = "No aplica"
        
        return results
    
    def clear(self):
        """Limpia el estado actual del motor."""
        self.f_p = None
        self.f_prime = None
        self.general_solution = None
        self.singular_solution = None
        self.singular_p_expr = None
        error_handler.info("ClairautEngine", "Motor limpiado")


# Instancia global
clairaut_engine = ClairautEngine()