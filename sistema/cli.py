"""Interfaz de línea de comandos: python3 paes.py <comando>"""
import argparse
import csv
import json
import random
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

from . import banco as B
from . import camino as C
from . import estado as E
from . import refuerzo as R
from . import generadores as G
from .taxonomia import TEMAS, nombre

RAIZ = Path(__file__).resolve().parent.parent
LETRAS = "ABCD"


# ───────────────────────── utilidades ─────────────────────────

def leer(prompt):
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def tabla_puntaje(prueba):
    return json.loads((RAIZ / "datos" / "tabla_puntaje.json").read_text())[prueba]


def puntaje_paes(prueba, p):
    return tabla_puntaje(prueba)[str(p)]


def parsear_respuestas(texto, prueba, banco):
    """Acepta 'ABCD…' (una letra por pregunta, '-' en blanco) o pares '5A 6C' / '5:A,6:C'."""
    nums = sorted(q["n"] for q in banco if q["prueba"] == prueba)
    t = texto.strip().upper().replace(" ", "")
    if re.fullmatch(r"[A-E\-.X]+", t) and len(t) in (len(nums), 55):
        orden = list(range(1, 56)) if len(t) == 55 else nums
        return {n: (c if c in "ABCDE" else None) for n, c in zip(orden, t)}
    pares = re.findall(r"(\d{1,2})[:=]?([A-E])", texto.upper())
    if not pares:
        sys.exit("No entendí las respuestas. Usa 55 letras seguidas (ej. CDCDAAB…, '-' = en blanco) o pares '1C 2D 3C'.")
    return {int(n): c for n, c in pares}


def fmt_pct(x):
    return f"{100 * x:3.0f}%"


# ───────────────────────── iniciar (siembra desde tu hoja) ─────────────────────────

def cmd_iniciar(args):
    if E.RUTA.exists() and not args.forzar:
        print("Ya existe progreso/estado.json (usa --forzar para rehacerlo desde tu hoja).")
        return
    est = E.vacio()
    banco = B.cargar()
    idx = {(q["prueba"], q["n"]): q for q in banco}
    filas = list(csv.DictReader(open(RAIZ / "datos" / "respuestas_ensayo_I2026.csv")))
    por_tema, correctas, punt = {}, 0, 0
    for r in filas:
        q = idx[("I2026", int(r["n"]))]
        if not r["correcta"] or q["eliminada"]:
            continue
        ok = r["marcada"] == r["correcta"]
        if B.puntuable(q):
            punt += 1
            correctas += ok
            t = por_tema.setdefault(q["tema"], [0, 0])
            t[1] += 1
            t[0] += ok
        if not ok or "sin método" in r["notas"]:
            nota = "acertada sin método: repasar igual" if ok else ("no supe resolverla" if "no supe" in r["notas"] else "")
            est_fecha = {28: "2026-11-18", 29: "2026-11-18", 30: "2026-11-18", 31: "2026-11-18"}.get(q["n"])
            if est_fecha and q["n"] != 31:      # ✓ 18 nov (tu banco de errores) → racha 1, próximo +3 días
                E.agregar_error(est, q["id"], nota, racha=1, ultimo=date(2026, 11, 18), proximo=date(2026, 11, 21))
            else:
                E.agregar_error(est, q["id"], nota, racha=0, ultimo=None, proximo=date(2026, 11, 21))
    E.registrar_ensayo(est, "I2026", correctas, punt, puntaje_paes("I2026", correctas), por_tema, fecha=date(2026, 11, 14))
    E.guardar(est)
    print(f"Progreso creado desde tu hoja: ensayo I2026 = {correctas}/{punt} puntuables → {puntaje_paes('I2026', correctas)} pts; "
          f"{len(est['errores'])} errores en tu banco con repetición espaciada.")


# ───────────────────────── prioridades / estado ─────────────────────────

