import re

INPUT_FILE = "datos/articulos.txt"
OUTPUT_FILE = "datos/articulos_final.txt"

def limpieza_profunda(texto):
    # 1. Eliminar guiones y espacios al inicio de la línea
    texto = re.sub(r'^[\s\-]+', '', texto)
    
    # 2. Eliminar barras invertidas (\) que quedaron del PDF
    texto = texto.replace('\\', '')
    
    # 3. Eliminar guiones que aparecen después de "Artículo X.-"
    texto = re.sub(r'(Artículo\s+\d+\s*\.\-\s*)[\s\-]+', r'\1', texto, flags=re.IGNORECASE)
    
    # 4. Reemplazar múltiples espacios por uno solo
    texto = re.sub(r'\s+', ' ', texto)
    
    # 5. Corregir palabras cortadas (ej: "trá\mite" → "trámite")
    texto = texto.replace('á\\', 'á')
    texto = texto.replace('é\\', 'é')
    texto = texto.replace('í\\', 'í')
    texto = texto.replace('ó\\', 'ó')
    texto = texto.replace('ú\\', 'ú')
    texto = texto.replace('ñ\\', 'ñ')
    
    # 6. Eliminar espacios antes de puntos y comas
    texto = re.sub(r'\s+\.', '.', texto)
    texto = re.sub(r'\s+\,', ',', texto)
    
    return texto.strip()

print(f"📖 Leyendo {INPUT_FILE}...")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lineas = f.readlines()

print(f"🔧 Procesando {len(lineas)} artículos...")
articulos_limpios = []
for i, linea in enumerate(lineas, 1):
    if not linea.strip():
        continue
    linea_limpia = limpieza_profunda(linea)
    if linea_limpia:
        articulos_limpios.append(linea_limpia)
    if i % 50 == 0:
        print(f"   Procesados {i} artículos...")

print(f"💾 Guardando {len(articulos_limpios)} artículos en {OUTPUT_FILE}...")
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for articulo in articulos_limpios:
        f.write(articulo + "\n")

print(f"✅ ¡Limpieza final completada!")