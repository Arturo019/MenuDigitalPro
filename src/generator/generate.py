"""
Generación de cartas digitales desde Excel: lee plantillas, rellena datos y guarda HTML + QR.
"""
import os
import pandas as pd
import qrcode

# Rutas del proyecto (config está en la raíz; se asume que la raíz está en sys.path al importar este módulo)
try:
    from config import BASE_DIR
except ImportError:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def generar_carta_excel(ruta_excel, template_color="blue"):

# 🌟 DEFINICIÓN DE MAPEO DE ALÉRGENOS 🌟
    # La clave (Key) es la palabra clave a buscar en la columna 'Alergenos' del Excel.
    # El valor (Value) es el nombre y ruta parcial de la imagen del icono.
    ALERGENO_MAPEO = {
        "Gluten": "gluten.png",
        "Crustáceos": "crustaceos.png", 
        "Huevo": "egg.png",
        "Pescado": "pescado.png",
        "Cacahuetes": "cacahuetes.png", 
        "Soja": "soja.png", 
        "Lactosa": "lacteos.png",# Usamos 'lacteos.png' para Leche, acorde a tu ejemplo.
        "Frutos Secos": "frutosSecos.png", 
        "Apio": "apio.png",
        "Mostaza": "mostaza.png",
        "Sesamo": "sesamo.png",
        "Sulfitos": "sulfitos.png", # Simplifico la clave para facilitar la coincidencia en el Excel.
        "Altramuces": "altramuces.png", 
        "Marisco": "marisco.png",
    }
    
    # Ruta base para los iconos, ajustada a tu formato: "../../static/icons/"
    BASE_ICON_PATH = "../../static/icons/"

    # 1️⃣ Leer Excel
    try:
        df = pd.read_excel(ruta_excel)
    except Exception as e:
        # Error genérico de lectura (archivo corrupto, formato no soportado)
        raise ValueError(f"Error al leer el archivo Excel/XML. Asegúrate de que el archivo no esté dañado. Detalle: {e}")

    # 🌟 MANEJO DE ERRORES: VERIFICAR COLUMNAS MANDATORIAS 🌟
    COLUMNAS_REQUERIDAS = ['Nombre Restaurante', 'Tipo', 'Nombre del plato', 'Ingredientes/Descripción', 'Precio', 'Alergenos']
    columnas_existentes = set(df.columns)
    columnas_faltantes = [col for col in COLUMNAS_REQUERIDAS if col not in columnas_existentes]

    if columnas_faltantes:
        mensaje_error = f"El archivo cargado no contiene todas las columnas requeridas: {', '.join(columnas_faltantes)}. Las columnas obligatorias son: {', '.join(COLUMNAS_REQUERIDAS)}"
        # Levantamos un ValueError específico que será capturado por Flask
        raise ValueError(mensaje_error)

    # 2️⃣ Obtener nombre del restaurante (tomamos el primero)
    nombre_restaurante = df['Nombre Restaurante'].iloc[0]

    # 3️⃣ Crear diccionario de tipos de plato
    categorias = {}
    for tipo in df["Tipo"].unique():
        categorias[tipo] = ""

    # 4️⃣ Generar HTML de cada plato (¡LÓGICA ACTUALIZADA PARA 14 ALÉRGENOS!)
    for _, row in df.iterrows():
        
        # 4.1 - Inicializar el HTML de los iconos
        alergeno_html = "" 
        
        # 4.2 - Obtener los alérgenos del plato y lista normalizada para el filtrado (coincide con value de los checkbox)
        texto_alergenos = str(row['Alergenos']).lower()
        alergenos_encontrados = []
        for palabra_clave, nombre_imagen in ALERGENO_MAPEO.items():
            if palabra_clave.lower() in texto_alergenos:
                ruta_completa_icono = f"{BASE_ICON_PATH}{nombre_imagen}"
                alergeno_html += f'<img src="{ruta_completa_icono}" alt="{palabra_clave}" class="icono-alergeno">'
                # Guardamos la clave en minúsculas para que coincida con value del checkbox (ej: "frutos secos")
                alergenos_encontrados.append(palabra_clave.lower())
        data_alergenos_val = ",".join(alergenos_encontrados)

        plato_html = f'''
        <div class="plato destacado" data-alergenos="{data_alergenos_val}">
            <div class="titulo">{row['Nombre del plato']}</div>
            <div class="precio">{row['Precio']} €</div>
            <div class="descripcion">{row['Ingredientes/Descripción']}</div>
            <div class="alergenos">
                {alergeno_html}
            </div>
        </div>

        '''

        categorias[row['Tipo']] += plato_html
    # 5️⃣ Leer plantilla HTML según el color seleccionado (templates/menu_{color}.html)
    template_file = f"menu_{template_color}.html"
    template_new_path = os.path.join(BASE_DIR, "templates", template_file)

    if os.path.exists(template_new_path):
        template_path = template_new_path
    else:
        # Respaldo: plantillas antiguas en carpeta plant/ (si existe)
        old_template_map = {
            "blue": "plantillaBlue.html",
            "brown_white": "plantillaBrown-White.html",
            "green": "plantillaGreen.html",
            "white_blue": "plantillaWhite-Blue.html",
        }
        template_old_path = os.path.join(
            BASE_DIR, "plant",
            old_template_map.get(template_color, "plantillaBlue.html"),
        )
        template_path = template_old_path if os.path.exists(template_old_path) else template_new_path
    with open(template_path, "r", encoding="utf-8") as f:
        plantilla = f.read()

    # 6️⃣ Reemplazar marcador del nombre del restaurante
    plantilla = plantilla.replace("{{Nombre Restaurante}}", nombre_restaurante)

    # 7️⃣ Crear fieldsets dinámicos
    fieldsets_html = ""
    for tipo, platos_html in categorias.items():
        fieldsets_html += f'''
        <fieldset>
            <legend>{tipo}</legend>
            <div class="containerPlatos">
                {platos_html}
            </div>
        </fieldset>
        '''

    # 8️⃣ Reemplazar marcador por todos los fieldsets generados
    plantilla = plantilla.replace("<!-- {{FIELDSETS_PLATOS}} -->", fieldsets_html)

    # 9️⃣ Guardar HTML generado
    output_dir = os.path.join(BASE_DIR, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # NUEVO: Limpiamos el nombre del restaurante quitando los espacios
    nombre_limpio = nombre_restaurante.replace(" ", "")
    
    # Creamos el nombre del archivo usando el nombre limpio y el color
    output_filename = f"carta_{nombre_limpio}_{template_color}.html" 
    
    salida = os.path.join(output_dir, output_filename)
    with open(salida, "w", encoding="utf-8") as f:
        f.write(plantilla)

    print(f"Carta generada correctamente: {output_filename} ✅")
    
    # IMPORTANTE: Ahora devolvemos la ruta de salida, el nombre del archivo y el nombre original del restaurante
    return salida, output_filename, nombre_restaurante



def generar_qr(url, user_id="default"):
    """Genera imagen QR y la guarda con un nombre único por usuario."""
    carpeta_qr = os.path.join(BASE_DIR, "static", "QRs")
    os.makedirs(carpeta_qr, exist_ok=True)

    # El archivo ahora se llamará qr_IDDELUSUARIO.png
    nombre_qr = f"qr_{user_id}.png"
    qr_path = os.path.join(carpeta_qr, nombre_qr)

    # Crear QR
    qr = qrcode.make(url)
    qr.save(qr_path)

    print(f"QR generado correctamente en: {qr_path}")
    return f"/static/QRs/{nombre_qr}"


if __name__ == "__main__":
    # Solo al ejecutar este script directamente (ej. pruebas)
    url_final = "http://10.89.92.5:5000"
    ruta_qr = generar_qr(url_final)
    print(f"Ruta del QR: {ruta_qr}")