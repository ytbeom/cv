#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$ROOT_DIR/pdf"

for lang in ko en; do
  echo "[$lang] Converting cv_${lang}.md → cv_${lang}.typ"
  python "$ROOT_DIR/scripts/md_to_typ.py" "$lang"

  echo "[$lang] Compiling cv_${lang}.typ → pdf/cv_${lang}.pdf"
  MSYS_NO_PATHCONV=1 docker run --rm \
    -v "$ROOT_DIR:/workspace" \
    -w /workspace \
    --entrypoint typst \
    pandoc/typst:latest \
    compile "cv_${lang}.typ" "pdf/cv_${lang}.pdf" --font-path fonts
done

echo ""
echo "PDFs generated:"
echo "  $ROOT_DIR/pdf/cv_ko.pdf"
echo "  $ROOT_DIR/pdf/cv_en.pdf"
