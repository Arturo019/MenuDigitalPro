"""
Aplicación Flask: rutas web, subida de Excel y generación de cartas.
Punto de entrada: ejecutar con `python scripts/import_excel.py` o `python app.py`.
"""
import os
import sys

# Configurar path ANTES de importar config o generator (raíz y src deben estar en sys.path)
_scripts_dir = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(_scripts_dir)
sys.path.insert(0, _root)
_src = os.path.join(_root, "src")
if _src not in sys.path:
    sys.path.append(_src)

from config import (
    BASE_DIR,
    BASE_URL,
    TEMPLATE_DIR,
    STATIC_DIR,
    OUTPUT_DIR,
    UPLOAD_FOLDER,
    SUPABASE_URL,
    SUPABASE_ANON_KEY,
    SUPABASE_SERVICE_ROLE_KEY,
)
from typing import Optional
from flask import Flask, request, render_template, send_from_directory, redirect, url_for, jsonify
from generator.generate import generar_carta_excel, generar_qr
from supabase import create_client, Client

# Cliente Supabase con clave anon (para lectura en /menu y para insert en upload)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Cliente con service_role: bypass RLS para activar/borrar cartas (solo si está configurada la clave)
supabase_admin: Optional[Client] = None
if SUPABASE_SERVICE_ROLE_KEY:
    supabase_admin = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
else:
    print("⚠️ SUPABASE_SERVICE_ROLE_KEY no configurada: activar/borrar carta desde Mis Cartas puede fallar por RLS.")

# ---------------------------------------------------------------------------
# App Flask
# ---------------------------------------------------------------------------
app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------------------------------------------------------------------
# Rutas: archivos estáticos generados (output)
# ---------------------------------------------------------------------------
@app.route("/output/<path:filename>")
def serve_output(filename):
    return send_from_directory(OUTPUT_DIR, filename)

# ---------------------------------------------------------------------------
# Rutas: páginas principales
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("inicio.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/logout")
def logout():
    # Página que ejecuta signOut() en el cliente y redirige a /login
    return render_template("logout.html")

@app.route("/mis_cartas")
def mis_cartas():
    return render_template("mis_cartas.html")

# ---------------------------------------------------------------------------
# API: activar y borrar carta (usan service_role para que RLS no bloquee)
# ---------------------------------------------------------------------------
@app.route("/api/activar-carta", methods=["POST"])
def api_activar_carta():
    """Pone activa=True en la carta indicada y activa=False en el resto del usuario."""
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    carta_id = data.get("carta_id")
    if not user_id or carta_id is None:
        return jsonify({"ok": False, "error": "Faltan user_id o carta_id"}), 400
    if not supabase_admin:
        return jsonify({
            "ok": False,
            "error": "Activar no disponible: configura SUPABASE_SERVICE_ROLE_KEY en Render (Supabase → Project Settings → API → service_role)."
        }), 503
    try:
        supabase_admin.table("cartas").update({"activa": False}).eq("user_id", user_id).execute()
        r = supabase_admin.table("cartas").update({"activa": True}).eq("id", carta_id).eq("user_id", user_id).execute()
        if not r.data:
            return jsonify({"ok": False, "error": "Carta no encontrada o no es tuya"}), 404
        return jsonify({"ok": True})
    except Exception as e:
        print(f"Error API activar-carta: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/borrar-carta", methods=["POST"])
