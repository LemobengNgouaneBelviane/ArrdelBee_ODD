import os
import re
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arrdel_backend.settings')
django.setup()

import pandas as pd
from accounts.models import User
from odd.models import Project

BASE_DIR = Path(__file__).resolve().parent.parent
FILES = [
    {
        'path': BASE_DIR / 'Cadre Logique BAFOUSSAM1 OK.xlsx',
        'group_col': 'objectifSpecifique',
        'title_col': 'objectifSpecifique',
        'description_col': 'objectifGlobal',
        'territory': 'Bafoussam I',
        'source': 'BAFOUSSAM1',
    },
    {
        'path': BASE_DIR / 'Cadre Logique BAFOUSSAM II.xlsx',
        'group_col': 'Projets',
        'title_col': 'Projets',
        'description_col': 'Objectifs principaux',
        'territory': 'Bafoussam II',
        'source': 'BAFOUSSAM2',
    },
    {
        'path': BASE_DIR / 'CADRE LOGIQUE BAFOUSSAM III ACTUALISE.xlsx',
        'group_col': 'objectifSpecifique',
        'title_col': 'objectifSpecifique',
        'description_col': 'objectifGlobal',
        'territory': 'Bafoussam III',
        'source': 'BAFOUSSAM3',
    },
]

BUDGET_RE = re.compile(r'[\d]+(?:[\s\xa0]?\d{3})*(?:[\.,]\d+)?')


def parse_budget(value):
    if pd.isna(value):
        return 0.0
    text = str(value).strip()
    if not text:
        return 0.0
    if re.search(r'pm', text, re.IGNORECASE):
        return 0.0
    candidate = BUDGET_RE.findall(text)
    if not candidate:
        return 0.0
    number_text = candidate[0].replace('\xa0', '').replace(' ', '').replace(',', '.')
    try:
        return float(number_text)
    except ValueError:
        digits = re.sub(r'[^0-9.]', '', number_text)
        try:
            return float(digits) if digits else 0.0
        except ValueError:
            return 0.0


def normalize_text(value):
    if pd.isna(value):
        return ''
    return str(value).strip()


def build_description(rows, description_col):
    if not rows:
        return ''
    first = rows[0]
    parts = []
    desc = normalize_text(first.get(description_col, ''))
    if desc:
        parts.append(desc)
    for field_name in ('resultats', 'Resultats', 'activite', 'action', 'tache', 'remarques'):
        if field_name in first and normalize_text(first.get(field_name, '')):
            parts.append(f"{field_name.capitalize()}: {normalize_text(first.get(field_name, ''))}")
    return '\n\n'.join(parts)


def import_projects():
    owner = User.objects.filter(is_superuser=True).first() or User.objects.first()
    if not owner:
        raise RuntimeError('Aucun utilisateur trouvé pour attribuer les projets. Créez d abord un utilisateur.')

    print(f"Utilisateur assigné aux projets : {owner.email}")
    print('Suppression des projets existants dans le portefeuille...')
    deleted, _ = Project.objects.all().delete()
    print(f'  Projets supprimés : {deleted}')

    imported = 0
    skipped = 0

    for file_cfg in FILES:
        file_path = file_cfg['path']
        if not file_path.exists():
            print(f"Fichier introuvable : {file_path}")
            skipped += 1
            continue

        print(f"Import depuis {file_cfg['source']} : {file_path.name}")
        df = pd.read_excel(file_path, sheet_name=0)

        group_col = file_cfg['group_col']
        title_col = file_cfg['title_col']
        desc_col = file_cfg['description_col']

        if group_col not in df.columns or title_col not in df.columns:
            print(f"  Colonnes attendues manquantes dans {file_path.name} : {group_col}, {title_col}")
            skipped += 1
            continue

        df[title_col] = df[title_col].astype(str).str.strip()
        if desc_col in df.columns:
            df[desc_col] = df[desc_col].astype(str).str.strip()
        else:
            df[desc_col] = ''

        if 'budget' in df.columns:
            df['budget'] = df['budget'].apply(parse_budget)
        else:
            df['budget'] = 0.0

        groups = {}
        for _, row in df.iterrows():
            title = normalize_text(row.get(title_col, ''))
            if not title or title.lower() in ('nan', 'none'):
                continue
            groups.setdefault(title, []).append(row)

        for title, rows in groups.items():
            project_description = build_description(rows, desc_col)
            budget = max((parse_budget(r.get('budget', 0)) for r in rows), default=0.0)
            territory = normalize_text(rows[0].get('territory', file_cfg['territory']))

            Project.objects.create(
                name=title[:255],
                description=project_description[:2000],
                territory=territory[:255],
                owner=owner,
                status='draft',
                budget=budget,
            )
            imported += 1

        print(f"  Projets créés depuis {file_path.name} : {len(groups)}")

    print('\nImport terminé')
    print(f"Projets importés : {imported}")
    print(f"Fichiers ignorés : {skipped}")


if __name__ == '__main__':
    import_projects()