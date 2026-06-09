#!/usr/bin/env python3
"""
Servidor MCP Minero Peruano - Con metadatos (status, sumilla)
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

DATA_FILE = os.path.join(os.path.dirname(__file__), "datos", "mineria_data.json")

def cargar_articulos():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        todos = []
        for fuente in data.get("fuentes", []):
            for art in fuente.get("articulos", []):
                item = {
                    "numero": art["numero"],
                    "texto": art["texto"],
                    "fuente": fuente["nombre"],
                    "codigo": fuente["codigo"]
                }
                if "status" in art:
                    item["status"] = art["status"]
                if "sumilla" in art:
                    item["sumilla"] = art["sumilla"]
                todos.append(item)
        return todos
    except Exception as e:
        print(f"Error cargando JSON: {e}")
        return []

ARTICULOS = cargar_articulos()
print(f"✅ Cargados {len(ARTICULOS)} artículos")

def obtener_articulo(numero: str) -> dict:
    for art in ARTICULOS:
        if art["numero"] == numero:
            resultado = {
                "encontrado": True,
                "numero": art["numero"],
                "texto": art["texto"],
                "fuente": art["fuente"]
            }
            if "status" in art:
                resultado["status"] = art["status"]
                if art["status"] == "derogado":
                    resultado["advertencia"] = "⚠️ Este artículo está derogado."
            if "sumilla" in art:
                resultado["sumilla"] = art["sumilla"]
            return resultado
    return {"encontrado": False, "mensaje": f"No se encontró artículo {numero}"}

def buscar_articulos(palabra: str) -> dict:
    palabra_lower = palabra.lower()
    resultados = []
    for art in ARTICULOS:
        if (palabra_lower in art["texto"].lower() or 
            (palabra_lower in art.get("sumilla", "").lower())):
            resultados.append({
                "numero": art["numero"],
                "texto_preview": art["texto"][:120] + "...",
                "sumilla": art.get("sumilla", ""),
                "status": art.get("status", "")
            })
    return {"total": len(resultados), "resultados": resultados[:10]}

def listar_articulos(desde: int = 1, hasta: int = 10) -> dict:
    resultados = []
    for art in ARTICULOS:
        try:
            num = int(art["numero"])
            if desde <= num <= hasta:
                resultados.append({"numero": art["numero"], "sumilla": art.get("sumilla", "")})
        except:
            pass
    return {"articulos": resultados}

class MCPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "articulos": len(ARTICULOS)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path != "/mcp":
            self.send_response(404)
            return
        length = int(self.headers.get('Content-Length', 0))
        try:
            body = json.loads(self.rfile.read(length))
        except:
            self.send_response(400)
            return
        tool = body.get("tool", "")
        args = body.get("arguments", {})
        if tool == "obtener_articulo":
            res = obtener_articulo(args.get("numero", ""))
        elif tool == "buscar_articulos":
            res = buscar_articulos(args.get("palabra", ""))
        elif tool == "listar_articulos":
            res = listar_articulos(args.get("desde", 1), args.get("hasta", 10))
        else:
            res = {"error": f"Herramienta '{tool}' no existe"}
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
    
    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    PORT = 8080
    try:
        server = HTTPServer(("localhost", PORT), MCPHandler)
        print(f"✅ Servidor MCP corriendo en http://localhost:{PORT}/mcp")
        print("Herramientas: obtener_articulo, buscar_articulos, listar_articulos")
        print("Presiona Ctrl+C para detener")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido")
        server.shutdown()