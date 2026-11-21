#!/usr/bin/env bash
# Descarga las pruebas oficiales de M2 (y sus clavijeros) publicadas por DEMRE → pruebas/pdf/
# Fuente: https://demre.cl/publicaciones  (documentos de difusión de la Universidad de Chile / DEMRE)
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p pruebas/pdf
BASE="https://demre.cl/publicaciones/pdf"

ARCHIVOS=(
  # Invierno jun-2023 (Adm. 2024) y su clavijero
  2024-23-06-19-paes-invierno-oficial-matematica2-p2024.pdf   2024-23-07-20-clavijero-paes-invierno-m2.pdf
  # Regular nov-2023 (Adm. 2024)
  2024-23-11-27-paes-regular-oficial-matematica2-p2024.pdf    2024-23-12-28-clavijero-paes-regular-m2.pdf
  # Invierno jun-2024 (Adm. 2025)
  2025-24-06-17-paes-invierno-oficial-matematica2-p2025.pdf   2025-24-07-19-clavijero-paes-invierno-m2.pdf
  # Regular dic-2024 (Adm. 2025): selección de 38 preguntas
  2025-24-12-02-paes-regular-matematica2-p2025.pdf            2025-25-01-06-clavijero-paes-regular-m2.pdf
  # Invierno jun-2025 (Adm. 2026)  ← es tu "ENSAYO M2 I2026"
  2026-25-06-16-paes-invierno-oficial-matematica2-p2026.pdf   2026-25-07-18-clavijero-paes-invierno-m2.pdf
  # Regular dic-2025 (Adm. 2026): selección de preguntas
  2026-25-12-01-paes-regular-matematica2-p2026.pdf            2026-26-01-05-clavijero-paes-regular-m2.pdf
  # Invierno jun-2026 (Adm. 2027)
  2027-26-06-15-paes-invierno-oficial-matematica2-p2027.pdf   2027-26-07-17-clavijero-paes-invierno-m2.pdf
)

for f in "${ARCHIVOS[@]}"; do
  if [[ -s "pruebas/pdf/$f" ]] && head -c4 "pruebas/pdf/$f" | grep -q '%PDF'; then
    echo "ya está   $f"; continue
  fi
  curl -fsSL --retry 3 -o "pruebas/pdf/$f" "$BASE/$f"
  head -c4 "pruebas/pdf/$f" | grep -q '%PDF' || { echo "¡no es un PDF!: $f" >&2; rm -f "pruebas/pdf/$f"; exit 1; }
  echo "descargado $f"
done
echo "Listo. Ahora: python3 scripts/extraer_preguntas.py && python3 scripts/construir_datos.py"
