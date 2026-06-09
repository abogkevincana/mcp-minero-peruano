import re

INPUT_FILE = "datos/articulos.txt"
OUTPUT_FILE = "datos/articulos_sin_guiones.txt"

def corregir_guiones(texto):
    # Eliminar guiones y espacios al inicio de la línea
    # Ejemplos: "- texto" o "- - texto" o "- - - texto" → "texto"
    texto = re.sub(r'^[\s\-]+', '', texto)
    
    # Eliminar guiones que aparecen después de "Artículo X.-" pero antes del texto
    # Ejemplo: "Artículo 150.- - - - La nulidad..." → "Artículo 150.- La nulidad..."
    texto = re.sub(r'(Artículo\s+\d+\s*\.\-\s*)[\s\-]+', r'\1', texto, flags=re.IGNORECASE)
    
    return texto

print(f"📖 Leyendo {INPUT_FILE}...")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lineas = f.readlines()

print(f"🔧 Procesando {len(lineas)} artículos...")
articulos_corregidos = []
for i, linea in enumerate(lineas, 1):
    if not linea.strip():
        continue
    linea_corregida = corregir_guiones(linea)
    articulos_corregidos.append(linea_corregida)
    if i % 50 == 0:
        print(f"   Procesados {i} artículos...")

print(f"💾 Guardando en {OUTPUT_FILE}...")
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for articulo in articulos_corregidos:
        f.write(articulo + "\n")

print(f"✅ ¡Corrección completada! {len(articulos_corregidos)} artículos procesados.")