def prioridades(est, banco):
    pesos, cont = B.pesos(banco)
    filas = []
    for t in TEMAS:
        err_e, n_e = 0, 0
        for en in est["ensayos"]:
            a, n = en["por_tema"].get(t, [0, 0])
            err_e += n - a
            n_e += n
        tasa = (err_e + 1) / (n_e + 2)          # suavizado de Laplace
        te = est["temas"].get(t)
        if te and te["intentos"] >= 5:
            w = min(1.0, te["intentos"] / 25)
            tasa = (1 - w) * tasa + w * (1 - te["aciertos"] / te["intentos"])
        if te and te["dominado"]:
            tasa *= 0.3
        peso = pesos.get(t, 0)
        pend = sum(1 for qid, e in est["errores"].items() if not e["dominada"] and qid.startswith(("I", "R")) and
                   B.por_id(banco).get(qid, {}).get("tema") == t)
        filas.append({"tema": t, "peso": peso, "n_oficial": cont.get(t, 0), "tasa_error": tasa,
                      "en_juego": 50 * peso * tasa, "ens": f"{n_e - err_e}/{n_e}", "pend": pend, "estado": te})
    return sorted(filas, key=lambda f: -f["en_juego"])


def cmd_estado(args):
    est, banco = E.cargar(), B.cargar()
    if not est["ensayos"]:
        print("Aún no hay progreso. Ejecuta: python3 paes.py iniciar")
        return
    dias = (C.FECHA_PAES_M2 - E.hoy()).days
    print(f"\n  PAES M2: lunes 30-nov 15:00 h  →  faltan {dias} día(s)\n")
    print("  Ensayos registrados:")
    for en in est["ensayos"]:
        print(f"    {en['fecha']}  {en['prueba']:6} {en['correctas']:2}/{en['puntuables']}  → {en['puntaje']} pts")
    pend = E.pendientes(est)
    dom = sum(1 for e in est["errores"].values() if e["dominada"])
    print(f"\n  Banco de errores: {len(est['errores'])} (dominadas {dom}) · repasos pendientes hoy: {len(pend)}")
    print("\n  Prioridad por tema = preguntas que se esperan perder en una PAES (de 50)\n")
    print(f"  {'tema':9} {'nombre':44} {'peso':>5} {'ensayos':>8} {'práctica':>14} {'se pierden':>10}")
    for f in prioridades(est, banco)[:16]:
        te = f["estado"]
        pr = f"niv{te['nivel']} {te['aciertos']}/{te['intentos']}" + ("★" if te["dominado"] else "") if te else "—"
        print(f"  {f['tema']:9} {nombre(f['tema'])[:44]:44} {fmt_pct(f['peso']):>5} {f['ens']:>8} {pr:>14} {f['en_juego']:>9.1f}")
    deb = [d for d in R.debiles(est, banco, tasas_tema(est, banco)) if d["n"]][:6]
    print("\n  Subtemas más débiles (preguntas que se esperan perder; evidencia de ensayos, oficiales y ejercicios)\n")
    for d in deb:
        print(f"  {d['tema']:9} {d['sub']:30} {d['err']} error(es) en {d['n']:<3} ~{d['en_juego']:.1f}" + ("" if d["gen"] else "   (solo preguntas oficiales)"))
    cs = est["cartas"]
    act = sum(1 for c in cs.values() if not c["dominada"])
    print(f"\n  Tarjetas de refuerzo: {act} activas · {len(cs) - act} dominadas · vencen hoy: {len(R.cartas_pendientes(est))}")
    print("\n  Siguiente paso: python3 paes.py hoy   (o python3 paes.py refuerzo)\n")


# ───────────────────────── práctica interactiva ─────────────────────────

def mostrar_ejercicio(ej, num_str=""):
    print(f"\n{num_str}[{ej['tema']} · {ej['subtema']} · nivel {ej['nivel']}]")
    print(ej["enunciado"])
    for i, (txt, _) in enumerate(ej["opciones"]):
        print(f"   {LETRAS[i]}) {txt}")


def corregir_ejercicio(ej, marcada):
    ok = marcada == ej["correcta"]
    if ok:
        print("   ✓ Correcto.")
    else:
        print(f"   ✗ Era {LETRAS[ej['correcta']]}) {ej['opciones'][ej['correcta']][0]}")
        if marcada is not None:
            print(f"     Tu opción: {ej['opciones'][marcada][1]}")
    print(f"   Solución: {ej['explicacion']}")
    return ok


def tasas_tema(est, banco):
    return {f["tema"]: f["tasa_error"] for f in prioridades(est, banco)}


