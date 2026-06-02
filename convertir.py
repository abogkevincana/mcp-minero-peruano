import json
import re

input_file = "datos/articulos.txt"
output_file = "datos/mineria_data.json"

with open(input_file, "r", encoding="utf-8") as f:
    lineas = f.readlines()

patron = re.compile(r"Artículo\s+(\d+(?:-\w+)?)\s*[.-]\s*(.*)", re.IGNORECASE)
articulos = []
for linea in lineas:
    linea = linea.strip()
    if not linea:
        continue
    match = patron.match(linea)
    if match:
        numero = match.group(1)
        texto = match.group(2).strip()
        articulos.append({"numero": numero, "texto": texto})

if not articulos:
    print("ERROR: No se encontraron artículos. Verifica el formato.")
    exit(1)

data = {
    "fuentes": [
        {
            "nombre": "TUO Ley General de Minería",
            "codigo": "LGM",
            "articulos": articulos
        }
    ]
}

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ Convertidos {len(articulos)} artículos a {output_file}")