#!/bin/bash
# QUICK START SCRIPT - Démarrer le système complet

clear

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          🎯 ODD ARRDEL - SYSTÈME COMPLÈTEMENT REMODELÉ       ║"
echo "║                                                                ║"
echo "║  ✅ Interface d'alignement professionnelle                    ║"
echo "║  ✅ Cartographie territoriale                                ║"
echo "║  ✅ Collecte des preuves avec workflow                       ║"
echo "║  ✅ Backend API complète & données pré-remplies              ║"
echo "╚════════════════════════════════════════════════════════════════╝"

echo ""
echo "📋 VÉRIFICATION DES PRÉREQUIS..."

# Vérifier les dossiers
if [ ! -d "frontend" ] || [ ! -d "app" ]; then
    echo "❌ Erreur: frontend/ ou app/ manquant"
    exit 1
fi

echo "✓ Structure de dossiers OK"

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 manquant"
    exit 1
fi
echo "✓ Python 3 trouvé"

# Vérifier Node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js manquant"
    exit 1
fi
echo "✓ Node.js trouvé"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 DÉMARRAGE AUTOMATIQUE DU SYSTÈME"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Activer venv
if [ ! -d "venv" ]; then
    echo ""
    echo "Setup: Création de l'environnement Python..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt -q
    echo "✓ Environnement Python créé"
else
    source venv/bin/activate
    echo "✓ Environnement Python réutilisé"
fi

# Installer dépendances frontend
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Setup: Installation des dépendances frontend..."
    npm install -q
    echo "✓ Dépendances frontend installées"
else
    echo "✓ Dépendances frontend déjà prêtes"
fi
cd ..

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SYSTÈME PRÊT À DÉMARRER!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "📖 INSTRUCTIONS DE DÉMARRAGE:"
echo ""
echo "TERMINAL 1 - Backend (FastAPI):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo "  → http://localhost:8000"
echo ""

echo "TERMINAL 2 - Frontend (Next.js):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  cd frontend"
echo "  npm run dev"
echo "  → http://localhost:3000"
echo ""

echo "═══════════════════════════════════════════════════════════════════"
echo "🎯 PAGES PRINCIPALES À EXPLORER:"
echo "═══════════════════════════════════════════════════════════════════"

echo ""
echo "1️⃣ ALIGNEMENT AUX ODD"
echo "   URL: http://localhost:3000/alignements"
echo "   Ce que vous pouvez faire:"
echo "   • Sélectionner un projet"
echo "   • Les ODD sont suggérés automatiquement"
echo "   • Entrer baseline (valeur actuelle)"
echo "   • Entrer target (objectif)"
echo "   • Le KPI se calcule automatiquement"
echo "   • Valider l'alignement"
echo ""

echo "2️⃣ CARTOGRAPHIE TERRITORIALE"
echo "   URL: http://localhost:3000/cartographie"
echo "   Ce que vous pouvez faire:"
echo "   • Sélectionner une région"
echo "   • Sélectionner une commune"
echo "   • Voir la carte et les projets"
echo "   • Visualiser les statistiques"
echo ""

echo "3️⃣ COLLECTE DES PREUVES"
echo "   URL: http://localhost:3000/collecte-preuves"
echo "   Ce que vous pouvez faire:"
echo "   • Entrer l'ID d'un projet"
echo "   • Voir les pièces requises"
echo "   • Avancer dans le workflow (4 niveaux)"
echo "   • Ajouter les preuves fournies"
echo "   • Sauvegarder"
echo ""

echo "═══════════════════════════════════════════════════════════════════"
echo "📊 DONNÉES PRÉ-REMPLIES:"
echo "═══════════════════════════════════════════════════════════════════"
echo "  • 705 projets chargés"
echo "  • 42 communes dans 5 régions"
echo "  • 17 ODD définies"
echo "  • 8 projets de test avec secteurs mappés"
echo ""

echo "═══════════════════════════════════════════════════════════════════"
echo "📚 DOCUMENTATION:"
echo "═══════════════════════════════════════════════════════════════════"
echo "  • FRONTEND_IMPROVEMENTS.md   ← Détails améliorations UI"
echo "  • IMPLEMENTATION_GUIDE.md    ← Spécifications API backend"
echo "  • SYSTEM_STATUS.md           ← Vue d'ensemble système"
echo "  • QUICK_START.md             ← Guide 5 minutes"
echo ""

echo "═══════════════════════════════════════════════════════════════════"
echo "✨ BON DÉVELOPPEMENT! ✨"
echo "═══════════════════════════════════════════════════════════════════"
