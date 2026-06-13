#!/bin/bash

echo "================================="
echo "       Kaido Deploy Script"
echo "================================="

# Add all changes
git add .

# Commit with timestamp
git commit -m "kaido update $(date '+%Y-%m-%d %H:%M:%S')"

# Push to current branch
git push

echo "================================="
echo "✔ Pushed to GitHub"
echo "================================="