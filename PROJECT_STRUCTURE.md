# Estructura del proyecto

Guía rápida para entender dónde está cada cosa.

## Cómo arrancar la aplicación

```bash
python app.py
# o
python scripts/import_excel.py
```

Luego abrir `http://127.0.0.1:5000/`.

---

## Carpetas principales

| Carpeta      | Uso |
|-------------|-----|
| **`config.py`** (raíz) | Rutas del proyecto (BASE_DIR, TEMPLATE_DIR, OUTPUT_DIR, etc.). Lo usan la app Flask y el generador. |
| **`app.py`** (raíz) | Punto de entrada: importa la app desde `scripts/import_excel.py` y la ejecuta. |
| **`scripts/`** | Código de la aplicación web: `import_excel.py` define todas las rutas Flask (/, /login, /upload, /mis_cartas, /output/..., etc.). |
| **`src/generator/`** | Lógica de negocio: `generate.py` lee Excel, rellena plantillas HTML y genera QR. No depende de Flask. |
| **`templates/`** | Plantillas Jinja: páginas (inicio, login, mis_cartas, upload_result) y plantillas de carta (menu_blue.html, menu_green.html, …). |
| **`static/`** | CSS, JS, iconos, QRs generados, Excel de plantilla. |
| **`output/`** | Cartas HTML generadas (carta_NombreRestaurante_color.html). Se sirven por la ruta `/output/<filename>`. |
| **`data/inputs/`** | Archivos Excel subidos por el usuario (creada al primer upload). |

---

## Rutas Flask (resumen)

- **`/`** → Inicio (subir carta, ejemplos).
- **`/login`**, **`/register`**, **`/logout`** → Auth (la sesión real es Supabase en el cliente).
- **`/mis_cartas`** → Lista de cartas guardadas (Supabase).
- **`/upload`** (POST) → Recibe Excel, llama a `generar_carta_excel` y `generar_qr`, devuelve `upload_result.html`.
- **`/output/<filename>`** → Sirve el HTML de una carta generada.
- **`/ver_carta`** → Redirige a la última carta generada (compatibilidad).

---

## Archivos clave

- **`config.py`** – Rutas compartidas.
- **`scripts/import_excel.py`** – Definición de la app y todas las rutas.
- **`src/generator/generate.py`** – `generar_carta_excel()`, `generar_qr()`.
- **`static/js/supabaseClient.js`** – Cliente Supabase (auth y BD).
- **`static/js/authCheck.js`** – Comprueba sesión y redirige a /login si no hay usuario (usado en mis_cartas; inicio permite ver sin sesión).
- **`static/js/inicio.js`** – Menú hamburguesa (inicio y mis_cartas).
- **`static/js/menu.js`** – Lógica del menú de alergias en las cartas generadas.

---

## Columnas obligatorias del Excel

El generador espera exactamente:  
`Nombre Restaurante`, `Tipo`, `Nombre del plato`, `Ingredientes/Descripción`, `Precio`, `Alergenos`.
