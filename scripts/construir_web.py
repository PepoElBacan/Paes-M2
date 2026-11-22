#!/usr/bin/env python3
"""Construye los datos de la app web móvil (web/*.json) a partir del banco, los generadores y las guías.

  web/ejercicios.json  pool de ejercicios generados (un registro por línea)
  web/datos.json       banco oficial compacto, tablas de puntaje, progreso inicial, plan
  web/guias.json       guías (camino/*.md y docs/*.md) convertidas a HTML

La página (web/index.html) se publica junto a estos archivos.
"""
import csv
import html
import json
import random
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "scripts"))
from extraer_preguntas import PRUEBAS  # noqa: E402
from sistema import banco as B  # noqa: E402
from sistema import camino as C  # noqa: E402
from sistema import generadores as G  # noqa: E402
from sistema.taxonomia import TEMAS  # noqa: E402
from lecciones import LECCIONES, TARJETAS  # noqa: E402

WEB = RAIZ / "web"
POR_NIVEL = 22     # ejercicios únicos por (generador, nivel)

SUBNOMBRES = {
    "vertice-maximo": "Vértice y valor máximo/mínimo", "reflexion-transformacion": "Reflexiones y traslaciones de la parábola",
    "discriminante-vieta": "Discriminante y raíces (Vieta)", "grafico-coeficientes": "Coeficientes desde gráfico o tabla",
    "modelar-ecuacion": "Plantear la ecuación cuadrática", "inversa": "Proporcionalidad inversa",
    "directa-razones": "Proporcionalidad directa y razones", "condicional-tablas": "Probabilidad condicional y tablas",
    "conteo-y-probabilidad": "Conteo y probabilidad con extracciones", "independencia-otros": "Independencia y otras probabilidades",
    "propiedades-evaluar": "Propiedades y evaluación de logaritmos", "modelos-con-log": "Modelos con logaritmos",
    "crecimiento-bacterias": "Crecimiento exponencial", "interes-compuesto": "Interés compuesto",
    "sin-o-infinitas": "Sistemas sin solución o con infinitas", "plantear": "Plantear sistemas",
    "porcentaje-precio": "Porcentajes y precios", "modelo-recta": "Modelos de recta", "hexagono": "Hexágono regular",
    "circulos": "Círculos y circunferencia", "pitagoras-razones": "Pitágoras y razones",
    "thales-semejanza": "Thales y semejanza", "homotecia": "Homotecia", "rotacion-reflexion-traslacion": "Rotación, reflexión y traslación",
    "volumen-cuerpos": "Volumen de cuerpos", "areas-figuras": "Áreas de figuras", "desviacion-varianza": "Desviación estándar y varianza",
    "cajon-posicion": "Diagramas de cajón y posición", "tablas-promedios": "Tablas y promedios",
    "combinaciones": "Combinaciones y permutaciones", "principio-multiplicativo": "Principio multiplicativo", "general": "General",
}

PLAN_MOVIL = {
    "2026-11-21": ("Ensayo completo cronometrado",
                   "Haz la prueba I2027 (invierno jun-2026) en papel: 2 h 20 min, sin calculadora. Abre el PDF desde Progreso → Corregir ensayo. "
                   "Cuando termines, marca tus respuestas ahí mismo: la app te da el puntaje y recalcula tus prioridades."),
    "2026-11-22": ("Probabilidad, conteo y dispersión", "Guías 5 y 6. Practica PYE-pro, PYE-con y PYE-dis. Primero tus repasos pendientes."),
    "2026-11-23": ("Geometría y vectores", "Guías 7 y 8: hexágono, cuadrados concéntricos, razón 16:9, homotecia con centro, rotaciones."),
    "2026-11-24": ("Suficiencia de datos y cuadrática", "Guía 9 + un set de cuadrática en nivel 3."),
    "2026-11-25": ("Sistemas, modelamiento y proporcionalidad", "Guías 2 y 3 en niveles 2–3. Repaso de errores (+3 días)."),
    "2026-11-26": ("Exponencial y logaritmos", "Guía 4. Resuelve P10 y P11 de tu ensayo sin ayuda. Repaso de errores (+7 días)."),
    "2026-11-27": ("Mini-ensayo de 25 preguntas", "Una prueba que no hayas visto (R2024 o I2024): primeras 25 preguntas en 65 min. Corrígelas en Progreso."),
    "2026-11-28": ("Repaso final", "Solo repasos pendientes y los 2 temas con más preguntas en juego (Progreso)."),
    "2026-11-29": ("Descanso activo", "Lee la hoja de fórmulas y la estrategia (20 min). Duerme temprano."),
    "2026-11-30": ("Día de la PAES M2 · 15:00 h", "Mañana liviana: fórmulas y 3–4 ejercicios fáciles. Lápiz grafito Nº 2 o portaminas HB, goma, sin calculadora."),
}