def registrar_gen(est, ej, ok, carta=None, sin_carta=False):
    """Registra un ejercicio generado: nivel del tema, subtema y, si falló, tarjeta de refuerzo."""
    t, sb = ej["tema"], ej["subtema"]
    subio = E.registrar_practica(est, t, ok)
    R.reg_sub(est, t, sb, ok)
    E.log_resp(est, 0, t, sb, ok)
    if carta:
        c = R.resolver_carta(est, carta, ok)
        if ok:
            print("   ✓ ¡Subtema dominado! Sale de tu refuerzo." if c["dominada"] else f"   Racha {c['racha']}/3 · vuelve el {c['proximo']}")
        else:
            print(f"   Vuelve mañana ({c['proximo']}) con otro ejercicio de este subtema.")
    elif not ok and not sin_carta:
        R.abrir_carta(est, t, sb, ej["nivel"])
        print("   ↻ Mañana te pongo otro ejercicio de este subtema (refuerzo).")
    if subio:
        print(f"   ⬆ ¡Subes a nivel {E.tema_estado(est, t)['nivel']} en {t}!")


def elegir_temas_prioritarios(est, banco, k=3):
    out = []
    for f in prioridades(est, banco):
        if f["tema"] in G.GENERADORES:
            out.append(f["tema"])
        if len(out) >= k:
            break
    return out


def cmd_practicar(args):
    est, banco = E.cargar(), B.cargar()
    temas = [args.tema] if args.tema else elegir_temas_prioritarios(est, banco)
    for t in temas:
        if t not in G.GENERADORES:
            sys.exit(f"No hay generador para {t}. Temas con ejercicios: {', '.join(G.GENERADORES)}")
    print(f"Práctica: {', '.join(temas)}  (responde A-D; Enter = saltar; q = salir)")
    aciertos = n = 0
    for i in range(args.n):
        t = temas[i % len(temas)]
        nivel = args.nivel or E.tema_estado(est, t)["nivel"]
        ej = G.ejercicio(t, nivel, subtema=args.subtema)
        mostrar_ejercicio(ej, f"{i + 1}/{args.n} ")
        r = leer("   Tu respuesta: ")
        if r is None or r.lower() == "q":
            break
        marcada = LETRAS.index(r.upper()) if r.upper() in tuple(LETRAS) else None
        ok = corregir_ejercicio(ej, marcada)
        n += 1
        aciertos += ok
        registrar_gen(est, ej, ok)
        E.guardar(est)
    if n:
        print(f"\nResultado: {aciertos}/{n}")


def cmd_refuerzo(args):
    """Sesión de refuerzo: tarjetas vencidas + ejercicios de tus subtemas más débiles."""
    est, banco = E.cargar(), B.cargar()
    items = R.items_refuerzo(est, banco, tasas_tema(est, banco), args.n)
    if not items:
        print("Aún no hay datos para detectar puntos débiles. Haz un ensayo o practica un tema.")
        return
    print("Refuerzo (responde A-D; Enter = saltar; q = salir)")
    aciertos = n = 0
    for i, (t, sb, carta, nivel) in enumerate(items, start=1):
        ej = G.ejercicio(t, nivel or E.tema_estado(est, t)["nivel"], subtema=sb)
        mostrar_ejercicio(ej, f"{i}/{len(items)} " + ("(refuerzo de un error anterior) " if carta else ""))
        r = leer("   Tu respuesta: ")
        if r is None or r.lower() == "q":
            break
        marcada = LETRAS.index(r.upper()) if r.upper() in tuple(LETRAS) else None
        ok = corregir_ejercicio(ej, marcada)
        n += 1
        aciertos += ok
        registrar_gen(est, ej, ok, carta)
        E.guardar(est)
    if n:
        print(f"\nResultado: {aciertos}/{n}")


# ───────────────────────── hojas (para resolver en papel) ─────────────────────────

