# __init__.py dentro de la carpeta routes

# Importaciones específicas de cada archivo de ruta. Esto asegura que solo se importen las funciones necesarias.
# Además, mejora la claridad del código y facilita el mantenimiento y la escalabilidad de la aplicación.

from .main import generate_graph_data, main, download_excel
from .index import index, login
from .agregar_montaje import agregar_montaje, actualizar_montaje, handle_procesar_busqueda_actualizar
from .anadir_elemento import anadir_elemento
from .dashboardFilter import get_select_data, graphic_dash

# Cada función se importa explícitamente por su nombre, evitando así conflictos de nombres y 
# la importación de funciones no utilizadas. Asegúrate de que estas funciones se usen en el resto de la aplicación.
