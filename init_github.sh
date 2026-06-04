#!/usr/bin/env bash
# =============================================================================
# init_github.sh — Initialise le dépôt Git et pousse sur GitHub
#
# Usage :
#   chmod +x scripts/init_github.sh
#   ./scripts/init_github.sh <url-repo-github>
#
# Exemple :
#   ./scripts/init_github.sh https://github.com/arbouzam-daniel/meteo-api.git
# =============================================================================

set -e

REPO_URL=${1:-""}

if [ -z "$REPO_URL" ]; then
  echo "❌ Usage : ./scripts/init_github.sh <url-du-repo-github>"
  echo "   Exemple : ./scripts/init_github.sh https://github.com/mon-compte/meteo-api.git"
  exit 1
fi

echo "🔧 Initialisation Git…"
git init
git add .
git commit -m "feat: initial API météo (vagues de chaleur v6 + pluies intenses v2)"

echo "🔗 Connexion au dépôt distant…"
git remote add origin "$REPO_URL"
git branch -M main
git push -u origin main

echo "✅ Dépôt poussé sur : $REPO_URL"
echo "   Accédez à : ${REPO_URL%.git}"
