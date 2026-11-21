# M1 · Función cuadrática  🔴 prioridad máxima

**Por qué va primero:** es el tema más frecuente de la PAES M2 — 33 de 349 preguntas oficiales analizadas (≈ 9,5 %, unas 5 de las 50 puntuables) — y en tu ensayo I2026 fue donde más puntos perdiste: **0 de 4 puntuables** (P28, P29, P30, P31) más el piloto P27.
Tu propio diario del 18-nov lo dice: *"mis errores son de signos y etiquetas, no de concepto"*. Eso es buena noticia: se arregla con método, no con más teoría.

## Lo esencial (todo lo que cae)

| Idea | Fórmula / regla |
|---|---|
| Forma general | f(x) = ax² + bx + c. Corta al eje Y en **c**. |
| Abre hacia… | a > 0 arriba (el vértice es un **mínimo**) · a < 0 abajo (**máximo**) |
| Vértice | **xᵥ = −b/(2a)** · yᵥ = f(xᵥ) · eje de simetría x = xᵥ |
| Raíces (cortes con X) | x = (−b ± √Δ)/(2a), con **Δ = b² − 4ac** |
| Discriminante | Δ > 0 dos raíces · Δ = 0 **una** (el vértice toca el eje X) · Δ < 0 ninguna real |
| Vieta | x₁ + x₂ = **−b/a** · x₁·x₂ = **c/a** · 1/x₁ + 1/x₂ = (x₁+x₂)/(x₁x₂) |
| Forma factorizada | f(x) = a(x − x₁)(x − x₂) → xᵥ = (x₁+x₂)/2 |
| Forma canónica | f(x) = a(x − h)² + k → vértice (h, k) |
| Transformaciones | −f(x): refleja en el eje X · f(−x): refleja en el eje Y · f(x − h) + k: traslada h a la derecha y k arriba |

## Método de 4 pasos para preguntas de gráfico o de signos de coeficientes
1. **a**: ¿abre arriba o abajo? → signo de a.
2. **c**: ¿dónde corta al eje Y? → signo de c.
3. **b**: de xᵥ = −b/(2a) sale **b = −2a·xᵥ**. Vértice a la *izquierda* del eje Y (xᵥ < 0) ⇒ a y b tienen el **mismo** signo; a la *derecha* (xᵥ > 0) ⇒ signos **distintos**.
4. **Δ**: ¿cuántos cortes con X? → signo de Δ.

## Tus 4 errores → 4 reglas
| Pregunta | Qué pasó | Regla |
|---|---|---|
| P28 · b desde el gráfico | no sacaste b de xᵥ | Usa xᵥ = −b/(2a) y **cuida el signo**: si xᵥ > 0 y a > 0 ⇒ b < 0 |
| P29 · coordenada **y** del vértice | probable confusión x/y | Primero calcula xᵥ, **después evalúas** f(xᵥ). "Altura máxima" = yᵥ; "¿en qué instante?" = xᵥ |
| P30 · altura máxima (cohete) | mismo tema | Subraya lo que pide: ¿tiempo o altura? Verifica que a < 0 |
| P31 · cuadrante del vértice | razonaste bien, fallaste la etiqueta | **Escribe (x, y) con sus signos** y recién entonces di el cuadrante: (+,−) = IV |
| P27 (piloto) · reflexión | — | Reflexión en X: **−f(x)** (cambia el signo de *todo* el polinomio). En Y: f(−x) |

## Trampas típicas de la PAES
- Piden "la ordenada del vértice" y respondes la abscisa (o al revés).
- "Una única solución" ⇒ Δ = 0 ⇒ suele haber **dos** valores del parámetro (±). Olvidar el negativo es un clásico (I2024 P26).
- Las transformaciones se aplican a la *función*, no solo a un punto.
- Tablas de valores (I2024 P25, I2027 P31): usa 3 puntos para plantear f(x) = ax² + bx + c, o aprovecha la simetría.

## Niveles (se sube con 4 aciertos de los últimos 5)
- **Nivel 1 · base:** vértice (x), ejes, cuadrantes sencillos.
- **Nivel 2 · tipo PAES:** modelos con altura/tiempo, coeficiente b desde las raíces, cuadrante del vértice, reflexiones.
- **Nivel 3 · experto:** discriminante con parámetro, Vieta (suma de inversos), tablas, composiciones de transformaciones.

