# PAES M2 · sistema de práctica personalizado

Sistema para prepararte para la **PAES de Competencia Matemática 2 (M2)** usando tus propios resultados:

1. **Banco oficial:** 7 pruebas M2 de DEMRE (invierno y regular, 2023–2026) con **349 preguntas clasificadas por tema y subtema**, con clave, página del PDF y marca de piloto/eliminada.
2. **Diagnóstico:** analiza tu hoja *PAES ALTERNATIVAS* (ensayo M2 I2026 + banco de errores) → `docs/diagnostico.md`.
3. **Gemelas:** para cada pregunta que fallaste, las preguntas del mismo tema en las otras pruebas → `docs/mapa_gemelas.md`.
4. **Ejercicios generados:** 37 generadores paramétricos (cada respuesta se calcula en código; cada opción incorrecta corresponde a un error típico y te lo explica).
5. **Repetición espaciada:** tus errores vuelven a +1, +3 y +7 días; con 3 aciertos seguidos quedan *dominados* (la misma regla de tu hoja).
6. **Camino guiado:** 10 módulos ordenados por impacto, con teoría esencial, tus errores y reglas → `camino/`.

> Estado de tu desempeño (ensayo I2026): **31/49 puntuables ⇒ 640 pts**. Mayor pérdida: **función cuadrática (0/4)**, el tema más frecuente de la PAES M2. Detalle en [`docs/diagnostico.md`](docs/diagnostico.md).

## App web para el celular

`web/` contiene una página de una sola pantalla pensada para el teléfono: ejercicios con explicación de errores, repaso espaciado de tus errores oficiales, corrección de ensayos (con puntaje PAES) y las guías. Usa los mismos datos y las mismas reglas que la CLI.
Se regenera con `python3 scripts/construir_web.py` (ejercicios, datos y guías) y se publica como Artifact de Claude: <https://claude.ai/artifact/AiFbSUCqFY84CtdCqDpGar>. Su progreso es independiente del de la CLI (`progreso/estado.json`).

## Inicio rápido

Requisitos: Python 3.9+; para (re)extraer texto/imágenes de los PDF: `poppler-utils` (`pdftotext`, `pdftoppm`).

```bash
git clone <este repo> && cd Paes-M2
scripts/descargar_pruebas.sh        # baja los PDF oficiales de demre.cl a pruebas/pdf/ (no se versionan)
python3 paes.py hoy                 # ¿qué hago hoy?  (el progreso ya viene sembrado desde tu hoja)
```

| Comando | Para qué |
|---|---|
| `python3 paes.py hoy` | plan del día: repasos pendientes + tema de mayor prioridad |
| `python3 paes.py estado` | panel: puntaje de ensayos, repasos, y cuántas preguntas "se pierden" por tema |
| `python3 paes.py repaso [--imagen]` | repasa tus errores oficiales (te dice PDF y página; corrige con la clave) |
| `python3 paes.py practicar ALG-cua -n 8` | ejercicios generados, interactivo; sube de nivel con 4/5 aciertos |
| `python3 paes.py hoja ALG-cua -n 10 --nivel 2` | hoja para resolver **en papel** → `python3 paes.py corregir <id> 1A 2C …` |
| `python3 paes.py gemelas I2026-31` | preguntas oficiales parecidas a esa (o `gemelas ALG-cua` para todo el tema) |
| `python3 paes.py ensayo I2027 CDCD…` | corrige un ensayo completo (55 letras, `-` = en blanco), da tu puntaje PAES y actualiza prioridades |
| `python3 paes.py camino` | módulos del camino guiado y su avance |
| `python3 paes.py pagina I2026-31` | dónde está una pregunta (PDF, página; renderiza PNG si hay `pdftoppm`) |
| `python3 paes.py autotest` | verifica los generadores de ejercicios |

