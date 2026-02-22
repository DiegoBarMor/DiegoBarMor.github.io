#!/bin/bash
set -euo pipefail

available_languages=("en" "fr")

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <language>"
    echo "Available languages: ${available_languages[*]}"
    exit 1
fi

language=$1

if [[ ! " ${available_languages[*]} " =~ $language ]]; then
    echo "Error: Invalid language '$1'."
    echo "Available languages: ${available_languages[*]}"
    exit 1
fi

TMPDIR=$(mktemp -d /tmp/cv-build-XXXX)
trap 'rm -rf "$TMPDIR"' EXIT

cp -r ./* "$TMPDIR"

cd "$TMPDIR"
echo "\input{cv-$language}" >> main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
cd - > /dev/null

ts=$(date "+%Y%m%d")
mkdir -p build
cp "$TMPDIR/main.pdf" "build/cv-$language-$ts.pdf"
