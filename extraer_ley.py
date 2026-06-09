import pdfplumber
import re
import json

# Configuración
PDF_PATH = r"C:\mcp-minero\ley_mineria.pdf"
OUTPUT_TXT = r"datos\articulos_extraidos.txt"

def extraer_articulos(pdf_path):
    texto_completo = ""
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            texto_completo += pagina.extract_text() + "\n"
    
    # Patrón para buscar artículos
    patron = re.compile(
        r"(Artículo|ARTÍCULO)\s+(\d+(?:-\w+)?)\s*[.-]\s*(.*?)(?=(?:Artículo|ARTÍCULO)\s+\d+|$)",
        re.DOTALL | re.IGNORECASE
    )
    
    articulos = patron.findall(texto_completo)
    return articulos

def limpiar_texto(texto):
    # Elimina saltos de línea y espacios extras
    texto = texto.replace("\n", " ").strip()
    texto = re.sub(r'\s+', ' ', texto)
    return texto

def guardar_articulos(articulos, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for _, num, texto in articulos:
            texto_limpio = limpiar_texto(texto)
            f.write(f"Artículo {num}.- {texto_limpio}\n")
    print(f"✅ Guardados {len(articulos)} artículos en {output_path}")

# Ejecutar
if __name__ == "__main__":
    try:
        print(f"📄 Leyendo PDF: {PDF_PATH}")
        articulos = extraer_articulos(PDF_PATH)
        print(f"📝 Encontrados {len(articulos)} artículos")
        guardar_articulos(articulos, OUTPUT_TXT)
        print("🎉 ¡Extracción completada!")
    except Exception as e:
        print(f"❌ Error: {e}")