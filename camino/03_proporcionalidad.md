# M3 · Proporcionalidad directa e inversa  🟠

**Tus datos:** 3/5 en tu ensayo; fallaste **P17** (gráfico de inversa y directa) y **P18** (gas: variación absoluta del volumen). Es un tema de peso alto en la PAES M2 (21 preguntas oficiales, ≈ 6 % de las puntuables), con muchos contextos de física.

## Lo esencial
| | Directa | Inversa |
|---|---|---|
| Relación | y = kx (**y/x constante**) | y = k/x (**x·y constante**) |
| Gráfico | recta que pasa por el origen | hipérbola (curva que nunca toca los ejes) |
| Si x se duplica | y se duplica | y se reduce a la mitad |
| Ejemplos | precio–cantidad, distancia–tiempo (v const.) | presión–volumen, velocidad–tiempo, nº de llaves–tiempo |

- **Trabajo/caudales:** suma *tasas* (1/tiempo): 1/a + 1/b − 1/c (el desagüe resta).
- **Variación absoluta** = |final − inicial|. **Variación porcentual** = (final − inicial)/inicial.
- Fórmulas con potencias (q = ½ρV², g = GM/R²): si V se duplica, q se **cuadruplica**; si R se duplica, g se divide por 4.

## Método
1. ¿Qué producto o cociente es constante? Escríbelo (P₁V₁ = P₂V₂).
2. Despeja **el dato que falta**, no lo que te piden por inercia.
3. Relee la pregunta: ¿valor final o variación? ¿unidades?

## Tus errores → reglas
- **P17:** en un gráfico mixto, identifica primero cuál curva es la recta por el origen (directa) y cuál la hipérbola (inversa) y recién ahí lee los puntos.
- **P18:** V₂ = P₁V₁/P₂ y **luego** resta |V₂ − V₁|.

## Práctica
```bash
python3 paes.py practicar ALG-prop -n 8
python3 paes.py hoja ALG-prop -n 8 --nivel 2
```

## Preguntas oficiales
<!-- GEMELAS ALG-prop -->
| Pregunta | pág. PDF | clave | de qué trata | subtema |
|---|---|---|---|---|
| I2027 P2 | 5 | D | Reparto equitativo entre 13 asistentes | directa-razones |
| I2027 P16 | 14 | D | Densidad y flotación | directa-razones |
| I2027 P20 | 17 | C | Tres llaves llenando un estanque (trabajo) | inversa |
| I2027 P21 | 18 | A | Vacaciones proporcionales | directa-razones |
| R2026 P1 | 5 | D | Máquina de acero: kg por pieza | directa-razones |
| R2026 P17 | 13 | A | Densidad del hierro en dos estados | directa-razones |
| R2026 P18 | 14 | D | Calamar: rapidez inversa a la masa | inversa |
| R2026 P20 | 15 | A | Ciclo de Carnot: razones de calor | inversa |
| R2026 P21 | 16 | C | Ondas sísmicas S y P: distancia al epicentro | inversa |
| I2026 P2 | 4 | D | Rendimiento de pintura y capas (regla de tres) | directa-razones |
| I2026 P17 | 14 | B | Gráfico de proporcionalidad inversa y directa | inversa |
| I2026 P18 | 15 | D | Gas: volumen y presión inversamente proporcionales | inversa |
| I2026 P19 | 16 | C | Densidad ρ=m/V | directa-razones |
| I2026 P24 | 19 | D | Rapidez media en dos tramos iguales | inversa |
| R2025 P14 | 9 | D | Herencia repartida en pagos mensuales iguales *(piloto)* | directa-razones |
| I2025 P18 | 15 | B | Distancia, tiempo y rapidez por tramos | inversa |
| I2025 P27 | 23 | D | Densidad = masa/volumen *(piloto)* | directa-razones |
| R2024 P20 | 17 | A | Reconocer tabla inversamente proporcional | inversa |
| R2024 P21 | 18 | C | Proporciones en compuesto (sacarosa) | directa-razones |
| R2024 P24 | 21 | A | Rapidez de computadores (razón) | inversa |
| I2024 P15 | 14 | B | Relación de proporcionalidad en el ojo humano *(piloto)* | directa-razones |
<!-- /GEMELAS -->

## ✅ Criterio de dominio
Nivel 3 y poder explicar en una línea por qué una tabla/gráfico es directo o inverso.
