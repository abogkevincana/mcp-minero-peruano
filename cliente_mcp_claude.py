import anthropic
import requests
import json
import os

# Configuración
MCP_SERVER_URL = "http://localhost:8080/mcp"

# Inicializa el cliente de Anthropic (lee la variable de entorno ANTHROPIC_API_KEY)
cliente = anthropic.Anthropic()

def ejecutar_herramienta_mcp(herramienta: str, argumentos: dict):
    payload = {"tool": herramienta, "arguments": argumentos}
    headers = {'Content-Type': 'application/json'}
    try:
        resp = requests.post(MCP_SERVER_URL, headers=headers, data=json.dumps(payload))
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": f"Fallo al conectar con MCP: {e}"}

herramientas = [
    {
        "name": "obtener_articulo",
        "description": "Obtiene un artículo de la Ley de Minería del Perú.",
        "input_schema": {
            "type": "object",
            "properties": {
                "numero": {"type": "string", "description": "Número del artículo"}
            },
            "required": ["numero"]
        }
    },
    {
        "name": "buscar_articulos",
        "description": "Busca artículos por palabra clave.",
        "input_schema": {
            "type": "object",
            "properties": {
                "palabra": {"type": "string", "description": "Palabra a buscar"}
            },
            "required": ["palabra"]
        }
    }
]

# Conversación simple
pregunta = input("🔨 Pregunta sobre la ley minera: ")
mensajes = [{"role": "user", "content": pregunta}]

respuesta = cliente.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=herramientas,
    messages=mensajes
)

bloque = respuesta.content[0]
if bloque.type == "tool_use":
    nombre = bloque.name
    args = bloque.input
    print(f"🛠️ Claude quiere ejecutar: {nombre} con {args}")
    resultado = ejecutar_herramienta_mcp(nombre, args)
    print("📄 Resultado del MCP:")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
elif bloque.type == "text":
    print("🤖 Respuesta de Claude:")
    print(bloque.text)