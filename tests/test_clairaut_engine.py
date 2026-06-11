# tests/test_clairaut_engine.py
# Pruebas unitarias para ClairautEngine

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sympy as sp
import numpy as np
from core.clairaut_engine import ClairautEngine


def test_engine_creation():
    """Prueba 1: Creación del motor"""
    print("\n=== Prueba 1: Creación del motor ===")
    engine = ClairautEngine()
    assert engine is not None
    assert engine.x == sp.Symbol('x', real=True)
    assert engine.p == sp.Symbol('p', real=True)
    assert engine.C == sp.Symbol('C', real=True)
    print("✅ Motor creado correctamente")


def test_f_p_squared():
    """Prueba 2: f(p) = p² (ejemplo obligatorio)"""
    print("\n=== Prueba 2: f(p) = p² ===")
    engine = ClairautEngine()
    p = sp.Symbol('p')
    f_expr = p**2
    
    engine.set_f_function(f_expr)
    
    # Verificar derivada
    assert str(engine.f_prime) == "2*p"
    print(f"   ✅ f'(p) = {engine.f_prime}")
    
    # Verificar solución general
    expected_general = sp.simplify(engine.C * engine.x + engine.C**2)
    assert sp.simplify(engine.general_solution - expected_general) == 0
    print(f"   ✅ Solución general: y = {engine.general_solution}")
    
    # Verificar solución singular
    expected_singular = -engine.x**2 / 4
    assert sp.simplify(engine.singular_solution - expected_singular) == 0
    print(f"   ✅ Solución singular: y = {engine.singular_solution}")


def test_f_p_cubed():
    """Prueba 3: f(p) = p³"""
    print("\n=== Prueba 3: f(p) = p³ ===")
    engine = ClairautEngine()
    p = sp.Symbol('p')
    f_expr = p**3
    
    engine.set_f_function(f_expr)
    
    # Verificar derivada
    assert str(engine.f_prime) == "3*p**2"
    print(f"   ✅ f'(p) = {engine.f_prime}")
    
    # Verificar que existe solución singular
    assert engine.singular_solution is not None
    print(f"   ✅ Solución singular encontrada: y = {engine.singular_solution}")


def test_f_one_over_p():
    """Prueba 4: f(p) = 1/p"""
    print("\n=== Prueba 4: f(p) = 1/p ===")
    engine = ClairautEngine()
    p = sp.Symbol('p')
    f_expr = 1/p
    
    engine.set_f_function(f_expr)
    
    # Verificar derivada
    assert str(engine.f_prime) == "-1/p**2"
    print(f"   ✅ f'(p) = {engine.f_prime}")
    
    # Verificar solución general
    assert engine.general_solution is not None
    print(f"   ✅ Solución general: y = {engine.general_solution}")
    
    # Verificar que C=0 causa singularidad (debe retornar None)
    lambda_c0 = engine.get_general_solution_lambda(0)
    assert lambda_c0 is None
    print(f"   ✅ C=0 correctamente omitido (singularidad)")


def test_general_solution_for_C():
    """Prueba 5: Solución general para valores específicos de C"""
    print("\n=== Prueba 5: Solución general para C específicos ===")
    engine = ClairautEngine()
    p = sp.Symbol('p')
    f_expr = p**2
    engine.set_f_function(f_expr)
    
    C_values = [-3, -2, -1, 0, 1, 2, 3]
    
    for C in C_values:
        expr = engine.get_general_solution_for_C(C)
        # Para p², todos los C son válidos (C=0 da y=0)
        assert expr is not None, f"C={C} no debería ser None"
        print(f"   ✅ C={C}: y = {expr}")
    
    print(f"   ✅ Todos los C values generan expresiones válidas")


