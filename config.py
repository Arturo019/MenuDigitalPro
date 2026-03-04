"""
Configuración central del proyecto: rutas de carpetas y constantes.
Usado por la app Flask (scripts) y por el generador de cartas (src/generator).
"""
import os

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
# URL base para el QR (para que el móvil abra la carta en tu servidor)
# Cambia esta IP por la IP local de tu PC en la red WiFi (ej: 192.168.1.100).
# Sin barra final. Ejemplo: "http://192.168.1.100:5000"
# Comprueba tu IP con: ipconfig (IPv4 del adaptador WiFi).
# Si el móvil no carga: permite Python en el Firewall de Windows (puerto 5000).
# ---------------------------------------------------------------------------
BASE_URL = "http://10.89.92.5:5000"

# ---------------------------------------------------------------------------
# Supabase: clave service_role (solo backend, NUNCA en el frontend).
# Necesaria para que "Hacer visible en el QR" y "Borrar" funcionen (bypass RLS).
# En Supabase: Project Settings → API → service_role (secret).
# Puedes ponerla aquí o en variable de entorno: SUPABASE_SERVICE_ROLE_KEY
# ---------------------------------------------------------------------------
SUPABASE_URL = "https://wtphpixmudjbcsnsgmrb.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind0cGhwaXhtdWRqYmNzbnNnbXJiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAxMDQ1OTgsImV4cCI6MjA4NTY4MDU5OH0.rTyb4WW2L8dXmr8RyxgWcUc0ONa2Gv972Pa8UkGAoro"
# Si no usas variable de entorno, se usa esta clave por defecto (solo en desarrollo; en producción usa env).
SUPABASE_SERVICE_ROLE_KEY = os.environ.get(
    "SUPABASE_SERVICE_ROLE_KEY",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind0cGhwaXhtdWRqYmNzbnNnbXJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDEwNDU5OCwiZXhwIjoyMDg1NjgwNTk4fQ.6iPdbTtn0QsjqbpF4d9UpZnPK-jjwLFuQ7jwORrqDK8"
)
