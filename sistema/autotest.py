"""Prueba automática de los generadores: ejecuta cada uno muchas veces y revisa invariantes."""
import collections
import random
import re

from . import generadores as G

MALO = re.compile(r"Fraction|\bNone\b|\bnan\b|\{|\}|\bTrue\b|\bFalse\b|\+ −|− −|\+\+|\(\)")


def correr(n=300, verbose=True):
    problemas = collections.Counter()
    ejemplos = {}
    total = 0
    for tema, gens in G.GENERADORES.items():
        for gen in gens:
            for nivel in (1, 2, 3):
                faltan = 0
                for semilla in range(n):
                    rnd = random.Random(f"{gen.__name__}{nivel}{semilla}")
                    total += 1
                    try:
                        g = gen(rnd, nivel)
                        assert g["tema"] == tema, f"tema {g['tema']} != {tema}"
                        ej = G.armar(rnd, g)
                    except G.FaltanDistractores:
                        faltan += 1
                        continue
                    except Exception as e:  # noqa: BLE001
                        problemas[f"{gen.__name__} n{nivel}: {type(e).__name__}: {e}"] += 1
                        ejemplos.setdefault(gen.__name__, semilla)
                        continue
                    textos = [o[0] for o in ej["opciones"]]
                    if len(set(textos)) != 4:
                        problemas[f"{gen.__name__} n{nivel}: opciones repetidas"] += 1
                    if textos[ej["correcta"]] != g["correcta"]:
                        problemas[f"{gen.__name__} n{nivel}: índice correcto mal"] += 1
                    for campo in [ej["enunciado"], ej["explicacion"]] + textos + [o[1] or "" for o in ej["opciones"]]:
                        if MALO.search(campo):
                            problemas[f"{gen.__name__} n{nivel}: texto sospechoso: {campo[:90]!r}"] += 1
                            break
                    for t, r in ej["opciones"]:
                        if t != g["correcta"] and not r:
                            problemas[f"{gen.__name__} n{nivel}: distractor sin explicación"] += 1
                if faltan > n * 0.25:
                    problemas[f"{gen.__name__} n{nivel}: {faltan}/{n} descartados por pocos distractores"] += 1
    if verbose:
        print(f"{total} ejercicios generados en {sum(len(v) for v in G.GENERADORES.values())} generadores")
        if problemas:
            print("PROBLEMAS:")
            for k, v in problemas.most_common(40):
                print(f"  {v:4d}  {k}")
        else:
            print("OK: sin problemas")
    return not problemas
