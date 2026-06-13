#!/bin/bash

set -e

echo "================================="
echo "   🚀 Kaido Full Build System"
echo "================================="

# -----------------------------
# PATHS
# -----------------------------
ROOT="$(cd "$(dirname "$0")" && pwd)"
PACKAGES_DIR="$ROOT/packages"
SOURCE_DIR="$PACKAGES_DIR/source"
RELEASE_DIR="$ROOT/release"

echo "📍 Root       : $ROOT"
echo "📦 Packages   : $PACKAGES_DIR"
echo "⚙️ Release    : $RELEASE_DIR"

# -----------------------------
# SYNC FIRST (IMPORTANT FIX)
# -----------------------------
echo ""
echo "🔄 Syncing with GitHub..."

git checkout main
git fetch origin
git pull --rebase origin main || true

# -----------------------------
# BUILD PACKAGES
# -----------------------------
echo ""
echo "📦 Building packages..."

mkdir -p "$PACKAGES_DIR"

for dir in "$SOURCE_DIR"/*/; do
    [ -d "$dir" ] || continue

    name=$(basename "$dir")
    zip_path="$PACKAGES_DIR/$name.zip"

    echo "→ Package: $name"

    rm -f "$zip_path"

    (
        cd "$dir"
        zip -r "$zip_path" . > /dev/null
    )

    echo "✔ Built package: $zip_path"
done

# -----------------------------
# BUILD CORE RELEASES
# -----------------------------
echo ""
echo "⚙️ Building core releases..."

for core_dir in "$RELEASE_DIR"/*/; do
    [ -d "$core_dir" ] || continue

    version=$(basename "$core_dir")
    zip_path="$RELEASE_DIR/$version.zip"

    echo "→ Core version: $version"

    rm -f "$zip_path"

    (
        cd "$core_dir"
        zip -r "$zip_path" . > /dev/null
    )

    echo "✔ Built core: $zip_path"
done

# -----------------------------
# GIT COMMIT LOGIC
# -----------------------------
echo ""
echo "📡 Preparing Git commit..."

git add -A

if git diff --cached --quiet; then
    echo "⚠️ No changes to commit"
    echo "================================="
    echo "✔ Build complete (nothing to push)"
    echo "================================="
    exit 0
fi

git commit -m "kaido build (packages + core) $(date '+%Y-%m-%d %H:%M:%S')"

# -----------------------------
# PUSH
# -----------------------------
echo ""
echo "🚀 Pushing to GitHub..."

git push origin main

# -----------------------------
# DONE
# -----------------------------
echo ""
echo "================================="
echo "✔ Full Kaido build complete"
echo "================================="