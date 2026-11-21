#!/usr/bin/env python3
"""Construye datos/banco_oficial.json a partir de las etiquetas manuales (datos/etiquetas/*.txt)
y de las claves/páginas extraídas de los PDF (pruebas/texto/*.json).

NO incluye el texto de las preguntas (propiedad de DEMRE / U. de Chile): solo tema, descriptor propio,
página del PDF y clave, para poder abrir el PDF oficial en la página correcta.
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
sys.path.insert(0, str(RAIZ))
from extraer_preguntas import PRUEBAS  # noqa: E402
from sistema.taxonomia import subtema as calc_subtema  # noqa: E402


def tabla_puntaje(clavijero):
    """Lee la tabla P -> puntaje PAES del clavijero (páginas 5-6)."""
    import subprocess
    txt = subprocess.run(["pdftotext", "-layout", "-f", "5", "-l", "6", str(clavijero), "-"],
                         capture_output=True, text=True, check=True).stdout
    tabla = {}
    for m in re.finditer(r"\b(\d{1,2})\s+(\d{3,4})\b", txt):
        p, paes = int(m.group(1)), int(m.group(2))
        if 0 <= p <= 50 and 100 <= paes <= 1000 and p not in tabla:
            tabla[p] = paes
    return tabla


def main():
    tablas = {}
    for pid, (archivo, clavij, etiqueta, tipo) in PRUEBAS.items():
        cp = RAIZ / "pruebas" / "pdf" / clavij
        tablas[pid] = tabla_puntaje(cp)
        tablas[pid].setdefault(50, 1000)     # el 50/50 siempre es 1000 (a veces el PDF lo imprime aparte)
        assert sorted(tablas[pid]) == list(range(51)), f"tabla incompleta en {pid}: {sorted(tablas[pid])}"
    (RAIZ / "datos" / "tabla_puntaje.json").write_text(json.dumps(tablas, indent=1))
    banco = []
    for pid, (archivo, clavij, etiqueta, tipo) in PRUEBAS.items():
        txt = RAIZ / "pruebas" / "texto" / f"{pid}.json"
        if not txt.exists():
            sys.exit("Falta pruebas/texto: ejecuta scripts/extraer_preguntas.py")
        info = {q["n"]: q for q in json.loads(txt.read_text())["preguntas"]}
        for linea in (RAIZ / "datos" / "etiquetas" / f"{pid}.txt").read_text().splitlines():
            n, tema, desc = linea.split("|", 2)
            n = int(n)
            q = info.get(n, {})
            texto = q.get("texto", "")
            suf = bool(re.search(r"\(1\).*\(2\)", texto) and re.search(r"por sí sola|determinar", texto)) \
                or desc.lower().startswith("suficiencia")
            banco.append({
                "id": f"{pid}-{n:02d}", "prueba": pid, "prueba_etiqueta": etiqueta, "n": n,
                "tema": tema, "subtema": calc_subtema(tema, desc), "descripcion": desc, "suficiencia": suf,
                "clave": q.get("clave"), "piloto": q.get("piloto", False),
                "eliminada": q.get("eliminada", False),
                "pdf": f"pruebas/pdf/{archivo}", "pagina_pdf": q.get("pagina_pdf"),
            })
    (RAIZ / "datos" / "banco_oficial.json").write_text(json.dumps(banco, ensure_ascii=False, indent=1))
    print(f"banco_oficial.json: {len(banco)} preguntas")


if __name__ == "__main__":
    main()
