# 📐 Visualizador de Ecuaciones Diferenciales de Clairaut

Aplicación de escritorio **offline** con interfaz gráfica (PyQt6) para analizar y graficar ecuaciones diferenciales de Clairaut de la forma:

$$y = x \cdot y' + f(y')$$

---

## 🚀 Requisitos del sistema

- **Python** 3.10 o superior
- **Sistema operativo:** Windows / Linux / macOS
- **Sin conexión a internet** — todo es local

---

## 📦 Instalación

### Opción A — Windows (recomendado)

```bat
install.bat
```

El script automáticamente:
1. Verifica que Python esté instalado
2. Crea el entorno virtual `venv/`
3. Instala todas las dependencias desde `requirements.txt`

### Opción B — Manual (Windows / Linux / macOS)

```bash
# 1. Ir al directorio del proyecto
cd clairaut_calculator

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt
```

### Dependencias

| Paquete | Versión mínima | Uso |
|---|---|---|
| `PyQt6` | 6.5.0 | Interfaz gráfica |
| `sympy` | 1.12 | Cálculo simbólico |
| `matplotlib` | 3.7.0 | Generación de gráficas |
| `numpy` | 1.24.0 | Operaciones numéricas |

---

## ▶️ Ejecución

### Windows
```bat
iniciar.bat
```

### Manual
```bash
python main.py
```

---

## 🎮 Cómo usar la aplicación

### 1. Ingresar una función f(p)

En el campo de entrada, escribe la función usando **`p`** como variable (minúscula). Presiona **Enter** o el botón **Calcular** para procesar.

### 2. Sintaxis válida

| Operador | Significado | Ejemplo |
|---|---|---|
| `+` | Suma | `p**2 + 1` |
| `-` | Resta | `p**3 - 2*p` |
| `*` | Multiplicación | `2*p` |
| `/` | División | `1/p` |
| `**` | Potencia | `p**2` |
| `^` | Potencia (alternativa) | `p^2` |

### 3. Funciones matemáticas disponibles

| Función | Significado | Ejemplo |
|---|---|---|
| `sin(p)` | Seno | `sin(p)` |
| `cos(p)` | Coseno | `cos(p)` |
| `tan(p)` | Tangente | `tan(p)` |
| `exp(p)` | Exponencial eᵖ | `exp(p)` |
| `log(p)` | Logaritmo natural | `log(p)` |
| `sqrt(p)` | Raíz cuadrada | `sqrt(p)` |
| `abs(p)` | Valor absoluto | `abs(p)` |

### 4. Constantes disponibles

| Constante | Valor | Ejemplo |
|---|---|---|
| `pi` | π ≈ 3.14159 | `pi * p**2` |
| `E` | e ≈ 2.71828 | `E**p` |

---

## 📝 Ejemplos

| Función | Entrada | Solución general | Solución singular |
|---|---|---|---|
| Cuadrática | `p**2` | y = Cx + C² | y = −x²/4 |
| Cúbica | `p**3` | y = Cx + C³ | y = (2√3/9)·(−x)^(3/2) |
| Recíproca | `1/p` | y = Cx + 1/C | y = −2√x |
| Cuadrática+1 | `p**2 + 1` | y = Cx + C² + 1 | y = 1 − x²/4 |
| Seno | `sin(p)` | y = Cx + sin(C) | y = −x·acos(−x) − √(1−x²) |
| Exponencial | `exp(p)` | y = Cx + eᶜ | y = x·(log(−x) − 1) |

---

## ⌨️ Atajos de teclado

| Tecla | Acción |
|---|---|
| `Enter` o `Ctrl+Enter` | Calcular y graficar |
| `Ctrl+L` | Limpiar campo de entrada |
| `F5` | Reiniciar aplicación |
| `Ctrl+Q` | Salir (con confirmación) |

---

## 🖱️ Interactividad en la gráfica

La gráfica incluye una barra de herramientas de matplotlib con:

