"""
Punto de entrada de la aplicación web.
Ejecutar con:  python app.py
Equivalente a: python scripts/import_excel.py
"""
import os
import sys

# Añadir carpeta scripts al path para importar la app Flask
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import import_excel

app = import_excel.app

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
