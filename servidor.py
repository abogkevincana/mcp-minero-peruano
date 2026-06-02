#!/usr/bin/env python3
"""
Servidor MCP Minero Peruano - Versión Ultra Liviana
Solo usa módulos nativos de Python (json, os, http.server)
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

# ============================================================
# CARGAR LOS DATOS DESDE EL JSON
# ============================================================
DATA_FILE = os.path.join(os.path.dirname(__file__), "datos", "mineria_data.json")

def cargar_articulos():
    """Lee el archivo JSON y devuelve una lista plana de artículos"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        todos = []
        for fuente in data.get("fuentes", []):
            for articulo in fuente.get("articulos", []):
                todos.append({
                    "numero": articulo["numero"],
                    "texto": articulo["texto"],
                    "fuente": fuente["nombre"],
                    "codigo": fuente["codigo"]
                })
        return todos
    except FileNotFoundError:
        print(f"❌ ERROR: No se encuentra el archivo {DATA_FILE}")
        print("   Asegúrate de haber ejecutado primero convertir.py")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: El archivo JSON tiene errores de sintaxis: {e}")
        return []
    except Exception as e:
        print(f"❌ ERROR inesperado: {e}")
        return []

# Cargar artículos al iniciar el servidor
ARTICULOS = cargar_articulos()
print(f"✅ Cargados {len(ARTICULOS)} artículos desde {DATA_FILE}")

# ============================================================
# HERRAMIENTAS (TOOLS) QUE CLAUDE PUEDE LLAMAR
# ============================================================

def obtener_articulo(numero: str) -> dict:
    """Busca un artículo por su número exacto (ej: '1', '2', '10')"""
    for art in ARTICULOS:
        if art["numero"] == numero:
            return {
                "encontrado": True,
                "numero": art["numero"],
                "texto": art["texto"],
                "fuente": art["fuente"]
            }
    return {
        "encontrado": False,
        "mensaje": f"No se encontró el artículo {numero}"
    }

def buscar_articulos(palabra: str) -> dict:
    """Busca artículos que contengan una palabra clave (insensible a mayúsculas)"""
    resultados = []
    for art in ARTICULOS:
        if palabra.lower() in art["texto"].lower():
            resultados.append({
                "numero": art["numero"],
                "texto_preview": art["texto"][:150] + "..." if len(art["texto"]) > 150 else art["texto"],
                "fuente": art["fuente"]
            })
    return {
        "total": len(resultados),
        "resultados": resultados[:10]
    }

def listar_articulos(desde: int = 1, hasta: int = 10) -> dict:
    """Lista artículos en un rango numérico (si los números son enteros)"""
    resultados = []
    for art in ARTICULOS:
        try:
            num_int = int(art["numero"])
            if desde <= num_int <= hasta:
                resultados.append({
                    "numero": art["numero"],
                    "texto_preview": art["texto"][:100] + "..." if len(art["texto"]) > 100 else art["texto"]
                })
        except ValueError:
            pass
    return {"articulos": resultados}

# ============================================================
# SERVIDOR HTTP COMPATIBLE CON MCP
# ============================================================
class MCPHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "ok",
                "articulos_cargados": len(ARTICULOS)
            }).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path != "/mcp":
            self.send_response(404)
            self.end_headers()
            return
        
        content_length = int(self.headers.get('Content-Length', 0))
        try:
            body = json.loads(self.rfile.read(content_length))
        except:
            self.send_response(400)
            self.end_headers()
            return
        
        tool_name = body.get("tool", "")
        arguments = body.get("arguments", {})
        
        if tool_name == "obtener_articulo":
            resultado = obtener_articulo(arguments.get("numero", ""))
        elif tool_name == "buscar_articulos":
            resultado = buscar_articulos(arguments.get("palabra", ""))
        elif tool_name == "listar_articulos":
            resultado = listar_articulos(arguments.get("desde", 1), arguments.get("hasta", 10))
        else:
            resultado = {
                "error": f"Herramienta '{tool_name}' no existe",
                "disponibles": ["obtener_articulo", "buscar_articulos", "listar_articulos"]
            }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(resultado, ensure_ascii=False).encode('utf-8'))
    
    def log_message(self, format, *args):
        pass

# ============================================================
# INICIAR EL SERVIDOR
# ============================================================
if __name__ == "__main__":
    PORT = 8080
    try:
        server = HTTPServer(("localhost", PORT), MCPHandler)
        print(f"✅ Servidor MCP Minero Peruano corriendo en http://localhost:{PORT}/mcp")
        print("Herramientas: obtener_articulo(numero), buscar_articulos(palabra), listar_articulos(desde, hasta)")
        print("Presiona Ctrl+C para detener")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
        server.shutdown()
    except Exception as e:
        print(f"❌ Error al iniciar el servidor: {e}")