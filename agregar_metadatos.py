import json

# Archivos
INPUT_JSON = "datos/mineria_data.json"
OUTPUT_JSON = "datos/mineria_data_con_metadatos.json"

# Abrir el JSON actual
with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

# Recorrer todos los artículos y añadir status y sumilla básica
total = 0
for fuente in data.get("fuentes", []):
    for articulo in fuente.get("articulos", []):
        # Añadir status (por defecto "vigente")
        if "status" not in articulo:
            articulo["status"] = "vigente"
        
        # Añadir sumilla básica (primeros 80 caracteres del texto)
        if "sumilla" not in articulo:
            texto = articulo.get("texto", "")
            # Limpiar un poco el texto para la sumilla
            texto_limpio = texto.replace("\n", " ").strip()
            sumilla = texto_limpio[:80] + "..." if len(texto_limpio) > 80 else texto_limpio
            articulo["sumilla"] = sumilla
        
        total += 1

# Guardar el nuevo JSON
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ Metadatos añadidos a {total} artículos")
print(f"📁 Guardado en: {OUTPUT_JSON}")