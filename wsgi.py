import sys
import os

# Agrega el directorio del proyecto al path
project_path = os.path.expanduser('home/Arcay/Lab4_Middle')
if project_path not in sys.path:
    sys.path.append(project_path)

# Importa el app de FastAPI
from main import app

# El WSGI debe exponer la aplicación como una variable llamada 'application'
application = app
