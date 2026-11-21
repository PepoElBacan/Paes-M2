"""Taxonomía de la PAES M2: temas, subtemas y prerrequisitos.

Cada pregunta oficial del banco tiene un `tema` (código) asignado a mano, y un `subtema`
que se deduce con las expresiones regulares de abajo a partir de la descripción.
"""
import re

# código -> (nombre, eje, prerrequisitos)
TEMAS = {
    "NUM-real": ("Números reales, intervalos y aproximación", "Números", []),
    "NUM-por": ("Porcentajes y variaciones porcentuales", "Números", []),
    "NUM-pot": ("Potencias, raíces y notación científica", "Números", []),
    "NUM-log": ("Logaritmos", "Números", ["NUM-pot"]),
    "ALG-expr": ("Expresiones algebraicas y productos notables", "Álgebra y funciones", []),
    "ALG-ecu": ("Ecuaciones e inecuaciones", "Álgebra y funciones", ["ALG-expr"]),
    "ALG-sis": ("Sistemas de ecuaciones 2x2", "Álgebra y funciones", ["ALG-ecu"]),
    "ALG-lin": ("Función lineal/afín y modelamiento", "Álgebra y funciones", ["ALG-ecu", "NUM-por"]),
    "ALG-prop": ("Proporcionalidad directa e inversa", "Álgebra y funciones", ["ALG-lin"]),
    "ALG-cua": ("Función y ecuación cuadrática", "Álgebra y funciones", ["ALG-expr", "ALG-lin"]),
    "ALG-exp": ("Función exponencial e interés compuesto", "Álgebra y funciones", ["NUM-pot", "NUM-por"]),
    "ALG-func": ("Otras funciones (potencia, raíz, tramos, trigonométricas)", "Álgebra y funciones", ["ALG-lin"]),
    "GEO-sem": ("Semejanza, Thales y Pitágoras", "Geometría", []),
    "GEO-area": ("Áreas, perímetros y volúmenes", "Geometría", ["GEO-sem"]),
    "GEO-circ": ("Circunferencia y polígonos regulares", "Geometría", ["GEO-sem"]),
    "GEO-trig": ("Trigonometría", "Geometría", ["GEO-sem"]),
    "GEO-vec": ("Vectores en el plano", "Geometría", []),
    "GEO-iso": ("Isometrías y homotecia", "Geometría", ["GEO-vec", "GEO-sem"]),
    "GEO-coor": ("Geometría analítica (coordenadas)", "Geometría", ["ALG-lin"]),
    "PYE-dis": ("Estadística descriptiva y dispersión", "Probabilidad y estadística", []),
    "PYE-con": ("Técnicas de conteo", "Probabilidad y estadística", []),
    "PYE-pro": ("Probabilidades", "Probabilidad y estadística", ["PYE-con"]),
    "PYE-var": ("Variable aleatoria, binomial y normal", "Probabilidad y estadística", ["PYE-pro"]),
}

# tema -> [(subtema, regex sobre la descripción en minúsculas)]; el primero que calce gana
SUBTEMAS = {
    "ALG-cua": [
        ("reflexion-transformacion", r"reflexi|trasladada|transformar|desplaz|rotaci|tangente|variaci[oó]n de uno"),
        ("discriminante-vieta", r"discriminante|[uú]nica soluci|vieta|raíces|producto de|suma de inversos|suma de"),
        ("grafico-coeficientes", r"gráfic|coeficiente|signos|tabla|propiedades|afirmaciones"),
        ("vertice-maximo", r"vértice|máxim|altura|cohete|pelota|temperatura|volumen|cultivo|pozo|origen|completar"),
        ("modelar-ecuacion", r"plantear|área|margen|isósceles|cuadro|suficiencia"),
    ],
    "ALG-prop": [
        ("inversa", r"inversa|gas|presi[oó]n|calamar|rapidez|tramos|ondas|sísmic|carnot|llaves|tabla"),
        ("directa-razones", r"densidad|rendimiento|regla|reparto|proporcional|máquina|herencia|vacaciones|sacarosa|pintura"),
    ],
    "PYE-pro": [
        ("condicional-tablas", r"condicional|tabla|sin reposici[oó]n|helado|hombres|total"),
        ("conteo-y-probabilidad", r"permutaci|par-par|lotería|secuencia|cartas|bolit|urna|caja|fichas|rifa|naipe"),
        ("independencia-otros", r"independiente|dardo|encuesta|robot|dos personas"),
    ],
    "NUM-log": [
        ("propiedades-evaluar", r"propiedades|evaluar|log de|tabla de log|aproximar|base|condici[oó]n"),
        ("modelos-con-log", r"decibel|intensidad|dB|esperanza"),
    ],
    "ALG-exp": [
        ("crecimiento-bacterias", r"bacteri|cultivo|duplic|tripl|cuadrupl|hongo|medicamento|luz|caverna|sierpinski"),
        ("interes-compuesto", r"inter[eé]s|ahorro|depósito|renovable|capital|presupuesto|estampillas|exponencial|gráfica"),
    ],
    "ALG-sis": [
        ("sin-o-infinitas", r"sin soluci|infinitas|[uú]nica|parámetro|condiciones"),
        ("plantear", r"monedas|plantear|adultos|cine|prendas|queso|puntos|suficiencia|precio|leche"),
    ],
    "ALG-lin": [
        ("porcentaje-precio", r"porcentaje|ganancia|precio|oferta|demanda"),
        ("modelo-recta", r"recta|gráfic|nivel|función|arriendo|costo|escala|temperatura|peso|intersecci"),
    ],
    "GEO-circ": [("hexagono", r"hex[aá]gono"), ("circulos", r"c[ií]rculo|circunferencia|cuerda|vueltas|inscrito")],
    "GEO-sem": [
        ("pitagoras-razones", r"pit[aá]goras|diagonal|escalera|razón|barcos|pulgadas|altura"),
        ("thales-semejanza", r"thales|semejan|homotecia|proyector|diámetro|lente"),
    ],
    "GEO-iso": [
        ("homotecia", r"homotecia"),
        ("rotacion-reflexion-traslacion", r"rotaci|reflexi|traslaci|planeta"),
    ],
    "GEO-area": [
        ("volumen-cuerpos", r"volumen|cilindr|prisma|esfera|cubo|paralelep"),
        ("areas-figuras", r"[aá]rea|cuadrad|rect[aá]ngulo|tri[aá]ngulo|elipse|logo|superficie|cuadril"),
    ],
    "PYE-dis": [
        ("desviacion-varianza", r"desviaci[oó]n|varianza|dispersi[oó]n|coeficiente de variaci"),
        ("cajon-posicion", r"caj[oó]n|cuartil|percentil|posici[oó]n|atípic|tramos|mediana"),
        ("tablas-promedios", r"tabla|promedio|histograma|frecuencia|encuesta|gráfico|dato"),
    ],
    "PYE-con": [("combinaciones", r"combinaci|grupos|comit[eé]|partidos|apret|trazos"), ("principio-multiplicativo", r".")],
}


def subtema(tema: str, descripcion: str) -> str:
    d = descripcion.lower()
    for sub, rx in SUBTEMAS.get(tema, []):
        if re.search(rx, d):
            return sub
    return "general"


def nombre(tema: str) -> str:
    return TEMAS[tema][0] if tema in TEMAS else tema