def cmd_hoja(args):
    est, banco = E.cargar(), B.cargar()
    temas = [args.tema] if args.tema else elegir_temas_prioritarios(est, banco)
    hid = f"{E.hoy().isoformat()}_{'-'.join(temas)}_{random.randrange(10**4):04d}"
    items, lineas = [], [f"# Hoja de ejercicios {hid}", "",
                         "Resuélvelos en papel, **sin calculadora**, y luego corrige con:",
                         f"`python3 paes.py corregir {hid} 1A 2C 3B ...`", ""]
    sol = ["", "---", "## Soluciones (no mires antes de intentar)", ""]
    for i in range(args.n):
        t = temas[i % len(temas)]
        nivel = args.nivel or E.tema_estado(est, t)["nivel"]
        ej = G.ejercicio(t, nivel, subtema=args.subtema)
        items.append({"tema": t, "nivel": nivel, "semilla": ej["semilla"], "subtema": args.subtema})
        lineas += [f"**{i + 1}.** *({t} · nivel {nivel})* {ej['enunciado']}", ""]
        lineas += [f"- {LETRAS[j]}) {txt}" for j, (txt, _) in enumerate(ej["opciones"])]
        lineas.append("")
        sol += [f"{i + 1}. **{LETRAS[ej['correcta']]}** — {ej['explicacion']}"]
    est["hojas"][hid] = {"fecha": E.hoy().isoformat(), "items": items, "corregida": False}
    E.guardar(est)
    ruta = RAIZ / "hojas" / f"{hid}.md"
    ruta.parent.mkdir(exist_ok=True)
    ruta.write_text("\n".join(lineas + sol) + "\n")
    print(f"Hoja creada: {ruta.relative_to(RAIZ)}")
    print(f"Cuando termines: python3 paes.py corregir {hid} <respuestas>")


def cmd_corregir(args):
    est = E.cargar()
    h = est["hojas"].get(args.hoja)
    if not h:
        sys.exit("Hoja no encontrada. IDs: " + ", ".join(est["hojas"]) if est["hojas"] else "No hay hojas.")
    pares = dict((int(n), c) for n, c in re.findall(r"(\d{1,2})[:=]?([A-D])", " ".join(args.respuestas).upper()))
    ok_total = 0
    for i, it in enumerate(h["items"], start=1):
        ej = G.ejercicio(it["tema"], it["nivel"], semilla=it["semilla"], subtema=it["subtema"])
        marcada = LETRAS.index(pares[i]) if i in pares else None
        print(f"\n{i}. [{it['tema']}] {ej['enunciado'][:110]}…" if len(ej["enunciado"]) > 110 else f"\n{i}. [{it['tema']}] {ej['enunciado']}")
        ok = corregir_ejercicio(ej, marcada)
        ok_total += ok
        if not h["corregida"]:
            registrar_gen(est, ej, ok)
    h["corregida"] = True
    E.guardar(est)
    print(f"\nResultado: {ok_total}/{len(h['items'])}")


# ───────────────────────── repaso de errores oficiales ─────────────────────────

def render_pagina(q):
    out = RAIZ / "pruebas" / "paginas"
    out.mkdir(parents=True, exist_ok=True)
    base = out / f"{q['prueba']}_P{q['n']:02d}"
    pdf = RAIZ / q["pdf"]
    if not pdf.exists():
        return None
    if not Path(str(base) + ".png").exists():
        subprocess.run(["pdftoppm", "-png", "-r", "110", "-f", str(q["pagina_pdf"]), "-l", str(q["pagina_pdf"]), "-singlefile", str(pdf), str(base)],
                       check=False, capture_output=True)
    return Path(str(base) + ".png") if Path(str(base) + ".png").exists() else None


