#!/usr/bin/env python3
"""Extrae las preguntas (texto crudo + página) y las claves de las pruebas M2 de DEMRE.

Entrada : pruebas/pdf/*.pdf   (descargados con scripts/descargar_pruebas.sh)
Salida  : pruebas/texto/<id>.json  (LOCAL, no se versiona: el texto de las preguntas
          es propiedad de la Universidad de Chile / DEMRE)

Requiere `pdftotext` (poppler-utils).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PDF = RAIZ / "pruebas" / "pdf"
OUT = RAIZ / "pruebas" / "texto"

# id interno -> (archivo prueba, archivo clavijero, etiqueta humana, tipo, fecha aplicación)
PRUEBAS = {
    "I2024": ("2024-23-06-19-paes-invierno-oficial-matematica2-p2024.pdf",
                "2024-23-07-20-clavijero-paes-invierno-m2.pdf", "Invierno jun-2023 (Adm. 2024)", "completa"),
    "R2024": ("2024-23-11-27-paes-regular-oficial-matematica2-p2024.pdf",
                "2024-23-12-28-clavijero-paes-regular-m2.pdf", "Regular nov-2023 (Adm. 2024)", "completa"),
    "I2025": ("2025-24-06-17-paes-invierno-oficial-matematica2-p2025.pdf",
                "2025-24-07-19-clavijero-paes-invierno-m2.pdf", "Invierno jun-2024 (Adm. 2025)", "completa"),
    "R2025": ("2025-24-12-02-paes-regular-matematica2-p2025.pdf",
                "2025-25-01-06-clavijero-paes-regular-m2.pdf", "Regular dic-2024 (Adm. 2025)", "seleccion"),
    "I2026": ("2026-25-06-16-paes-invierno-oficial-matematica2-p2026.pdf",
                "2026-25-07-18-clavijero-paes-invierno-m2.pdf", "Invierno jun-2025 (Adm. 2026)", "completa"),
    "R2026": ("2026-25-12-01-paes-regular-matematica2-p2026.pdf",
                "2026-26-01-05-clavijero-paes-regular-m2.pdf", "Regular dic-2025 (Adm. 2026)", "seleccion"),
    "I2027": ("2027-26-06-15-paes-invierno-oficial-matematica2-p2027.pdf",
                "2027-26-07-17-clavijero-paes-invierno-m2.pdf", "Invierno jun-2026 (Adm. 2027)", "completa"),
}


def texto_paginas(pdf: Path):
    out = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    return out.split("\f")


def claves(pdf: Path):
    """Devuelve {n: clave}, set(pilotos), set(eliminadas) leyendo la tabla CLAVES."""
    txt = subprocess.run(["pdftotext", "-layout", "-f", "3", "-l", "3", str(pdf), "-"],
                         capture_output=True, text=True, check=True).stdout
    ks, pil, eli = {}, set(), set()
    for m in re.finditer(r"\b(\d{1,2})(\*{0,2})(?=\s)(?:[ \t]+([A-E])(?=\s|$))?", txt):
        n, est, k = int(m.group(1)), m.group(2), m.group(3)
        if not 1 <= n <= 55:
            continue
        if k:
            ks[n] = k
        if est == "*":
            pil.add(n)
        if est == "**":
            eli.add(n)
    return ks, pil, eli


def preguntas(pdf: Path, completa: bool):
    pags = texto_paginas(pdf)
    # saltar portada/instrucciones: empezar tras la última página con la tabla de símbolos
    ini = 0
    for i, t in enumerate(pags[:8]):
        if "SÍMBOLOS MATEMÁTICOS" in t or "SIMBOLOS MATEMATICOS" in t.upper():
            ini = i + 1
    res = {}
    ultimo = 0
    for p in range(ini, len(pags)):
        t = pags[p]
        for m in re.finditer(r"(?m)^[ \t]*(\d{1,2})(?:\.\s*(?=\S)|[ \t]*\n\s*(?=\S))", t):
            n = int(m.group(1))
            ok = (n == ultimo + 1) if completa else (ultimo < n <= min(55, ultimo + 8))
            if ok:
                res[n] = {"pagina": p + 1, "inicio": m.start(), "pag_txt": t}
                ultimo = n
    out = {}
    nums = sorted(res)
    for i, n in enumerate(nums):
        a = res[n]
        t = a["pag_txt"][a["inicio"]:]
        if i + 1 < len(nums):
            b = res[nums[i + 1]]
            if b["pagina"] == a["pagina"]:
                t = a["pag_txt"][a["inicio"]:b["inicio"]]
        out[n] = {"pagina": a["pagina"], "texto": re.sub(r"\s+", " ", t).strip()[:900]}
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for pid, (f, c, etiqueta, tipo) in PRUEBAS.items():
        pf, cf = PDF / f, PDF / c
        if not pf.exists() or not cf.exists():
            print(f"[!] falta {pid}: ejecuta scripts/descargar_pruebas.sh", file=sys.stderr)
            continue
        ks, pil, eli = claves(cf)
        qs = preguntas(pf, tipo == "completa")
        data = {"id": pid, "etiqueta": etiqueta, "tipo": tipo, "pdf": f, "preguntas": []}
        for n in sorted(qs):
            data["preguntas"].append({
                "n": n, "pagina_pdf": qs[n]["pagina"], "clave": ks.get(n),
                "piloto": n in pil, "eliminada": n in eli, "texto": qs[n]["texto"]})
        (OUT / f"{pid}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
        print(f"{pid}: {len(qs)} preguntas, {len(ks)} claves, {len(pil)} pilotos, {len(eli)} eliminadas")


if __name__ == "__main__":
    main()
