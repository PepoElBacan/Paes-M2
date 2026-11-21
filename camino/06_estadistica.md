# M6 · Estadística: posición y dispersión  🟡

**Tus datos:** PYE-dis 2/3. Fallaste **P46** (desviación estándar). Es el 2.º tema más frecuente (26 preguntas oficiales): tablas, histogramas, diagramas de cajón, coeficientes de variación.

## Lo esencial
- **Media** x̄ = Σx/n · **Mediana** (centro ordenado) · **Moda** (más frecuente).
- **Cuartiles** Q₁, Q₂, Q₃ · **Rango** = máx − mín · **IQR** = Q₃ − Q₁. En el diagrama de cajón: 25 % de los datos entre cada par de marcas.
- **Varianza** σ² = Σ(x − x̄)²/n · **Desviación estándar** σ = √σ². (En M2 se trata el grupo como población: divide por n.)
- **Coeficiente de variación** CV = σ/x̄ (dispersión relativa).
- **Datos atípicos:** fuera de [Q₁ − 1,5·IQR ; Q₃ + 1,5·IQR].
- **Transformaciones:** sumar una constante mueve media y mediana, **no** la dispersión. Multiplicar por k multiplica σ por |k| y σ² por k².
- Tabla con frecuencia acumulada: la frecuencia de un dato es la diferencia entre acumuladas consecutivas.

## Método para σ
1. Calcula x̄. 2. Resta x̄ a cada dato. 3. Eleva al cuadrado. 4. Promedia (÷ n). 5. Saca la raíz — **no te quedes en la varianza**.
Para comparar dispersiones sin calcular: mira qué tan alejados están los datos de la media.

## Tus errores → reglas
- **P46:** "σ menor que…" se resuelve comparando desviaciones respecto a la media, no calculando todo. Revisa si las condiciones mantienen el promedio en 5.

## Práctica
```bash
python3 paes.py practicar PYE-dis -n 6
```

## Preguntas oficiales
<!-- GEMELAS PYE-dis -->
| Pregunta | pág. PDF | clave | de qué trata | subtema |
|---|---|---|---|---|
| I2027 P42 | 36 | B | Frecuencia acumulada: medidas | tablas-promedios |
| I2027 P43 | 37 | C | Promedio con nota pendiente | tablas-promedios |
| I2027 P44 | 38 | D | Coeficiente de dispersión por cuartiles | desviacion-varianza |
| I2027 P45 | 39 | A | Diagrama de cajón de tiempos de reacción | cajon-posicion |
| I2027 P55 | 47 | B | Masas de 83 personas: datos parciales | tablas-promedios |
| R2026 P43 | 27 | D | Encuesta de mascotas (tabla/gráfico) | tablas-promedios |
| R2026 P44 | 28 | D | Dato perdido en tabla de edades | tablas-promedios |
| R2026 P55 | 36 | B | Suficiencia de datos: promedios y varianzas | desviacion-varianza |
| I2026 P43 | 36 | D | Histograma de horas de estudio | tablas-promedios |
| I2026 P45 | 38 | B | Diagramas de cajón de tres grupos | cajon-posicion |
| I2026 P46 | 39 | A | Desviación estándar con datos desconocidos | desviacion-varianza |
| R2025 P43 | 24 | A | Diagrama de cajón con 100 datos *(piloto)* | cajon-posicion |
| R2025 P55 | 33 | E | Edades entre 60 y 90: medidas | general |
| I2025 P42 | 36 | B | Datos atípicos con cuartiles | cajon-posicion |
| I2025 P43 | 37 | A | Diagramas de cajón de dos grupos *(piloto)* | cajon-posicion |
| I2025 P44 | 38 | A | Tabla de glucemia: frecuencias | tablas-promedios |
| I2025 P45 | 39 | C | Coeficiente de variación *(piloto)* | desviacion-varianza |
| R2024 P44 | 38 | A | Gráfico lluvia: días y milímetros | tablas-promedios |
| R2024 P45 | 39 | D | Comparar resultados en dos grupos | general |
| R2024 P46 | 40 | B | Tablas de frecuencias de edades | tablas-promedios |
| R2024 P47 | 41 | A | Tabla de estudiantes y promedios | tablas-promedios |
| R2024 P54 | 46 | B | Suficiencia de datos: 50% con nota sobre 5,2 | tablas-promedios |
| R2024 P55 | 47 | A | Suficiencia de datos: varianza de edades | desviacion-varianza |
| I2024 P43 | 35 | B | Medidas de posición con tabla de puntajes | cajon-posicion |
| I2024 P44 | 36 | C | Desviación estándar con rango cero | desviacion-varianza |
| I2024 P54 | 46 | B | Suficiencia de datos: percentiles / tramos | cajon-posicion |
<!-- /GEMELAS -->

## ✅ Criterio de dominio
Nivel 3 y leer un diagrama de cajón (cuartiles, rango, simetría) en menos de 1 minuto.
