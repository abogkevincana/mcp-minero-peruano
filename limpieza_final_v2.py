import re

INPUT_FILE = "datos/articulos.txt"
OUTPUT_FILE = "datos/articulos_final_v2.txt"

def limpieza_total(texto):
    # 1. Eliminar TODOS los guiones y espacios al inicio (cualquier cantidad)
    texto = re.sub(r'^[\s\-]+', '', texto)
    
    # 2. Eliminar letras sueltas como "j" entre palabras (ej: "será j deducida" → "será deducida")
    texto = re.sub(r'\s+[a-z]\s+', ' ', texto)
    
    # 3. Eliminar barras invertidas
    texto = texto.replace('\\', '')
    
    # 4. Eliminar espacios múltiples
    texto = re.sub(r'\s+', ' ', texto)
    
    # 5. Asegurar formato "Artículo X.-" sin guiones extra después
    texto = re.sub(r'(Artículo\s+\d+\s*\.\-\s*)[\s\-]+', r'\1', texto, flags=re.IGNORECASE)
    
    # 6. Corregir palabras con acentos cortados
    for buscar, reemplazar in [('á\\', 'á'), ('é\\', 'é'), ('í\\', 'í'), ('ó\\', 'ó'), ('ú\\', 'ú'), ('ñ\\', 'ñ')]:
        texto = texto.replace(buscar, reemplazar)
    
    return texto.strip()

print("📖 Leyendo archivo...")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lineas = f.readlines()

print(f"🔧 Procesando {len(lineas)} artículos...")
limpios = []
for i, linea in enumerate(lineas, 1):
    if not linea.strip():
        continue
    limpia = limpieza_total(linea)
    if limpia:
        limpios.append(limpia)
    if i % 50 == 0:
        print(f"   Procesados {i}...")

print(f"💾 Guardando {len(limpios)} artículos...")
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for art in limpios:
        f.write(art + "\n")

print("✅ ¡Limpieza completada!")