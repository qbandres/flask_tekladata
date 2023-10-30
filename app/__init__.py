from flask import Flask
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno del archivo .env en las variables de entorno del sistema.

# Creación de una nueva instancia de la aplicación Flask. 'app' es ahora una instancia de la clase 'Flask'.
app = Flask(__name__)

# Establece una clave secreta para tu aplicación Flask. Esta clave se utiliza para mantener seguras las sesiones de los usuarios y para otras medidas de seguridad.
app.secret_key = 'Claudia13'

# Define un diccionario de usuarios para la autenticación. Aquí, se usa 'os.getenv' para obtener valores de las variables de entorno,
# permitiendo una gestión de contraseñas más segura y flexible.
usuarios = {
    'andres': os.getenv('USER_ANDRES_PASS'),
    'jorge': os.getenv('USER_JORGE_PASS'),
    'favio': os.getenv('USER_FAVIO_PASS')
}

# Configura la conexión a la base de datos MySQL. 'os.getenv' se utiliza para obtener la configuración de la base de datos
# desde las variables de entorno, con valores predeterminados especificados en caso de que estas variables no estén establecidas.
db_connection = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", "20011074"),
    database=os.getenv("DB_NAME", "qbandres")
)

# Importa las rutas después de configurar la aplicación. Esto es importante porque las rutas necesitan acceder a la instancia 'app'
# y a otras configuraciones establecidas previamente. Debe hacerse después de definir la aplicación y la configuración relevante.
from app.routes import *
