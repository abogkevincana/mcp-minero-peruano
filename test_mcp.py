import requests, json
resp = requests.post("http://localhost:8080/mcp", headers={"Content-Type": "application/json"}, data=json.dumps({"tool": "obtener_articulo", "arguments": {"numero": "1"}}))
print(resp.status_code, resp.json())