def cmd_repaso(args):
    est, banco = E.cargar(), B.cargar()
    ids = B.por_id(banco)
    of = [("of", q) for q in E.pendientes(est)]
    ca = [("carta", k) for k in R.cartas_pendientes(est)]
    cola = []
    for i in range(max(len(of), len(ca))):          # intercala tarjetas de refuerzo y preguntas oficiales
        if i < len(ca):
            cola.append(ca[i])
        if i < len(of):
            cola.append(of[i])
    cola = cola[: args.n]
    if not cola:
        print("🎉 No tienes repasos pendientes hoy.")
        return
    print(f"{len(cola)} repaso(s): {sum(1 for t, _ in cola if t == 'of')} preguntas oficiales y "
          f"{sum(1 for t, _ in cola if t == 'carta')} ejercicios de refuerzo.\n")
    for tipo, x in cola:
        if tipo == "carta":
            c = est["cartas"][x]
            ej = G.ejercicio(c["tema"], c["nivel"], subtema=c["sub"])
            mostrar_ejercicio(ej, "(refuerzo de un error anterior) ")
            r = leer("   Tu respuesta (A-D, Enter = saltar, q = salir): ")
            if r is None or r.lower() == "q":
                break
            if not r:
                continue
            ok = corregir_ejercicio(ej, LETRAS.index(r.upper()) if r.upper() in tuple(LETRAS) else None)
            registrar_gen(est, ej, ok, x)
            E.guardar(est)
            continue
        qid = x
        q = ids[qid]
        e = est["errores"][qid]
        if not args.misma and q["tema"] in G.GENERADORES:
            # un ejercicio NUEVO del mismo tema: el resultado actualiza el calendario de tu error original
            sb = q["subtema"] if q["subtema"] in R.subtemas_gen().get(q["tema"], set()) else None
            ej = G.ejercicio(q["tema"], max(2, E.tema_estado(est, q["tema"])["nivel"]), subtema=sb)
            mostrar_ejercicio(ej, f"(repaso de tu error {B.etiqueta(q)}: otro ejercicio del mismo tema) ")
            r = leer("   Tu respuesta (A-D, Enter = saltar, q = salir): ")
            if r is None or r.lower() == "q":
                break
            if not r:
                continue
            ok = corregir_ejercicio(ej, LETRAS.index(r.upper()) if r.upper() in tuple(LETRAS) else None)
            registrar_gen(est, ej, ok, sin_carta=True)
            e = E.registrar_intento(est, qid, ok, sin_oficial=True)
            print(f"   Tu error {B.etiqueta(q)}: " + ("¡DOMINADO!" if e["dominada"] else (f"racha {e['racha']}/3 · vuelve {e['proximo']}" if ok else f"vuelve mañana ({e['proximo']})")))
            E.guardar(est)
            continue
        print(f"▶ {B.etiqueta(q)}  ({q['prueba_etiqueta']})  → {q['pdf']}  pág. {q['pagina_pdf']}")
        print(f"   Tema: {q['tema']} · {q['descripcion']}" + (f"   [{e['nota']}]" if e["nota"] else ""))
        if q["eliminada"] or not q["clave"]:
            continue
        if args.imagen:
            png = render_pagina(q)
            if png:
                print(f"   Imagen: {png.relative_to(RAIZ)}")
        r = leer("   Tu respuesta (A-E, Enter = saltar, q = salir): ")
        if r is None or r.lower() == "q":
            break
        if not r:
            continue
        ok = r.upper() == q["clave"]
        E.registrar_intento(est, qid, ok)
        E.log_resp(est, 1, q["tema"], q["subtema"], ok)
        e = est["errores"][qid]
        if ok:
            print(f"   ✓ Correcto (racha {e['racha']}/3)" + (" · ¡DOMINADA!" if e["dominada"] else f" · próximo repaso: {e['proximo']}"))
        else:
            print(f"   ✗ La clave es {q['clave']}. Vuelve a verla mañana ({e['proximo']}). Practica el tema: python3 paes.py practicar {q['tema']}")
        E.guardar(est)


# ───────────────────────── gemelas ─────────────────────────

def cmd_gemelas(args):
    banco = B.cargar()
    ids = B.por_id(banco)
    if args.objetivo in ids:
        q = ids[args.objetivo]
        base = [q]
    elif re.fullmatch(r"[A-Za-z]\d{4}-?P?\d{1,2}", args.objetivo):
        m = re.fullmatch(r"([A-Za-z]\d{4})-?P?(\d{1,2})", args.objetivo)
        q = ids.get(f"{m.group(1).upper()}-{int(m.group(2)):02d}")
        if not q:
            sys.exit("No encontré esa pregunta.")
        base = [q]
    else:
        base = None
    if base:
        q = base[0]
        print(f"{B.etiqueta(q)}: {q['descripcion']}  [{q['tema']} · {q['subtema']}]\nGemelas en otras pruebas:")
        for g in B.gemelas(q, banco, max_n=args.max):
            print(f"  {B.etiqueta(g):10} p.{g['pagina_pdf']:<3} clave {g['clave'] or '—'}  {g['descripcion']}  [{g['subtema']}]")
        return
    tema = args.objetivo
    if tema not in TEMAS:
        sys.exit(f"Tema desconocido. Temas: {', '.join(TEMAS)}")
    print(f"Preguntas oficiales de {tema} ({nombre(tema)}), de la más reciente a la más antigua:")
    for g in sorted([x for x in banco if x["tema"] == tema], key=lambda x: (B.ORDEN_PRUEBAS.index(x["prueba"]), x["n"])):
        flag = " (piloto)" if g["piloto"] else (" (eliminada)" if g["eliminada"] else "")
        print(f"  {B.etiqueta(g):10} p.{g['pagina_pdf']:<3} clave {g['clave'] or '—'}  {g['descripcion']}{flag}  [{g['subtema']}]")


