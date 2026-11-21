"""Estado de progreso: repetición espaciada (+1, +3, +7 días; dominada con 3 aciertos seguidos),
nivel por tema para los ejercicios generados, y registro de ensayos.

El archivo vive en progreso/estado.json (se puede versionar con git).
"""
import json
from datetime import date, datetime, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
RUTA = RAIZ / "progreso" / "estado.json"
INTERVALOS = [1, 3, 7]          # días hasta el próximo intento según racha (0, 1, 2)
VENTANA = 5                     # ejercicios generados que se miran para subir de nivel
UMBRAL = 4                      # aciertos en la ventana para subir de nivel


def hoy():
    return date.today()


def vacio():
    return {"version": 1, "temas": {}, "errores": {}, "ensayos": [], "hojas": {}, "oficiales": {}, "sub": {}, "cartas": {}}


def cargar():
    est = json.loads(RUTA.read_text()) if RUTA.exists() else vacio()
    for k, v in vacio().items():                  # estados antiguos: agrega lo que falte
        est.setdefault(k, v)
    return est


def guardar(est):
    RUTA.parent.mkdir(parents=True, exist_ok=True)
    RUTA.write_text(json.dumps(est, ensure_ascii=False, indent=1, sort_keys=True))


# ── errores oficiales (banco de errores con repetición espaciada) ──

def agregar_error(est, qid, nota="", racha=0, ultimo=None, proximo=None):
    e = est["errores"].setdefault(qid, {"racha": racha, "intentos": 0, "ultimo": ultimo.isoformat() if ultimo else None,
                                        "proximo": (proximo or hoy()).isoformat(), "dominada": False, "nota": nota})
    if nota and nota not in e["nota"]:
        e["nota"] = (e["nota"] + " | " + nota).strip(" |")
    return e


def registrar_intento(est, qid, ok, fecha=None):
    fecha = fecha or hoy()
    e = est["errores"].setdefault(qid, {"racha": 0, "intentos": 0, "ultimo": None, "proximo": fecha.isoformat(), "dominada": False, "nota": ""})
    e["intentos"] += 1
    e["ultimo"] = fecha.isoformat()
    est.setdefault("oficiales", {})[qid] = {"ok": bool(ok), "f": fecha.isoformat()}
    if ok:
        e["racha"] += 1
        if e["racha"] >= 3:
            e["dominada"] = True
            e["proximo"] = None
        else:
            e["proximo"] = (fecha + timedelta(days=INTERVALOS[e["racha"]])).isoformat()
    else:
        e["racha"] = 0
        e["dominada"] = False
        e["proximo"] = (fecha + timedelta(days=INTERVALOS[0])).isoformat()
    return e


def pendientes(est, fecha=None):
    """IDs de errores que toca repasar hoy (o antes), los más atrasados primero."""
    fecha = fecha or hoy()
    out = []
    for qid, e in est["errores"].items():
        if e["dominada"] or not e["proximo"]:
            continue
        p = datetime.fromisoformat(e["proximo"]).date()
        if p <= fecha:
            out.append((p, qid))
    return [q for _, q in sorted(out)]


# ── práctica con ejercicios generados ──

def tema_estado(est, tema):
    return est["temas"].setdefault(tema, {"nivel": 1, "ventana": [], "intentos": 0, "aciertos": 0, "dominado": False})


def registrar_practica(est, tema, ok):
    t = tema_estado(est, tema)
    t["intentos"] += 1
    t["aciertos"] += int(ok)
    t["ventana"] = (t["ventana"] + [int(ok)])[-VENTANA:]
    subio = False
    if len(t["ventana"]) >= VENTANA and sum(t["ventana"]) >= UMBRAL:
        if t["nivel"] < 3:
            t["nivel"] += 1
            t["ventana"] = []
            subio = True
        else:
            t["dominado"] = True
    elif len(t["ventana"]) >= VENTANA and sum(t["ventana"]) <= 1 and t["nivel"] > 1:
        t["nivel"] -= 1                   # si te va muy mal, baja y consolida
        t["ventana"] = []
    return subio


def registrar_ensayo(est, prueba, correctas, puntuables, puntaje, por_tema, fecha=None, resp=None):
    en = {"prueba": prueba, "fecha": (fecha or hoy()).isoformat(), "correctas": correctas,
          "puntuables": puntuables, "puntaje": puntaje, "por_tema": por_tema}
    if resp:
        en["resp"] = {str(k): v for k, v in resp.items() if v}
    est["ensayos"].append(en)
