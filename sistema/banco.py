"""Acceso al banco oficial etiquetado y búsqueda de preguntas 'gemelas'."""
import json
from pathlib import Path

from .taxonomia import TEMAS

RAIZ = Path(__file__).resolve().parent.parent
# de la más reciente a la más antigua
ORDEN_PRUEBAS = ["I2027", "R2026", "I2026", "R2025", "I2025", "R2024", "I2024"]


def cargar():
    return json.loads((RAIZ / "datos" / "banco_oficial.json").read_text())


def por_id(banco=None):
    return {q["id"]: q for q in (banco or cargar())}


def puntuable(q):
    return not q["piloto"] and not q["eliminada"]


def pesos(banco=None):
    """Fracción de preguntas puntuables por tema (qué tan 'frecuente' es en la PAES)."""
    banco = banco or cargar()
    total = sum(1 for q in banco if puntuable(q))
    cont = {}
    for q in banco:
        if puntuable(q):
            cont[q["tema"]] = cont.get(q["tema"], 0) + 1
    return {t: n / total for t, n in cont.items()}, cont


def gemelas(q, banco=None, mismo_subtema=True, max_n=8, excluir_prueba=True):
    """Preguntas oficiales del mismo tema (y, si es posible, subtema) en OTRAS pruebas."""
    banco = banco or cargar()
    cand = [x for x in banco if x["tema"] == q["tema"] and x["id"] != q["id"] and (not excluir_prueba or x["prueba"] != q["prueba"])]
    if mismo_subtema:
        mismas = [x for x in cand if x["subtema"] == q["subtema"]]
        if len(mismas) >= 2:
            cand = mismas
    cand.sort(key=lambda x: (ORDEN_PRUEBAS.index(x["prueba"]), x["n"]))
    return cand[:max_n]


def etiqueta(q):
    return f"{q['prueba']} P{q['n']}"


def nombre_tema(t):
    return TEMAS[t][0] if t in TEMAS else t
