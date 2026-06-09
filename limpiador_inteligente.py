import re

INPUT_FILE = "datos/articulos.txt"
OUTPUT_FILE = "datos/articulos_limpio_definitivo.txt"

def limpiar_inteligente(texto):
    # 1. Proteger el formato "Artículo X.-" (NO tocar)
    #    (Este patrón no se modifica)
    
    # 2. Eliminar guiones sueltos que NO pertenecen al formato de artículo
    #    Ejemplo: "- La" → " La", "-Los" → " Los", "-El" → " El"
    texto = re.sub(r'-\s+(La|la|El|el|Los|los|Las|las|Una|una)', r' \1', texto)
    
    # 3. Eliminar guiones pegados a palabras al inicio (ej: "-La" → "La")
    texto = re.sub(r'^-([A-ZÁÉÍÓÚ])', r'\1', texto)
    texto = re.sub(r'\s-([A-ZÁÉÍÓÚ])', r' \1', texto)
    
    # 4. Eliminar múltiples guiones seguidos (ej: "- - - texto" → "texto")
    texto = re.sub(r'(\s|^)[\s\-]+', r'\1', texto)
    
    # 5. Eliminar letras sueltas como "j" entre palabras
    texto = re.sub(r'\s+[a-z]\s+', ' ', texto)
    
    # 6. Eliminar barras invertidas y caracteres raros
    texto = texto.replace('\\', '')
    texto = texto.replace('\xa0', ' ')
    
    # 7. Corregir espacios múltiples
    texto = re.sub(r'\s+', ' ', texto)
    
    # 8. Corregir espacios antes de puntos
    texto = re.sub(r'\s+\.', '.', texto)
    
    return texto.strip()

print("📖 Leyendo archivo...")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lineas = f.readlines()

print(f"🔧 Procesando {len(lineas)} artículos...")
limpios = []
for i, linea in enumerate(lineas, 1):
    if not linea.strip():
        continue
    limpia = limpiar_inteligente(linea)
    if limpia:
        limpios.append(limpia)
    if i % 50 == 0:
        print(f"   Procesados {i}...")

print(f"💾 Guardando {len(limpios)} artículos...")
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for art in limpios:
        f.write(art + "\n")

print("✅ ¡Limpieza inteligente completada!")