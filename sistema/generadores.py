"""Generadores de ejercicios tipo PAES M2 (alternativas A-D).

Cada generador recibe (rnd, nivel) y devuelve un dict con:
  tema, subtema, enunciado, correcta (str), distractores [(str, por_qué)], explicacion (str)
`armar()` lo convierte en un ejercicio listo para mostrar. La respuesta correcta siempre se calcula
en código y, cuando es posible, se verifica numéricamente con asserts (ver `paes.py autotest`).

Niveles:  1 = base · 2 = tipo PAES · 3 = trampas / experto
"""
import math
import random
from fractions import Fraction as Fr
from itertools import product

SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def sup(n):
    return str(n).translate(SUP)


def num(x):
    """Entero o fracción con signo menos tipográfico."""
    x = Fr(x)
    s = str(abs(x.numerator)) if x.denominator == 1 else f"{abs(x.numerator)}/{x.denominator}"
    return ("−" if x < 0 else "") + s


def dec(x, nd=2):
    return f"{x:.{nd}f}".replace(".", ",").replace("-", "−")


def poly(a, b, c, var="x"):
    partes = []
    for coef, mon in ((a, var + "²"), (b, var), (c, "")):
        coef = Fr(coef)
        if coef == 0:
            continue
        mag = abs(coef)
        cs = "" if (mag == 1 and mon) else num(mag)
        t = cs + mon
        if not partes:
            partes.append(("−" if coef < 0 else "") + t)
        else:
            partes.append((" − " if coef < 0 else " + ") + t)
    return "".join(partes) or "0"


def raiz(k, n):
    """k·√n simplificado como texto."""
    f = 1
    for d in range(int(math.isqrt(n)), 1, -1):
        if n % (d * d) == 0:
            f, n = d, n // (d * d)
            break
    k = Fr(k) * f
    if n == 1:
        return num(k)
    ks = "" if k == 1 else num(k)
    return f"{ks}√{n}"


class FaltanDistractores(Exception):
    pass


def armar(rnd, g):
    ops = [(g["correcta"], None)]
    vistos = {g["correcta"]}
    for s, r in g["distractores"]:
        if s not in vistos:
            vistos.add(s)
            ops.append((s, r))
    if len(ops) < 4:
        raise FaltanDistractores(g["subtema"])
    ops = ops[:4]
    rnd.shuffle(ops)
    idx = next(i for i, (s, _) in enumerate(ops) if s == g["correcta"])
    return {"tema": g["tema"], "subtema": g["subtema"], "enunciado": g["enunciado"],
            "opciones": ops, "correcta": idx, "explicacion": g["explicacion"]}


# ───────────────────────── ALG-cua ─────────────────────────

def cua_vertice(rnd, nivel):
    a = rnd.choice([1, -1]) if nivel == 1 else rnd.choice([1, -1, 2, -2, 3, -3])
    h, k = rnd.randint(-6, 6), rnd.randint(-9, 9)
    if h == 0:
        h = 2
    b, c = -2 * a * h, a * h * h + k
    f = lambda x: a * x * x + b * x + c
    assert f(h) == k and all(f(h + d) * a >= k * a for d in (-1, 1))
    pide_y = nivel >= 2
    enun = f"Considera la función f(x) = {poly(a, b, c)}. ¿Cuál es la coordenada {'y' if pide_y else 'x'} de su vértice?"
    if pide_y:
        correcta = num(k)
        mal = [(num(f(Fr(-b, a))), "Usaste x = −b/a (olvidaste el 2 de −b/2a)."),
               (num(f(Fr(b, 2 * a))), "Te equivocaste de signo en x = −b/(2a)."),
               (num(c), "Diste el intercepto con el eje Y (f(0)), no el vértice."),
               (num(h), "Diste la coordenada x del vértice, no la y.")]
        expl = f"xᵥ = −b/(2a) = {num(h)}. Luego yᵥ = f({num(h)}) = {num(k)}. Siempre: primero x, después evalúas."
    else:
        correcta = num(h)
        mal = [(num(Fr(-b, a)), "Olvidaste el 2: x = −b/(2a), no −b/a."),
               (num(-h), "Error de signo: x = −b/(2a)."),
               (num(k), "Esa es la coordenada y del vértice."),
               (num(Fr(b, 2 * a) + 1), "Cálculo mal hecho; recalcula −b/(2a).")]
        expl = f"xᵥ = −b/(2a) = −({num(b)})/(2·{num(a)}) = {num(h)}."
    return dict(tema="ALG-cua", subtema="vertice-maximo", enunciado=enun, correcta=correcta,
                distractores=mal, explicacion=expl)


def cua_max(rnd, nivel):
    t0, a, c = rnd.randint(2, 8), rnd.randint(1, 5), rnd.randint(0, 30)
    b = 2 * a * t0
    h = lambda t: -a * t * t + b * t + c
    assert all(h(t0) >= h(t0 + d) for d in (-1, 1))
    cosa = rnd.choice(["un cohete", "una pelota", "un dron"])
    enun = (f"La altura (en metros) de {cosa} t segundos después del lanzamiento es h(t) = {poly(-a, b, c, 't')}. "
            f"¿Cuál es la altura máxima que alcanza?")
    mal = [(num(c), "Esa es la altura inicial h(0)."),
           (num(t0), "Ese es el instante del máximo, no la altura."),
           (num(b * t0), "Solo evaluaste el término bt."),
           (num(h(t0 + 1)), "Evaluaste en t = tᵥ + 1, no en el vértice.")]
    return dict(tema="ALG-cua", subtema="vertice-maximo", enunciado=enun, correcta=num(h(t0)), distractores=mal,
                explicacion=f"tᵥ = −b/(2a) = {t0}. Altura máxima = h({t0}) = {num(h(t0))} m. "
                            f"Como a<0 la parábola abre hacia abajo: el vértice es un máximo.")


def cua_cuadrante(rnd, nivel):
    while True:
        r1, r2 = sorted(rnd.sample(range(-8, 9), 2))
        if r1 + r2 != 0:
            break
    a = rnd.choice([1, 2, 3, -1, -2])
    xv, yv = Fr(r1 + r2, 2), Fr(-a * (r2 - r1) ** 2, 4)
    assert a * (xv - r1) * (xv - r2) == yv
    q = {(1, 1): "I", (-1, 1): "II", (-1, -1): "III", (1, -1): "IV"}[(1 if xv > 0 else -1, 1 if yv > 0 else -1)]
    espejo_x = {"I": "II", "II": "I", "III": "IV", "IV": "III"}[q]
    espejo_y = {"I": "IV", "IV": "I", "II": "III", "III": "II"}[q]
    ambos = {"I": "III", "III": "I", "II": "IV", "IV": "II"}[q]
    forma = poly(a, -a * (r1 + r2), a * r1 * r2)
    enun = (f"La parábola f(x) = {forma} corta al eje X en x = {num(r1)} y x = {num(r2)}. "
            f"¿En qué cuadrante está su vértice?")
    mal = [(f"Cuadrante {espejo_x}", "Cambiaste el signo de la coordenada x del vértice."),
           (f"Cuadrante {espejo_y}", "Cambiaste el signo de la coordenada y del vértice."),
           (f"Cuadrante {ambos}", "Cambiaste los dos signos.")]
    rnd.shuffle(mal)
    return dict(tema="ALG-cua", subtema="vertice-maximo", enunciado=enun, correcta=f"Cuadrante {q}",
                distractores=mal + [("Sobre el eje Y", "El vértice está justo en la mitad de las raíces; solo está en el eje Y si suman 0.")],
                explicacion=f"xᵥ = (r₁+r₂)/2 = {num(xv)}. Con a {'>' if a > 0 else '<'} 0 el vértice está "
                            f"{'debajo' if a > 0 else 'encima'} del eje X, así que yᵥ {'<' if a > 0 else '>'} 0 (calcula {num(yv)}). "
                            f"REGLA: escribe (x, y) = ({num(xv)}, {num(yv)}) con sus signos y recién ahí di el cuadrante → {q}.")


