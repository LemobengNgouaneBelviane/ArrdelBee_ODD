## ODD Arrdel — Alignement & Performance (prototype)

Ce dépôt contient un prototype FastAPI/SQLAlchemy pour:
- importer 4 fichiers Excel (Référentiel ODD, Cadre Logique, Matrice Problèmes‑Solutions, Inventaire PCD)
- aligner les projets aux indicateurs ODD
- calculer une performance (cible vs réalisée) avec code couleur
- exposer une API et un workflow de validation à 4 niveaux

### Démarrage rapide

1) Créer un environnement Python puis installer:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Définir la base PostgreSQL (exemple):

```bash
export DATABASE_URL="postgresql+psycopg://user:pass@localhost:5432/odd_arrdel"
```

3) Créer les tables (dev) puis importer les Excel:

```bash
python -m app.db_init
python scripts/seed_from_excel.py \
  --odd "/home/belviane/Téléchargements/ODD_Arrdel/ODD, Objctifs, Cibles et Indicateurs 082023(1).xlsx" \
  --logframe "/home/belviane/Téléchargements/ODD_Arrdel/Liste des tableaux des Cadres logiques 19082024 Ok.xlsx" \
  --problem_solution "/home/belviane/Téléchargements/ODD_Arrdel/ARRDEL_Matrice_des_PB_et_Besoins_OUEST_12072024_Copie_ACTUALISE.xls" \
  --pcd "/home/belviane/Téléchargements/ODD_Arrdel/Inventaire des pb et besoins et analyse des PCD.xlsx"
```

4) Lancer l’API:

```bash
uvicorn app.main:app --reload
```

### Endpoints (FR)
- `GET /sante`
- `GET /projets/non-alignes?limit=200`
- `POST /alignements/valider`
- `GET /projets/{project_id}/configuration-collecte`
- `POST /projets/{project_id}/preuves`
- `POST /preuves/{evidence_id}`
- `GET /projets/{project_id}/justification`
- `GET /tableau-de-bord/impact?limit=200`

### Notes
- Les scripts tentent d’inférer les feuilles/colonnes; si vos en-têtes diffèrent, ajustez `scripts/seed_from_excel.py`.
- Pour la prod, il est recommandé d’ajouter Alembic (migrations) et une gestion de fichiers preuves (S3/minio).

