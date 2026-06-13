#!/bin/bash

echo "================================="
echo "   🚀 Kaido Full Build System"
echo "================================="

ROOT="$(cd "$(dirname "$0")" && pwd)"
RELEASE_DIR="$ROOT/release"
SOURCE_DIR="$RELEASE_DIR/source"  # optional if you ever modularize

echo "📍 Root: $ROOT"

# -----------------------------
# ASK VERSION
# -----------------------------
echo ""
read -p "📦 Enter version (e.g. 1.0, 1.1, 2.0): " VERSION

if [ -z "$VERSION" ]; then
    echo "❌ Version cannot be empty"
    exit 1
fi

echo ""
echo "🔨 Building version: $VERSION"

# -----------------------------
# BUILD CORE VERSION ZIP
# -----------------------------
VERSION_DIR="$RELEASE_DIR/$VERSION"
VERSION_ZIP="$RELEASE_DIR/$VERSION.zip"
LATEST_ZIP="$RELEASE_DIR/latest.zip"

if [ ! -d "$VERSION_DIR" ]; then
    echo "❌ Version folder not found: $VERSION_DIR"
    exit 1
fi

echo "📦 Creating $VERSION.zip..."

rm -f "$VERSION_ZIP"

(
    cd "$VERSION_DIR" || exit
    zip -r "$VERSION_ZIP" . > /dev/null
)

echo "✔ Built: $VERSION.zip"

# -----------------------------
# UPDATE LATEST
# -----------------------------
echo ""
echo "🧪 Updating latest.zip..."

rm -f "$LATEST_ZIP"
cp "$VERSION_ZIP" "$LATEST_ZIP"

echo "✔ Updated latest.zip"

# -----------------------------
# GIT COMMIT
# -----------------------------
echo ""
echo "📡 Preparing Git commit..."

git add -A

if git diff --cached --quiet; then
    echo "⚠️ No changes to commit"
    exit 0
fi

git commit -m "kaido release v$VERSION (update latest)"

# -----------------------------
# PUSH
# -----------------------------
echo ""
echo "🚀 Pushing to GitHub..."

git pull --rebase origin main
git push origin main

# -----------------------------
# DONE
# -----------------------------
echo ""
echo "================================="
echo "✔ Kaido build complete"
echo "📦 Version: $VERSION"
echo "📦 Latest updated"
echo "================================="