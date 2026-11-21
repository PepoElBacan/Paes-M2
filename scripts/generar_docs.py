#!/usr/bin/env python3
"""Regenera las partes automáticas de la documentación:
  · tablas de preguntas oficiales dentro de camino/*.md   (bloques <!-- GEMELAS ... --> y <!-- SUFICIENCIA -->)
  · docs/mapa_gemelas.md  (cada error tuyo del ensayo I2026 y sus gemelas en las otras pruebas)
  · docs/diagnostico.md   (análisis de tu desempeño)
"""
import csv
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from sistema import banco as B  # noqa: E402
from sistema.taxonomia import TEMAS  # noqa: E402

BANCO = B.cargar()
POR_ID = B.por_id(BANCO)


def fila(q):
    marca = " *(piloto)*" if q["piloto"] else (" *(eliminada)*" if q["eliminada"] else "")
    return f"| {B.etiqueta(q)} | {q['pagina_pdf']} | {q['clave'] or '—'} | {q['descripcion']}{marca} | {q['subtema']} |"


def tabla(qs):
    qs = sorted(qs, key=lambda x: (B.ORDEN_PRUEBAS.index(x["prueba"]), x["n"]))
    return ["| Pregunta | pág. PDF | clave | de qué trata | subtema |", "|---|---|---|---|---|"] + [fila(q) for q in qs]


def rellenar_camino():
    for md in sorted((RAIZ / "camino").glob("*.md")):
        s = md.read_text()

        def gem(m):
            temas = [t.strip() for t in m.group(1).split(",")]
            bloques = []
            for t in temas:
                qs = [q for q in BANCO if q["tema"] == t and not (q["descripcion"].lower().startswith("suficiencia") and False)]
                if len(temas) > 1:
                    bloques.append(f"\n**{t} — {TEMAS[t][0]}** ({len(qs)} preguntas)\n")
                bloques += tabla(qs) if qs else ["(sin preguntas etiquetadas)"]
            return f"<!-- GEMELAS {m.group(1)} -->\n" + "\n".join(bloques) + "\n<!-- /GEMELAS -->"
        s = re.sub(r"<!-- GEMELAS ([^>]*?) -->.*?<!-- /GEMELAS -->", gem, s, flags=re.S)
        suf = [q for q in BANCO if q["suficiencia"]]
        s = re.sub(r"<!-- SUFICIENCIA -->.*?<!-- /SUFICIENCIA -->",
                   "<!-- SUFICIENCIA -->\n" + "\n".join(tabla(suf)) + "\n<!-- /SUFICIENCIA -->", s, flags=re.S)
        md.write_text(s)
    print("camino/*.md actualizado")


def errores_i2026():
    out = []
    for r in csv.DictReader(open(RAIZ / "datos" / "respuestas_ensayo_I2026.csv")):
        q = POR_ID[f"I2026-{int(r['n']):02d}"]
        if q["eliminada"] or not r["correcta"]:
            continue
        if r["marcada"] != r["correcta"] or "sin método" in r["notas"]:
            out.append((q, r))
    return out


def mapa():
    L = ["# Mapa de gemelas: tus errores de I2026 y dónde reaparecen",
         "",
         "Para cada pregunta que fallaste (o acertaste sin método) en tu ensayo **I2026** (PAES invierno jun-2025), "
         "aquí están las preguntas **del mismo tema y subtema** en las otras 6 pruebas oficiales. "
         "Úsalas como práctica escalonada: resuélvelas sin mirar la clave y compara.",
         "",
         "> Las clasificaciones son manuales (tema, subtema y descripción propios). Abre el PDF en la página indicada. "
         "Los PDFs se bajan con `scripts/descargar_pruebas.sh`.",
         ""]
    for q, r in errores_i2026():
        estado = "acertada sin método" if r["marcada"] == r["correcta"] else f"marcaste {r['marcada']}, correcta {r['correcta']}"
        piloto = " (piloto: no puntúa)" if q["piloto"] else ""
        L += [f"## {B.etiqueta(q)} — {q['descripcion']}{piloto}",
              f"*{q['tema']} · {q['subtema']} · {estado}" + (f" · tu nota: {r['notas']}" if r["notas"] else "") + "*", ""]
        gem = B.gemelas(q, BANCO, max_n=6)
        L += tabla(gem) if gem else ["(sin gemelas)"]
        L.append("")
    (RAIZ / "docs").mkdir(exist_ok=True)
    (RAIZ / "docs" / "mapa_gemelas.md").write_text("\n".join(L))
    print("docs/mapa_gemelas.md generado")