| Botón | Función |
|---|---|
| 🏠 | Restablecer vista original |
| 🔍+ | Zoom in |
| 🔍− | Zoom out |
| ✋ | Pan (mover gráfica) |
| 💾 | Guardar imagen como PNG |
| 📐 | Ajustar límites |

---

## 📊 Interpretación de resultados

La interfaz se divide en dos paneles:

### Panel izquierdo — Resultados matemáticos

Muestra 5 secciones con desplazamiento vertical:

| Sección | Contenido |
|---|---|
| **Ecuación diferencial de Clairaut** | Forma original `y = x·y' + f(y')` y forma con `p = y'` sustituida |
| **Función y derivada** | `f(p)` ingresada y su derivada `f'(p)` |
| **Solución general** | `y = C·x + f(C)` con el valor de C |
| **Solución singular (envolvente)** | Condición `x + f'(p) = 0` y la solución `y` resultante |
| **Pasos de resolución** | Desglose paso a paso del proceso matemático (9 pasos) |

El borde del panel de solución singular cambia a **verde** si existe solución, o a **rojo** si hay un error.

### Panel derecho — Gráfica

| Elemento | Significado |
|---|---|
| Líneas punteadas de colores | Soluciones generales para C ∈ {−3, −2, −1, 0, 1, 2, 3} |
| Línea roja gruesa | Solución singular (envolvente) |
| Leyenda | Identifica cada curva |
| Ejes | x (horizontal) e y (vertical), rango x ∈ [−5, 5] |

---

## 🔧 Funcionamiento matemático

### Ecuación de Clairaut

$$y = x \cdot y' + f(y')$$

Usando la notación `p = y'`:

$$y = x \cdot p + f(p)$$

### Solución general

Se obtiene reemplazando `p = C` (constante arbitraria):

$$y = C \cdot x + f(C)$$

### Solución singular

Se obtiene de la condición de diferenciación:

$$x + f'(p) = 0$$

Despejando `p = p(x)` y sustituyendo:

$$y = x \cdot p(x) + f(p(x))$$

### Interpretación geométrica

- La **solución general** es una familia de rectas (una por cada valor de C).
- La **solución singular** es la **envolvente** de esa familia.
- Cada recta de la familia es tangente a la envolvente en exactamente un punto.

---

## ⚠️ Casos especiales

### Funciones con dominio restringido

Algunas funciones solo existen en ciertos rangos. La aplicación los maneja automáticamente y no grafica valores inválidos.

| Función | Dominio real |
|---|---|
| `sqrt(p)` | p ≥ 0 |
| `log(p)` | p > 0 |
| `1/p` | p ≠ 0 |
| `sin(p)` | Todo ℝ |

### Singularidad en C = 0

Para funciones como `1/p`, la solución general `y = Cx + 1/C` no está definida en C = 0. El programa omite ese valor automáticamente.

### Números complejos

El motor convierte a NaN la parte imaginaria cuando el resultado de la evaluación numérica tiene componente imaginaria superior a 1×10⁻¹⁰, evitando que valores complejos artefacten la gráfica.

---

## ❌ Mensajes de error comunes

| Mensaje | Causa | Solución |
|---|---|---|
| `La función f(p) no puede estar vacía` | Campo vacío | Escribe una función |
| `La expresión no contiene la variable 'p'` | Usaste otra variable | Usa `p` como variable |
| `f(p) no puede ser una constante` | Solo ingresaste un número | Ejemplo: `p**2` |
| `f(p) no puede ser solo 'p'` | Expresión trivial | Usa `p**2`, `sin(p)`, etc. |
| `Error de sintaxis` | Escritura incorrecta | Revisa paréntesis y operadores |
| `La expresión contiene variables no permitidas` | Usaste `x`, `y` u otra variable | Usa solo `p` |

---

## 📁 Estructura del proyecto

