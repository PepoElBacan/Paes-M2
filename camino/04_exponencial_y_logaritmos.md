# M4 · Exponencial y logaritmos  🟠

**Tus datos:** fallaste **P10** (log₂ 15 con log 2 y log 3, "no supe") y **P11** (cultivos que se duplican); acertaste **P42/P52 sin método** → repásalas igual. Entre exponencial y logaritmos suman 33 preguntas oficiales.

## Lo esencial
**Exponencial:** f(t) = A·bᵗ. Crecimiento si b > 1, decrecimiento si 0 < b < 1.
- Duplica cada d unidades: **A·2^(t/d)**. Triplica: A·3^(t/d). *El exponente es el número de períodos transcurridos.*
- Interés compuesto: **C·(1 + i)ⁿ** (≠ interés simple C(1 + i·n)).

**Logaritmos:** log_b N = x ⇔ bˣ = N
- log(a·b) = log a + log b · log(a/b) = log a − log b · log(aⁿ) = n·log a
- **Cambio de base:** log_b a = log a / log b (¡no al revés!)
- log 1 = 0 · log_b b = 1 · **log 5 = log(10/2) = 1 − log 2**
- Modelos con logaritmo (decibeles, β = 10·log(I/I₀)): reemplaza y despeja con cuidado.

## Receta para "aproxima log_b N con log 2 y log 3" (tu P10)
1. Descompón N en factores 2, 3, 5: 15 = 3·5.
2. log 15 = log 3 + log 5 = 0,48 + (1 − 0,30) = 0,48 + 0,70.
3. Divide por log de la base: log₂ 15 = (0,48 + 0,70) ÷ 0,30.

## Tus errores → reglas
- **P10:** aprende log 5 = 1 − log 2 y la receta de 3 pasos.
- **P11:** período ≠ tiempo total: calcula T/d antes de elevar. Si hay dos cultivos, **calcula cada uno aparte y suma**.

## Práctica
```bash
python3 paes.py practicar NUM-log -n 8
python3 paes.py practicar ALG-exp -n 8
```

## Preguntas oficiales
<!-- GEMELAS NUM-log,ALG-exp -->

**NUM-log — Logaritmos** (15 preguntas)

| Pregunta | pág. PDF | clave | de qué trata | subtema |
|---|---|---|---|---|
| I2027 P13 | 12 | B | Decibeles con logaritmo | modelos-con-log |
| I2026 P10 | 10 | D | Aproximar log2 15 con log 2 y log 3 | propiedades-evaluar |
| I2026 P12 | 11 | B | Intensidad sonora en dB (log) | modelos-con-log |
| I2026 P52 | 44 | B | Suficiencia de datos: logaritmos | general |
| R2025 P6 | 7 | A | Log de producto con p=3^x y b=3^y | propiedades-evaluar |
| I2025 P6 | 7 | B | Ubicar en recta suma de raíz, potencia y logaritmo | general |
| I2025 P7 | 8 | C | Esperanza de vida vs PIB (modelo con log) | modelos-con-log |
| I2025 P10 | 10 | B | Propiedades: log 5 a partir de log 2 | propiedades-evaluar |
| I2025 P11 | 11 | A | Evaluar log de producto/cociente | propiedades-evaluar |
| R2024 P12 | 11 | C | Usar tabla de log para calcular otro log | propiedades-evaluar |
| R2024 P13 | 11 | A | Log con base p y condición log_p b = c | propiedades-evaluar |
| I2024 P9 | 10 | B | Evaluar log3 9 + log8 2 | propiedades-evaluar |
| I2024 P11 | 11 | E | Propiedades: log de cociente | propiedades-evaluar |
| I2024 P12 | 12 | B | Decibelios, fórmula con logaritmo | modelos-con-log |
| I2024 P13 | 12 | B | Log en distinta base con dato log_m p | propiedades-evaluar |

**ALG-exp — Función exponencial e interés compuesto** (18 preguntas)

| Pregunta | pág. PDF | clave | de qué trata | subtema |
|---|---|---|---|---|
| I2027 P14 | 13 | D | Cantidad de medicamento en el tiempo | crecimiento-bacterias |
| I2027 P15 | 13 | B | Dos opciones de depósito con interés compuesto *(piloto)* | interes-compuesto |
| I2027 P17 | 15 | C | Triángulo de Sierpinski: sucesión y potencias | crecimiento-bacterias |
| R2026 P12 | 10 | D | Diámetro de un hongo en el tiempo | crecimiento-bacterias |
| R2026 P14 | 11 | C | Cuentas de ahorro P y Q con interés compuesto | interes-compuesto |
| R2026 P30 | 20 | A | Gráfica de f(x)=a·b^(x-2) | interes-compuesto |
| R2026 P31 | 21 | A | Intensidad de luz en una caverna *(piloto)* | crecimiento-bacterias |
| R2026 P52 | 33 | D | Suficiencia de datos: función exponencial bˣ | interes-compuesto |
| I2026 P11 | 10 | C | Cultivos de bacterias que se duplican | crecimiento-bacterias |
| I2026 P14 | 12 | C | Interés compuesto mensual 1,5% | interes-compuesto |
| R2025 P4 | 6 | D | Masa de cultivo bacteriano que se cuadruplica | crecimiento-bacterias |
| I2025 P2 | 4 | C | Colección de estampillas con variación repetida | interes-compuesto |
| I2025 P12 | 12 | B | Bacterias que duplican cada hora (gráfico) | crecimiento-bacterias |
| I2025 P13 | 13 | D | Depósito a plazo renovable, interés compuesto | interes-compuesto |
| I2025 P51 | 43 | B | Suficiencia de datos: crecimiento 10% anual | general |
| R2024 P14 | 12 | A | Bacterias que se triplican cada 10 días | crecimiento-bacterias |
| R2024 P16 | 13 | B | Interés compuesto trimestral | interes-compuesto |
| I2024 P10 | 11 | C | Bacterias que se triplican por día | crecimiento-bacterias |
<!-- /GEMELAS -->

## ✅ Criterio de dominio
Nivel 3 en ambos temas y resolver P10 y P11 de tu ensayo sin ayuda dos días seguidos.
