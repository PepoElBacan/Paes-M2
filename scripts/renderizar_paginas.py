"""Renderiza como imagen las páginas del PDF oficial donde está cada pregunta (web/paginas/<prueba>_<pág>.jpg).

La app las usa para que Claude lea la pregunta oficial por sí solo (visión), sin que tengas que subir una foto.
Son material con derechos reservados del DEMRE: web/paginas/ está en .gitignore y solo se publica en tu Artifact privado.

Requisitos: pruebas/pdf/ (scripts/descargar_pruebas.sh) y poppler-utils (pdftoppm).
"""
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "scripts"))
from extraer_preguntas import PRUEBAS  # noqa: E402
from sistema import banco as B  # noqa: E402
from paginas_pdf import continua  # noqa: E402

SALIDA = RAIZ / "web" / "paginas"
ANCHO = 950      # px: la plataforma reduce las imágenes a ~1,2 megapíxeles de todos modos


def paginas_necesarias():
    """{prueba: {páginas}} : la página de cada pregunta y, si es la última de su página, la siguiente"""
    por = {}
    for q in B.cargar():
        por.setdefault(q["prueba"], []).append(q)
    out = {}
    for pid, qs in por.items():
        qs.sort(key=lambda q: q["n"])
        pags = set()
        for i, q in enumerate(qs):
            pags.add(q["pagina_pdf"])
            if continua(pid, q["pagina_pdf"]):
                pags.add(q["pagina_pdf"] + 1)          # la pregunta continúa en la página siguiente
        out[pid] = pags
    return out


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    total = 0
    necesarias = paginas_necesarias()
    esperadas = {f"{pid}_{p:02d}.jpg" for pid, pags in necesarias.items() for p in pags}
    for f in SALIDA.glob("*.jpg"):                    # páginas que ya no hacen falta
        if f.name not in esperadas:
            f.unlink()
    for pid, pags in necesarias.items():
        pdf = RAIZ / "pruebas" / "pdf" / PRUEBAS[pid][0]
        if not pdf.exists():
            print(f"falta {pdf.name}: ejecuta scripts/descargar_pruebas.sh")
            continue
        for p in sorted(pags):
            destino = SALIDA / f"{pid}_{p:02d}"
            if destino.with_suffix(".jpg").exists():
                total += 1
                continue
            r = subprocess.run(["pdftoppm", "-f", str(p), "-l", str(p), "-jpeg", "-jpegopt", "quality=72",
                                "-scale-to-x", str(ANCHO), "-scale-to-y", "-1", "-singlefile", str(pdf), str(destino)],
                               capture_output=True, text=True)
            if r.returncode != 0:
                print(f"error {pid} p.{p}: {r.stderr.strip()}")
            else:
                total += 1
    kb = sum(f.stat().st_size for f in SALIDA.glob("*.jpg")) / 1024
    print(f"{total} páginas en web/paginas ({kb / 1024:.1f} MB)")


if __name__ == "__main__":
    main()