def api_borrar_carta():
    """Elimina la carta solo si pertenece al user_id."""
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    carta_id = data.get("carta_id")
    if not user_id or carta_id is None:
        return jsonify({"ok": False, "error": "Faltan user_id o carta_id"}), 400
    if not supabase_admin:
        return jsonify({
            "ok": False,
            "error": "Borrar no disponible: configura SUPABASE_SERVICE_ROLE_KEY en Render (Supabase → Project Settings → API → service_role)."
        }), 503
    try:
        supabase_admin.table("cartas").delete().eq("id", carta_id).eq("user_id", user_id).execute()
        return jsonify({"ok": True})
    except Exception as e:
        print(f"Error API borrar-carta: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# ---------------------------------------------------------------------------
# Rutas: subida y generación de carta
# ---------------------------------------------------------------------------
@app.route("/upload", methods=["POST"])
def upload_file():
    if "xmlfile" not in request.files:
        return "No se envió ningún archivo", 400

    file = request.files["xmlfile"]

    if file.filename == "":
        return "Archivo vacío", 400

    # Obtener el color de plantilla seleccionado (por defecto blue)
    template_color = request.form.get("template_color", "blue")
    print(f"🎨 Color recibido del formulario: '{template_color}'")

    # Guardamos el archivo en la carpeta configurada
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    try:
        # 1. GENERAMOS LA CARTA
        ruta_carta, archivo_generado, nombre_restaurante = generar_carta_excel(filepath, template_color)

        # 2. CAPTURAMOS EL USUARIO Y GENERAMOS EL QR ÚNICO
        user_id = request.form.get("user_id")
        if not user_id:
            return "Error: Debes iniciar sesión para subir una carta.", 400

        # URL del QR: usa BASE_URL de config (pon ahí la IP de tu PC para que el móvil llegue al servidor)
        url_invariable = f"{BASE_URL.rstrip('/')}/menu/{user_id}"
        qr_path = generar_qr(url_invariable, user_id)

        # 3. GUARDAMOS LA CARTA EN SUPABASE (activa por defecto; usamos admin si hay para evitar RLS)
        client_db = supabase_admin if supabase_admin else supabase
        try:
            client_db.table("cartas").update({"activa": False}).eq("user_id", user_id).execute()
            client_db.table("cartas").insert({
                "user_id": user_id,
                "nombre_restaurante": nombre_restaurante,
                "archivo_html": archivo_generado,
                "color_plantilla": template_color,
                "activa": True,
            }).execute()
        except Exception as error_bd:
            print(f"Error al guardar en BD: {error_bd}")

        # 4. MOSTRAMOS EL RESULTADO AL USUARIO
        return render_template(
            "upload_result.html",
            page_title="Carta generada",
            heading="Carta generada",
            subtitle_lines=[
                f'Archivo "{file.filename}" subido correctamente.',
                f"Plantilla: {template_color}",
            ],
            qr_path=qr_path,
            qr_note="Tu carta está activa. Escanea el QR desde el móvil para ver el menú. En 'Mis Cartas' puedes cambiar qué carta muestra el QR.",
            detail=None,
            
            # Pasamos estos datos por si los muestras en el HTML
            archivo_generado=archivo_generado,
            nombre_restaurante=nombre_restaurante,
            color_plantilla=template_color,
            
            # Actualizamos el botón para que lleve a la carta exacta
            cta_href=f"/output/{archivo_generado}",
            cta_label="Ver carta generada",
        )
    except ValueError as e:
        # Captura el error de formato (columnas faltantes o error de lectura de pandas)
        print(f"Error de generación: {e}")
        # Opcionalmente, se puede borrar el archivo subido aquí.
        return (
            render_template(
                "upload_result.html",
                page_title="Error al generar",
                heading="Error al generar la carta",
                subtitle_lines=["El archivo subido no tiene el formato o contenido correcto."],
                qr_path=None,
                qr_note=None,
                detail=f"Detalle: {e}",
                cta_href="/",
                cta_label="Volver al inicio",
            ),
            400,
        )
    except Exception as e:
        # Captura cualquier otro error inesperado durante la generación (ej. permiso de archivo)
        print(f"Error inesperado durante la generación: {e}")
        return (
            render_template(
                "upload_result.html",
                page_title="Error inesperado",
                heading="Error inesperado",
                subtitle_lines=["Ocurrió un error al procesar el archivo."],
                qr_path=None,
                qr_note=None,
                detail=f"Detalle: {e}",
                cta_href="/",
                cta_label="Volver al inicio",
            ),
            500,
        )



# ---------------------------------------------------------------------------
# Ruta: menú por usuario (QR en la mesa)
# ---------------------------------------------------------------------------
@app.route('/menu/<user_id>')
def ver_menu_restaurante(user_id):
    try:
        # Lectura con admin si hay (evita RLS); así el móvil sin sesión puede ver la carta
        client = supabase_admin if supabase_admin else supabase
        respuesta = client.table('cartas') \
            .select('archivo_html') \
            .eq('user_id', user_id) \
            .eq('activa', True) \
            .limit(1) \
            .execute()
        
        # Si encontramos una carta activa...
        if respuesta.data and len(respuesta.data) > 0:
            archivo_html = respuesta.data[0]['archivo_html']
            # Redirigimos a la ruta que ya tienes creada para mostrar el HTML
            return redirect(url_for('serve_output', filename=archivo_html))
        else:
            return "Este restaurante aún no tiene una carta activa. El dueño debe activarla en su panel.", 404
            
    except Exception as e:
        print(f"Error al buscar la carta: {e}")
        return "Hubo un error al buscar el menú.", 500


# ---------------------------------------------------------------------------
# Rutas: ver carta (última generada, por compatibilidad)
# ---------------------------------------------------------------------------
@app.route("/ver_carta")
def ver_carta():
    try:
        carta_files = [
            f for f in os.listdir(OUTPUT_DIR)
            if f.startswith("carta_") and f.endswith(".html")
        ]
        if not carta_files:
            return "<h3>No hay ninguna carta generada aún.</h3>"
        
        # Tomar la más reciente
        latest_file = max(
            carta_files,
            key=lambda f: os.path.getmtime(os.path.join(OUTPUT_DIR, f)),
        )
        output_path = os.path.join(OUTPUT_DIR, latest_file)
        
        with open(output_path, "r", encoding="utf-8") as f:
            html = f.read()
        return html
    except FileNotFoundError:
        return "<h3>No hay ninguna carta generada aún.</h3>"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
