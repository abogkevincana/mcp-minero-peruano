import anthropic

cliente = anthropic.Anthropic()  # usa variable de entorno ANTHROPIC_API_KEY

mensaje = cliente.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=100,
    messages=[{"role": "user", "content": "Di 'Hola mundo'"}]
)
print(mensaje.content[0].text)