## Práctica
```bash
python3 paes.py practicar ALG-cua -n 8            # interactivo
python3 paes.py hoja ALG-cua -n 10 --nivel 2      # para resolver en papel, sin calculadora
python3 paes.py gemelas I2026-31                  # preguntas oficiales parecidas a la que fallaste
```

## Preguntas oficiales de este módulo (de la más reciente a la más antigua)
<!-- GEMELAS ALG-cua -->
| Pregunta | pág. PDF | clave | de qué trata | subtema |
|---|---|---|---|---|
| I2027 P29 | 26 | D | Parábola tangente al eje X: rotación y traslación *(piloto)* | reflexion-transformacion |
| I2027 P30 | 27 | D | Parábola con vértice en el origen | vertice-maximo |
| I2027 P31 | 27 | D | Tablas de dos cuadráticas: parámetros h y k | grafico-coeficientes |
| I2027 P32 | 28 | B | Altura de una pelota lanzada | vertice-maximo |
| R2026 P27 | 19 | B | Gráfica de f(x)=ax²+bx+c: signos de coeficientes | grafico-coeficientes |
| I2026 P27 | 21 | B | Reflexión de una parábola respecto al eje X *(piloto)* | reflexion-transformacion |
| I2026 P28 | 22 | A | Coeficiente b desde el gráfico | grafico-coeficientes |
| I2026 P29 | 23 | C | Coordenada y del vértice | vertice-maximo |
| I2026 P30 | 24 | A | Altura máxima de un cohete | vertice-maximo |
| I2026 P31 | 24 | D | Cuadrante del vértice según sus raíces | discriminante-vieta |
| R2025 P26 | 13 | D | Transformar f(x)=x²-4x+5 (desplazamientos) | reflexion-transformacion |
| R2025 P27 | 14 | D | Cuadro con margen uniforme: ecuación cuadrática | modelar-ecuacion |
| R2025 P28 | 15 | A | Afirmaciones sobre f(x)=ax²+bx+c | grafico-coeficientes |
| R2025 P30 | 15 | D | Propiedades del vértice y la gráfica | grafico-coeficientes |
| R2025 P53 | 31 | C | Suficiencia de datos: f(13)=p, f(14)=q | modelar-ecuacion |
| I2025 P16 | 14 | A | Completar el cuadrado: hallar b | vertice-maximo |
| I2025 P29 | 25 | C | Leer coeficientes desde gráfica cuadrática | grafico-coeficientes |
| I2025 P30 | 26 | C | Discriminante: intervalo de valores de b | discriminante-vieta |
| I2025 P31 | 26 | C | Volumen de un pozo modelado con parábola | vertice-maximo |
| I2025 P52 | 44 | C | Suficiencia de datos: coeficientes de cuadrática | grafico-coeficientes |
| R2024 P30 | 26 | A | Suma de inversos con raíces de 5x²-x-5=0 | discriminante-vieta |
| R2024 P32 | 27 | D | Triángulo isósceles: plantear ecuación cuadrática | modelar-ecuacion |
| R2024 P33 | 28 | B | Parábola trasladada: vértice | reflexion-transformacion |
| R2024 P52 | 44 | C | Suficiencia de datos: f(x)=ax²+3x+c | modelar-ecuacion |
| I2024 P23 | 20 | D | Plantear ecuación cuadrática: área del triángulo | modelar-ecuacion |
| I2024 P24 | 20 | C | Cultivo modelado con parábola *(piloto)* | vertice-maximo |
| I2024 P25 | 21 | A | Función cuadrática desde tabla de puntos | grafico-coeficientes |
| I2024 P26 | 21 | A | Discriminante cero: única solución | discriminante-vieta |
| I2024 P27 | 22 | B | Relaciones de Vieta (suma y producto de raíces) | discriminante-vieta |
| I2024 P28 | 22 | D | Temperatura máxima con parábola | vertice-maximo |
| I2024 P29 | 23 | D | Producto de raíces igual a un valor | discriminante-vieta |
| I2024 P30 | 23 | B | Parábola con f(p)=0, relación entre coeficientes | grafico-coeficientes |
| I2024 P31 | 24 | B | Recorrido de f(x)=bx²-4 | general |
<!-- /GEMELAS -->

## ✅ Criterio de dominio
Nivel 3 en ALG-cua **y** al menos 8 de las 10 gemelas oficiales más recientes correctas, sin mirar la solución.
