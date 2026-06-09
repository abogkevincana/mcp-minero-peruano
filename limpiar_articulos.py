import re

# Archivos
INPUT_FILE = "datos/articulos.txt"
OUTPUT_FILE = "datos/articulos_limpios.txt"

def limpiar_texto(texto):
    # Eliminar guiones al inicio que no pertenecen al artículo
    texto = re.sub(r'^-\s*', '', texto)
    
    # Reemplazar múltiples espacios por uno solo
    texto = re.sub(r'\s+', ' ', texto)
    
    # Eliminar caracteres raros comunes en PDFs (ej: \xa0, \u200b, etc.)
    texto = texto.replace('\xa0', ' ')
    texto = texto.replace('\u200b', '')
    
    # Corregir palabras pegadas (ej: "texto." seguido de "Artículo" sin espacio)
    texto = re.sub(r'\.([A-ZÁÉÍÓÚ])', r'. \1', texto)
    
    # Asegurar formato "Artículo X.-" (punto y guión)
    texto = re.sub(r'(Artículo\s+\d+)\s*[\.\-]?\s*', r'\1.- ', texto, flags=re.IGNORECASE)
    
    # Eliminar espacios al inicio y final
    texto = texto.strip()
    
    return texto

def limpiar_archivo():
    print(f"📖 Leyendo {INPUT_FILE}...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lineas = f.readlines()
    
    articulos_limpios = []
    for i, linea in enumerate(lineas, 1):
        if not linea.strip():
            continue
        texto_limpio = limpiar_texto(linea)
        articulos_limpios.append(texto_limpio)
        if i % 50 == 0:
            print(f"   Procesados {i} artículos...")
    
    print(f"💾 Guardando {len(articulos_limpios)} artículos en {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for articulo in articulos_limpios:
            f.write(articulo + "\n")
    
    print(f"✅ ¡Limpieza completada! {len(articulos_limpios)} artículos procesados.")

if __name__ == "__main__":
    limpiar_archivo()