"""Refuerzo de errores en ejercicios generados y detección de subtemas débiles.

· Cada ejercicio generado que fallas abre (o reinicia) una *tarjeta de refuerzo* de su subtema.
  La tarjeta vuelve a +1, +3 y +7 días, con OTRO ejercicio del mismo subtema; con 3 aciertos
  seguidos queda dominada (la misma regla que el banco de errores oficiales).
· `debiles()` ordena los subtemas por "preguntas que se esperan perder": usa tus ensayos por pregunta,
  tus resultados con preguntas oficiales y tus ejercicios generados, encogiendo hacia la tasa de error del tema
  cuando hay pocos datos.
"""
import csv
import json
import random
from datetime import timedelta

from . import estado as E
from . import generadores as G

INTERVALOS = E.INTERVALOS
_SUBS_GEN = None


def subtemas_gen():
    """{tema: {subtemas que sus generadores pueden producir}} (se calcula una vez)."""
    global _SUBS_GEN
    if _SUBS_GEN is None:
        _SUBS_GEN = {}
        for tema, gens in G.GENERADORES.items():
            s = set()
            for gen in gens:
                for nivel in (1, 2, 3):
                    for semilla in range(12):
                        try:
                            s.add(gen(random.Random(f"sub|{gen.__name__}|{nivel}|{semilla}"), nivel)["subtema"])
                        except Exception:  # noqa: BLE001
                            pass
            _SUBS_GEN[tema] = s
    return _SUBS_GEN


def clave(tema, sub):
    return f"{tema}|{sub}"


def reg_sub(est, tema, sub, ok):
    e = est["sub"].setdefault(clave(tema, sub), {"i": 0, "a": 0, "v": []})
    e["i"] += 1
    e["a"] += int(ok)
    e["v"] = (e["v"] + [int(ok)])[-10:]


def abrir_carta(est, tema, sub, nivel):
    """Falló un ejercicio: el subtema vuelve mañana (si ya había tarjeta, se reinicia)."""
    k = clave(tema, sub)
    manana = (E.hoy() + timedelta(days=1)).isoformat()
    c = est["cartas"].get(k)
    if not c:
        est["cartas"][k] = {"tema": tema, "sub": sub, "nivel": nivel or 1, "racha": 0, "intentos": 0,
                            "proximo": manana, "dominada": False}
    else:
        c.update(racha=0, dominada=False, proximo=manana, nivel=max(1, min(c["nivel"], nivel or 1)))


def resolver_carta(est, k, ok):
    c = est["cartas"][k]
    c["intentos"] += 1
    if ok:
        c["racha"] += 1
        if c["racha"] >= 3:
            c["dominada"], c["proximo"] = True, None
        else:
            c["proximo"] = (E.hoy() + timedelta(days=INTERVALOS[c["racha"]])).isoformat()
    else:
        c["racha"], c["dominada"] = 0, False
        c["proximo"] = (E.hoy() + timedelta(days=INTERVALOS[0])).isoformat()
    return c


def cartas_pendientes(est, fecha=None):
    f = (fecha or E.hoy()).isoformat()
    out = [k for k, c in est["cartas"].items() if not c["dominada"] and c["proximo"] and c["proximo"] <= f
           and c["sub"] in subtemas_gen().get(c["tema"], set())]
    return sorted(out, key=lambda k: (est["cartas"][k]["proximo"], k))


def _resp_ensayo(en):
    if en.get("resp"):
        return {str(k): v for k, v in en["resp"].items()}
    if en["prueba"] == "I2026" and en["fecha"] == "2026-11-14":       # ensayo sembrado desde tu hoja
        filas = csv.DictReader(open(E.RAIZ / "datos" / "respuestas_ensayo_I2026.csv"))
        return {r["n"]: r["marcada"] for r in filas}
    return None


def debiles(est, banco, tasa_tema):
    """Lista de subtemas ordenada por preguntas esperadas a perder (de 50). `tasa_tema` = {tema: tasa de error}."""
    ev = {}

    def add(k, e, n):
        x = ev.setdefault(k, [0, 0])
        x[0] += e
        x[1] += n
    por_pr = {}
    for q in banco:
        por_pr.setdefault(q["prueba"], []).append(q)
    for en in est["ensayos"]:
        r = _resp_ensayo(en)
        if not r:
            continue
        for q in por_pr.get(en["prueba"], []):
            m = r.get(str(q["n"]))
            if m and not q["piloto"] and not q["eliminada"] and q["clave"]:
                add(clave(q["tema"], q["subtema"]), int(m != q["clave"]), 1)
    ids = {q["id"]: q for q in banco}
    for qid, o in est.get("oficiales", {}).items():
        q = ids.get(qid)
        if q and q["clave"]:
            add(clave(q["tema"], q["subtema"]), int(not o["ok"]), 1)
    for k, e in est["sub"].items():
        add(k, len(e["v"]) - sum(e["v"]), len(e["v"]))
    cnt, tot = {}, 0
    for q in banco:
        if not q["piloto"] and not q["eliminada"]:
            tot += 1
            cnt[clave(q["tema"], q["subtema"])] = cnt.get(clave(q["tema"], q["subtema"]), 0) + 1
    out = []
    for k in set(cnt) | set(ev):
        tema, sub = k.split("|")
        e, n = ev.get(k, (0, 0))
        tasa = (e + 2 * tasa_tema.get(tema, 0.5)) / (n + 2)
        w = max(cnt.get(k, 0) / tot, 1 / tot)
        if sub == "general" and not n:
            continue
        out.append({"k": k, "tema": tema, "sub": sub, "err": e, "n": n, "tasa": tasa, "en_juego": 50 * w * tasa,
                    "gen": sub in subtemas_gen().get(tema, set())})
    return sorted(out, key=lambda x: -x["en_juego"])


def items_refuerzo(est, banco, tasa_tema, n=9):
    """[(tema, subtema|None, clave_de_tarjeta|None, nivel|0)]: tarjetas vencidas primero, luego los subtemas más débiles."""
    items = [(est["cartas"][k]["tema"], est["cartas"][k]["sub"], k, est["cartas"][k]["nivel"]) for k in cartas_pendientes(est)[:4]]
    deb = [d for d in debiles(est, banco, tasa_tema) if d["gen"]][:4]
    j = 0
    while len(items) < n and deb:
        d = deb[j % len(deb)]
        items.append((d["tema"], d["sub"], None, 0))
        j += 1
    return items
