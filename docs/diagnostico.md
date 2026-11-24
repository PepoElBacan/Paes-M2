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


---

# Segundo ensayo: I2027 (24 nov)

**Resultado:** 35 correctas de 49 puntuables ⇒ **687 puntos PAES** (antes: 31 correctas ⇒ 640; **+47 pts**, +4 preguntas).

## Comparación por tema (ensayo 1 → ensayo 2)

| Tema | I2026 | I2027 | Cambio |
|---|---|---|---|
| ALG-cua Función y ecuación cuadrática | 0/4 | 3/3 | mejora |
| PYE-dis Estadística descriptiva y dispersión | 2/3 | 3/5 | igual |
| PYE-pro Probabilidades | 2/4 | 0/2 | empeora |
| ALG-prop Proporcionalidad directa e inversa | 3/5 | 2/4 | igual |
| NUM-pot Potencias, raíces y notación científica | 3/3 | 2/2 | igual |
| GEO-area Áreas, perímetros y volúmenes | – | 2/2 | sin dato |
| NUM-real Números reales, intervalos y aproximación | 2/2 | 1/2 | empeora |
| ALG-exp Función exponencial e interés compuesto | 1/2 | 2/2 | mejora |
| ALG-lin Función lineal/afín y modelamiento | 1/2 | 2/2 | mejora |
| NUM-por Porcentajes y variaciones porcentuales | 4/4 | 3/5 | empeora |
| GEO-iso Isometrías y homotecia | 2/3 | 0/1 | empeora |
| NUM-log Logaritmos | 2/3 | 1/1 | mejora |
| ALG-ecu Ecuaciones e inecuaciones | 3/3 | – | sin dato |
| ALG-func Otras funciones (potencia, raíz, tramos, trigonométricas) | 2/2 | 5/5 | igual |
| ALG-sis Sistemas de ecuaciones 2x2 | 0/1 | 2/3 | mejora |
| GEO-sem Semejanza, Thales y Pitágoras | 2/3 | – | sin dato |
| ALG-expr Expresiones algebraicas y productos notables | 1/2 | 1/1 | mejora |
| PYE-con Técnicas de conteo | – | 2/2 | sin dato |
| GEO-vec Vectores en el plano | 0/1 | 1/1 | mejora |
| GEO-trig Trigonometría | 1/1 | 2/2 | igual |
| PYE-var Variable aleatoria, binomial y normal | – | 0/2 | sin dato |
| GEO-circ Circunferencia y polígonos regulares | 0/1 | 1/2 | mejora |

## Errores del ensayo (ya están en tu banco de errores)

| P | Marcaste | Clave | Tema | Qué era | ¿Lo entendí? |
|---|---|---|---|---|---|
| P1 | B | C | NUM-real | Enteros con restos 2 mod 5 y 4 mod 7 | sí |
| P4 | B | D | NUM-por | Turistas extranjeros: variación porcentual | sí |
| P8 | C | B | NUM-por | Tabla de emisiones MP10: variaciones | no |
| P15 (piloto) | D | B | ALG-exp | Dos opciones de depósito con interés compuesto | no |
| P16 | C | D | ALG-prop | Densidad y flotación | no |
| P21 | B | A | ALG-prop | Vacaciones proporcionales | sí |
| P23 | A | C | ALG-sis | Queso y crema con litros de leche | no |
| P29 (piloto) | B | D | ALG-cua | Parábola tangente al eje X: rotación y traslación | no |
| P34 (piloto) | D | C | GEO-iso | Homotecia de triángulo con coordenadas | no |
| P35 | C | A | GEO-iso | Homotecia H entre triángulos ABC y A'B'C' | no |
| P37 | C | B | GEO-circ | Siete círculos concéntricos: suma de áreas | no |
| P42 | A | B | PYE-dis | Frecuencia acumulada: medidas | sí |
| P46 | A | B | PYE-var | Estudio de gimnasios: muestreo/inferencia | no |
| P47 | B | C | PYE-pro | Probabilidad geométrica con dardo | no |
| P48 | B | D | PYE-pro | Probabilidad total: lluvia y atraso | no |
| P51 | A | C | PYE-var | Extracción de ADN: éxito del proceso | no |
| P53 (piloto) | A | D | GEO-sem | Suficiencia de datos: altura/semejanza | no |
| P55 | C | B | PYE-dis | Masas de 83 personas: datos parciales | no |

## Qué muestra este ensayo

1. **La cuadrática ya no es el problema:** pasó de 0/4 a 3/3. El trabajo de refuerzo funcionó.
2. **Probabilidades y variable aleatoria** (PYE-pro, PYE-var): 0/4 en conjunto (probabilidad geométrica, probabilidad total, muestreo/inferencia, éxito de un proceso). Es la mayor pérdida ahora.
3. **Homotecia** (GEO-iso): fallaste P35 y también el piloto P34, las dos sobre homotecia entre triángulos. No es un tema nuevo para ti: ya tenías errores de isometrías en el ensayo anterior (rotación, vectores).
4. **Porcentajes y proporcionalidad en contexto** (P4, P8, P16, P21): cuatro errores en problemas con tablas o situaciones reales; de ellos entendiste P4 y P21 y no P8 y P16.
5. **No entendiste 14 de 18 errores** (P8, P15, P16, P23, P29, P34, P35, P37, P46, P47, P48, P51, P53, P55): son los que más conviene volver a ver con una explicación, no solo repetir.
6. **4 de tus 18 errores fueron en preguntas piloto**: no cuentan para el puntaje.
7. Cada pregunta extra vale unos 13–15 puntos en este tramo: 40 correctas ⇒ 757 pts (+5 que hoy) y 42 ⇒ 785 pts. Probabilidades (4 errores), homotecia y porcentajes con tablas son justo esas preguntas.
