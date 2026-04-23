#!/bin/bash
# Script de démarrage rapide - ODD ARRDEL System

set -e

echo "🚀 ODD ARRDEL - Démarrage du système complet"
echo "=============================================="

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Vérifications préalables
if [ ! -d "$PROJECT_ROOT/frontend" ]; then
    echo "❌ Dossier frontend introuvable"
    exit 1
fi

if [ ! -d "$PROJECT_ROOT/app" ]; then
    echo "❌ Dossier app (backend) introuvable"
    exit 1
fi

echo ""
echo "📋 Configuration du système..."
echo ""

# Backend
echo "🔧 Installation backend (Python venv)..."
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    python3 -m venv "$PROJECT_ROOT/venv"
    source "$PROJECT_ROOT/venv/bin/activate"
    pip install -r "$PROJECT_ROOT/requirements.txt" -q
    echo "✓ Backend installé"
else
    source "$PROJECT_ROOT/venv/bin/activate"
    echo "✓ Environnement Python réutilisé"
fi

# Frontend
echo ""
echo "🔧 Installation frontend (Node.js)..."
cd "$PROJECT_ROOT/frontend"
if [ ! -d "node_modules" ]; then
    npm install -q
    echo "✓ Frontend installé"
else
    echo "✓ Dépendances Node déjà installées"
fi

echo ""
echo "✅ Configuration terminée!"
echo ""
echo "🖥️  PORT ALLOCATION:"
echo "   Backend FastAPI: http://localhost:8000"
echo "   Frontend Next.js: http://localhost:3000"
echo ""
echo "📖 PROCHAINES ÉTAPES:"
echo "   1. Lancer le backend: uvicorn app.main:app --reload"
echo "   2. Lancer le frontend: npm run dev (dans le dossier frontend)"
echo ""
echo "🎯 Pages principales:"
echo "   - Alignements: http://localhost:3000/alignements"
echo "   - Cartographie: http://localhost:3000/cartographie"
echo "   - Collecte: http://localhost:3000/collecte-preuves"
echo ""
echo "📚 Documentation: voir FRONTEND_IMPROVEMENTS.md"
