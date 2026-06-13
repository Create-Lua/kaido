#!/bin/bash

echo "================================="
echo "   Kaido Build + Deploy Script"
echo "================================="

# -----------------------------
# CONFIG
# -----------------------------
SOURCE_DIR="release/1.0"
OUTPUT_DIR="release"
ZIP_NAME="latest.zip"
ZIP_PATH="$OUTPUT_DIR/$ZIP_NAME"

# -----------------------------
# BUILD ZIP
# -----------------------------
echo "Zipping package..."

# remove old zip if exists
rm -f "$ZIP_PATH"

# create fresh zip
cd "$SOURCE_DIR" || exit

zip -r "../../$ZIP_PATH" . > /dev/null

cd - > /dev/null

echo "✔ Created $ZIP_PATH"

# -----------------------------
# GIT PUSH
# -----------------------------
echo "Committing changes..."

git add .

git commit -m "kaido build $(date '+%Y-%m-%d %H:%M:%S')"

git push

echo "================================="
echo "✔ Build + Deploy complete"
echo "================================="