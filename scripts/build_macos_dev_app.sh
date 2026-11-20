#!/bin/sh
# Build a local-only macOS application with PyInstaller from the active environment.
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
output_dir=$(mkdir -p -- "${1:?Usage: build_macos_dev_app.sh OUTPUT_DIRECTORY}" && cd -- "$1" && pwd)
cd "$repo_dir"

iconset="$output_dir/STEPS.iconset"
mkdir -p "$iconset"
assets="$repo_dir/app/assets/brand"
for size in 16 32 256 512; do
    cp "$assets/steps-app-icon-$size.png" "$iconset/icon_${size}x${size}.png"
done
for size in 16 128 256; do
    cp "$assets/steps-app-icon-$((size * 2)).png" "$iconset/icon_${size}x${size}@2x.png"
done
iconutil -c icns "$iconset" -o "$output_dir/STEPS.icns"

python -m PyInstaller --noconfirm --onedir --windowed --name STEPS-Dev \
    --osx-bundle-identifier de.n05a.steps.dev --icon "$output_dir/STEPS.icns" \
    --distpath "$output_dir/dist" --workpath "$output_dir/work" --specpath "$output_dir" \
    --paths "$repo_dir" \
    --add-data "$assets:app/assets/brand" \
    --add-data "$repo_dir/app/locales/*.json:app/locales" \
    --add-data "$repo_dir/design/tokens/tokens.json:design/tokens" \
    --add-data "$repo_dir/src/steps/progression/*.json:src/steps/progression" \
    --add-data "$repo_dir/knowledge/sources/registry.yaml:knowledge/sources" \
    --add-data "$repo_dir/LICENSE:." \
    "$repo_dir/app/main.py"
