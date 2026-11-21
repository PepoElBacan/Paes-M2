# M2 · Sistemas 2x2 y modelamiento (lineal y porcentajes)  🔴

**Tus datos:** ALG-sis 0/1 (P25 monedas) y ALG-lin 1/2 (P26 precio con % de ganancia); en el taller del 19-nov apareció un concepto nuevo: **sistema sin solución con parámetro (k = 6)**.

## Lo esencial
**Sistemas 2x2** — a₁x + b₁y = c₁ ; a₂x + b₂y = c₂

| Razones | Resultado |
|---|---|
| a₁/a₂ ≠ b₁/b₂ | **una** solución (rectas que se cruzan) |
| a₁/a₂ = b₁/b₂ ≠ c₁/c₂ | **ninguna** (rectas paralelas) |
| a₁/a₂ = b₁/b₂ = c₁/c₂ | **infinitas** (misma recta) |

Métodos: sustitución, igualación, reducción. Nunca hay "exactamente dos" soluciones.

**Modelar con función afín:** f(x) = mx + n → *n* es el valor inicial (costo fijo), *m* es la tasa de cambio (por unidad/día/…).
**Porcentajes:** aumentar p % = × (1 + p/100) · disminuir p % = × (1 − p/100) · varios cambios se **multiplican**, no se suman.
**"p % sobre el costo"** ⇒ precio = costo × (1 + p/100). Cambia el costo ⇒ cambia la base.

## Método para problemas planteados
1. **Define las incógnitas con letras y unidades** (x = monedas de $500).
2. Escribe una ecuación por cada dato.
3. Resuelve… y **vuelve a leer qué pedían** (monedas de $500, no de $100; dinero total, no cantidad).

## Tus errores → reglas
| Pregunta | Regla |
|---|---|
| P25 · monedas $500 y $100 | Antes de marcar, comprueba tu respuesta en **las dos** ecuaciones y confirma qué pide la pregunta |
| P26 · precio con % de ganancia | El % se calcula sobre el **nuevo** costo: precio = (costo nuevo)·(1 + g) — rehácelo |
| Taller 19-nov · k = 6 | Sin solución ⇔ paralelas: k/a = d/b **y** la constante NO es proporcional |

## Niveles
1. Resolver un sistema y plantear con monedas/edades. 2. Sin solución/infinitas con parámetro; % sobre el costo. 3. Modelos afines con gráficos (arriendos, oferta/demanda) y condiciones.

## Práctica
```bash
python3 paes.py practicar ALG-sis -n 8
python3 paes.py practicar ALG-lin -n 6
python3 paes.py hoja ALG-sis -n 8 --nivel 2
```

## Preguntas oficiales
<!-- GEMELAS ALG-sis,ALG-lin -->

**ALG-sis — Sistemas de ecuaciones 2x2** (12 preguntas)

| Pregunta | pág. PDF | clave | de qué trata | subtema |
|---|---|---|---|---|
| I2027 P22 | 19 | A | Condiciones para sistema con solución única | sin-o-infinitas |
| I2027 P23 | 20 | C | Queso y crema con litros de leche | plantear |
| I2027 P24 | 21 | C | 20 prendas entre faldas y jeans | plantear |
| I2026 P25 | 20 | C | Sistema 2x2: monedas de $500 y $100 | plantear |
| R2025 P24 | 13 | B | Sistema: preguntas de 1, 2 y 3 puntos | plantear |
| I2025 P24 | 20 | C | Sistema con infinitas soluciones y parámetros | sin-o-infinitas |
| R2024 P25 | 22 | A | Plantear sistema: adultos y niños al cine | plantear |
| R2024 P27 | 24 | B | Sistema sin solución con parámetro k | sin-o-infinitas |
| R2024 P28 | 25 | C | Sistema infinitas/única solución según a | sin-o-infinitas |
| I2024 P17 | 15 | C | Sistema con infinitas soluciones (hallar p y q) | sin-o-infinitas |
| I2024 P19 | 17 | B | Ecuación que forma sistema sin solución | sin-o-infinitas |
| I2024 P53 | 45 | C | Suficiencia de datos: precios de relojes y novelas | plantear |

**ALG-lin — Función lineal/afín y modelamiento** (17 preguntas)

| Pregunta | pág. PDF | clave | de qué trata | subtema |
|---|---|---|---|---|
| I2027 P25 | 22 | C | Costo de arriendo de vehículo (gráfico) | modelo-recta |
| I2027 P26 | 23 | A | Oferta y demanda lineales | porcentaje-precio |
| R2026 P24 | 17 | D | Dos autos en sentidos opuestos | general |
| I2026 P23 | 18 | B | Relación lineal Celsius-Fahrenheit | general |
| I2026 P26 | 21 | A | Modelar precio con % de ganancia | porcentaje-precio |
| R2025 P13 | 8 | D | Gráfico del precio de un producto | porcentaje-precio |
| I2025 P17 | 15 | C | Peso corregido en función del peso real | modelo-recta |
| I2025 P22 | 18 | — | Gráfico de f(x)=2x+c (eliminada) *(eliminada)* | modelo-recta |
| I2025 P25 | 21 | D | Intersección de dos rectas f y g | modelo-recta |
| I2025 P26 | 22 | B | Nivel de agua nt = at + b | modelo-recta |
| R2024 P19 | 16 | D | Gráfica lineal profundidad-presión | modelo-recta |
| R2024 P22 | 19 | C | Conversión entre escalas de temperatura (gráfico) | modelo-recta |
| R2024 P29 | 25 | B | Nivel de agua modelado por recta | modelo-recta |
| R2024 P34 | 29 | B | Estanque que pierde agua (función afín) | modelo-recta |
| I2024 P20 | 17 | D | k para que recta forme región de área dada | modelo-recta |
| I2024 P21 | 18 | B | Dos autos con rapidez constante (modelo lineal) | general |
| I2024 P22 | 19 | A | Función de consumo bencina por litro | modelo-recta |
<!-- /GEMELAS -->

## ✅ Criterio de dominio
Nivel 3 en ALG-sis y ALG-lin; cero errores de "respondí otra cosa" en las últimas 10.