def cua_coef_b(rnd, nivel):
    while True:
        r1, r2 = sorted(rnd.sample(range(-7, 8), 2))
        if r1 + r2 != 0:
            break
    a = rnd.choice([1, 2, -1, -2, 3])
    b, c = -a * (r1 + r2), a * r1 * r2
    assert all(a * r * r + b * r + c == 0 for r in (r1, r2))
    enun = (f"La gráfica de f(x) = ax² + bx + c corta al eje X en x = {num(r1)} y en x = {num(r2)}, "
            f"y se sabe que a = {num(a)}. ¿Cuál es el valor de b?")
    mal = [(num(a * (r1 + r2)), "Error de signo: b = −a(r₁+r₂), no a(r₁+r₂)."),
           (num(c), "Ese es c = a·r₁·r₂, no b."),
           (num(-(r1 + r2)), "Olvidaste multiplicar por a."),
           (num(Fr(-a * (r1 + r2), 2)), "Dividiste por 2 (eso es la coordenada x del vértice).")]
    return dict(tema="ALG-cua", subtema="grafico-coeficientes", enunciado=enun, correcta=num(b), distractores=mal,
                explicacion=f"f(x) = a(x − r₁)(x − r₂) = a x² − a(r₁+r₂)x + a·r₁r₂. Entonces b = −a(r₁+r₂) = {num(b)}.")


def cua_reflexion(rnd, nivel):
    a, b, c = rnd.choice([1, 2, 3, -1, -2]), rnd.choice([-5, -4, -3, -2, 2, 3, 4, 5]), rnd.choice([-6, -3, -1, 1, 2, 4, 5])
    f = (a, b, c)
    ejeX, ejeY, orig = (-a, -b, -c), (a, -b, c), (-a, b, -c)
    solo_a = (-a, b, c)
    casos = {
        "eje X": (ejeX, "g(x) = −f(x)"),
        "eje Y": (ejeY, "g(x) = f(−x)"),
        "origen": (orig, "g(x) = −f(−x)"),
    }
    nombre = rnd.choice(list(casos))
    corr, regla = casos[nombre]
    otras = {"eje X": "la reflexión respecto al eje X", "eje Y": "la reflexión respecto al eje Y",
             "origen": "la reflexión respecto al origen"}
    mal = [(poly(*v), f"Esa es {otras[k]}.") for k, (v, _) in casos.items() if k != nombre]
    mal.append((poly(*solo_a), "Solo cambiaste el signo de a (no de todo f)."))
    enun = f"Si f(x) = {poly(*f)}, ¿cuál es la expresión de la función g que resulta de reflejar la gráfica de f respecto al {nombre}?"
    return dict(tema="ALG-cua", subtema="reflexion-transformacion", enunciado=enun, correcta=poly(*corr), distractores=mal,
                explicacion=f"Reflexión respecto al {nombre}: {regla}. Aplica el signo a TODO el polinomio → {poly(*corr)}.")


def cua_discriminante(rnd, nivel):
    d, t = rnd.randint(1, 3), rnd.randint(1, 4)
    a, m = d, d * t * t
    k = 2 * d * t
    assert k * k - 4 * a * m == 0
    coef = "" if a == 1 else str(a)
    enun = f"¿Para qué valores de k la ecuación {coef}x² + kx + {m} = 0 tiene una única solución real?"
    mal = [(f"Solo k = {k}", "Olvidaste el valor negativo: k² = 4am tiene dos soluciones."),
           (f"k = ±{d * t}", "Olvidaste el 4 del discriminante (usaste k² = am)."),
           (f"k = ±{k * k}", "Pusiste k² en vez de k."),
           (f"k = ±{4 * a * m}", "Igualaste k a 4am; falta la raíz cuadrada.")]
    return dict(tema="ALG-cua", subtema="discriminante-vieta", enunciado=enun, correcta=f"k = ±{k}", distractores=mal,
                explicacion=f"Una única solución ⇔ discriminante = 0: k² − 4·{a}·{m} = 0 ⇒ k² = {4 * a * m} ⇒ k = ±{k}.")


def cua_vieta(rnd, nivel):
    while True:
        r1, r2 = rnd.sample([x for x in range(-6, 7) if x != 0], 2)
        if r1 + r2 != 0:
            break
    a = rnd.choice([1, 2, 3, 5])
    b, c = -a * (r1 + r2), a * r1 * r2
    suma, prod = Fr(r1 + r2), Fr(r1 * r2)
    tipo = rnd.choice(["suma", "producto"] if nivel == 1 else ["suma", "producto", "inversos"])
    ec = f"{poly(a, b, c)} = 0"
    if tipo == "suma":
        pide, res = "la suma de las raíces", suma
        mal = [(num(-suma), "Error de signo: suma = −b/a."), (num(Fr(c, a)), "Ese es el producto (c/a)."),
               (num(Fr(b, 1)), "Olvidaste dividir por a."), (num(Fr(-b, 2 * a)), "Esa es la mitad: x del vértice.")]
    elif tipo == "producto":
        pide, res = "el producto de las raíces", prod
        mal = [(num(-prod), "Error de signo: producto = c/a."), (num(suma), "Esa es la suma."),
               (num(Fr(c, 1)), "Olvidaste dividir por a."), (num(Fr(a, c)), "Invertiste: producto = c/a, no a/c.")]
    else:
        pide, res = "la suma de los inversos de las raíces (1/x₁ + 1/x₂)", suma / prod
        mal = [(num(prod / suma), "Invertiste la fracción."), (num(-suma / prod), "Error de signo."),
               (num(suma), "Esa es x₁ + x₂, no la suma de inversos."), (num(1 / suma + 1 / prod), "Mezclaste suma y producto.")]
    assert tipo != "inversos" or res == Fr(1, r1) + Fr(1, r2)
    return dict(tema="ALG-cua", subtema="discriminante-vieta", enunciado=f"Sean x₁ y x₂ las soluciones de {ec}. ¿Cuál es {pide}?",
                correcta=num(res), distractores=mal,
                explicacion=f"Vieta: x₁ + x₂ = −b/a = {num(suma)} y x₁·x₂ = c/a = {num(prod)}. "
                            f"1/x₁ + 1/x₂ = (x₁+x₂)/(x₁x₂). No necesitas resolver la ecuación.")


# ───────────────────────── ALG-sis ─────────────────────────

