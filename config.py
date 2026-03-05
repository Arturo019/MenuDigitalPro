"""
Configuración central del proyecto: rutas de carpetas y constantes.
Usado por la app Flask (scripts) y por el generador de cartas (src/generator).
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Raíz del proyecto (carpeta donde está config.py)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Carpetas principales
SRC_DIR = os.path.join(BASE_DIR, "src")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "data", "inputs")

# Carpetas dentro de static (para referencia)
QR_FOLDER = os.path.join(STATIC_DIR, "QRs")
ICONS_FOLDER = os.path.join(STATIC_DIR, "icons")

# ---------------------------------------------------------------------------
# URL base para el QR (la que se codifica en el código QR).
# - Red local: solo dispositivos en tu WiFi (ej: "http://10.89.92.5:5000").
# - Para que CUALQUIERA pueda escanear el QR: sube la app a un servidor con URL
#   pública y pon aquí esa URL (o define la variable de entorno BASE_URL).
#   Ejemplo: "https://tu-app.onrender.com" o "https://cartadigital.tudominio.com"
# Sin barra final. Variable de entorno: BASE_URL (prioridad sobre el valor por defecto).
# ---------------------------------------------------------------------------
BASE_URL = os.environ.get("BASE_URL", "http://10.89.92.5:5000")

# ---------------------------------------------------------------------------
# Supabase: clave service_role (solo backend, NUNCA en el frontend).
# Necesaria para que "Hacer visible en el QR" y "Borrar" funcionen (bypass RLS).
# En Supabase: Project Settings → API → service_role (secret).
# Puedes ponerla aquí o en variable de entorno: SUPABASE_SERVICE_ROLE_KEY
# ---------------------------------------------------------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
