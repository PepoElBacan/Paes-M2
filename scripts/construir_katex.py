#!/usr/bin/env python3
"""Genera web/katex.css: la hoja de estilos de KaTeX con las fuentes incrustadas (data URI woff2).

La app no puede cargar hojas de estilo ni fuentes desde una CDN, así que se incrustan.
Uso:  npm pack katex@0.16.9 && tar xzf katex-0.16.9.tgz && python3 scripts/construir_katex.py package/dist
"""
import base64
import re
import sys
from pathlib import Path

dist = Path(sys.argv[1] if len(sys.argv) > 1 else "package/dist")
css = (dist / "katex.min.css").read_text()
MANTENER = {"Main-Regular", "Main-Bold", "Main-Italic", "Main-BoldItalic", "Math-Italic", "Math-BoldItalic",
            "AMS-Regular", "Size1-Regular", "Size2-Regular", "Size3-Regular", "Size4-Regular"}


def bloque(m):
    b = m.group(0)
    nombre = re.search(r"fonts/KaTeX_([\w-]+)\.woff2", b).group(1)
    if nombre not in MANTENER:
        return ""
    datos = base64.b64encode((dist / "fonts" / f"KaTeX_{nombre}.woff2").read_bytes()).decode()
    familia = re.search(r"font-family:([^;}]+)", b).group(1)
    peso = re.search(r"font-weight:(\w+)", b)
    estilo = re.search(r"font-style:(\w+)", b)
    return ("@font-face{font-family:%s;src:url(data:font/woff2;base64,%s) format(\"woff2\");font-display:swap%s%s}"
            % (familia, datos, ";font-weight:" + peso.group(1) if peso else "", ";font-style:" + estilo.group(1) if estilo else ""))


salida = re.sub(r"@font-face\{[^}]*\}", bloque, css)
Path("web/katex.css").write_text(salida)
print(f"web/katex.css: {len(salida) / 1024:.0f} KB, {salida.count('@font-face')} fuentes")
