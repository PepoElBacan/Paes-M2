# Investigación: qué funciona para subir mucho el puntaje, y si el 1000 es posible

*Resumen de lo que encontré (búsquedas del 21-nov-2026) y de lo que calculé con las tablas oficiales. Los hallazgos de investigación vienen de resúmenes y extractos, no de los artículos completos; donde algo es solo de prensa, lo digo.*

## 1. ¿Se puede llegar a 1000? ¿Es necesario?

**Qué exige el 1000.** La tabla oficial de cada prueba convierte aciertos (P, de 50) en puntaje PAES:

| P | I2024 | R2024 | I2025 | R2025 | I2026 | R2026 | I2027 |
|---|---|---|---|---|---|---|---|
| 50 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 |
| 49 | 914 | 915 | 1000 | 1000 | 1000 | 1000 | 1000 |
| 48 | 889 | 890 | 926 | 903 | 919 | 897 | 898 |
| 47 | 867 | 868 | 900 | 879 | 894 | 876 | 876 |
| 45 | 827 | 829 | 856 | 836 | 850 | 838 | 837 |
| 43 | 790 | 792 | 818 | 797 | 811 | 803 | 801 |
| 40 | 745 | 748 | 768 | 750 | 762 | 759 | 757 |
| 35 | 675 | 678 | 695 | 678 | 687 | 688 | 687 |

- En las **5 pruebas más recientes (I2025 en adelante), 49 de 50 ya dan 1000**. En las dos de 2023 hacían falta 50 de 50 (49 daba ~915).
- Es decir: **a lo más 1 error** en las 50 preguntas puntuables. Las otras 5 de las 55 son pilotos y no cuentan.
- Cada pregunta pesa lo mismo (instrucción oficial de DEMRE), así que no hay "preguntas baratas": también hay que acertar las raras.

**Qué probabilidad tienes según tu tasa de acierto por pregunta** (modelo simple: 50 preguntas independientes, misma probabilidad de acierto):

| Acierto por pregunta | 50/50 | ≥ 49/50 | ≥ 43/50 | ≥ 40/50 |
|---|---|---|---|---|
| 99 % | 61% | 91% | 100% | 100% |
| 97 % | 22% | 56% | 100% | 100% |
| 95 % | 8% | 28% | 100% | 100% |
| 92 % | 2% | 8% | 96% | 100% |
| 90 % | 1% | 3% | 88% | 99% |
| 85 % | 0% | 0% | 52% | 88% |
| 80 % | 0% | 0% | 19% | 58% |

Lectura: para tener ~50 % de probabilidad de llegar a 1000 en una prueba concreta, necesitas **≈ 97 % de acierto por pregunta**, o sea dominar casi todo el temario, incluidas las preguntas atípicas. Tu ensayo I2026 fue 31/49 ≈ 63 %.

**Tu realidad con 9 días.** Pasar de ~63 % a ~97 % no es realista en 9 días; sí lo es subir bastante. Meta razonable: **40–45 correctas (≈ 760–850 puntos)** reforzando cuadrática, probabilidad, dispersión, proporcionalidad y logaritmos, que concentran tus errores. El 1000 es un objetivo de largo plazo (otra rendición), no de esta semana.

