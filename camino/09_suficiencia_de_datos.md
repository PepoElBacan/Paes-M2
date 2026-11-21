# M9 · Suficiencia de datos  🟡 (formato, no tema)

**Tus datos:** P53 fallada (productos notables); P52 acertada sin método; P55 piloto fallado. Hay entre 4 y 5 preguntas de este formato por prueba (casi siempre las últimas, hacia P51–P55): ¡**≈ 8–10 % de la prueba**!

## Reglas del formato
No se pide resolver: se decide **si se puede determinar** la respuesta.
- **A** (1) sola · **B** (2) sola · **C** ambas juntas (ninguna sola) · **D** cada una sola · **E** ni juntas alcanzan.

## Método (siempre el mismo)
1. Traduce la pregunta: *"¿qué valor necesito?"* (ej. x² − y², que es (x+y)(x−y)).
2. Mira la afirmación (1) **sola**: ¿fija ese valor? Anota sí/no.
3. Mira la (2) **sola**. Anota sí/no.
4. Solo si ninguna sola: júntalas. ¿Ahora sí?
5. Responde con la tabla: sí/no → D · sí/no → A · no/sí → B · no/no + juntas sí → C · no/no + juntas no → E.
6. **No calcules el número final**: basta saber que se podría.

## Trampas
- Una afirmación que "parece" dar datos pero repite lo del enunciado.
- Datos que dan **dos** soluciones posibles (±, o raíces distintas) ⇒ **no** determina.
- Con sistemas: dos ecuaciones **proporcionales** no sirven como dos datos.
- En probabilidad sin reposición, necesitas *cuántas bolas hay y de qué tipo* (P55).
- En logaritmos/potencias, mira si con la afirmación basta para evaluar la expresión completa (P52).

## Práctica
```bash
python3 paes.py practicar ALG-expr -n 8     # mezcla productos notables con suficiencia de datos
```
Con las preguntas oficiales: busca "Suficiencia" en `python3 paes.py gemelas <tema>` (hay una por cada eje en cada prueba).

## Preguntas oficiales de suficiencia
<!-- SUFICIENCIA -->
| Pregunta | pág. PDF | clave | de qué trata | subtema |
|---|---|---|---|---|
| I2027 P52 | 45 | A | Suficiencia de datos: raíz n-ésima irracional | general |
| I2027 P53 | 45 | D | Suficiencia de datos: altura/semejanza *(piloto)* | pitagoras-razones |
| I2027 P54 | 46 | D | Suficiencia de datos: red de paralelepípedo y cuerpo generado | volumen-cuerpos |
| I2027 P55 | 47 | B | Masas de 83 personas: datos parciales | tablas-promedios |
| R2026 P51 | 32 | A | Suficiencia de datos: irracionales y (p+q)² | general |
| R2026 P52 | 33 | D | Suficiencia de datos: función exponencial bˣ | interes-compuesto |
| R2026 P53 | 34 | D | Suficiencia de datos: suelo con alfombras | general |
| R2026 P54 | 35 | — | Suficiencia de datos: cuerdas de circunferencia *(eliminada)* | circulos |
| R2026 P55 | 36 | B | Suficiencia de datos: promedios y varianzas | desviacion-varianza |
| I2026 P52 | 44 | B | Suficiencia de datos: logaritmos | general |
| I2026 P53 | 44 | A | Suficiencia de datos: productos notables | general |
| I2026 P54 | 45 | B | Suficiencia de datos: superficie de un cofre *(piloto)* | areas-figuras |
| I2026 P55 | 46 | A | Suficiencia de datos: prob. condicional sin reposición *(piloto)* | condicional-tablas |
| R2025 P52 | 31 | A | Suficiencia de datos con racionales x e y | general |
| R2025 P53 | 31 | C | Suficiencia de datos: f(13)=p, f(14)=q | modelar-ecuacion |
| R2025 P54 | 32 | C | Aforo con aproximación a la unidad | general |
| R2025 P55 | 33 | E | Edades entre 60 y 90: medidas | general |
| I2025 P51 | 43 | B | Suficiencia de datos: crecimiento 10% anual | general |
| I2025 P52 | 44 | C | Suficiencia de datos: coeficientes de cuadrática | grafico-coeficientes |
| I2025 P53 | 45 | D | Suficiencia de datos: perímetro de trapecio | general |
| I2025 P54 | 46 | C | Tiempo de vaciado de un cilindro (raíz) | general |
| I2025 P55 | 47 | A | Probabilidad condicional con fracciones | condicional-tablas |
| R2024 P52 | 44 | C | Suficiencia de datos: f(x)=ax²+3x+c | modelar-ecuacion |
| R2024 P53 | 45 | E | Suficiencia de datos: área de cuadrilátero | areas-figuras |
| R2024 P54 | 46 | B | Suficiencia de datos: 50% con nota sobre 5,2 | tablas-promedios |
| R2024 P55 | 47 | A | Suficiencia de datos: varianza de edades | desviacion-varianza |
| I2024 P52 | 44 | D | Suficiencia de datos con racionales a,b,c | general |
| I2024 P53 | 45 | C | Suficiencia de datos: precios de relojes y novelas | plantear |
| I2024 P54 | 46 | B | Suficiencia de datos: percentiles / tramos | cajon-posicion |
| I2024 P55 | 47 | E | Comisión de debate (hombres y mujeres) *(piloto)* | principio-multiplicativo |
<!-- /SUFICIENCIA -->

## ✅ Criterio de dominio
Responder 4 de 5 preguntas de suficiencia de un ensayo en menos de 12 minutos.