# ───────────────────────── Markdown → HTML mínimo ─────────────────────────

def inline(s):
    partes = re.split(r"(`[^`]+`)", s)
    out = []
    for p in partes:
        if p.startswith("`") and p.endswith("`") and len(p) > 1:
            out.append("<code>" + html.escape(p[1:-1], quote=False) + "</code>")
            continue
        p = html.escape(p, quote=False)
        p = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', p)
        p = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", p)
        p = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", p)
        out.append(p)
    return "".join(out)


def md_a_html(md):
    lineas = md.split("\n")
    out, i = [], 0
    while i < len(lineas):
        l = lineas[i]
        if not l.strip():
            i += 1
            continue
        m = re.match(r"^(#{1,3})\s+(.*)$", l)
        if m:
            n = len(m.group(1)) + 1
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
            i += 1
        elif l.strip() == "---":
            out.append("<hr>")
            i += 1
        elif l.startswith("```"):
            j = i + 1
            while j < len(lineas) and not lineas[j].startswith("```"):
                j += 1
            out.append("<pre>" + html.escape("\n".join(lineas[i + 1:j])) + "</pre>")
            i = j + 1
        elif l.startswith("|"):
            j = i
            while j < len(lineas) and lineas[j].startswith("|"):
                j += 1
            filas = [[c.strip() for c in r.strip().strip("|").split("|")] for r in lineas[i:j]]
            filas = [f for f in filas if not all(re.fullmatch(r":?-{2,}:?", c) for c in f)]
            t = "<div class='tw'><table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in filas[0]) + "</tr></thead><tbody>"
            for f in filas[1:]:
                t += "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in f) + "</tr>"
            out.append(t + "</tbody></table></div>")
            i = j
        elif l.startswith(">"):
            j = i
            buf = []
            while j < len(lineas) and lineas[j].startswith(">"):
                buf.append(lineas[j].lstrip("> ").rstrip())
                j += 1
            items = [b for b in buf if b]
            out.append("<blockquote>" + "<br>".join(inline(b) for b in items) + "</blockquote>")
            i = j
        elif re.match(r"^\s*(-|\d+\.)\s+", l):
            ordenada = bool(re.match(r"^\s*\d+\.", l))
            j, items = i, []
            while j < len(lineas) and re.match(r"^\s*(-|\d+\.)\s+", lineas[j]):
                t = re.sub(r"^\s*(-|\d+\.)\s+", "", lineas[j])
                t = t.replace("[ ]", "☐").replace("[x]", "☑")
                items.append(f"<li>{inline(t)}</li>")
                j += 1
            tag = "ol" if ordenada else "ul"
            out.append(f"<{tag}>{''.join(items)}</{tag}>")
            i = j
        else:
            j, buf = i, []
            while j < len(lineas) and lineas[j].strip() and not re.match(r"^(#{1,3}\s|\||>|```|---$|\s*(-|\d+\.)\s+)", lineas[j]):
                buf.append(lineas[j])
                j += 1
            out.append("<p>" + inline(" ".join(buf)) + "</p>")
            i = j if j > i else i + 1
    return "\n".join(out)


def limpiar_guia(md):
    """Quita lo que solo sirve en la CLI: bloques bash, tablas de preguntas oficiales (la app las ofrece como botón)."""
    md = re.sub(r"## Práctica\n+```bash.*?```\n?", "", md, flags=re.S)
    md = re.sub(r"## Preguntas oficiales[^\n]*\n.*?<!-- /(GEMELAS|SUFICIENCIA) -->\n?", "", md, flags=re.S)
    md = re.sub(r"\n```bash.*?```", "", md, flags=re.S)
    md = md.replace("`python3 paes.py practicar ALG-cua --nivel 1 -n 4`", "ejercicios de ALG-cua nivel 1 (pestaña Practicar)")
    md = re.sub(r"Con las preguntas oficiales: busca[^\n]*\n", "", md)
    md = re.sub(r"`(?:camino|docs)/[^`]*`", "la guía correspondiente", md)
    return md