def diagnostico():
    tabla_p = json.loads((RAIZ / "datos" / "tabla_puntaje.json").read_text())["I2026"]
    pesos, cont = B.pesos(BANCO)
    est = {}
    for r in csv.DictReader(open(RAIZ / "datos" / "respuestas_ensayo_I2026.csv")):
        q = POR_ID[f"I2026-{int(r['n']):02d}"]
        if q["eliminada"] or not r["correcta"] or q["piloto"]:
            continue
        a, n = est.setdefault(q["tema"], [0, 0])
        est[q["tema"]] = [a + (r["marcada"] == r["correcta"]), n + 1]
    punt = sum(n for _, n in est.values())
    aciertos = sum(a for a, _ in est.values())
    L = ["# Diagnóstico de tu desempeño (ensayo I2026 + banco de errores)", "",
         f"**Resultado:** {aciertos} correctas de {punt} puntuables ⇒ **{tabla_p[str(aciertos)]} puntos PAES** (tabla oficial de esa prueba).", "",
         "## ¿Cuánto vale cada pregunta extra?", "", "| Correctas | Puntaje PAES |", "|---|---|"]
    for p in (aciertos, aciertos + 3, aciertos + 5, aciertos + 8, aciertos + 10, 40, 45):
        L.append(f"| {p} | {tabla_p[str(p)]} |")
    L += ["", f"Arreglar solo la **función cuadrática** (0/4 ⇒ 4/4) llevaría de {aciertos} a {aciertos + 4} correctas "
          f"(**+{tabla_p[str(aciertos + 4)] - tabla_p[str(aciertos)]} pts**).", "",
          "## Por tema (solo preguntas puntuables)", "",
          "| Tema | Tu resultado | % acierto | Peso en la PAES* | Preguntas que se pierden por prueba** |", "|---|---|---|---|---|"]
    filas = []
    for t, (a, n) in est.items():
        tasa = (n - a + 1) / (n + 2)
        filas.append((50 * pesos.get(t, 0) * tasa, t, a, n))
    for en_juego, t, a, n in sorted(filas, reverse=True):
        L.append(f"| {t} {TEMAS[t][0]} | {a}/{n} | {100 * a // n} % | {100 * pesos.get(t, 0):.1f} % ({cont.get(t, 0)} preg.) | {en_juego:.1f} |")
    L += ["", "\\* Peso = fracción de las preguntas puntuables de las 7 pruebas analizadas (349 preguntas etiquetadas).",
          "\\** Estimación = 50 × peso × tasa de error suavizada ((errores+1)/(n+2)). Es la métrica con la que el sistema ordena tus prioridades.", "",
          "## Patrones que se ven en tus errores", "",
          "1. **Signos y etiquetas, no conceptos** (cuadrantes, \"respondí otra cosa\"): P31 y P25. Se corrige con reglas de verificación (ver `docs/estrategia_de_prueba.md`).",
          "2. **Cuadrática (P28–P31 y piloto P27)**: es el tema con más peso en la PAES y el de mayor pérdida; el módulo M1 es la prioridad nº 1.",
          "3. **\"No supe resolverla\"** en 10 preguntas (P10, 16, 17, 27–31, 46, 48, 50): hay brechas de método en logaritmos, proporcionalidad inversa, "
          "desviación estándar y permutaciones.",
          "4. **Dos aciertos \"sin método\"** (P42, P52): aprovéchalos como repaso igual; en el día de la prueba no se puede depender del azar.",
          "5. Los 5 **pilotos no puntúan** (P27, 34, 50, 54, 55 en tu prueba): errores en pilotos no cuestan puntos — no te angusties por ellos.",
          "6. Te sobraron **23 min 21 s**: úsalos de forma sistemática para revisar signos/etiquetas en el último tercio de la prueba.", ""]
    (RAIZ / "docs").mkdir(exist_ok=True)
    (RAIZ / "docs" / "diagnostico.md").write_text("\n".join(L))
    print("docs/diagnostico.md generado")


if __name__ == "__main__":
    rellenar_camino()
    mapa()
    diagnostico()
