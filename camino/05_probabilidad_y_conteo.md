# M5 · Probabilidad y conteo  🟠

**Tus datos:** PYE-pro 2/4 (fallaste **P47** secuencia de figuras y **P48** permutaciones par-par; piloto P50 condicional y P55 suficiencia). Con conteo y variable aleatoria son 39 preguntas oficiales (≈ 11 %).

## Lo esencial
**Probabilidad**
- Laplace: P(A) = casos favorables / casos totales (equiprobables). Complemento: P(Aᶜ) = 1 − P(A).
- Sin reposición: se **multiplican** las probabilidades y el denominador baja (6/10 · 5/9).
- **Condicional:** P(A|B) = P(A∩B)/P(B) → el "universo" es lo que viene *después de "dado que"*. En tablas 2×2: divide por el total de la fila/columna condicionante.
- Independientes: P(A∩B) = P(A)·P(B). Unión: P(A∪B) = P(A) + P(B) − P(A∩B).
- Probabilidad total (lluvia/atraso): suma de ramas del árbol.

**Conteo**
- Principio multiplicativo: pasos independientes ⇒ se multiplican las opciones. Cuidado con restricciones (primera cifra ≠ 0, último dígito 0 ó 5).
- Permutaciones n! (ordenar todos) · P(n,k) = n!/(n−k)! (**cargos distintos**, importa el orden).
- Combinaciones C(n,k) = n!/(k!(n−k)!) (**comité**, no importa el orden).

**Binomial** (n ensayos, éxito p): P(X = k) = C(n,k)·pᵏ·(1−p)ⁿ⁻ᵏ · E(X) = np.
**Normal:** simétrica en la media; ≈ 68 % a ±1σ, 95 % a ±2σ, 99,7 % a ±3σ.

## Método
1. ¿Es *conteo* (cuántas formas) o *probabilidad* (qué fracción)?
2. ¿Orden importa? ¿hay reposición? ¿hay "dado que"?
3. Escribe el espacio muestral **con números concretos** antes de usar fórmulas (patrones: lista los primeros 6 términos).

## Tus errores → reglas
- **P47 (patrón de figuras):** encuentra la regla escribiendo los primeros términos y recién después cuenta casos favorables.
- **P48 (par-par):** P = (k/n)·((k−1)/(n−1)); el segundo factor *baja*.
- **P50/P55 (condicional):** subraya "dado que / sabiendo que" y restringe el universo.

## Práctica
```bash
python3 paes.py practicar PYE-pro -n 8
python3 paes.py practicar PYE-con -n 8
```

## Preguntas oficiales
<!-- GEMELAS PYE-pro,PYE-con,PYE-var -->

**PYE-pro — Probabilidades** (23 preguntas)

| Pregunta | pág. PDF | clave | de qué trata | subtema |
|---|---|---|---|---|
| I2027 P47 | 41 | C | Probabilidad geométrica con dardo | independencia-otros |
| I2027 P48 | 42 | D | Probabilidad total: lluvia y atraso | condicional-tablas |
| R2026 P47 | 29 | D | Encuesta de 3000 personas: probabilidad | independencia-otros |
| I2026 P47 | 39 | D | Secuencia de figuras: patrón y probabilidad | conteo-y-probabilidad |
| I2026 P48 | 40 | B | Permutaciones: probabilidad par-par | conteo-y-probabilidad |
| I2026 P49 | 41 | D | Lotería con tres números del 1 al 99 | conteo-y-probabilidad |
| I2026 P50 | 42 | D | Probabilidad condicional con dos sabores de helado *(piloto)* | condicional-tablas |
| I2026 P51 | 43 | B | Tabla hombres/mujeres: piercing y tatuaje | condicional-tablas |
| I2026 P55 | 46 | A | Suficiencia de datos: prob. condicional sin reposición *(piloto)* | condicional-tablas |
| R2025 P45 | 25 | B | Rifa con 80 números | conteo-y-probabilidad |
| R2025 P47 | 26 | B | Dos personas al azar sin reposición | condicional-tablas |
| R2025 P48 | 27 | C | Cajas A y B con fichas | conteo-y-probabilidad |
| I2025 P49 | 41 | A | Robot con giro aleatorio | independencia-otros |
| I2025 P50 | 42 | D | Dos cajas con bolitas | conteo-y-probabilidad |
| I2025 P55 | 47 | A | Probabilidad condicional con fracciones | condicional-tablas |
| R2024 P48 | 42 | A | Naipe de 40 cartas | conteo-y-probabilidad |
| R2024 P49 | 42 | C | Sucesos independientes | independencia-otros |
| R2024 P50 | 43 | E | 4 bolitas sin reposición | condicional-tablas |
| R2024 P51 | 43 | B | Rifa de dos premios | conteo-y-probabilidad |
| I2024 P45 | 37 | D | Probabilidad con cartas de 4 tipos | conteo-y-probabilidad |
| I2024 P46 | 38 | A | Probabilidad con dos urnas | conteo-y-probabilidad |
| I2024 P48 | 40 | B | Probabilidad condicional (productos devueltos) | condicional-tablas |
| I2024 P51 | 43 | D | Cartas boca abajo y permutaciones | conteo-y-probabilidad |

**PYE-con — Técnicas de conteo** (11 preguntas)

| Pregunta | pág. PDF | clave | de qué trata | subtema |
|---|---|---|---|---|
| I2027 P49 | 42 | C | Comité de dos personas | combinaciones |
| I2027 P50 | 43 | B | Fotografía en distintas poses (permutaciones) | principio-multiplicativo |
| R2025 P49 | 28 | C | Apretones de mano: combinaciones | combinaciones |
| R2025 P50 | 29 | A | Trazos entre puntos de una circunferencia | combinaciones |
| I2025 P46 | 39 | A | Comité: elegir cargos de un grupo (permutación) | combinaciones |
| I2025 P47 | 40 | D | Torneo todos contra todos: combinaciones | combinaciones |
| I2025 P48 | 40 | A | Directiva de tres cargos con restricción | principio-multiplicativo |
| I2024 P47 | 39 | D | Principio multiplicativo: claves de candado | principio-multiplicativo |
| I2024 P49 | 41 | D | Contar números de 3 cifras múltiplos de 5 | principio-multiplicativo |
| I2024 P50 | 42 | C | Combinaciones: grupos de 2 dulces | combinaciones |
| I2024 P55 | 47 | E | Comisión de debate (hombres y mujeres) *(piloto)* | principio-multiplicativo |

**PYE-var — Variable aleatoria, binomial y normal** (5 preguntas)

| Pregunta | pág. PDF | clave | de qué trata | subtema |
|---|---|---|---|---|
| I2027 P46 | 40 | B | Estudio de gimnasios: muestreo/inferencia | general |
| I2027 P51 | 44 | C | Extracción de ADN: éxito del proceso | general |
| R2026 P49 | 30 | A | Pregunta de V/F al azar: binomial | general |
| R2026 P50 | 31 | A | Distribución normal con media y desviación | general |
| R2025 P51 | 30 | D | Test de verdadero/falso: binomial | general |
<!-- /GEMELAS -->

## ✅ Criterio de dominio
Nivel 3 en PYE-pro y PYE-con, y distinguir en 10 s si una pregunta es permutación o combinación.