def test_singular_solution_lambda():
    """Prueba 6: Conversión a lambda de solución singular"""
    print("\n=== Prueba 6: Conversión a lambda de solución singular ===")
    engine = ClairautEngine()
    p = sp.Symbol('p')
    f_expr = p**2
    engine.set_f_function(f_expr)
    
    lambda_func = engine.get_singular_solution_lambda()
    assert lambda_func is not None
    
    # Probar evaluación en varios puntos
    x_vals = [-2, -1, 0, 1, 2]
    for x in x_vals:
        y = lambda_func(x)
        expected = - (x**2) / 4
        assert abs(y - expected) < 1e-10
        print(f"   ✅ x={x}: y={y} (esperado={expected})")


def test_get_results_dict():
    """Prueba 7: Diccionario de resultados"""
    print("\n=== Prueba 7: Diccionario de resultados ===")
    engine = ClairautEngine()
    p = sp.Symbol('p')
    f_expr = p**2
    engine.set_f_function(f_expr)
    
    results = engine.get_results_dict()
    
    assert 'f_p' in results
    assert 'f_prime' in results
    assert 'general_solution' in results
    assert 'singular_solution' in results
    assert 'has_singular' in results
    assert results['has_singular'] is True
    
    print(f"   ✅ Diccionario contiene todas las claves")
    print(f"   ✅ has_singular = {results['has_singular']}")


def test_format_results_for_display():
    """Prueba 8: Formateo de resultados para UI"""
    print("\n=== Prueba 8: Formateo de resultados para UI ===")
    engine = ClairautEngine()
    p = sp.Symbol('p')
    f_expr = p**2
    engine.set_f_function(f_expr)
    
    formatted = engine.format_results_for_display()
    
    assert 'f_p' in formatted
    assert 'f_prime' in formatted
    assert 'general' in formatted
    assert 'singular' in formatted
    assert 'singular_condition' in formatted
    assert 'steps' in formatted
    assert isinstance(formatted['steps'], list)
    assert len(formatted['steps']) >= 4
    
    print(f"   ✅ f(p) = {formatted['f_p']}")
    print(f"   ✅ f'(p) = {formatted['f_prime']}")
    print(f"   ✅ Solución general = {formatted['general']}")
    print(f"   ✅ Solución singular = {formatted['singular']}")
    print(f"   ✅ Pasos = {len(formatted['steps'])} elementos")


def test_clear_engine():
    """Prueba 9: Limpiar el motor"""
    print("\n=== Prueba 9: Limpiar el motor ===")
    engine = ClairautEngine()
    p = sp.Symbol('p')
    f_expr = p**2
    engine.set_f_function(f_expr)
    
    assert engine.f_p is not None
    
    engine.clear()
    
    assert engine.f_p is None
    assert engine.f_prime is None
    assert engine.general_solution is None
    assert engine.singular_solution is None
    
    print("   ✅ Motor limpiado correctamente")


def test_multiple_functions():
    """Prueba 10: Múltiples funciones en secuencia"""
    print("\n=== Prueba 10: Múltiples funciones en secuencia ===")
    engine = ClairautEngine()
    
    functions = [
        ("p**2", "2*p", "-x**2/4"),
        ("p**3", "3*p**2", None),  # Singular existe pero expresión compleja
        ("1/p", "-1/p**2", None),
    ]
    
    for f_str, expected_prime, _ in functions:
        p = sp.Symbol('p')
        f_expr = sp.sympify(f_str)
        engine.set_f_function(f_expr)
        
        assert str(engine.f_prime) == expected_prime
        print(f"   ✅ f(p)={f_str} → f'(p)={engine.f_prime}")
    
    print("   ✅ Todas las funciones procesadas correctamente")


def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("=" * 60)
    print("EJECUTANDO PRUEBAS DE ClairautEngine")
    print("=" * 60)
    
    try:
        test_engine_creation()
        test_f_p_squared()
        test_f_p_cubed()
        test_f_one_over_p()
        test_general_solution_for_C()
        test_singular_solution_lambda()
        test_get_results_dict()
        test_format_results_for_display()
        test_clear_engine()
        test_multiple_functions()
        
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