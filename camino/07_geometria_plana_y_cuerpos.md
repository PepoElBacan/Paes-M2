# M7 · Geometría: semejanza, áreas, volúmenes y circunferencia  🟡

**Tus datos:** fallaste **P16** (razón 16:9 y diagonal en pulgadas), **P35** (hexágono regular inscrito: área) y el piloto **P34** (cuadrados concéntricos). Es el bloque más grande de geometría (44 preguntas oficiales).

## Lo esencial
- **Pitágoras:** a² + b² = c². Diagonal de rectángulo l×a: √(l² + a²).
- **Semejanza:** razón de lados k ⇒ razón de **áreas k²** y de **volúmenes k³**. Thales: paralelas cortan segmentos proporcionales.
- **Áreas:** triángulo bh/2 · trapecio (B + b)h/2 · círculo πr² · **hexágono regular de lado l: (3√3/2)·l²** (6 triángulos equiláteros de área l²√3/4; el radio circunscrito mide l).
- **Volúmenes:** prisma = (área base)·h · cilindro πr²h · cono ⅓πr²h · esfera ⁴⁄₃πr³.
- **Cuadrado inscrito** que une puntos que dividen cada lado en a y b: lado² = a² + b²; razón de áreas = (a² + b²)/(a + b)².
- **Unidades:** 1 pulgada = 2,54 cm → cm → pulgadas **se divide**.
- **Razón 16 : 9** con lado mayor 16k: diagonal = k·√(16² + 9²) = k√337.

## Método
1. Dibuja y **rotula** con las variables del enunciado.
2. Descompón en figuras conocidas (triángulos equiláteros, rectángulos, triángulos rectángulos).
3. Si cambia una dimensión, usa razones (k, k², k³) en vez de recalcular todo.

## Tus errores → reglas
- **P16:** razón a : b ⇒ lados a·k y b·k. Luego Pitágoras, luego conversión de unidades (¡al final!).
- **P35:** el hexágono es 6 triángulos equiláteros: A = 6·(l²√3/4).
- **P34:** en el cuadrado interior usa Pitágoras con los dos segmentos en que quedó dividido el lado.

## Práctica
```bash
python3 paes.py practicar GEO-circ -n 5
python3 paes.py practicar GEO-sem -n 5
python3 paes.py practicar GEO-area -n 5
```

## Preguntas oficiales
<!-- GEMELAS GEO-sem,GEO-area,GEO-circ -->

**GEO-sem — Semejanza, Thales y Pitágoras** (13 preguntas)

| Pregunta | pág. PDF | clave | de qué trata | subtema |
|---|---|---|---|---|
| I2027 P53 | 45 | D | Suficiencia de datos: altura/semejanza *(piloto)* | pitagoras-razones |
| R2026 P40 | 26 | B | Proyector: imagen proporcional por semejanza | thales-semejanza |
| I2026 P16 | 13 | C | Razón 16:9, diagonal y pulgadas (Pitágoras) | pitagoras-razones |
| I2026 P33 | 26 | B | Altura sobre la hipotenusa en triángulo rectángulo | pitagoras-razones |
| I2026 P40 | 33 | C | Diámetro del sol por semejanza | thales-semejanza |
| R2025 P37 | 20 | B | Dos barcos con rumbos perpendiculares (Pitágoras) | pitagoras-razones |
| I2025 P33 | 28 | A | Homotecia en un lente: razón de ampliación | pitagoras-razones |
| I2025 P38 | 33 | A | Pitágoras: escalera apoyada en pared | pitagoras-razones |
| I2025 P53 | 45 | D | Suficiencia de datos: perímetro de trapecio | general |
| I2024 P32 | 25 | A | Teorema de Thales con paralelas | thales-semejanza |
| I2024 P33 | 26 | B | Thales en triángulo con DE paralela a BC | thales-semejanza |
| I2024 P34 | 27 | B | Triángulos semejantes rectángulo 9-12-15 *(piloto)* | thales-semejanza |
| I2024 P35 | 28 | E | Rectángulos semejantes y área | thales-semejanza |

