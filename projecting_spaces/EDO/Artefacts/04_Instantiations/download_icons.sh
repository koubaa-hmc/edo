#!/bin/bash

# Download Lucide icons (SVG and JSON metadata)
# Icon list from icon_mapping.md

ICONS=(
  "search-code"
  "user-check"
  "log-in"
  "filter"
  "badge-check"
  "network"
  "cpu"
  "link-2"
  "shield-check"
  "activity"
  "chevron-right"
  "copy"
  "quote"
  "download"
  "file-edit"
  "flag"
  "file-text"
  "share-2"
  "save"
  "calendar-days"
  "map-pin"
  "upload"
  "plug"
  "check-circle-2"
  "alert-triangle"
  "code-2"
)

OUTPUT_DIR="/Users/ot2661/Library/Mobile Documents/com~apple~CloudDocs/write/on over/projecting/projecting/EDO/Artefacts/04_Instantiations/icons"

mkdir -p "$OUTPUT_DIR"

echo "Downloading ${#ICONS[@]} Lucide icons..."

for icon in "${ICONS[@]}"; do
  echo "Downloading $icon..."
  
  # Download SVG from unpkg CDN
  curl -sL "https://unpkg.com/lucide-static@latest/icons/${icon}.svg" -o "${OUTPUT_DIR}/${icon}.svg"
  
  if [ -f "${OUTPUT_DIR}/${icon}.svg" ] && [ -s "${OUTPUT_DIR}/${icon}.svg" ]; then
    # Extract viewBox and path data to create JSON metadata
    viewBox=$(grep -o 'viewBox="[^"]*"' "${OUTPUT_DIR}/${icon}.svg" | cut -d'"' -f2)
    pathData=$(grep -o 'd="[^"]*"' "${OUTPUT_DIR}/${icon}.svg" | cut -d'"' -f2)
    
    # Create JSON metadata file
    cat > "${OUTPUT_DIR}/${icon}.json" << EOF
{
  "name": "${icon}",
  "viewBox": "${viewBox}",
  "width": 24,
  "height": 24,
  "tags": ["${icon//-/ }"],
  "paths": [
    "${pathData}"
  ]
}
EOF
    echo "  ✓ ${icon}.svg and ${icon}.json created"
  else
    echo "  ✗ Failed to download ${icon}"
  fi
done

echo ""
echo "Download complete!"
echo "Icons saved to: ${OUTPUT_DIR}"
ls -la "${OUTPUT_DIR}"
