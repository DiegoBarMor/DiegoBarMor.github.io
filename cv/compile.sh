#!/bin/bash
set -euo pipefail

available_versions=("en" "en_uni" "fr")

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <version>"
    echo "Available versions: ${available_versions[*]}"
    exit 1
fi

version=$1

if [[ ! " ${available_versions[*]} " =~ $version ]]; then
    echo "Error: Invalid version '$1'."
    echo "Available versions: ${available_versions[*]}"
    exit 1
fi

TMPDIR=$(mktemp -d /tmp/cv-build-XXXX)
trap 'rm -rf "$TMPDIR"' EXIT

cp -r ./* "$TMPDIR"

cd "$TMPDIR"
echo "\input{cv-$version}" >> main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
cd - > /dev/null

mkdir -p build
mv "$TMPDIR/main.pdf" "build/cv-$version.pdf"