**GEO-area — Áreas, perímetros y volúmenes** (25 preguntas)

| Pregunta | pág. PDF | clave | de qué trata | subtema |
|---|---|---|---|---|
| I2027 P10 | 10 | D | Volumen de cubo al cuadruplicar la arista | volumen-cuerpos |
| I2027 P54 | 46 | D | Suficiencia de datos: red de paralelepípedo y cuerpo generado | volumen-cuerpos |
| R2026 P26 | 18 | C | Cuadrado inscrito en cuadrado: áreas | areas-figuras |
| R2026 P34 | 22 | C | Logo de rectángulo con secciones de color | areas-figuras |
| R2026 P35 | 23 | C | Volumen de prisma al variar dimensiones | volumen-cuerpos |
| R2026 P36 | 23 | C | Estructura de dos prismas rectos | volumen-cuerpos |
| R2026 P53 | 34 | D | Suficiencia de datos: suelo con alfombras | general |
| I2026 P34 | 27 | D | Cuadrados concéntricos: razón de áreas *(piloto)* | areas-figuras |
| I2026 P36 | 29 | — | Cubos de hielo y volumen (eliminada) *(eliminada)* | volumen-cuerpos |
| I2026 P54 | 45 | B | Suficiencia de datos: superficie de un cofre *(piloto)* | areas-figuras |
| R2025 P3 | 5 | D | Área de triángulo con semiperímetro (Herón) | areas-figuras |
| R2025 P34 | 17 | B | Volumen de cimientos de casas *(piloto)* | volumen-cuerpos |
| R2025 P35 | 18 | B | Área de un cuadrilátero *(piloto)* | areas-figuras |
| R2025 P36 | 19 | C | Área de elipse πab | areas-figuras |
| R2025 P39 | 21 | C | Cilindro a cubo: volumen y área | volumen-cuerpos |
| I2025 P37 | 32 | A | Volumen de perfil de aluminio | volumen-cuerpos |
| R2024 P3 | 5 | B | Cuadrados A y B: relación de lados y áreas | areas-figuras |
| R2024 P11 | 10 | A | Triángulo equilátero vs cuadrado (áreas) *(piloto)* | areas-figuras |
| R2024 P35 | 30 | D | Superficie triangular a pintar (proporciones) | areas-figuras |
| R2024 P37 | 32 | A | Volumen de un cilindro (arteria) *(piloto)* | volumen-cuerpos |
| R2024 P53 | 45 | E | Suficiencia de datos: área de cuadrilátero | areas-figuras |
| I2024 P3 | 5 | E | Igualar áreas de círculo, cuadrado y triángulo *(piloto)* | areas-figuras |
| I2024 P7 | 9 | C | Volumen de esferas y relación entre radios | volumen-cuerpos |
| I2024 P36 | 29 | D | Variación del área total de un prisma | volumen-cuerpos |
| I2024 P41 | 33 | B | Volumen de mancuerna (cilindros) | volumen-cuerpos |

**GEO-circ — Circunferencia y polígonos regulares** (6 preguntas)

| Pregunta | pág. PDF | clave | de qué trata | subtema |
|---|---|---|---|---|
| I2027 P37 | 33 | B | Siete círculos concéntricos: suma de áreas | circulos |
| I2027 P38 | 33 | A | Vueltas a parque circular | circulos |
| R2026 P54 | 35 | — | Suficiencia de datos: cuerdas de circunferencia *(eliminada)* | circulos |
| I2026 P35 | 28 | A | Hexágono regular inscrito en círculo: área | hexagono |
| I2025 P35 | 30 | A | Área de hexágono regular desde su perímetro *(piloto)* | hexagono |
| R2024 P43 | 37 | A | Triángulo rectángulo inscrito en circunferencia | circulos |
<!-- /GEMELAS -->

## ✅ Criterio de dominio
Nivel 3 y escribir de memoria las fórmulas de la tabla "Lo esencial".
