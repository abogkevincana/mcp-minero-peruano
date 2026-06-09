import json
import re

INPUT_FILE = "datos/mineria_data.json"
OUTPUT_FILE = "datos/mineria_data_sumillas_mejoradas.json"

def generar_sumilla(texto):
    """
    Genera una sumilla descriptiva basada en palabras clave del artículo
    """
    # Limpiar texto
    texto = texto.replace("\n", " ").strip()
    texto = re.sub(r'\s+', ' ', texto)
    
    # Eliminar guiones iniciales
    texto = re.sub(r'^[\s\-]+', '', texto)
    
    # Convertir a minúsculas para análisis
    texto_lower = texto.lower()
    
    # Detectar tema principal por palabras clave
    temas = []
    
    if any(p in texto_lower for p in ['cateo', 'prospección']):
        temas.append("cateo y prospección")
    if any(p in texto_lower for p in ['concesión', 'concesiones']):
        temas.append("concesión minera")
    if any(p in texto_lower for p in ['comercialización', 'comercializar']):
        temas.append("comercialización")
    if any(p in texto_lower for p in ['exploración']):
        temas.append("exploración")
    if any(p in texto_lower for p in ['explotación']):
        temas.append("explotación")
    if any(p in texto_lower for p in ['beneficio']):
        temas.append("beneficio")
    if any(p in texto_lower for p in ['seguridad', 'higiene']):
        temas.append("seguridad e higiene")
    if any(p in texto_lower for p in ['medio ambiente', 'ambiental']):
        temas.append("medio ambiente")
    if any(p in texto_lower for p in ['cierre', 'cierre de minas']):
        temas.append("cierre de minas")
    if any(p in texto_lower for p in ['nulidad']):
        temas.append("nulidad")
    if any(p in texto_lower for p in ['abandono']):
        temas.append("abandono")
    if any(p in texto_lower for p in ['penalidad', 'multa']):
        temas.append("penalidades")
    if any(p in texto_lower for p in ['derecho real']):
        temas.append("derecho real")
    if any(p in texto_lower for p in ['concesionario', 'titular']):
        temas.append("derechos del titular")
    
    # Si se detectaron temas, crear sumilla basada en ellos
    if temas:
        temas_unicos = list(set(temas))
        sumilla = f"Regula aspectos relacionados con: {', '.join(temas_unicos)}."
    else:
        # Si no se detectan temas, tomar primeras palabras significativas
        # Eliminar palabras comunes al inicio
        texto_sin_articulo = re.sub(r'^(artículo\s+\d+\.?\-?\s*)', '', texto, flags=re.IGNORECASE)
        palabras = texto_sin_articulo.split()[:15]
        sumilla = " ".join(palabras) + ("..." if len(palabras) == 15 else "")
    
    return sumilla

print("📖 Leyendo archivo JSON...")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

print("🔧 Generando sumillas mejoradas...")
total = 0
for fuente in data.get("fuentes", []):
    for articulo in fuente.get("articulos", []):
        texto = articulo.get("texto", "")
        if texto:
            nueva_sumilla = generar_sumilla(texto)
            articulo["sumilla"] = nueva_sumilla
            total += 1
        
        if total % 50 == 0:
            print(f"   Procesados {total} artículos...")

print(f"💾 Guardando {total} artículos con sumillas mejoradas...")
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ ¡Sumillas mejoradas completadas!")