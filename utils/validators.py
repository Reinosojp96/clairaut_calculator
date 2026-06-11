# utils/validators.py
# Validación de la función f(p) ingresada por el usuario

import sympy as sp


class ClairautValidator:
    """
    Valida que la expresión de f(p) sea correcta y utilizable
    para una ecuación diferencial de Clairaut.
    """

    def __init__(self):
        self.p = sp.Symbol('p', real=True)

    def validate(self, f_expr_str: str):
        """
        Valida la expresión de f(p).

        Args:
            f_expr_str (str): Cadena ingresada por el usuario (ej: "p**2", "1/p")

        Returns:
            tuple[bool, str, any]: (es_válido, mensaje_error, expresión_sympy)
        """
        # 1. Entrada vacía
        if not f_expr_str or f_expr_str.strip() == "":
            return False, "La función f(p) no puede estar vacía.", None

        # 2. Limpiar espacios
        expr_str = f_expr_str.strip()

        # 3. Intentar convertir a expresión sympy
        try:
            f_expr = sp.sympify(expr_str, locals={'p': self.p})
        except sp.SympifyError as e:
            return False, f"Error de sintaxis: {str(e)}", None
        except Exception as e:
            return False, f"Error inesperado al interpretar la expresión: {str(e)}", None

        # 4. Verificar que la variable 'p' esté presente
        symbols = f_expr.free_symbols
        if len(symbols) > 1:
            return False, f"La expresión contiene variables no permitidas: {symbols}. Use solo 'p'.", None
        if len(symbols) == 0:
            return False, "La expresión no contiene la variable 'p'. Debe depender de 'p'.", None
        if len(symbols) == 1 and self.p not in symbols:
            return False, "La expresión no contiene la variable 'p'.", None

        # 5. Verificar que no sea una constante (degenerado)
        if f_expr.is_constant():
            return False, "f(p) no puede ser una constante. Debe depender de 'p'.", None
        
        # 5.1 Caso especial: "p" sola (es constante pero is_constant no lo detecta bien)
        expr_str_simple = str(f_expr).strip()
        if expr_str_simple == "p":
            return False, "f(p) no puede ser solo 'p'. Debe ser una expresión no trivial (ej: p**2, sin(p), etc.).", None

        # 6. Verificar que sea diferenciable
        try:
            sp.diff(f_expr, self.p)
        except Exception as e:
            return False, f"No se puede derivar f(p): {str(e)}", None

        # 7. Verificar que se pueda resolver x + f'(p) = 0
        try:
            f_prime = sp.diff(f_expr, self.p)
            condition = sp.Symbol('x', real=True) + f_prime
            sp.solve(condition, self.p)
        except Exception as e:
            # No es fatal, solo advertimos
            return True, f"Advertencia: Posible problema al resolver solución singular: {str(e)}", f_expr

        # Todo correcto
        return True, "Válido", f_expr

    def is_safe_for_plotting(self, f_expr, x_vals, c_vals):
        """
        Verifica que la solución general no genere valores extremos o infinitos.
        """
        try:
            import numpy as np
            x_sym = sp.Symbol('x', real=True)
            C_sym = sp.Symbol('C', real=True)

            sol_gral = C_sym * x_sym + f_expr.subs(sp.Symbol('p'), C_sym)

            for xi in np.linspace(min(x_vals), max(x_vals), 5):
                for Ci in c_vals:
                    val = float(sol_gral.subs({x_sym: xi, C_sym: Ci}).evalf())
                    if np.isnan(val) or np.isinf(val):
                        return False, f"Valor no finito detectado en x={xi}, C={Ci}"
            return True, "Seguro para graficar"
        except Exception as e:
            return False, f"Error en validación de graficado: {str(e)}"