# utils/constants.py
# Constantes globales para el visualizador de Clairaut

# Valores de C para la solución general
C_VALUES = [-3, -2, -1, 0, 1, 2, 3]

# Rango de x para las gráficas
X_MIN = -5.0
X_MAX = 5.0
NUM_POINTS = 400

# Rango de y para la gráfica
Y_MIN_AUTO = True
Y_MANUAL_MIN = -10.0
Y_MANUAL_MAX = 10.0

# Tamaño de la ventana principal
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Tamaño del widget de gráfica
GRAPH_WIDTH = 800
GRAPH_HEIGHT = 600

# Estilos para gráficas
DEFAULT_LINEWIDTH = 2
SINGULAR_LINEWIDTH = 3
SINGULAR_COLOR = 'red'
GENERAL_LINESTYLE = '--'
GENERAL_COLORMAP = 'tab10'

# Títulos y etiquetas
APP_TITLE = "Visualizador de Ecuaciones de Clairaut"
X_LABEL = "x"
Y_LABEL = "y"
LEGEND_TITLE = "Soluciones"

# Mensajes
MSG_INVALID_FUNCTION = "Error: La función f(p) no es válida."
MSG_SINGULAR_NOT_FOUND = "No se pudo encontrar una solución singular explícita."
MSG_ENTER_FUNCTION = "Ingrese f(p), por ejemplo: p**2, p**3, 1/p"