# ───────────────────────── datos ─────────────────────────

def ejercicios():
    pool, total = [], 0
    for tema, gens in G.GENERADORES.items():
        for nivel in (1, 2, 3):
            vistos = set()
            reg = []
            for gen in gens:
                n_gen = 0
                for semilla in range(400):
                    if n_gen >= POR_NIVEL:
                        break
                    rnd = random.Random(f"web|{gen.__name__}|{nivel}|{semilla}")
                    try:
                        g = gen(rnd, nivel)
                        ej = G.armar(rnd, g)
                    except G.FaltanDistractores:
                        continue
                    if ej["enunciado"] in vistos:
                        continue
                    vistos.add(ej["enunciado"])
                    n_gen += 1
                    reg.append({"t": tema, "s": ej["subtema"], "n": nivel, "q": ej["enunciado"],
                                "o": [o[0] for o in ej["opciones"]], "r": [o[1] or "" for o in ej["opciones"]],
                                "c": ej["correcta"], "e": ej["explicacion"]})
            pool += reg
            total += len(reg)
    return pool


def main():
    WEB.mkdir(exist_ok=True)
    pool = ejercicios()
    (WEB / "ejercicios.json").write_text("[\n" + ",\n".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in pool) + "\n]\n")

    banco = []
    for q in B.cargar():
        banco.append({"i": q["id"], "p": q["prueba"], "n": q["n"], "t": q["tema"], "s": q["subtema"], "d": q["descripcion"],
                      "k": q["clave"], "pl": q["piloto"], "el": q["eliminada"], "g": q["pagina_pdf"], "u": q["suficiencia"]})
    pruebas = {pid: {"etq": et, "tipo": tipo, "pdf": pdf}
               for pid, (pdf, clav, et, tipo) in PRUEBAS.items()}
    semilla = json.loads((RAIZ / "progreso" / "estado.json").read_text())
    modulos = [{"id": m[0], "titulo": m[1], "temas": m[2], "guia": m[3].split("/")[-1][:-3]} for m in C.MODULOS]
    datos = {
        "banco": banco, "pruebas": pruebas, "orden": B.ORDEN_PRUEBAS,
        "tabla": json.loads((RAIZ / "datos" / "tabla_puntaje.json").read_text()),
        "temas": {k: {"n": v[0], "eje": v[1]} for k, v in TEMAS.items()},
        "gens": sorted(G.GENERADORES), "modulos": modulos, "semilla": semilla,
        "plan": {k: {"t": v[0], "d": v[1]} for k, v in PLAN_MOVIL.items()},
        "paes": "2026-11-30T15:00:00", "subn": SUBNOMBRES,
        "ens_sem": {"I2026": {r["n"]: r["marcada"] for r in csv.DictReader(open(RAIZ / "datos" / "respuestas_ensayo_I2026.csv"))}},
    }
    (WEB / "datos.json").write_text(json.dumps(datos, ensure_ascii=False, separators=(",", ":")))

    guias = {}
    for m in C.MODULOS:
        ruta = RAIZ / m[3]
        guias[ruta.stem] = {"titulo": f"{m[0]} · {m[1]}", "html": md_a_html(limpiar_guia(ruta.read_text()))}
    for clave, archivo, titulo in (("formulas", "hoja_de_formulas.md", "Hoja de fórmulas"),
                                   ("estrategia", "estrategia_de_prueba.md", "Estrategia de prueba"),
                                   ("diagnostico", "diagnostico.md", "Diagnóstico de tu ensayo"),
                                   ("investigacion", "investigacion.md", "Cómo estudiar: evidencia y meta")):
        txt = limpiar_guia((RAIZ / "docs" / archivo).read_text())
        guias[clave] = {"titulo": titulo, "html": md_a_html(txt)}
    (WEB / "guias.json").write_text(json.dumps(guias, ensure_ascii=False, separators=(",", ":")))
    (WEB / "lecciones.json").write_text(json.dumps({"lecciones": LECCIONES,
        "tarjetas": [{"id": a, "m": b, "q": c, "a": d} for a, b, c, d in TARJETAS]}, ensure_ascii=False, separators=(",", ":")))
    for f in ("ejercicios", "datos", "guias", "lecciones"):
        print(f"web/{f}.json  {(WEB / (f + '.json')).stat().st_size / 1024:.0f} KB")
    print(f"{len(pool)} ejercicios en el pool")


if __name__ == "__main__":
    main()
