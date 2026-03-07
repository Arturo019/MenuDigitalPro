# Proyecto generación de cartas desde Excel

Aplicación web (Flask) para subir un Excel con la carta del restaurante, elegir una plantilla de diseño y generar una carta digital (HTML) con código QR. Incluye autenticación con Supabase y listado de “Mis Cartas”.

## Requisitos

- Python 3.10+
- Dependencias: `pip install -r requirements.txt`

## Cómo ejecutar

```bash
python app.py
```

O bien: `python scripts/import_excel.py`

Abrir en el navegador: `http://127.0.0.1:5000/`

## Estructura del proyecto

Ver **`PROJECT_STRUCTURE.md`** para una guía detallada. Resumen:

- **`config.py`** – Rutas del proyecto (carpetas templates, static, output, etc.).
- **`app.py`** – Punto de entrada; arranca la app Flask.
- **`scripts/import_excel.py`** – Rutas web (inicio, login, upload, mis_cartas, output).
- **`src/generator/generate.py`** – Generación de cartas desde Excel y QR.
- **`templates/`** – Páginas HTML (inicio, login, mis_cartas, upload_result) y plantillas de carta (menu_blue, menu_green, …).
- **`static/`** – CSS, JS (Supabase, authCheck, menú), iconos, QRs.
- **`output/`** – Cartas HTML generadas.

## Columnas obligatorias del Excel

El archivo debe tener estas columnas:  
`Nombre Restaurante`, `Tipo`, `Nombre del plato`, `Ingredientes/Descripción`, `Precio`, `Alergenos`.

Puedes usar la plantilla `ExcelFinal.xlsx` (enlace en la página de inicio).

## Uso del generador por código

```python
# Asegurar que la raíz del proyecto está en sys.path
from generator.generate import generar_carta_excel, generar_qr

ruta_html, nombre_archivo, nombre_rest = generar_carta_excel(
    "data/inputs/mi_archivo.xlsx",
    template_color="blue"
)
qr_url = generar_qr("http://127.0.0.1:5000/output/" + nombre_archivo)
```

## Notas

- La autenticación es con Supabase en el cliente; `/logout` carga una página que ejecuta signOut y redirige a login.
- Si usas OneDrive, evita mover o renombrar carpetas durante la sincronización.

