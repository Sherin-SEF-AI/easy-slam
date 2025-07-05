#!/bin/bash
# Script to build Sphinx docs and deploy as static site to /docs for GitHub Pages
set -e

# Go to project root
cd "$(dirname "$0")/.."

# Build Sphinx docs
cd docs
make html
cd ..

# Prepare /docs folder in repo root (not docs/)
rm -rf docs_html
mkdir -p docs_html
cp -r docs/_build/html/* docs_html/

# Remove old static docs if present
rm -rf ../docs
mv docs_html ../docs

# Add, commit, and push
cd ..
git add docs/
git commit -m "Deploy static Sphinx docs to /docs for GitHub Pages" || echo "No changes to commit."
git push origin main

echo "Static documentation deployed to /docs and pushed to GitHub."
echo "Now set GitHub Pages source to /docs folder in repository settings." 