"""Camino guiado: módulos en orden de impacto y plan de los días que quedan hasta la PAES."""
from datetime import date

FECHA_PAES_M2 = date(2026, 11, 30)   # lun 30 nov, 15:00 h (calendario DEMRE Proceso 2027: "Nov 30 15:00 Rendición PAES M2")

# id, título, temas, archivo de la guía
MODULOS = [
    ("M1", "Función cuadrática", ["ALG-cua"], "camino/01_funcion_cuadratica.md"),
    ("M2", "Sistemas 2x2 y modelamiento (lineal y %)", ["ALG-sis", "ALG-lin"], "camino/02_sistemas_y_modelamiento.md"),
    ("M3", "Proporcionalidad directa e inversa", ["ALG-prop"], "camino/03_proporcionalidad.md"),
    ("M4", "Exponencial y logaritmos", ["ALG-exp", "NUM-log"], "camino/04_exponencial_y_logaritmos.md"),
    ("M5", "Probabilidad y conteo", ["PYE-pro", "PYE-con", "PYE-var"], "camino/05_probabilidad_y_conteo.md"),
    ("M6", "Estadística: posición y dispersión", ["PYE-dis"], "camino/06_estadistica.md"),
    ("M7", "Geometría: semejanza, áreas y circunferencia", ["GEO-sem", "GEO-area", "GEO-circ"], "camino/07_geometria_plana_y_cuerpos.md"),
    ("M8", "Vectores, isometrías y trigonometría", ["GEO-vec", "GEO-iso", "GEO-trig", "GEO-coor"], "camino/08_vectores_isometrias_trigonometria.md"),
    ("M9", "Suficiencia de datos", ["ALG-expr"], "camino/09_suficiencia_de_datos.md"),
    ("M10", "Mantener la base: números y álgebra", ["NUM-real", "NUM-por", "NUM-pot", "ALG-ecu", "ALG-func"], "camino/10_mantener_la_base.md"),
]

# Plan día a día (mismo esqueleto que tu REGISTRO DIARIO, con los módulos del sistema).
PLAN = {
    "2026-11-21": ("ENSAYO COMPLETO cronometrado (2 h 20 min) + análisis",
                   "Haz la prueba I2027 completa (abre pruebas/pdf/2027-26-06-15-...pdf, sin calculadora) y luego: "
                   "python3 paes.py ensayo I2027 <tus 55 respuestas>. El sistema recalcula tus prioridades.", ["M1"]),
    "2026-11-22": ("Probabilidad, conteo y dispersión", "Módulos M5 y M6. Primero los repasos pendientes.", ["M5", "M6"]),
    "2026-11-23": ("Geometría: hexágono/áreas, vectores, rotación", "Módulos M7 y M8.", ["M7", "M8"]),
    "2026-11-24": ("Tras el ensayo I2027: probabilidades (M5)", "Vuelve a ver los errores que marcaste «no entendí»: P47, P48, P46, P51. Practica PYE-pro.", ["M5"]),
    "2026-11-25": ("Homotecia, porcentajes con tablas y proporcionalidad (+3 d)", "Módulos M8, M2 y M3: P34, P35, P4, P8, P16, P21, P23.", ["M8", "M2", "M3"]),
    "2026-11-26": ("Dispersión con datos parciales + lo que queda (+7 d)", "Módulo M6: P42, P55; círculos concéntricos P37; restos P1.", ["M6"]),
    "2026-11-27": ("Mini-ensayo M2 de 25 preguntas (ver tu REGISTRO) + ciencias", "Elige una prueba aún sin usar (R2024 o I2024) y haz las 25 primeras en 65 min.", ["M10"]),
    "2026-11-28": ("Repaso final de errores + puntos débiles", "Solo repasos pendientes y tus 2 temas más débiles ahora: probabilidades y homotecia (python3 paes.py estado).", []),
    "2026-11-29": ("DESCANSO ACTIVO", "Repaso liviano de tus fórmulas (docs/hoja_de_formulas.md). Dormir temprano.", []),
    "2026-11-30": ("DÍA PAES M2 (15:00 h)", "Mañana: solo repaso liviano de fórmulas. Estrategia en docs/estrategia_de_prueba.md.", []),
}


def modulo_de_tema(tema):
    for m in MODULOS:
        if tema in m[2]:
            return m
    return None