```
clairaut_calculator/
├── core/                        # Lógica matemática
│   ├── __init__.py
│   ├── clairaut_engine.py       # Motor principal (ClairautEngine)
│   ├── symbolic_utils.py        # Operaciones simbólicas (SymbolicUtils)
│   └── plotting_utils.py        # Generación de datos para gráficas
├── controllers/                 # Orquestación
│   ├── __init__.py
│   ├── dependency_container.py  # Inyección de dependencias
│   └── clairaut_controller.py   # Controlador PyQt (señales/slots)
├── ui/                          # Interfaz gráfica
│   ├── __init__.py
│   ├── main_window.py           # Ventana principal
│   ├── input_widget.py          # Widget de entrada f(p)
│   ├── results_display.py       # Panel de resultados matemáticos
│   └── graph_widget.py          # Widget de gráfica matplotlib
├── utils/                       # Utilidades generales
│   ├── __init__.py
│   ├── constants.py             # Constantes globales (rango, colores, etc.)
│   ├── validators.py            # Validación de la expresión f(p)
│   └── error_handler.py         # Sistema de manejo y reporte de errores
├── tests/                       # Pruebas unitarias
│   ├── __init__.py
│   ├── test_clairaut_engine.py
│   ├── test_validators.py
│   └── test_requirements.py
├── resources/
│   ├── styles.qss               # Hoja de estilos Qt (actualmente vacía)
│   └── icons/
├── main.py                      # Punto de entrada
├── install.bat                  # Instalación automática (Windows)
├── iniciar.bat                  # Inicio rápido (Windows)
├── requirements.txt
└── README.md
```

---

## 🧪 Ejecutar pruebas

```bash
# Pruebas del motor matemático
python tests/test_clairaut_engine.py

# Pruebas del validador de expresiones
python tests/test_validators.py

# Validación completa de requisitos del sistema
python tests/test_requirements.py
```

---

## 📚 Ejercicios recomendados

### Ejercicio 1 — Parábola envolvente
Ingresa `p**2`. Observa cómo las rectas de la solución general (una por cada C) son tangentes a la parábola `y = −x²/4`.

### Ejercicio 2 — Función cúbica
Ingresa `p**3`. La envolvente singular solo existe para `x ≤ 0` (restricción de la raíz cuadrada).

### Ejercicio 3 — Función recíproca
Ingresa `1/p`. Observa que C = 0 se omite automáticamente y la envolvente solo se grafica para `x ≥ 0`.

### Ejercicio 4 — Función seno
Ingresa `sin(p)`. La envolvente tiene forma de arco con dominio restringido a `|x| ≤ 1`.

### Ejercicio 5 — Composición
Ingresa `p**2 + sin(p)` y explora cómo se combinan los efectos de ambas funciones.

---

## 🛠️ Solución de problemas

**La gráfica no se muestra**
```bash
python -c "import matplotlib.pyplot as plt; plt.plot([1,2,3],[1,4,9]); plt.show()"
```

**PyQt6 no se instala en Linux**
```bash
sudo apt-get install python3-pyqt6
```

**Fuentes no se ven bien en Windows**
La aplicación selecciona automáticamente entre `Segoe UI`, `Arial`, `Microsoft Sans Serif`, `DejaVu Sans` o `Helvetica`, según las fuentes disponibles.

**La aplicación no arranca**
```bash
pip install -r requirements.txt --upgrade
```

---

## 📄 Licencia

Proyecto académico — Curso de Ecuaciones Diferenciales.

---

## 👥 Autores

Desarrollado como proyecto integrador para el curso de Ecuaciones Diferenciales.

---

## 🙏 Agradecimientos

- [SymPy](https://www.sympy.org/) — Cálculo simbólico
- [Matplotlib](https://matplotlib.org/) — Visualización de gráficas
- [PyQt6](https://pypi.org/project/PyQt6/) — Interfaz gráfica
- [NumPy](https://numpy.org/) — Operaciones numéricas
