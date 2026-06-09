# MCP Minero Peruano

Servidor MCP (Model Context Protocol) para la **Ley General de Minería del Perú (TUO DS 014-92-EM)**.

## 🚀 Características actuales

- ✅ 228 artículos extraídos desde el PDF oficial
- ✅ Metadatos: `status` (vigente) y `sumilla` (resumen automático)
- ✅ Herramientas MCP: `obtener_articulo`, `buscar_articulos`, `listar_articulos`
- ✅ Compatible con Claude Desktop, DeepSeek y cualquier cliente MCP

## 📜 Normativa actual incluida

- ✅ TUO de la Ley General de Minería (DS 014-92-EM) - 228 artículos

## 🗺️ Hoja de ruta (próximas incorporaciones)

| Normativa | Estado |
|-----------|--------|
| Reglamento de Seguridad y Salud Ocupacional en Minería (DS 024-2016-EM) | 🔜 Próximamente |
| Ley de Cierre de Minas (Ley 28090 y modificatorias) | 🔜 Próximamente|
| Reglamento de Protección Ambiental para Actividades Mineras | 🔜 Próximamente |
| TUO de la Ley Ambiental para Minería | 🔜 Próximamente |
| Jurisprudencia relevante del Tribunal Minero | 🔜 En estudio |

## 🎯 Objetivo del proyecto

Construir la **base de datos normativa minera peruana más completa y accesible** para inteligencia artificial, permitiendo consultas precisas, sin alucinaciones, y con trazabilidad de fuentes oficiales.

## 📦 Instalación

```bash
git clone https://github.com/abogkevincana/mcp-minero-peruano.git
cd mcp-minero-peruano
python servidor.py