# ───────────────────────── ensayo completo ─────────────────────────

def cmd_ensayo(args):
    est, banco = E.cargar(), B.cargar()
    prueba = args.prueba.upper()
    qs = {q["n"]: q for q in banco if q["prueba"] == prueba}
    if not qs:
        sys.exit(f"Prueba desconocida. Opciones: {', '.join(B.ORDEN_PRUEBAS)}")
    resp = parsear_respuestas(" ".join(args.respuestas), prueba, banco)
    correctas = punt = 0
    por_tema, falladas = {}, []
    for n, q in sorted(qs.items()):
        if q["eliminada"] or not q["clave"]:
            continue
        marcada = resp.get(n)
        ok = marcada == q["clave"]
        if B.puntuable(q):
            punt += 1
            correctas += ok
            t = por_tema.setdefault(q["tema"], [0, 0])
            t[1] += 1
            t[0] += ok
        if not ok and marcada is not None or (not ok and marcada is None and n in resp):
            falladas.append((q, marcada))
        elif not ok and n not in resp:
            pass
    paes = puntaje_paes(prueba, correctas) if punt >= 49 else None
    print(f"\n{prueba} — {qs[min(qs)]['prueba_etiqueta']}")
    print(f"Correctas puntuables: {correctas}/{punt}" + (f"  →  puntaje PAES {paes}" if paes else "  (selección parcial: sin conversión a puntaje)"))
    print("\nPor tema (aciertos/preguntas):")
    for t, (a, n) in sorted(por_tema.items(), key=lambda x: x[1][0] / x[1][1]):
        print(f"  {t:9} {a}/{n}  {nombre(t)}")
    print("\nErradas (se agregan a tu banco de errores):")
    for q, m in falladas:
        mark = "en blanco" if m is None else f"marcaste {m}"
        print(f"  P{q['n']:<2} {mark:<12} clave {q['clave']}  {q['tema']:9} {q['descripcion']}" + ("  (piloto: no puntúa)" if q["piloto"] else ""))
        E.agregar_error(est, q["id"], "ensayo " + prueba, proximo=E.hoy() + timedelta(days=1))
    if not args.sin_guardar:
        E.registrar_ensayo(est, prueba, correctas, punt, paes, por_tema, resp=resp)
        E.guardar(est)
        print("\nGuardado. Revisa tus nuevas prioridades: python3 paes.py estado")


# ───────────────────────── hoy ─────────────────────────

def cmd_hoy(args):
    est, banco = E.cargar(), B.cargar()
    if not est["ensayos"]:
        print("Primero: python3 paes.py iniciar")
        return
    hoy = E.hoy()
    dias = (C.FECHA_PAES_M2 - hoy).days
    print(f"\n═══ {['lunes','martes','miércoles','jueves','viernes','sábado','domingo'][hoy.weekday()]} {hoy.strftime('%d-%m-%Y')} · faltan {dias} día(s) para la PAES M2 ═══\n")
    plan = C.PLAN.get(hoy.isoformat())
    if plan:
        titulo, detalle, mods = plan
        print(f"Plan del día: {titulo}\n  {detalle}\n")
    pend = E.pendientes(est)
    ids = B.por_id(banco)
    nca = len(R.cartas_pendientes(est))
    print(f"1) REPASO ({len(pend)} preguntas oficiales + {nca} ejercicios de refuerzo): python3 paes.py repaso")
    for qid in pend[:5]:
        q = ids[qid]
        print(f"     · {B.etiqueta(q):10} {q['descripcion']}")
    deb = [d for d in R.debiles(est, banco, tasas_tema(est, banco)) if d["gen"]][:3]
    if deb:
        print("\n   PUNTOS MÁS DÉBILES → python3 paes.py refuerzo")
        for d in deb:
            print(f"     · {d['tema']} {d['sub']} ({d['err']} error(es) en {d['n']})" if d["n"] else f"     · {d['tema']} {d['sub']} (sin datos aún)")
    pr = prioridades(est, banco)
    gen = [f for f in pr if f["tema"] in G.GENERADORES]
    top = gen[0]
    mod = C.modulo_de_tema(top["tema"])
    print(f"\n2) FOCO NUEVO: {top['tema']} — {nombre(top['tema'])}   (se esperan perder ~{top['en_juego']:.1f} preguntas)")
    if mod:
        print(f"     Guía: {mod[3]}")
    te = est["temas"].get(top["tema"], {"nivel": 1})
    print(f"     Práctica: python3 paes.py practicar {top['tema']} -n 8        (nivel actual {te['nivel']})")
    print(f"     En papel:  python3 paes.py hoja {top['tema']} -n 8")
    print(f"     Gemelas oficiales: python3 paes.py gemelas {top['tema']}")
    print("\n3) ELÍGETE UN RETO si te sobra tiempo: " + ", ".join(f"{f['tema']} ({f['en_juego']:.1f})" for f in gen[1:4]))
    print()