Temas con generadores: `ALG-cua ALG-sis ALG-prop ALG-lin ALG-exp NUM-log NUM-por ALG-expr(+suficiencia) ALG-ecu GEO-sem GEO-circ GEO-area GEO-vec GEO-iso GEO-trig PYE-dis PYE-pro PYE-con`.
Los demás temas (números reales, potencias, funciones por tramos, binomial/normal…) se practican con las **preguntas oficiales** (`gemelas <tema>`).

## El ciclo recomendado
`ensayo` → `estado` (¿qué tema pierde más?) → **guía del módulo** en `camino/` → `practicar`/`hoja` hasta nivel 3 → **gemelas oficiales** → `repaso` diario → nuevo `ensayo`.
Plan concreto hasta el día de la prueba: [`docs/plan_9_dias.md`](docs/plan_9_dias.md). Estrategia: [`docs/estrategia_de_prueba.md`](docs/estrategia_de_prueba.md). Fórmulas: [`docs/hoja_de_formulas.md`](docs/hoja_de_formulas.md).

## Pruebas incluidas (IDs = año de admisión, como en tu hoja: *I2026 = Invierno, Admisión 2026*)

| ID | Aplicación | Tipo | Preguntas etiquetadas |
|---|---|---|---|
| I2024 | PAES Invierno, jun-2023 | completa | 55 |
| R2024 | PAES Regular, nov-2023 | completa | 55 |
| I2025 | PAES Invierno, jun-2024 | completa | 55 |
| R2025 | PAES Regular, dic-2024 | *selección* DEMRE | 38 |
| **I2026** | PAES Invierno, jun-2025 (**tu ensayo**) | completa | 55 |
| R2026 | PAES Regular, dic-2025 | *selección* DEMRE | 36 |
| I2027 | PAES Invierno, jun-2026 | completa | 55 |

DEMRE solo publicó una *selección* de preguntas de la regular de 2024 y 2025 (no la prueba completa). La regular de 2026 se rinde el **lunes 30-nov, 15:00 h** (calendario DEMRE) y aún no existe.
Fuentes: <https://demre.cl/publicaciones> (cada prueba y su clavijero). Los PDF **no se versionan** (son material con derechos reservados de la Universidad de Chile / DEMRE): se descargan con `scripts/descargar_pruebas.sh`.

## Estructura

```
paes.py                    # entrada de la CLI
sistema/                   # taxonomía, banco, generadores, repetición espaciada, CLI
datos/                     # banco_oficial.json (tema/subtema/clave/página), tabla de puntajes, tus respuestas del ensayo, etiquetas manuales
progreso/estado.json       # tu progreso (errores, niveles, ensayos): versionable
camino/                    # 10 módulos guiados (tablas de preguntas oficiales generadas automáticamente)
docs/                      # diagnóstico, mapa de gemelas, plan, estrategia, fórmulas
web/                       # app web móvil (index.html + datos generados)
scripts/                   # descargar PDFs, extraer preguntas, construir datos, generar docs y la app web
tests/                     # python3 -m unittest discover -s tests
```

## Cómo se construyó (y límites)

- **Preguntas:** texto extraído con `pdftotext`; la numeración y las claves se validaron contra tu hoja (las 55 claves de I2026 coinciden con las tuyas). El texto de las preguntas queda solo en local (`pruebas/texto/`, ignorado por git); el repositorio guarda únicamente clasificación y descripciones propias.
- **Clasificación por tema/subtema:** manual, a partir del enunciado. Puede haber errores en las preguntas con fórmulas muy largas (en el PDF las expresiones matemáticas se extraen mal); abre la página con `paes.py pagina` y corrígela en `datos/etiquetas/*.txt`, luego `python3 scripts/construir_datos.py && python3 scripts/generar_docs.py`.
- **Prioridad por tema** = 50 × (peso del tema en las 7 pruebas) × (tasa de error suavizada de tus ensayos y práctica). Con pocos datos es una guía, no una verdad: cada ensayo nuevo la afina.
- Solo M2. Ciencias (Física) y Competencia Lectora de tu hoja no están incluidos.
