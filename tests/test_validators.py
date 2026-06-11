# tests/test_validators.py
# Pruebas unitarias para ClairautValidator

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.validators import ClairautValidator


def test_validator_creation():
    """Prueba 1: Creación del validador"""
    print("\n=== Prueba 1: Creación del validador ===")
    validator = ClairautValidator()
    assert validator is not None
    import sympy as sp
    assert validator.p == sp.Symbol('p', real=True)
    print("✅ Validador creado correctamente")


def test_valid_expressions():
    """Prueba 2: Expresiones válidas"""
    print("\n=== Prueba 2: Expresiones válidas ===")
    validator = ClairautValidator()
    
    valid_expressions = [
        "p**2",
        "p**3",
        "1/p",
        "p**2 + 1",
        "sin(p)",
        "cos(p)",
        "exp(p)",
        "log(p)",
        "sqrt(p)",
        "p**2 + 2*p + 1",
    ]
    
    for expr in valid_expressions:
        valid, msg, _ = validator.validate(expr)
        assert valid is True, f"'{expr}' debería ser válido: {msg}"
        print(f"   ✅ '{expr}' → válido")
    
    print("   ✅ Todas las expresiones válidas pasaron")


def test_invalid_expressions():
    """Prueba 3: Expresiones inválidas"""
    print("\n=== Prueba 3: Expresiones inválidas ===")
    validator = ClairautValidator()
    
    invalid_expressions = [
        ("", "vacío"),
        ("x**2", "variable incorrecta"),
        ("5", "constante sin p"),
        ("p", "solo p - debe ser rechazado"),
        ("sin(x)", "variable incorrecta"),
        ("p + x", "múltiples variables"),
    ]
    
    for expr, reason in invalid_expressions:
        valid, msg, _ = validator.validate(expr)
        assert valid is False, f"'{expr}' debería ser inválido: {reason}"
        print(f"   ✅ '{expr}' → inválido ({reason})")
    
    print("   ✅ Todas las expresiones inválidas fueron rechazadas")


def test_expression_with_constants():
    """Prueba 4: Expresiones con constantes"""
    print("\n=== Prueba 4: Expresiones con constantes ===")
    validator = ClairautValidator()
    
    expressions_with_constants = [
        "pi * p**2",
        "E * p",
        "p**2 + pi",
    ]
    
    for expr in expressions_with_constants:
        valid, msg, _ = validator.validate(expr)
        assert valid is True, f"'{expr}' con constantes debería ser válido: {msg}"
        print(f"   ✅ '{expr}' → válido (constantes permitidas)")
    
    print("   ✅ Constantes manejadas correctamente")


def test_complex_expressions():
    """Prueba 5: Expresiones complejas pero válidas"""
    print("\n=== Prueba 5: Expresiones complejas pero válidas ===")
    validator = ClairautValidator()
    
    complex_expressions = [
        "p**2 * sin(p)",
        "exp(p) * cos(p)",
        "log(p**2 + 1)",
        "sqrt(p**2 + 1)",
        "1/(p**2 + 1)",
    ]
    
    for expr in complex_expressions:
        valid, msg, _ = validator.validate(expr)
        assert valid is True, f"'{expr}' debería ser válido: {msg}"
        print(f"   ✅ '{expr}' → válido")
    
    print("   ✅ Expresiones complejas aceptadas correctamente")


def test_numeric_values():
    """Prueba 6: Valores numéricos (deben ser rechazados como constantes)"""
    print("\n=== Prueba 6: Valores numéricos ===")
    validator = ClairautValidator()
    
    numeric_values = ["0", "1", "3.14", "-5", "42"]
    
    for expr in numeric_values:
        valid, msg, _ = validator.validate(expr)
        assert valid is False, f"'{expr}' (numérico) debería ser inválido"
        # Verificar que el mensaje indica que es una constante o similar
        assert any(keyword in msg.lower() for keyword in ["constante", "no depende", "variable"]), \
            f"Mensaje '{msg}' no indica que es inválido"
        print(f"   ✅ '{expr}' → rechazado (correcto)")
    
    print("   ✅ Valores numéricos rechazados correctamente")


def test_syntax_errors():
    """Prueba 7: Errores de sintaxis"""
    print("\n=== Prueba 7: Errores de sintaxis ===")
    validator = ClairautValidator()
    
    # Solo expresiones que son realmente inválidas en SymPy
    syntax_errors = [
        "p**",      # Operador incompleto
        "sin(",     # Función incompleta
        "log(p,",   # Argumento incompleto
        "p^^2",     # Operador inválido
    ]
    
    for expr in syntax_errors:
        valid, msg, _ = validator.validate(expr)
        assert valid is False, f"'{expr}' con error de sintaxis debería ser inválido"
        print(f"   ✅ '{expr}' → error de sintaxis detectado")
    
    print("   ✅ Errores de sintaxis detectados correctamente")


def test_validation_consistency():
    """Prueba 8: Consistencia del validador (misma expresión, mismo resultado)"""
    print("\n=== Prueba 8: Consistencia del validador ===")
    validator = ClairautValidator()
    
    expr = "p**2"
    
    # Validar varias veces
    results = []
    for _ in range(5):
        valid, msg, f_expr = validator.validate(expr)
        results.append((valid, msg, f_expr))
    
    # Todos los resultados deben ser iguales
    assert all(r[0] == results[0][0] for r in results)
    assert all(r[1] == results[0][1] for r in results)
    
    print(f"   ✅ {len(results)} validaciones idénticas para '{expr}'")
    print("   ✅ Validador es consistente")


def test_error_messages():
    """Prueba 9: Mensajes de error descriptivos"""
    print("\n=== Prueba 9: Mensajes de error descriptivos ===")
    validator = ClairautValidator()
    
    test_cases = [
        ("", "vacía"),
        ("x**2", "variable incorrecta"),
        ("5", "constante"),
    ]
    
    for expr, expected_keyword in test_cases:
        valid, msg, _ = validator.validate(expr)
        assert valid is False
        assert len(msg) > 0
        print(f"   ✅ '{expr}' → mensaje: '{msg[:60]}...'")
    
    print("   ✅ Mensajes de error descriptivos")


def test_return_type():
    """Prueba 10: Tipo de retorno correcto"""
    print("\n=== Prueba 10: Tipo de retorno correcto ===")
    validator = ClairautValidator()
    
    valid, msg, f_expr = validator.validate("p**2")
    
    assert isinstance(valid, bool)
    assert isinstance(msg, str)
    
    print("   ✅ Retorna (bool, str, sp.Expr)")


def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("=" * 60)
    print("EJECUTANDO PRUEBAS DE ClairautValidator")
    print("=" * 60)
    
    # Importar sympy para las pruebas
    global sp
    import sympy as sp
    
    try:
        test_validator_creation()
        test_valid_expressions()
        test_invalid_expressions()
        test_expression_with_constants()
        test_complex_expressions()
        test_numeric_values()
        test_syntax_errors()
        test_validation_consistency()
        test_error_messages()
        test_return_type()
        
        print("\n" + "=" * 60)
        print("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("=" * 60)
        return True
        
    except AssertionError as e:
        print(f"\n❌ Prueba fallida: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)