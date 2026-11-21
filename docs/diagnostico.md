# Diagnóstico de tu desempeño (ensayo I2026 + banco de errores)

**Resultado:** 31 correctas de 49 puntuables ⇒ **640 puntos PAES** (tabla oficial de esa prueba).

## ¿Cuánto vale cada pregunta extra?

| Correctas | Puntaje PAES |
|---|---|
| 31 | 640 |
| 34 | 676 |
| 36 | 701 |
| 39 | 747 |
| 41 | 776 |
| 40 | 762 |
| 45 | 850 |

Arreglar solo la **función cuadrática** (0/4 ⇒ 4/4) llevaría de 31 a 35 correctas (**+47 pts**).

## Por tema (solo preguntas puntuables)

| Tema | Tu resultado | % acierto | Peso en la PAES* | Preguntas que se pierden por prueba** |
|---|---|---|---|---|
| ALG-cua Función y ecuación cuadrática | 0/4 | 0 % | 9.6 % (30 preg.) | 4.0 |
| PYE-pro Probabilidades | 2/4 | 50 % | 6.7 % (21 preg.) | 1.7 |
| PYE-dis Estadística descriptiva y dispersión | 2/3 | 66 % | 7.3 % (23 preg.) | 1.5 |
| ALG-lin Función lineal/afín y modelamiento | 1/2 | 50 % | 5.1 % (16 preg.) | 1.3 |
| ALG-exp Función exponencial e interés compuesto | 1/2 | 50 % | 5.1 % (16 preg.) | 1.3 |
| ALG-sis Sistemas de ecuaciones 2x2 | 0/1 | 0 % | 3.8 % (12 preg.) | 1.3 |
| ALG-prop Proporcionalidad directa e inversa | 3/5 | 60 % | 5.7 % (18 preg.) | 1.2 |
| NUM-log Logaritmos | 2/3 | 66 % | 4.8 % (15 preg.) | 1.0 |
| GEO-iso Isometrías y homotecia | 2/3 | 66 % | 4.8 % (15 preg.) | 1.0 |
| ALG-expr Expresiones algebraicas y productos notables | 1/2 | 50 % | 3.5 % (11 preg.) | 0.9 |
| GEO-vec Vectores en el plano | 0/1 | 0 % | 2.5 % (8 preg.) | 0.8 |
| GEO-sem Semejanza, Thales y Pitágoras | 2/3 | 66 % | 3.5 % (11 preg.) | 0.7 |
| NUM-real Números reales, intervalos y aproximación | 2/2 | 100 % | 5.4 % (17 preg.) | 0.7 |
| NUM-pot Potencias, raíces y notación científica | 3/3 | 100 % | 5.7 % (18 preg.) | 0.6 |
| ALG-func Otras funciones (potencia, raíz, tramos, trigonométricas) | 2/2 | 100 % | 4.1 % (13 preg.) | 0.5 |
| GEO-circ Circunferencia y polígonos regulares | 0/1 | 0 % | 1.3 % (4 preg.) | 0.4 |
| ALG-ecu Ecuaciones e inecuaciones | 3/3 | 100 % | 4.1 % (13 preg.) | 0.4 |
| NUM-por Porcentajes y variaciones porcentuales | 4/4 | 100 % | 4.8 % (15 preg.) | 0.4 |
| GEO-trig Trigonometría | 1/1 | 100 % | 1.6 % (5 preg.) | 0.3 |

\* Peso = fracción de las preguntas puntuables de las 7 pruebas analizadas (349 preguntas etiquetadas).
\** Estimación = 50 × peso × tasa de error suavizada ((errores+1)/(n+2)). Es la métrica con la que el sistema ordena tus prioridades.

## Patrones que se ven en tus errores

1. **Signos y etiquetas, no conceptos** (cuadrantes, "respondí otra cosa"): P31 y P25. Se corrige con reglas de verificación (ver `docs/estrategia_de_prueba.md`).
2. **Cuadrática (P28–P31 y piloto P27)**: es el tema con más peso en la PAES y el de mayor pérdida; el módulo M1 es la prioridad nº 1.
3. **"No supe resolverla"** en 10 preguntas (P10, 16, 17, 27–31, 46, 48, 50): hay brechas de método en logaritmos, proporcionalidad inversa, desviación estándar y permutaciones.
4. **Dos aciertos "sin método"** (P42, P52): aprovéchalos como repaso igual; en el día de la prueba no se puede depender del azar.
5. Los 5 **pilotos no puntúan** (P27, 34, 50, 54, 55 en tu prueba): errores en pilotos no cuestan puntos — no te angusties por ellos.
6. Te sobraron **23 min 21 s**: úsalos de forma sistemática para revisar signos/etiquetas en el último tercio de la prueba.
