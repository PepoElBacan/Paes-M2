# M8 · Vectores, isometrías, homotecia y trigonometría  🟡

**Tus datos:** fallaste **P37** (operaciones con vectores en gráfico) y **P41** (rotación de un cuadrado + razones trigonométricas); acertaste **P42** (refracción, sen 2θ) *sin método* → repásala.

## Lo esencial
**Vectores** (a, b): suma/resta coordenada a coordenada · k·(a, b) = (ka, kb) · módulo √(a² + b²).
Leer un gráfico: coordenadas = (x final − x inicial, y final − y inicial).

**Transformaciones del plano**
| | (x, y) → |
|---|---|
| Traslación por (p, q) | (x + p, y + q) |
| Reflexión en eje X / eje Y / origen | (x, −y) / (−x, y) / (−x, −y) |
| Rotación 90° antihoraria / horaria (centro origen) | (−y, x) / (y, −x) |
| **Homotecia** centro C, razón k | **P′ = C + k·(P − C)** · k < 0 invierte al otro lado del centro · áreas × k² |

Las isometrías (traslación, reflexión, rotación) conservan lados y ángulos; la homotecia conserva ángulos y cambia lados por |k|.

**Trigonometría**
- sen = opuesto/hipotenusa · cos = adyacente/hipotenusa · tan = opuesto/adyacente · sen²θ + cos²θ = 1.
- **sen 2θ = 2·sen θ·cos θ** · cos 2θ = cos²θ − sen²θ.
- Ángulos notables: sen 30° = ½, sen 45° = √2/2, sen 60° = √3/2 (cos al revés).
- Desfase: sen(x + π) = −sen x.

## Método
1. Ordena: escribe cada transformación como una fila de la tabla y aplícalas **en el orden del enunciado**.
2. En rotaciones de figuras, rota **un vértice** y deduce el resto.
3. Trigonometría: dibuja el triángulo rectángulo y rotula opuesto/adyacente respecto al ángulo pedido.

## Tus errores → reglas
- **P37:** lee las coordenadas de cada vector con la cuadrícula y opera: v − u + 2w ⇒ cada coordenada por separado.
- **P41:** rotar el cuadrado ⇒ calcula las nuevas coordenadas de un vértice y arma el triángulo rectángulo para sen/cos.

## Práctica
```bash
python3 paes.py practicar GEO-vec -n 5
python3 paes.py practicar GEO-iso -n 6
python3 paes.py practicar GEO-trig -n 5
```

## Preguntas oficiales
<!-- GEMELAS GEO-vec,GEO-iso,GEO-trig,GEO-coor -->

**GEO-vec — Vectores en el plano** (8 preguntas)

| Pregunta | pág. PDF | clave | de qué trata | subtema |
|---|---|---|---|---|
| I2027 P39 | 34 | B | Magnitud de suma de vectores v_n | general |
| R2026 P37 | 24 | A | Hallar un vector con condición u-2v=(9,0) | general |
| I2026 P37 | 30 | D | Operaciones con vectores en gráfico | general |
| I2025 P36 | 31 | D | Rotación de un vector en 60° | general |
| R2024 P38 | 32 | E | Vector en 2º cuadrante: signos de coordenadas | general |
| R2024 P40 | 34 | C | Nutria cruzando río: suma de vectores | general |
| R2024 P41 | 35 | D | Suma de vectores y cuadrante de w | general |
| I2024 P40 | 32 | E | Combinación de vectores u y v | general |

**GEO-iso — Isometrías y homotecia** (17 preguntas)

| Pregunta | pág. PDF | clave | de qué trata | subtema |
|---|---|---|---|---|
| I2027 P34 | 30 | C | Homotecia de triángulo con coordenadas *(piloto)* | homotecia |
| I2027 P35 | 31 | A | Homotecia H entre triángulos ABC y A'B'C' | homotecia |
| I2027 P40 | 34 | — | Traslación y reflexión de un círculo *(eliminada)* | rotacion-reflexion-traslacion |
| R2026 P38 | 25 | A | Reflexión respecto al eje Y + traslación | rotacion-reflexion-traslacion |
| I2026 P38 | 31 | B | Planeta y luna: traslación/rotación | rotacion-reflexion-traslacion |
| I2026 P39 | 32 | A | Homotecia de razón negativa con centro en origen | homotecia |
| I2026 P41 | 34 | D | Rotación de un cuadrado + razones trigonométricas | rotacion-reflexion-traslacion |
| R2025 P32 | 16 | E | Homotecia centrada en origen aplicada a vector | homotecia |
| R2025 P40 | 22 | C | Traslación según vector con parámetro k | rotacion-reflexion-traslacion |
| I2025 P34 | 29 | A | Homotecia de una circunferencia | homotecia |
| I2025 P39 | 34 | A | Traslación y reflexión de figura | rotacion-reflexion-traslacion |
| I2025 P40 | 34 | A | Reflexión respecto a recta vertical | rotacion-reflexion-traslacion |
| R2024 P36 | 31 | C | Homotecia del cuadrado ABCD | homotecia |
| R2024 P39 | 33 | D | Traslación y luego rotación de 90° | rotacion-reflexion-traslacion |
| I2024 P37 | 30 | B | Homotecia: sombra proyectada | homotecia |
| I2024 P38 | 31 | C | Homotecia con centro (1,-1) y razón -2 | homotecia |
| I2024 P39 | 31 | A | Homotecia de cuadrado: relación de áreas | homotecia |

**GEO-trig — Trigonometría** (5 preguntas)

| Pregunta | pág. PDF | clave | de qué trata | subtema |
|---|---|---|---|---|
| I2027 P36 | 32 | D | Punto penal y ángulo de tiro al arco | general |
| I2027 P41 | 35 | D | Funicular: pendiente y ángulo | general |
| I2026 P42 | 35 | D | Refracción: sen(2θ) | general |
| I2025 P41 | 35 | B | Escalera de 3 m con ángulo de 37° | general |
| I2024 P42 | 34 | D | Razones trigonométricas con tabla | general |

**GEO-coor — Geometría analítica (coordenadas)** (1 preguntas)

| Pregunta | pág. PDF | clave | de qué trata | subtema |
|---|---|---|---|---|
| R2024 P42 | 36 | C | Área de triángulo con vértices en coordenadas | general |
<!-- /GEMELAS -->

## ✅ Criterio de dominio
Nivel 3 en los tres temas y hacer una homotecia con centro ≠ origen sin errores de signo.
