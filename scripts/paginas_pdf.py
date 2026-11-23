"""¿La pregunta continúa en la página siguiente del PDF? (según si en su página aparecen las alternativas A) … D))"""
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
from extraer_preguntas import PRUEBAS  # noqa: E402


@lru_cache(maxsize=None)
def texto_pagina(pid, pag):
    pdf = RAIZ / "pruebas" / "pdf" / PRUEBAS[pid][0]
    if not pdf.exists():
        return None
    r = subprocess.run(["pdftotext", "-f", str(pag), "-l", str(pag), "-layout", str(pdf), "-"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def continua(pid, pag):
    t = texto_pagina(pid, pag)
    if t is None:
        return False
    return not re.search(r"(^|\s)D\)", t)