def cmd_fortalezas(args):
    est, banco = E.cargar(), B.cargar()
    deb = [d for d in R.debiles(est, banco, tasas_tema(est, banco)) if d["n"] >= 3]
    fuertes = sorted((d for d in deb if d["err"] / d["n"] <= 0.25), key=lambda d: (d["err"] / d["n"], -d["n"]))
    camino = [d for d in deb if 0.25 < d["err"] / d["n"] <= 0.5]
    domE = sum(1 for e in est["errores"].values() if e["dominada"])
    domC = sum(1 for c in est["cartas"].values() if c["dominada"])
    print(f"\n  Dominados: {domE} preguntas oficiales · {domC} subtemas de refuerzo")
    sin_err = [f for f in prioridades(est, banco) if f["ens"].split("/")[1] not in ("0",) and f["ens"].split("/")[0] == f["ens"].split("/")[1]
               and int(f["ens"].split("/")[1]) >= 2]
    if sin_err:
        print("  Temas sin errores en tus ensayos: " + ", ".join(f"{f['tema']} {f['ens']}" for f in sin_err))
    print("\n  Subtemas sólidos (≥ 75 % con 3 o más respuestas):")
    for d in fuertes or []:
        print(f"    ✓ {d['tema']:9} {d['sub']:30} {d['n'] - d['err']}/{d['n']}")
    if not fuertes:
        print("    (aún no hay evidencia suficiente: hacen falta 3 respuestas por subtema)")
    if camino:
        print("\n  En camino (50–75 %):")
        for d in camino:
            print(f"    · {d['tema']:9} {d['sub']:30} {d['n'] - d['err']}/{d['n']}")
    print()


