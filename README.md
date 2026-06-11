# 📐 Visualizador de Ecuaciones Diferenciales de Clairaut

Aplicación de escritorio **offline** con interfaz gráfica para analizar y graficar ecuaciones diferenciales de Clairaut.

$$y = x \cdot y' + f(y')$$

---

## 🚀 Requisitos del sistema

- **Python** 3.10 o superior
- **Sistema operativo:** Windows / Linux / macOS
- **Sin conexión a internet** (todo es local)

---

## 📦 Instalación

```bash
# 1. Clonar o descargar el proyecto
cd clairaut_calculator

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar la aplicación
python main.py
🎮 Cómo usar la aplicación
1. Ingresar una función f(p)
En el campo "Ingrese f(p)" escribe la función usando la variable p (minúscula).

2. Sintaxis válida
Operador	Significado	Ejemplo
+	Suma	p**2 + 1
-	Resta	p**3 - 2*p
*	Multiplicación	2*p
/	División	1/p
**	Potencia	p**2
^	Potencia (alternativa)	p^2
3. Funciones matemáticas disponibles
Función	Significado	Ejemplo
sin(p)	Seno	sin(p)
cos(p)	Coseno	cos(p)
tan(p)	Tangente	tan(p)
exp(p)	Exponencial e^p	exp(p)
log(p)	Logaritmo natural	log(p)
sqrt(p)	Raíz cuadrada	sqrt(p)
abs(p)	Valor absoluto	abs(p)
4. Constantes disponibles
Constante	Valor	Ejemplo
pi	π ≈ 3.14159	pi * p**2
E	e ≈ 2.71828	E**p
📝 Ejemplos de funciones
Función	Entrada	Solución general	Solución singular
Cuadrática	p**2	y = Cx + C²	y = -x²/4
Cúbica	p**3	y = Cx + C³	y = (2√3/9)·(-x)^(3/2)
Recíproca	1/p	y = Cx + 1/C	y = -2√x
Cuadrática+1	p**2 + 1	y = Cx + C² + 1	y = 1 - x²/4
Seno	sin(p)	y = Cx + sin(C)	y = -x·acos(-x) - √(1-x²)
Exponencial	exp(p)	y = Cx + e^C	y = x·(log(-x) - 1)
⌨️ Atajos de teclado
Tecla	Acción
Enter o Ctrl+Enter	Calcular y graficar
Ctrl+L	Limpiar campo de entrada
F5	Reiniciar aplicación
Ctrl+Q	Salir (con confirmación)
🖱️ Interactividad en la gráfica
La gráfica incluye una barra de herramientas con:

Botón	Función
🏠	Restablecer vista original
🔍+	Zoom in
🔍-	Zoom out
✋	Pan (mover gráfica)
💾	Guardar imagen como PNG
📐	Ajustar límites
📊 Interpretación de resultados
Panel izquierdo - Resultados matemáticos
Sección	Muestra
Función y derivada	f(p) = ... y f'(p) = ...
Solución general	y = C·x + f(C)
Solución singular	Condición: x + f'(p) = 0 → p = ... y y = ...
Panel derecho - Gráfica
Elemento	Significado
Líneas punteadas de colores	Soluciones generales para C = -3, -2, -1, 0, 1, 2, 3
Línea roja gruesa	Solución singular (envolvente)
Leyenda	Identifica cada curva
Ejes	x (horizontal) e y (vertical)
🔧 Funcionamiento matemático
Ecuación de Clairaut
y
=
x
⋅
y
′
+
f
(
y
′
)
y=x⋅y 
′
 +f(y 
′
 )

Donde:

y' = derivada de y respecto a x

f(p) = función ingresada por el usuario

p = y'

Solución general
Se obtiene reemplazando p = C (constante):

y
=
C
⋅
x
+
f
(
C
)
y=C⋅x+f(C)

Solución singular
Se obtiene de la condición:

x
+
f
′
(
p
)
=
0
x+f 
′
 (p)=0

Despejando p y reemplazando en y = x·p + f(p):

y
=
x
⋅
p
(
x
)
+
f
(
p
(
x
)
)
y=x⋅p(x)+f(p(x))

Interpretación geométrica
La solución general es una familia de curvas (una para cada C)

La solución singular es la envolvente de esa familia

Cada curva de la familia es tangente a la envolvente

⚠️ Casos especiales
Funciones con dominio restringido
Algunas funciones solo existen en ciertos rangos:

Función	Dominio real
sqrt(p)	p ≥ 0
log(p)	p > 0
1/p	p ≠ 0
sin(p)	Todo ℝ
La aplicación maneja estos casos automáticamente (no grafica valores inválidos).

Singularidad en C=0
Para funciones como 1/p, la solución general y = Cx + 1/C no está definida en C=0. El programa omite automáticamente ese valor.

❌ Mensajes de error comunes
Mensaje	Significado	Solución
La función f(p) no puede estar vacía	No ingresaste nada	Escribe una función
La expresión no contiene la variable 'p'	Usaste otra variable	Usa p como variable
f(p) no puede ser una constante	Ingresaste solo un número	Ejemplo: p**2
Error de sintaxis	Error al escribir	Revisa la sintaxis
📁 Estructura del proyecto
text
clairaut_calculator/
├── core/                    # Lógica matemática
│   ├── symbolic_utils.py    # Operaciones simbólicas
│   ├── clairaut_engine.py   # Motor de Clairaut
│   └── plotting_utils.py    # Generación de datos
├── controllers/             # Orquestación
│   ├── dependency_container.py
│   └── clairaut_controller.py
├── ui/                      # Interfaz gráfica
│   ├── main_window.py
│   ├── input_widget.py
│   ├── results_display.py
│   └── graph_widget.py
├── utils/                   # Utilidades
│   ├── constants.py
│   ├── validators.py
│   └── error_handler.py
├── tests/                   # Pruebas unitarias
├── main.py                  # Punto de entrada
├── requirements.txt
└── README.md
🧪 Ejecutar pruebas
bash
# Pruebas del motor matemático
python tests/test_clairaut_engine.py

# Pruebas del validador
python tests/test_validators.py

# Validación completa de requisitos
python tests/test_requirements.py
📚 Ejercicios recomendados para practicar
Ejercicio 1 - Parábola envolvente
Ingresa p**2 y observa cómo las rectas de la solución general son tangentes a la parábola y = -x²/4.

Ejercicio 2 - Función cúbica
Ingresa p**3. La envolvente solo existe para x ≤ 0 (por la raíz cuadrada).

Ejercicio 3 - Función recíproca
Ingresa 1/p. Observa que C=0 no se grafica (singularidad) y la envolvente solo para x ≥ 0.

Ejercicio 4 - Función seno
Ingresa sin(p). La envolvente tiene forma de arco con dominio restringido a |x| ≤ 1.

Ejercicio 5 - Composición
Ingresa p**2 + sin(p) y explora cómo se combinan los efectos.

🛠️ Solución de problemas
Problema: La gráfica no se ve
bash
# Verificar matplotlib
python -c "import matplotlib.pyplot as plt; plt.plot([1,2,3],[1,4,9]); plt.show()"
Problema: PyQt6 no se instala en Linux
bash
sudo apt-get install python3-pyqt6
Problema: Fuentes no se ven en Windows
La aplicación usa automáticamente Segoe UI o Arial.

Problema: La aplicación no arranca
bash
# Verificar todas las dependencias
pip install -r requirements.txt --upgrade
📄 Licencia
Proyecto académico - Curso de Ecuaciones Diferenciales

👥 Autores
Desarrollado como proyecto integrador para el curso de Ecuaciones Diferenciales.

🙏 Agradecimientos
SymPy - Cálculo simbólico

Matplotlib - Visualización de gráficas

PyQt6 - Interfaz gráfica

NumPy - Operaciones numéricas

✅ ¡Listo para usar!
bash
python main.py
Ingresa cualquier función f(p) y obtén instantáneamente:

✅ Solución general

✅ Derivada f'(p)

✅ Condición singular

✅ Solución singular (envolvente)

✅ Gráfica interactiva de la familia de curvas