def sis_monedas(rnd, nivel):
    A, B = rnd.choice([(500, 100), (1000, 500), (100, 50), (100, 10), (500, 50)])
    x, y = rnd.randint(4, 25), rnd.randint(4, 25)
    if x == y:
        y += 3
    N, M = x + y, A * x + B * y
    assert x == (M - B * N) // (A - B) and (M - B * N) % (A - B) == 0
    Ms = f"{M:,}".replace(",", " ")
    enun = (f"En una alcancía hay {N} monedas, algunas de ${A} y otras de ${B}; en total suman ${Ms}. "
            f"¿Cuántas monedas de ${A} hay?")
    mal = [(str(y), f"Esa es la cantidad de monedas de ${B}."), (str(N // 2), "Supusiste mitad y mitad."),
           (str(abs(x - y)), "Esa es la diferencia entre ambas cantidades."), (str(M // A), f"Supusiste que todas eran de ${A}.")]
    return dict(tema="ALG-sis", subtema="plantear", enunciado=enun, correcta=str(x), distractores=mal,
                explicacion=f"Sea x = monedas de ${A}, y = monedas de ${B}. x + y = {N}; {A}x + {B}y = {M}. "
                            f"Reemplaza y = {N} − x: {A}x + {B}({N} − x) = {M} ⇒ {A - B}x = {M - B * N} ⇒ x = {x}. "
                            f"Responde lo que pide la pregunta (monedas de ${A}).")


def sis_sin_solucion(rnd, nivel):
    a, b = rnd.randint(1, 4), rnd.randint(2, 5)
    m = rnd.choice([2, 3, 4])
    c = rnd.randint(1, 6)
    e = m * c + rnd.choice([1, 2, -1, 3])
    k, d = m * a, m * b
    enun = f"¿Para qué valor de k el sistema {a}x + {b}y = {c} ; kx + {d}y = {e} no tiene solución?"
    mal = [(str(a), "Igualaste k con el coeficiente de x de la primera ecuación."),
           (str(d), "Confundiste k con el coeficiente de y."),
           (str(k + a), "Cálculo mal hecho: debe mantenerse la proporción de los coeficientes."),
           (str(-k), "Error de signo: las rectas paralelas tienen coeficientes con la misma razón.")]
    return dict(tema="ALG-sis", subtema="sin-o-infinitas", enunciado=enun, correcta=str(k), distractores=mal,
                explicacion=f"Sin solución ⇔ rectas paralelas: k/{a} = {d}/{b} ≠ {e}/{c}. Como {d}/{b} = {m}, k = {m}·{a} = {k}. "
                            f"Y como {e}/{c} ≠ {m}, no son la misma recta (si fueran la misma habría infinitas soluciones).")


def sis_tipo(rnd, nivel):
    tipo = rnd.choice(["unica", "ninguna", "infinitas"])
    a, b, c = rnd.randint(1, 5), rnd.randint(1, 5), rnd.randint(1, 9)
    m = rnd.choice([2, 3, -1, -2])
    if tipo == "unica":
        eq2 = (a + 1, b + 2, rnd.randint(1, 9))
    elif tipo == "ninguna":
        eq2 = (m * a, m * b, m * c + 1)
    else:
        eq2 = (m * a, m * b, m * c)
    det = a * eq2[1] - eq2[0] * b
    if det != 0:
        res = "unica"
    elif a * eq2[2] - eq2[0] * c == 0 and b * eq2[2] - eq2[1] * c == 0:
        res = "infinitas"
    else:
        res = "ninguna"
    if res != tipo:                      # (p. ej. a+1,b+2 paralelas por casualidad): reintentar
        return sis_tipo(rnd, nivel)
    t = {"unica": "Una única solución", "ninguna": "Ninguna solución", "infinitas": "Infinitas soluciones"}
    mal = [(t[k], "Compara las razones a₁/a₂, b₁/b₂ y c₁/c₂ con cuidado.") for k in t if k != tipo]
    mal.append(("Exactamente dos soluciones", "Un sistema lineal 2x2 nunca tiene exactamente dos soluciones."))
    enun = f"¿Cuántas soluciones tiene el sistema {a}x + {b}y = {c} ; {eq2[0]}x + {eq2[1]}y = {eq2[2]}?"
    return dict(tema="ALG-sis", subtema="sin-o-infinitas", enunciado=enun, correcta=t[tipo], distractores=mal,
                explicacion=f"Razones: {a}/{eq2[0]}, {b}/{eq2[1]}, {c}/{eq2[2]}. Distintas las dos primeras → única; "
                            f"las tres iguales → infinitas; las dos primeras iguales y la tercera distinta → ninguna.")


def sis_infinitas(rnd, nivel):
    p0, B, D, m = rnd.randint(1, 5), rnd.randint(2, 6), rnd.randint(1, 5), rnd.choice([2, 3, 4, 5])
    A, C, q = m * p0, m * D, m * B
    enun = f"El sistema {A}x + qy = {C} ; px + {B}y = {D} tiene infinitas soluciones. ¿Cuáles son los valores de p y q, respectivamente?"
    mal = [(f"{m * p0} y {B}", "Escalaste mal: la segunda ecuación es la primera dividida por " + str(m) + "."),
           (f"{q} y {p0}", "Intercambiaste p y q."),
           (f"{p0} y {B}", "q no puede ser igual a B: debe cumplir q/B = A/p."),
           (f"{p0 + 1} y {q}", "p debe cumplir A/p = C/D.")]
    return dict(tema="ALG-sis", subtema="sin-o-infinitas", enunciado=enun, correcta=f"{p0} y {q}", distractores=mal,
                explicacion=f"Infinitas soluciones ⇒ ecuaciones proporcionales: {A}/p = q/{B} = {C}/{D} = {m}. "
                            f"Entonces p = {A}/{m} = {p0} y q = {m}·{B} = {q}.")


# ───────────────────────── ALG-prop ─────────────────────────

def prop_inversa_gas(rnd, nivel):
    P1, V1 = rnd.choice([(2, 30), (4, 24), (5, 40), (3, 36), (2, 48), (6, 20)])
    divs = [d for d in range(1, V1 * P1 + 1) if (P1 * V1) % d == 0 and d != P1 and d <= 24]
    P2 = rnd.choice(divs)
    V2 = Fr(P1 * V1, P2)
    var = abs(V2 - V1)
    enun = (f"A temperatura constante, la presión y el volumen de un gas son inversamente proporcionales. "
            f"Si a {P1} atm el volumen es {V1} L, ¿en cuántos litros varía el volumen (en valor absoluto) cuando la presión pasa a {P2} atm?")
    directo = Fr(V1 * P2, P1)
    mal = [(num(V2), "Ese es el volumen final, no la variación."),
           (num(abs(directo - V1)), "Usaste proporcionalidad directa (V·P no es V/P)."),
           (num(V2 + V1), "Sumaste en vez de restar."),
           (num(abs(Fr(V1 * P1, P2 + 1) - V1)), "Error al despejar V₂ = P₁V₁/P₂.")]
    return dict(tema="ALG-prop", subtema="inversa", enunciado=enun, correcta=num(var), distractores=mal,
                explicacion=f"Inversa: P₁·V₁ = P₂·V₂ ⇒ V₂ = {P1}·{V1}/{P2} = {num(V2)} L. Variación absoluta = |{num(V2)} − {V1}| = {num(var)} L. "
                            f"Lee qué pide: ¿volumen final o variación?")


def prop_tabla(rnd, nivel):
    k = rnd.choice([12, 24, 36, 60])
    xs = rnd.choice([(2, 3, 4), (3, 4, 6), (2, 4, 6)])
    q = rnd.randint(2, 4)
    inv = (xs, tuple(k // x for x in xs))
    dire = (xs, tuple(q * x for x in xs))
    afin = (xs, tuple(q * x + 3 for x in xs))
    cuad = (xs, tuple(x * x for x in xs))
    fmt = lambda t: "x: " + ", ".join(map(str, t[0])) + "  |  y: " + ", ".join(map(str, t[1]))
    assert len({x * y for x, y in zip(*inv)}) == 1
    mal = [(fmt(dire), "Aquí y/x es constante: proporcionalidad DIRECTA."),
           (fmt(afin), "Aquí y = qx + 3: relación afín (no pasa por el origen), ni directa ni inversa."),
           (fmt(cuad), "Aquí y = x²: no es proporcional.")]
    return dict(tema="ALG-prop", subtema="inversa", enunciado="¿En cuál de las siguientes tablas x e y son inversamente proporcionales?",
                correcta=fmt(inv), distractores=mal + [(fmt((xs, tuple(k - x for x in xs))), "Aquí y = k − x: relación afín decreciente, no inversa.")],
                explicacion="Inversa ⇔ el PRODUCTO x·y es constante. Directa ⇔ el COCIENTE y/x es constante. "
                            "Revisa los dos con las tres columnas, no solo con la primera.")


def prop_trabajo(rnd, nivel):
    while True:
        a, b = rnd.sample([2, 3, 4, 5, 6, 10, 12], 2)
        c = rnd.choice([8, 12, 15, 20, 24, 30])
        den = Fr(1, a) + Fr(1, b) - Fr(1, c)
        if den > 0:
            break
    T = 1 / den
    enun = (f"Una llave llena un estanque vacío en {a} horas y otra lo llena en {b} horas. Una llave de desagüe lo vacía, "
            f"estando lleno, en {c} horas. Si las tres se abren al mismo tiempo con el estanque vacío, ¿en cuántas horas se llena?")
    mal = [(num(1 / (Fr(1, a) + Fr(1, b) + Fr(1, c))), "Sumaste también el desagüe: el desagüe RESTA caudal."),
           (num(Fr(a + b, 2)), "No se promedian los tiempos: se suman los caudales (1/t)."),
           (num(Fr(a * b, a + b)), "Ignoraste el desagüe."),
           (num(den), "Esa es la fracción del estanque que se llena en 1 hora, no el tiempo.")]
    return dict(tema="ALG-prop", subtema="inversa", enunciado=enun, correcta=num(T), distractores=mal,
                explicacion=f"Caudales (estanque/hora): 1/{a} + 1/{b} − 1/{c} = {num(den)}. Tiempo = 1/caudal = {num(T)} horas.")


# ───────────────────────── ALG-lin ─────────────────────────

def lin_porcentaje(rnd, nivel):
    g = rnd.choice([20, 25, 30, 40, 50])
    q = rnd.choice([400, 800, 1000, 1200])
    d = rnd.choice([100, 200, 300])
    p_ant = Fr(q * (100 + g), 100)
    nuevo = Fr((q + d) * (100 + g), 100)
    enun = (f"Una panadería fija el precio de venta de un producto para ganar un {g} % SOBRE EL COSTO de producción, que hoy es ${q}. "
            f"Si el costo sube ${d} y se mantiene el {g} % de ganancia sobre el nuevo costo, ¿cuál es el nuevo precio de venta?")
    mal = [(num(p_ant + d), "Sumaste el aumento al precio antiguo: el % se calcula sobre el NUEVO costo."),
           (num(p_ant * Fr(100 + g, 100)), "Aplicaste el % sobre el precio de venta, no sobre el costo."),
           (num(q + d + Fr(g * q, 100)), "Calculaste la ganancia sobre el costo antiguo."),
           (num(Fr((q + d) * g, 100)), "Esa es solo la ganancia, no el precio.")]
    return dict(tema="ALG-lin", subtema="porcentaje-precio", enunciado=enun, correcta=num(nuevo), distractores=mal,
                explicacion=f"Precio = costo·(1 + {g}/100). Nuevo costo = {q + d}. Precio = {q + d}·{Fr(100 + g, 100)} = {num(nuevo)}. "
                            f"(Por eso en I2026 P26 el % se calcula sobre el nuevo costo.)")


def lin_arriendo(rnd, nivel):
    while True:
        d1, d2 = rnd.randint(10, 20), rnd.randint(25, 40)
        x = rnd.randint(3, 9)
        F1 = rnd.randint(30, 60)
        F2 = F1 - (d2 - d1) * x
        if F2 >= 5:
            break
    assert F1 + d1 * x == F2 + d2 * x
    enun = (f"La empresa A cobra un fijo de ${F1} mil más ${d1} mil por día de arriendo. La empresa B cobra un fijo de ${F2} mil "
            f"más ${d2} mil por día. ¿Para cuántos días de arriendo ambas empresas cobran lo mismo?")
    mal = [(str(x + 1), "Revisa: iguala los costos y despeja."),
           (num(F1 - F2), "Esa es la diferencia de fijos; falta dividir por la diferencia de tarifas."),
           (num(Fr(F1 - F2, d2 + d1)), "Sumaste las tarifas en vez de restarlas."),
           (str(x - 1), "Revisa la igualdad de costos.")]
    return dict(tema="ALG-lin", subtema="modelo-recta", enunciado=enun, correcta=str(x), distractores=mal,
                explicacion=f"{F1} + {d1}x = {F2} + {d2}x ⇒ {F1 - F2} = {d2 - d1}x ⇒ x = {x}.")


# ───────────────────────── ALG-exp ─────────────────────────

def exp_duplicacion(rnd, nivel):
    dA, dB = rnd.choice([(10, 20), (10, 40), (20, 10), (5, 10), (20, 40), (40, 10)])
    T = rnd.choice([20, 40])
    if T % dA or T % dB:
        T = 40
    a0, b0 = rnd.choice([100, 200, 500]), rnd.choice([50, 100, 300])
    tot = a0 * 2 ** (T // dA) + b0 * 2 ** (T // dB)
    f = lambda n: f"{n:,}".replace(",", " ")
    enun = (f"Dos cultivos de bacterias duplican su cantidad: el primero cada {dA} minutos y el segundo cada {dB} minutos. "
            f"Inicialmente hay {a0} y {b0} bacterias, respectivamente. ¿Cuántas bacterias hay en total transcurridos {T} minutos?")
    mal = [(f((a0 + b0) * 2 ** (T // dA)), "Usaste el mismo período para ambos cultivos."),
           (f(a0 * 2 * (T // dA) + b0 * 2 * (T // dB)), "Trataste el crecimiento como lineal (·2·n) en vez de 2ⁿ."),
           (f(a0 * (T // dA) ** 2 + b0 * (T // dB) ** 2), "Elevaste n al cuadrado: el exponente es n, la base es 2."),
           (f((a0 + b0) * 2 ** (T // dB)), "Usaste el período del segundo cultivo para ambos.")]
    return dict(tema="ALG-exp", subtema="crecimiento-bacterias", enunciado=enun, correcta=f(tot), distractores=mal,
                explicacion=f"Cultivo 1: {a0}·2^({T}/{dA}) = {a0 * 2 ** (T // dA)}. Cultivo 2: {b0}·2^({T}/{dB}) = {b0 * 2 ** (T // dB)}. Suma = {f(tot)}.")


def exp_interes(rnd, nivel):
    C = rnd.choice([350, 200, 500, 120]) * 1000
    i, n = rnd.choice([(1.5, 3), (2, 4), (0.5, 6), (2.5, 2)])
    fac = dec(1 + i / 100, 3)
    cap = "$" + f"{C:,}".replace(",", " ")
    corr = f"{cap} · {fac}{sup(n)}"
    mal = [(f"{cap} · {dec(i / 100, 3)}{sup(n)}", "Usaste solo la tasa: falta el 1 (el capital sigue ahí)."),
           (f"{cap} · {dec(1 + i * n / 100, 3)}", "Eso es interés SIMPLE; el compuesto capitaliza cada período."),
           (f"{cap} · ({fac}{sup(n)} − 1)", "Eso es solo el interés ganado, no el capital final."),
           (f"{cap} · {fac} · {n}", "Multiplicaste por n en vez de elevar a n.")]
    return dict(tema="ALG-exp", subtema="interes-compuesto",
                enunciado=f"Se depositan {cap} con interés compuesto de {dec(i, 1)} % por período. ¿Qué expresión da el capital después de {n} períodos?",
                correcta=corr, distractores=mal,
                explicacion=f"Cada período multiplica por (1 + i) = {fac}. Después de {n} períodos: C·(1+i)ⁿ = {corr}.")


# ───────────────────────── NUM-log ─────────────────────────

def log_aprox(rnd, nivel):
    la, lb = 0.30, 0.48          # log 2, log 3
    l5 = round(1 - la, 2)
    assert abs(math.log10(2) - la) < 0.01 and abs(math.log10(3) - lb) < 0.01 and abs(math.log10(5) - l5) < 0.01
    m, base = rnd.choice([(20, 3), (30, 2), (45, 2), (50, 3), (40, 3), (60, 3)])   # sin log₂15: es la pregunta I2026 P10
    fac = {2: la, 3: lb, 5: l5}
    ps, x = [], m
    for p in (2, 3, 5):
        while x % p == 0:
            ps.append(p)
            x //= p
    num_t = " + ".join(dec(fac[p]) for p in ps)
    den = dec(fac[base])
    corr = f"({num_t}) ÷ {den}"
    val = sum(fac[p] for p in ps) / fac[base]
    assert abs(val - math.log(m, base)) < 0.2
    otro = 3 if base == 2 else 2
    mal = [(f"({' · '.join(dec(fac[p]) for p in ps)}) ÷ {den}", "log(a·b) = log a + log b: se SUMA, no se multiplica."),
           (f"({num_t}) ÷ {dec(fac[otro])}", "Usaste la base equivocada en el cambio de base: log_b N = log N / log b."),
           (f"({' + '.join(dec(fac[p]) if p != 5 else dec(la) for p in ps)}) ÷ {den}", "Usaste log 2 como si fuera log 5 (log 5 = 1 − log 2 ≈ 0,70)."),
           (f"{den} ÷ ({num_t})", "Invertiste el cociente del cambio de base.")]
    return dict(tema="NUM-log", subtema="propiedades-evaluar",
                enunciado=f"Si log 2 ≈ 0,30 y log 3 ≈ 0,48, ¿cuál expresión aproxima log_{base} {m}?" + ("" if nivel >= 3 else " (log = log base 10; recuerda que log 5 = log(10/2))"),
                correcta=corr, distractores=mal,
                explicacion=f"log_{base} {m} = log {m} / log {base}. Descompón {m} = {' · '.join(map(str, ps))} ⇒ log {m} = {num_t.replace(' + ', ' + ')}, "
                            f"usando log 5 = 1 − log 2 = 0,70.")


def log_eval(rnd, nivel):
    cands = [(2, 3, 8), (2, 5, 32), (3, 2, 9), (3, 3, 27), (5, 2, 25), (2, 4, 16), (3, 4, 81), (10, 3, 1000), (2, 6, 64), (5, 3, 125)]
    (b1, e1, n1), (b2, e2, n2), (b3, e3, n3) = rnd.sample(cands, 3)
    corr = e1 + e2 - e3
    enun = f"¿Cuál es el valor de log_{b1} {n1} + log_{b2} {n2} − log_{b3} {n3}?"
    assert b1 ** e1 == n1 and b2 ** e2 == n2 and b3 ** e3 == n3
    mal = [(str(e1 + e2 + e3), "Pusiste + en lugar de − en el tercer término."),
           (str(e1 * e2 - e3), "log a + log b no es el producto de los logaritmos."),
           (str(n1 // b1 + n2 // b2 - n3 // b3), "Dividiste N entre la base: log_b N pregunta '¿a qué exponente?'."),
           (str(e1 - e2 - e3), "Error de signo en el segundo término.")]
    return dict(tema="NUM-log", subtema="propiedades-evaluar", enunciado=enun, correcta=str(corr), distractores=mal,
                explicacion=f"log_b N = exponente al que hay que elevar b para obtener N: {b1}^{e1}={n1} ⇒ {e1}; {b2}^{e2}={n2} ⇒ {e2}; "
                            f"{b3}^{e3}={n3} ⇒ {e3}. Total: {e1} + {e2} − {e3} = {corr}.")


def log_cambio_base(rnd, nivel):
    t = rnd.randint(2, 5)
    a, b = rnd.choice([1, 2]), rnd.choice([1, 2, 3])
    res = Fr(a, t) + b
    enun = f"Si log_m p = {t} (con m, p > 1), ¿cuál es el valor de log_p ({'m' if a == 1 else f'm{sup(a)}'}·p{sup(b) if b > 1 else ''})?"
    mal = [(num(a * t + b), "Invertiste: log_p m = 1/log_m p, no log_m p."), (num(Fr(a, t) * b), "log(AB) = log A + log B: se suma."),
           (num(Fr(t, a) + b), "Invertiste la fracción log_p m = 1/t."), (num(Fr(1, t) + b * t), "Aplicaste mal la propiedad de la potencia.")]
    return dict(tema="NUM-log", subtema="propiedades-evaluar", enunciado=enun, correcta=num(res), distractores=mal,
                explicacion=f"log_p m = 1/log_m p = 1/{t}. Entonces log_p(m^{a}·p^{b}) = {a}·(1/{t}) + {b}·1 = {num(res)}.")


# ───────────────────────── ALG-expr / ALG-ecu ─────────────────────────

def expr_notables(rnd, nivel):
    a, b = rnd.randint(1, 5), rnd.choice([-5, -4, -3, -2, 2, 3, 4, 5])
    if rnd.random() < 0.5:
        enun = f"¿Cuál de las siguientes expresiones es igual a ({'' if a == 1 else a}x {'+' if b > 0 else '−'} {abs(b)})²?"
        corr = poly(a * a, 2 * a * b, b * b)
        mal = [(poly(a * a, 0, b * b), "Olvidaste el doble producto 2ab."), (poly(a * a, a * b, b * b), "El doble producto es 2·a·b, no a·b."),
               (poly(a * a, -2 * a * b, b * b), "Error de signo en el doble producto.")]
        expl = "(p + q)² = p² + 2pq + q². El signo del término del medio sale del signo dentro del paréntesis."
    else:
        enun = f"¿Cuál es la factorización de {poly(a * a, 0, -b * b)}?"
        corr = f"({'' if a == 1 else a}x + {abs(b)})({'' if a == 1 else a}x − {abs(b)})"
        mal = [(f"({'' if a == 1 else a}x − {abs(b)})²", "Eso es un cuadrado de binomio; la diferencia de cuadrados es (p+q)(p−q)."),
               (f"({'' if a == 1 else a}x + {abs(b)})²", "Eso da un término central 2pq que aquí no existe."),
               (f"({'' if a == 1 else a * a}x + {b * b})({'' if a == 1 else a * a}x − {b * b})", "Debes sacar la raíz cuadrada de cada término.")]
        expl = "p² − q² = (p + q)(p − q): saca la raíz de cada término."
    return dict(tema="ALG-expr", subtema="general", enunciado=enun, correcta=corr, distractores=mal, explicacion=expl)


def ecu_inecuacion(rnd, nivel):
    a, b, c = rnd.randint(2, 6), rnd.randint(-8, 8), rnd.randint(-8, 8)
    # -a x + b <= c  → x >= (b-c)/a
    lim = Fr(b - c, a)
    enun = f"¿Cuál es el conjunto solución de la inecuación {num(-a)}x + {num(b)} ≤ {num(c)}?".replace("+ −", "− ")
    corr = f"[{num(lim)}, ∞["
    mal = [(f"]−∞, {num(lim)}]", "Al dividir por un número NEGATIVO el sentido de la desigualdad se invierte."),
           (f"]−∞, {num(-lim)}]", "Error de signo y no invertiste la desigualdad."),
           (f"[{num(-lim)}, ∞[", "Error de signo al despejar."),
           (f"]{num(lim)}, ∞[", "El ≤ incluye el extremo: el intervalo es cerrado en ese lado.")]
    assert all(-a * x + b <= c for x in (lim, lim + 1)) and not (-a * (lim - 1) + b <= c)
    return dict(tema="ALG-ecu", subtema="general", enunciado=enun, correcta=corr, distractores=mal,
                explicacion=f"{num(-a)}x ≤ {num(c - b)} ⇒ dividir por {num(-a)} (negativo) INVIERTE el signo ⇒ x ≥ {num(lim)}.")


# ───────────────────────── Suficiencia de datos ─────────────────────────

def _cierre(conocido, nz=True):
    u, v, p, w = conocido
    cambio = True
    while cambio:
        cambio = False
        reglas = [(u and w and not v, "v"), (v and w and not u, "u"), (u and p and not v and nz, "v"), (v and p and not u and nz, "u"),
                  (u and v and not p, "p"), (u and v and not w, "w"), (w and u and not v, "v"), (w and v and not u, "u")]
        for cond, var in reglas:
            if cond:
                idx = "uvpw".index(var)
                if not [u, v, p, w][idx]:
                    [u, v, p, w] = [True if i == idx else x for i, x in enumerate([u, v, p, w])]
                    cambio = True
    return u, v, p, w


def suf_datos(rnd, nivel):
    S = {"suma": "x + y = {a}", "dif": "x − y = {b}", "prod": "x² − y² = {c}", "x": "x = {d}"}
    es = {"suma": (1, 0, 0, 0), "dif": (0, 1, 0, 0), "prod": (0, 0, 1, 0), "x": (0, 0, 0, 1)}
    u0, v0 = rnd.choice([2, 3, 4, 5, 6]), rnd.choice([1, 2, 3, 4])
    vals = dict(a=u0, b=v0, c=u0 * v0, d=Fr(u0 + v0, 2))
    ob, tg = rnd.choice([("x² − y²", "p"), ("x − y", "v"), ("x + y", "u"), ("y", "y")])
    s1, s2 = rnd.sample(list(S), 2)

    def determina(claves):
        k = [False] * 4
        for c in claves:
            k = [a or b for a, b in zip(k, es[c])]
        u, v, p, w = _cierre(tuple(k))
        if tg == "p":
            return p or (u and v)
        if tg == "v":
            return v
        if tg == "u":
            return u
        return u and v                # y se determina cuando se conocen x+y y x−y
    d1, d2, dj = determina([s1]), determina([s2]), determina([s1, s2])
    if d1 and d2:
        r = "D) Cada una por sí sola, (1) ó (2)"
    elif d1:
        r = "A) (1) por sí sola"
    elif d2:
        r = "B) (2) por sí sola"
    elif dj:
        r = "C) Ambas juntas, (1) y (2)"
    else:
        r = "E) Se requiere información adicional"
    enun = (f"[Suficiencia de datos] x e y son números reales con x + y ≠ 0 y x − y ≠ 0. ¿Se puede determinar el valor de {ob}?\n"
            f"   (1) {S[s1].format(**vals)}\n   (2) {S[s2].format(**vals)}")
    todas = ["A) (1) por sí sola", "B) (2) por sí sola", "C) Ambas juntas, (1) y (2)", "D) Cada una por sí sola, (1) ó (2)", "E) Se requiere información adicional"]
    mal = [(o, "Evalúa primero cada afirmación POR SEPARADO y recién después juntas.") for o in todas if o != r]
    return dict(tema="ALG-expr", subtema="general", enunciado=enun, correcta=r, distractores=mal,
                explicacion="Ten en mente x² − y² = (x+y)(x−y). Anota qué cantidad fija cada afirmación (x+y, x−y, su producto o x) y "
                            "qué se puede deducir con una sola y con ambas. No resuelvas el problema: solo decide si se PUEDE.")


# ───────────────────────── Geometría ─────────────────────────

def geo_razon_diagonal(rnd, nivel):
    a, b = rnd.choice([(4, 3), (5, 12), (8, 15), (7, 24), (16, 10), (20, 21)])   # sin 16:9: es la pregunta I2026 P16
    k = rnd.choice(["k", "p", "t"])
    hip2 = a * a + b * b
    diag = raiz(1, hip2)
    expr = f"{diag}{k}" if diag.isdigit() else f"{k}·{diag}"
    en_pulg = rnd.random() < 0.5 and nivel >= 2
    enun = (f"Una pantalla rectangular tiene sus lados en la razón {a} : {b}. Si el lado MAYOR mide {a}{k} cm, "
            f"¿cuánto mide su diagonal{' en pulgadas (1 pulgada = 2,54 cm)' if en_pulg else ' en cm'}?")
    if en_pulg:
        corr = f"{expr} ÷ 2,54"
        mal = [(f"{expr} · 2,54", "Para pasar de cm a pulgadas se DIVIDE por 2,54."),
               (f"{a + b}{k} ÷ 2,54", "La diagonal no es a + b: usa Pitágoras."),
               (expr, "Falta convertir a pulgadas."),
               (f"{k}·√{a * a - b * b} ÷ 2,54", "Restaste los cuadrados (eso daría un cateto).")]
    else:
        corr = expr
        mal = [(f"{a + b}{k}", "La diagonal no es la suma de los lados: Pitágoras d² = a² + b²."),
               (f"{k}·√{a * a - b * b}", "Restaste los cuadrados (eso daría un cateto)."),
               (f"{k}·√{a + b}", "Sumaste antes de elevar al cuadrado: d² = a² + b², no (a + b)."),
               (f"{hip2}{k}", "Olvidaste sacar la raíz cuadrada.")]
    return dict(tema="GEO-sem", subtema="pitagoras-razones", enunciado=enun, correcta=corr, distractores=mal,
                explicacion=f"Lados: {a}{k} y {b}{k}. d² = ({a}{k})² + ({b}{k})² = {hip2}{k}² ⇒ d = {expr}. Luego convierte unidades si lo piden.")


def geo_hexagono(rnd, nivel):
    s = rnd.randint(2, 9)
    area = Fr(3 * s * s, 2)
    variante = rnd.choice(["lado", "radio"] if nivel == 1 else ["lado", "radio", "perimetro"])
    if variante == "lado":
        enun = f"¿Cuál es el área de un hexágono regular de lado {s} cm?"
    elif variante == "radio":
        enun = f"Un hexágono regular está inscrito en una circunferencia de radio {s} cm. ¿Cuál es su área?"
    else:
        enun = f"Un hexágono regular tiene perímetro {6 * s} cm. ¿Cuál es su área?"
    corr = f"{num(area)}√3 cm²"
    mal = [(f"{num(Fr(s * s, 4))}√3 cm²", "Esa es el área de UN triángulo equilátero; el hexágono tiene 6."),
           (f"{3 * s * s}√3 cm²", "Falta dividir por 2: A = (3√3/2)·l²."),
           (f"{6 * s * s} cm²", "El hexágono no es 6 cuadrados de lado l."),
           (f"{num(Fr(3 * s * s, 2))} cm²", "Olvidaste el √3.")]
    return dict(tema="GEO-circ", subtema="hexagono", enunciado=enun, correcta=corr, distractores=mal,
                explicacion=f"El hexágono regular se parte en 6 triángulos equiláteros de lado l = {s}. "
                            f"Área de cada uno = (l²√3)/4. Total = 6·(l²√3)/4 = (3√3/2)·l² = {num(area)}√3 cm². "
                            f"(Radio de la circunferencia circunscrita = lado.)")


def _termino_vec(cu, cv, cw):
    partes = []
    for coef, nom in ((cu, "u"), (cv, "v"), (cw, "w")):
        if coef == 0:
            continue
        t = nom if abs(coef) == 1 else f"{abs(coef)}{nom}"
        partes.append(("−" if coef < 0 else "") + t if not partes else f" {'−' if coef < 0 else '+'} {t}")
    return "".join(partes)


def geo_vectores(rnd, nivel):
    if nivel <= 2:
        u, v, w = [(rnd.randint(-5, 5), rnd.randint(-5, 5)) for _ in range(3)]
        cu, cv, cw = rnd.choice([(1, 1, -1), (1, -1, 2), (-1, 1, 2), (2, -1, 1), (1, 2, -1)])
        g = lambda su, sv, sw: (su * cu * u[0] + sv * cv * v[0] + sw * cw * w[0], su * cu * u[1] + sv * cv * v[1] + sw * cw * w[1])
        fm = lambda t: f"({num(t[0])}, {num(t[1])})"
        corr = g(1, 1, 1)
        mal = [(fm(g(1, 1, -1)), "Error de signo con w."), (fm(g(1, -1, 1)), "Error de signo con v: el signo afecta a TODAS las coordenadas."),
               (fm((corr[1], corr[0])), "Intercambiaste las coordenadas (x, y)."), (fm(g(-1, 1, 1)), "Error de signo con u.")]
        enun = (f"Si u = ({u[0]}, {u[1]}), v = ({v[0]}, {v[1]}) y w = ({w[0]}, {w[1]}), ¿cuáles son las coordenadas de {_termino_vec(cu, cv, cw)}?")
        return dict(tema="GEO-vec", subtema="general", enunciado=enun, correcta=fm(corr), distractores=mal,
                    explicacion="Opera coordenada a coordenada; el signo y el escalar se aplican a las dos coordenadas de cada vector.")
    a0, b0, q = rnd.randint(1, 5), rnd.randint(1, 5), rnd.randint(1, 4)
    T = (5 * a0, 3 * b0 - 2 * q)
    zu, zv = (a0, 5 * b0), (-2 * a0, b0 + q)
    corr_v = (zu[0] + zv[0], zu[1] + zv[1])
    assert (zu[0] - 2 * zv[0], zu[1] - 2 * zv[1]) == T
    enun = f"Los vectores u = (a, 5b) y v = (−2a, b + {q}) cumplen u − 2v = ({num(T[0])}, {num(T[1])}). ¿Cuáles son las coordenadas de u + v?"
    fm = lambda t: f"({num(t[0])}, {num(t[1])})"
    mal = [(fm((zu[0] - zv[0], zu[1] - zv[1])), "Calculaste u − v en vez de u + v."), (fm(zu), "Esas son las coordenadas de u, no de u + v."),
           (fm((corr_v[1], corr_v[0])), "Intercambiaste las coordenadas."), (fm(zv), "Esas son las coordenadas de v.")]
    return dict(tema="GEO-vec", subtema="general", enunciado=enun, correcta=fm(corr_v), distractores=mal,
                explicacion=f"u − 2v = (a + 4a, 5b − 2b − {2 * q}) = (5a, 3b − {2 * q}) = ({num(T[0])}, {num(T[1])}) ⇒ a = {a0}, b = {b0}. "
                            f"Entonces u = {fm(zu)}, v = {fm(zv)} y u + v = {fm(corr_v)}.")


def geo_isometrias(rnd, nivel):
    P = (rnd.randint(-6, 6), rnd.randint(-6, 6))
    if P[0] == 0 or P[1] == 0:
        P = (3, -2)
    ops = {
        "una reflexión respecto al eje X": lambda p: (p[0], -p[1]),
        "una reflexión respecto al eje Y": lambda p: (-p[0], p[1]),
        "una rotación de 90° en sentido antihorario con centro en el origen": lambda p: (-p[1], p[0]),
        "una rotación de 90° en sentido horario con centro en el origen": lambda p: (p[1], -p[0]),
    }
    dx, dy = rnd.randint(-4, 4), rnd.randint(-4, 4)
    tras = (f"una traslación según el vector ({dx}, {dy})".replace("-", "−"), lambda p: (p[0] + dx, p[1] + dy))
    n1, f1 = rnd.choice(list(ops.items()))
    seq = [(n1, f1), tras] if rnd.random() < 0.5 else [tras, (n1, f1)]

    def aplicar(orden, sustituir=None):
        Q = P
        for nm, f in orden:
            Q = (sustituir if (sustituir and nm == n1) else f)(Q)
        return Q
    Q = aplicar(seq)
    fm = lambda t: f"({t[0]}, {t[1]})".replace("-", "−")
    inv = ops[[k for k in ops if k != n1][0]]
    mal = [(fm(aplicar(list(reversed(seq)))), "Aplicaste las transformaciones en el orden contrario."),
           (fm(aplicar(seq, inv)), "Usaste otra isometría (eje o sentido de giro equivocado)."),
           (fm((Q[1], Q[0])), "Intercambiaste las coordenadas."), (fm((-Q[0], -Q[1])), "Error de signo global.")]
    return dict(tema="GEO-iso", subtema="rotacion-reflexion-traslacion",
                enunciado=f"Al punto {fm(P)} se le aplica {seq[0][0]} y luego {seq[1][0]}. ¿Cuáles son las coordenadas finales?",
                correcta=fm(Q), distractores=mal,
                explicacion="Aplica las transformaciones UNA a UNA, en el orden dicho. Reflexión eje X: (x,y)→(x,−y); eje Y: (x,y)→(−x,y); "
                            "giro 90° antihorario: (x,y)→(−y,x); horario: (x,y)→(y,−x); traslación: sumas el vector.")


def geo_homotecia(rnd, nivel):
    C = (rnd.randint(-3, 3), rnd.randint(-3, 3))
    P = (rnd.randint(-5, 5), rnd.randint(-5, 5))
    k = rnd.choice([2, 3, -1, -2, Fr(1, 2)]) if nivel >= 2 else rnd.choice([2, 3, -2])
    k = Fr(k)
    if P == C:
        P = (C[0] + 2, C[1] - 1)
    img = (C[0] + k * (P[0] - C[0]), C[1] + k * (P[1] - C[1]))
    fmt = lambda t: f"({num(t[0])}, {num(t[1])})"
    sin_centro = (k * P[0], k * P[1])
    mk = lambda t: fmt(t)
    mal = [(mk(sin_centro), "Ignoraste el centro: la homotecia se calcula desde C, no desde el origen."),
           (mk((C[0] - k * (P[0] - C[0]), C[1] - k * (P[1] - C[1]))), "Error de signo en la razón (k negativa invierte el sentido)."),
           (mk((C[0] + (P[0] - C[0]) * k + 1, C[1] + (P[1] - C[1]) * k - 1)), "Error aritmético al multiplicar."),
           (mk((P[0] + k * C[0], P[1] + k * C[1])), "Fórmula mal usada: P' = C + k(P − C).")]
    return dict(tema="GEO-iso", subtema="homotecia",
                enunciado=f"Se aplica una homotecia de centro C{fmt(C)} y razón {num(k)} al punto P{fmt(P)}. ¿Cuáles son las coordenadas de la imagen P'?",
                correcta=fmt(img), distractores=mal,
                explicacion=f"P' = C + k·(P − C) = {fmt(C)} + ({num(k)})·({num(P[0] - C[0])}, {num(P[1] - C[1])}) = {fmt(img)}. "
                            + ("Razón negativa: la imagen queda al otro lado del centro." if k < 0 else "Razón positiva: la imagen queda del mismo lado del centro; |k| > 1 amplía, |k| < 1 reduce."))


def geo_cuadrados(rnd, nivel):
    a, b = rnd.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4)])
    s = rnd.randint(1, 3)
    L = (a + b) * s
    inner = (a * a + b * b) * s * s
    razon = Fr(a * a + b * b, (a + b) ** 2)
    enun = (f"En un cuadrado de lado {L} cm se marca en cada lado un punto que lo divide en segmentos de {a * s} cm y {b * s} cm "
            f"(en el mismo sentido en los cuatro lados) y se unen los puntos formando un cuadrado interior. ¿Cuál es el área del cuadrado interior?")
    assert L * L * razon == inner
    mal = [(f"{num(Fr(L * L, 2))} cm²", "No es siempre la mitad: eso ocurre solo con puntos medios."),
           (f"{(a * s) ** 2 + (b * s) ** 2 + 2} cm²", "Revisa Pitágoras: lado² = (a)² + (b)²."),
           (f"{L * L - 4 * a * s * b * s} cm²" if L * L - 4 * a * s * b * s != inner else f"{inner + 1} cm²", "Restaste 4 veces el producto en vez de 4 triángulos de área ab/2."),
           (f"{(a * s + b * s)} cm²", "Esa es la suma de segmentos (el lado del cuadrado grande).")]
    return dict(tema="GEO-area", subtema="areas-figuras", enunciado=enun, correcta=f"{inner} cm²", distractores=mal,
                explicacion=f"Lado del interior² = ({a * s})² + ({b * s})² = {inner} (Pitágoras en cada triángulo esquina). "
                            f"Otra vía: {L}² − 4·(½·{a * s}·{b * s}) = {L * L} − {2 * a * s * b * s} = {inner}.")


def geo_trig(rnd, nivel):
    cat1, cat2, h = rnd.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)])
    op, ad = (cat1, cat2) if rnd.random() < 0.5 else (cat2, cat1)
    assert op * op + ad * ad == h * h
    if nivel <= 1:
        f = rnd.choice(["sen", "cos", "tan"])
        val = {"sen": Fr(op, h), "cos": Fr(ad, h), "tan": Fr(op, ad)}[f]
        mal = [(num({"sen": Fr(ad, h), "cos": Fr(op, h), "tan": Fr(ad, op)}[f]), "Confundiste cateto opuesto con adyacente."),
               (num(Fr(op, ad) if f != "tan" else Fr(op, h)), "Usaste otra razón trigonométrica."),
               (num(Fr(h, op)), "Invertiste la razón (hipotenusa va en el denominador de sen/cos)."),
               (num(Fr(op + ad, h)), "Sumaste los catetos.")]
        pide = f"{f} θ"
        expl = f"sen = opuesto/hipotenusa, cos = adyacente/hipotenusa, tan = opuesto/adyacente. Aquí: {op}, {ad}, {h}."
    else:
        val = 2 * Fr(op, h) * Fr(ad, h)
        mal = [(num(2 * Fr(op, h)), "sen(2θ) = 2·senθ·cosθ: olvidaste el cos θ."), (num(Fr(op, h) * Fr(ad, h)), "Olvidaste el factor 2."),
               (num(Fr(op, h) + Fr(ad, h)), "sen(2θ) no es senθ + cosθ."), (num(2 * Fr(op, ad)), "Usaste tan θ en vez de sen θ·cos θ.")]
        pide = "sen(2θ)"
        expl = f"senθ = {op}/{h}, cosθ = {ad}/{h}. sen(2θ) = 2·senθ·cosθ = {num(val)}."
    return dict(tema="GEO-trig", subtema="general",
                enunciado=f"En un triángulo rectángulo los catetos miden {op} y {ad} (θ es el ángulo opuesto al cateto de {op}). ¿Cuánto vale {pide}?",
                correcta=num(val), distractores=mal, explicacion=expl)


# ───────────────────────── Probabilidad y estadística ─────────────────────────

def pye_desviacion(rnd, nivel):
    for _ in range(5000):
        n = rnd.choice([4, 5, 6])
        dev = [rnd.randint(-5, 5) for _ in range(n)]
        if sum(dev) != 0:
            continue
        var = Fr(sum(d * d for d in dev), n)
        if var.denominator == 1 and math.isqrt(int(var)) ** 2 == var and var >= 4:
            break
    media = rnd.randint(8, 20)
    datos = sorted(media + d for d in dev)
    sd = math.isqrt(int(var))
    muestral = math.sqrt(float(sum(d * d for d in dev)) / (n - 1))
    enun = f"¿Cuál es la desviación estándar del grupo de datos {', '.join(map(str, datos))}? (considera los datos como población)"
    mal = [(str(int(var)), "Esa es la VARIANZA; la desviación estándar es su raíz cuadrada."),
           (dec(muestral), "Dividiste por n − 1 (desviación muestral); en M2 se usa n."),
           (str(Fr(sum(abs(d) for d in dev), n).__float__()).replace(".", ",").rstrip("0").rstrip(","), "Esa es la desviación media, no la estándar."),
           (str(sd + 1), "Cálculo mal hecho: revisa las desviaciones al cuadrado.")]
    return dict(tema="PYE-dis", subtema="desviacion-varianza", enunciado=enun, correcta=str(sd), distractores=mal,
                explicacion=f"Media = {media}. Desviaciones: {dev}. Cuadrados: {[d * d for d in dev]}, suma = {sum(d * d for d in dev)}. "
                            f"Varianza = {sum(d * d for d in dev)}/{n} = {int(var)} ⇒ σ = √{int(var)} = {sd}.")


def pye_permutaciones(rnd, nivel):
    n = rnd.choice([6, 8, 10])
    k = n // 2
    tipo = rnd.choice(["par-par", "impar-par"])
    pr = Fr(k * (k - 1), n * (n - 1)) if tipo == "par-par" else Fr(k * k, n * (n - 1))
    quien = "las dos primeras bolas son pares" if tipo == "par-par" else "la primera bola es impar y la segunda es par"
    enun = f"Se ordenan al azar en una fila {n} bolas numeradas del 1 al {n}. ¿Cuál es la probabilidad de que {quien}?"
    mal = [(num(Fr(1, 4)), "Usaste 1/2·1/2: supusiste reposición; al no reponer el segundo cambia."),
           (num(Fr(k * k, n * n)), "Con reposición: (k/n)²; aquí las bolas no se devuelven."),
           (num(Fr(k * (k - 1), n * n)), "El denominador del segundo evento es n − 1, no n."),
           (num(Fr(k, n - 1) if tipo == "par-par" else Fr(k, n)), "Olvidaste multiplicar las dos probabilidades.")]
    return dict(tema="PYE-pro", subtema="conteo-y-probabilidad", enunciado=enun, correcta=num(pr), distractores=mal,
                explicacion=f"Hay {k} pares y {k} impares. Primera bola: {k}/{n}. Segunda (sin reponer): "
                            f"{k - 1 if tipo == 'par-par' else k}/{n - 1}. Se multiplican: {num(pr)}.")


def pye_condicional(rnd, nivel):
    H, M = rnd.choice([(100, 100), (60, 40), (80, 120), (50, 150)])
    pH = rnd.randint(1, H - 1)
    pM = rnd.randint(1, M - 1)
    tH, tM = H - pH, M - pM
    enun = (f"En un grupo de {H} hombres y {M} mujeres, cada persona tiene piercing o tatuajes, pero no ambos. "
            f"{pH} hombres y {pM} mujeres tienen piercing. Si se elige al azar una persona con tatuajes, ¿cuál es la probabilidad de que sea mujer?")
    corr = Fr(tM, tH + tM)
    mal = [(num(Fr(tM, M)), "Eso es P(tatuaje | mujer): condicionaste al revés."), (num(Fr(tM, H + M)), "Dividiste por el total del grupo, no por el total de personas con tatuajes."),
           (num(Fr(M, H + M)), "Esa es P(mujer), sin usar la condición."), (num(Fr(tH, tH + tM)), "Esa es P(hombre | tatuaje).")]
    return dict(tema="PYE-pro", subtema="condicional-tablas", enunciado=enun, correcta=num(corr), distractores=mal,
                explicacion=f"Con tatuajes: hombres {tH}, mujeres {tM}, total {tH + tM}. P(mujer | tatuaje) = {tM}/{tH + tM} = {num(corr)}. "
                            f"El 'universo' es lo que está después de 'dado que'.")


def pye_conteo_cargos(rnd, nivel):
    n, k = rnd.choice([(8, 3), (7, 3), (10, 3), (9, 2), (6, 3)])
    orden = rnd.random() < 0.5
    if orden:
        enun = f"De un grupo de {n} personas se elegirá una directiva con {k} cargos distintos (presidente, secretario, tesorero...). ¿De cuántas formas se puede elegir?"
        corr, otro = math.perm(n, k), math.comb(n, k)
        expl = f"Importa el orden (cargos distintos): {n}·{n - 1}·... = P({n},{k}) = {corr}."
    else:
        enun = f"De un grupo de {n} personas se elegirá un comité de {k} integrantes, todos con la misma función. ¿De cuántas formas se puede elegir?"
        corr, otro = math.comb(n, k), math.perm(n, k)
        expl = f"No importa el orden: C({n},{k}) = {corr}."
    mal = [(str(otro), "Confundiste con/sin orden: ¿los cargos son distintos o iguales?"), (str(n ** k), "Eso permite repetir personas."),
           (str(n * k), "Sumaste/multiplicaste mal: se multiplican las opciones de cada paso."), (str(math.factorial(n)), "Eso ordena a todos, no a k de ellos.")]
    return dict(tema="PYE-con", subtema="combinaciones", enunciado=enun, correcta=str(corr), distractores=mal, explicacion=expl)


def pye_conteo_numeros(rnd, nivel):
    D = sorted({0} | set(rnd.sample(range(1, 10), rnd.choice([3, 4]))))
    ultimo = [d for d in D if d in (0, 5)]
    n = len(D)
    cnt = sum(1 for a, b, c in product(D, D, D) if a != 0 and c in (0, 5))
    assert cnt == (n - 1) * n * len(ultimo)
    enun = f"¿Cuántos números de 3 cifras múltiplos de 5 se pueden formar con los dígitos {', '.join(map(str, D))} si los dígitos pueden repetirse?"
    mal = [(str(n * n * len(ultimo)), "Permitiste que la primera cifra sea 0 (entonces no tendría 3 cifras)."),
           (str((n - 1) * n * n), "Olvidaste que el último dígito debe ser 0 ó 5."),
           (str((n - 1) * (n - 1) * len(ultimo)), "Restaste dos veces: solo la primera cifra excluye al 0."),
           (str(n * (n - 1) * (n - 2)), "Eso es sin repetición y sin la condición del múltiplo de 5.")]
    return dict(tema="PYE-con", subtema="principio-multiplicativo", enunciado=enun, correcta=str(cnt), distractores=mal,
                explicacion=f"Primera cifra: {n - 1} opciones (no 0). Segunda: {n}. Tercera: debe ser 0 ó 5 → {len(ultimo)}. Total = {cnt}.")


def por_sucesivo(rnd, nivel):
    d1, d2 = rnd.sample([10, 20, 25, 30, 40, 50], 2)
    f = Fr(100 - d1, 100) * Fr(100 - d2, 100)
    enun = f"El precio de un producto se rebaja un {d1} % y luego, sobre el precio ya rebajado, otro {d2} %. ¿Por cuánto queda multiplicado el precio original?"
    mal = [(num(Fr(100 - d1 - d2, 100)), "Los % sucesivos no se suman: el segundo se aplica sobre el nuevo precio."),
           (num(Fr(d1 + d2, 100)), "Eso sería el descuento total (mal calculado), no el factor final."),
           (num(Fr(d1 * d2, 10000)), "Multiplicaste los descuentos en vez de los factores (1 − d)."),
           (num(1 - f), "Esa es la fracción que se descontó en total, no por la que queda multiplicado.")]
    return dict(tema="NUM-por", subtema="general", enunciado=enun, correcta=num(f), distractores=mal,
                explicacion=f"Factor = (1 − {d1}/100)·(1 − {d2}/100) = {num(Fr(100 - d1, 100))}·{num(Fr(100 - d2, 100))} = {num(f)}.")


GENERADORES = {
    "ALG-cua": [cua_vertice, cua_max, cua_cuadrante, cua_coef_b, cua_reflexion, cua_discriminante, cua_vieta],
    "ALG-sis": [sis_monedas, sis_sin_solucion, sis_tipo, sis_infinitas],
    "ALG-prop": [prop_inversa_gas, prop_tabla, prop_trabajo],
    "ALG-lin": [lin_porcentaje, lin_arriendo],
    "ALG-exp": [exp_duplicacion, exp_interes],
    "NUM-log": [log_aprox, log_eval, log_cambio_base],
    "ALG-expr": [expr_notables, suf_datos],
    "ALG-ecu": [ecu_inecuacion],
    "GEO-sem": [geo_razon_diagonal],
    "GEO-circ": [geo_hexagono],
    "GEO-vec": [geo_vectores],
    "GEO-iso": [geo_isometrias, geo_homotecia],
    "GEO-area": [geo_cuadrados],
    "GEO-trig": [geo_trig],
    "PYE-dis": [pye_desviacion],
    "PYE-pro": [pye_permutaciones, pye_condicional],
    "PYE-con": [pye_conteo_cargos, pye_conteo_numeros],
    "NUM-por": [por_sucesivo],
}


def ejercicio(tema, nivel=1, semilla=None, subtema=None):
    """Devuelve un ejercicio reproducible: la misma (tema, nivel, semilla) da siempre lo mismo."""
    if semilla is None:
        semilla = random.randrange(10 ** 9)
    for intento in range(60):
        rnd = random.Random(f"{tema}|{nivel}|{subtema}|{semilla}|{intento}")
        g = rnd.choice(GENERADORES[tema])(rnd, nivel)
        if subtema is not None and g["subtema"] != subtema:
            continue
        try:
            ej = armar(rnd, g)
        except FaltanDistractores:
            continue
        ej.update(nivel=nivel, semilla=semilla)
        return ej
    raise RuntimeError(f"no se pudo generar ejercicio de {tema} nivel {nivel}")