def cmd_meta(args):
    est = E.cargar()
    tablas = json.loads((RAIZ / "datos" / "tabla_puntaje.json").read_text())
    need = sorted(next((p for p in range(51) if t[str(p)] >= args.puntaje), 51) for t in tablas.values())
    print(f"\n  {args.puntaje} puntos exigen ~{need[len(need) // 2]} de 50 correctas "
          f"({need[0]}–{need[-1]} según la prueba; tablas oficiales de las 7 pruebas).")
    ult = [e for e in est["ensayos"] if e.get("puntaje")]
    if ult:
        c = ult[-1]["correctas"]
        falta = need[len(need) // 2] - c
        print(f"  Tu último ensayo ({ult[-1]['prueba']}): {c} correctas · " + ("ya llegas a la meta." if falta <= 0 else f"te faltan ~{falta}."))
    if args.puntaje >= 950:
        print("  Con 49 o 50 de 50 se llega al 1000 en las pruebas recientes: casi cero errores (ver docs/investigacion.md).")
    print()


def cmd_camino(args):
    est, banco = E.cargar(), B.cargar()
    pr = {f["tema"]: f for f in prioridades(est, banco)} if est["ensayos"] else {}
    print("\nCAMINO GUIADO (de mayor a menor impacto)\n")
    for mid, titulo, temas, archivo in C.MODULOS:
        en_juego = sum(pr[t]["en_juego"] for t in temas if t in pr)
        estados = []
        for t in temas:
            te = est["temas"].get(t)
            if t not in G.GENERADORES:
                estados.append(f"{t}:oficiales")
            elif te:
                estados.append(f"{t}:niv{te['nivel']}" + ("★" if te["dominado"] else ""))
            else:
                estados.append(f"{t}:—")
        print(f"  {mid:3} {titulo:48} ~{en_juego:4.1f} preg. en juego   {' '.join(estados)}")
        print(f"       guía: {archivo}")
    print("\nNiveles de dominio por tema: 1 base → 2 tipo PAES → 3 trampas/experto (★ = dominado).")
    print("Subes de nivel con 4 aciertos de los últimos 5 ejercicios.\n")


def cmd_pagina(args):
    ids = B.por_id()
    q = ids.get(args.id.upper())
    if not q:
        m = re.fullmatch(r"([A-Za-z]\d{4})-?P?(\d{1,2})", args.id)
        q = ids.get(f"{m.group(1).upper()}-{int(m.group(2)):02d}") if m else None
    if not q:
        sys.exit("Pregunta no encontrada (ej. I2027-12 ó I2027P12).")
    png = render_pagina(q)
    print(f"{B.etiqueta(q)} → {q['pdf']} pág. {q['pagina_pdf']}" + (f"\nImagen: {png}" if png else "\n(PDF no descargado: ejecuta scripts/descargar_pruebas.sh)"))


def cmd_autotest(args):
    from . import autotest
    sys.exit(0 if autotest.correr(args.n) else 1)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="paes.py", description="Sistema de práctica PAES M2 personalizado")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("iniciar", help="crea tu progreso a partir de tu hoja de resultados")
    p.add_argument("--forzar", action="store_true")
    p.set_defaults(f=cmd_iniciar)
    sub.add_parser("estado", help="panel de prioridades y progreso").set_defaults(f=cmd_estado)
    sub.add_parser("hoy", help="qué hacer hoy").set_defaults(f=cmd_hoy)
    sub.add_parser("camino", help="módulos del camino guiado").set_defaults(f=cmd_camino)
    p = sub.add_parser("practicar", help="ejercicios generados (interactivo)")
    p.add_argument("tema", nargs="?")
    p.add_argument("-n", type=int, default=6)
    p.add_argument("--nivel", type=int, choices=[1, 2, 3])
    p.add_argument("--subtema")
    p.set_defaults(f=cmd_practicar)
    p = sub.add_parser("refuerzo", help="sesión con tus puntos más débiles (tarjetas vencidas + subtemas flojos)")
    p.add_argument("-n", type=int, default=9)
    p.set_defaults(f=cmd_refuerzo)
    sub.add_parser("fortalezas", help="lo que ya dominas (subtemas sólidos)").set_defaults(f=cmd_fortalezas)
    p = sub.add_parser("meta", help="cuántas correctas exige un puntaje: meta 850")
    p.add_argument("puntaje", type=int)
    p.set_defaults(f=cmd_meta)
    p = sub.add_parser("hoja", help="genera una hoja de ejercicios para resolver en papel")
    p.add_argument("tema", nargs="?")
    p.add_argument("-n", type=int, default=8)
    p.add_argument("--nivel", type=int, choices=[1, 2, 3])
    p.add_argument("--subtema")
    p.set_defaults(f=cmd_hoja)
    p = sub.add_parser("corregir", help="corrige una hoja: corregir ID 1A 2C ...")
    p.add_argument("hoja")
    p.add_argument("respuestas", nargs="+")
    p.set_defaults(f=cmd_corregir)
    p = sub.add_parser("repaso", help="repaso espaciado de tus errores oficiales")
    p.add_argument("-n", type=int, default=8)
    p.add_argument("--imagen", action="store_true", help="renderiza la página del PDF como PNG")
    p.add_argument("--misma", action="store_true", help="repasar la misma pregunta oficial en vez de un ejercicio nuevo del mismo tema")
    p.set_defaults(f=cmd_repaso)
    p = sub.add_parser("gemelas", help="preguntas oficiales parecidas: por tema (ALG-cua) o por pregunta (I2026-28)")
    p.add_argument("objetivo")
    p.add_argument("--max", type=int, default=8)
    p.set_defaults(f=cmd_gemelas)
    p = sub.add_parser("ensayo", help="corrige un ensayo completo: ensayo I2027 CDCD...")
    p.add_argument("prueba")
    p.add_argument("respuestas", nargs="+")
    p.add_argument("--sin-guardar", action="store_true")
    p.set_defaults(f=cmd_ensayo)
    p = sub.add_parser("pagina", help="dónde está una pregunta oficial (PDF y página)")
    p.add_argument("id")
    p.set_defaults(f=cmd_pagina)
    p = sub.add_parser("autotest", help="verifica los generadores")
    p.add_argument("-n", type=int, default=200)
    p.set_defaults(f=cmd_autotest)
    args = ap.parse_args(argv)
    args.f(args)