**¿Es necesario el 1000?** Depende de la carrera: cada una define su puntaje ponderado de corte y cuánto pesa M2 en esa ponderación. Con la nota de corte de tu carrera y su ponderación de M2 se calcula cuánto M2 necesitas; si me los dices, lo calculo. (En la app, la tarjeta "Mi meta" muestra cuántas correctas exige cada puntaje.)
Dato de contexto: La Tercera informó [2.861 puntajes nacionales en la PAES regular 2025](https://www.latercera.com/nacional/noticia/paes-regular-deja-2861-puntajes-nacionales-casi-mil-mas-que-su-version-anterior/), casi todos en M1; una nota de [Emol](https://www.emol.com/noticias/Nacional/2026/07/27/1206755/universidades-aumentan-peso-prueba-matematica.html) menciona solo unos pocos máximos en M2 (**no pude confirmar esa cifra en DEMRE**). M2 es, en la práctica, la prueba donde el 1000 es más raro.

## 2. Qué dice la evidencia, y qué implementé

| Técnica | Qué encontré | Qué hace el sistema |
|---|---|---|
| **Practicarse con pruebas** (recuperación) | La revisión de [Dunlosky et al. (2013)](https://www.psychologicalscience.org/journals/pspi/1529100612453266/) calificó la **práctica con pruebas** y la **práctica distribuida** con la utilidad más alta de 10 técnicas; releer y subrayar, las que más usan los estudiantes, no mejoran el rendimiento de forma consistente. | Toda la app es resolver, no leer. Las guías son de consulta. |
| **Práctica distribuida** | Igual que arriba: espaciar el estudio en el tiempo. | Repaso +1, +3, +7 días de errores oficiales y de ejercicios. |
| **Práctica intercalada** | En un [ensayo aleatorio con 54 cursos de 7.º básico](https://ies.ed.gov/ncee/wwc/Study/88770) (Rohrer y cols., 2020), quienes intercalaron tipos de problemas sacaron **61 % vs 38 %** en una prueba sorpresa posterior (d = 0,83), con los mismos problemas en distinto orden. Es un estudio con niños y de otro contenido; el efecto en PAES puede ser menor. | Las sesiones de refuerzo, repaso y mini-ensayo **mezclan temas** y evitan dos seguidos del mismo subtema. |
| **Confianza y errores confiados** | El efecto de [hipercorrección](https://link.springer.com/article/10.1007/s11409-006-6894-z): los errores cometidos **con alta seguridad se corrigen mejor** al ver la respuesta, porque la sorpresa atrae atención (Butterfield y Metcalfe). Es la misma idea de tu banco de Ciencias ("Segura (error confiado)"). | Antes de ver el resultado marcas **Seguro / Dudé / Adiviné**. Los errores confiados se marcan y se priorizan; un acierto dudando también entra a refuerzo. |
| **Analizar el porqué del error** | Prensa chilena: una especialista dice que lo más valioso es [revisar por qué se cometió cada error](https://www.radioagricultura.cl/noticias/nacional/paes-2026-estudiar-mas-horas-no-garantiza-un-mejor-puntaje-segun-experta_20261118/) y que resolver muchos ejercicios no garantiza por sí solo un mejor puntaje. (Fuente de prensa, no un estudio.) | Al fallar eliges la causa: no sabía el método, cálculo/signo, leí mal, me confundí de fórmula, falta de tiempo. La pestaña Historial te muestra cómo fallas. |
| **Ensayos en condiciones reales** | [La Tercera](https://www.latercera.com/educacion/noticia/paes-10-consejos-estrategicos-para-lograr-el-mejor-puntaje-de-ingreso-a-la-universidad-en-2027/) recomienda ensayos para detectar fortalezas y debilidades y entrenar la presión de tiempo. [Emol](https://www.emol.com/noticias/Tendencias/2026/11/12/1216791/consejos-prueba-paes-estudio-previo.html): en los días previos, descanso y repasos breves. | **Mini-ensayo cronometrado** (2 min 30 s por pregunta, sin feedback hasta el final) y corrección de ensayos oficiales con puntaje. |

## 3. Lo que no implementé (y por qué)
- **Resúmenes y subrayado:** utilidad baja según la evidencia.
- **Garantías de puntaje:** ninguna fuente que encontré mide cuánto sube el puntaje PAES con cada técnica; lo que muestro es evidencia general de aprendizaje, con las salvedades de arriba.

## 4. Cómo usarlo para acercarte a tu meta
1. Cada día: **Repaso** (errores oficiales + tarjetas de refuerzo).
2. **Sesión de refuerzo** con tus subtemas más débiles (mezclados).
3. Dos veces por semana: **mini-ensayo cronometrado**; revisa por qué fallaste y marca la causa.
4. Cada ensayo oficial: corrígelo en la app; mira **Fortalezas** (lo que ya puedes dejar de repasar) y **Evolución**.
