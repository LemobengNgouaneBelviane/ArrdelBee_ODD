#!/usr/bin/env python
import sys
sys.path.insert(0, '/home/belviane/Téléchargements/ODD_Arrdel')

from app.database import SessionLocal, engine
from app.models import Base, Department, Commune, SDGGoal, Project

db = SessionLocal()

# Créer les départements
deps = [
    Department(name="Littoral"),
    Department(name="Centre"),
    Department(name="Sud"),
    Department(name="Nord"),
    Department(name="Est"),
]
db.add_all(deps)
db.flush()

# Créer quelques communes
communes_data = [
    ("Douala", 1, 4.05, 9.75),
    ("Yaoundé", 2, 3.87, 11.53),
    ("Kfemen", 5, 2.9, 12.4),
    ("Bafoussam", 2, 5.76, 10.42),
    ("Buea", 3, 4.15, 9.74),
]

for name, dept_id, lat, lon in communes_data:
    c = Commune(name=name, department_id=dept_id, latitude=lat, longitude=lon)
    db.add(c)
db.flush()

# Créer les ODD (17 au total)
odds = [
    {
        "code": "1",
        "title": "Pas de pauvreté",
        "description": "Éliminer la pauvreté sous toutes ses formes",
    },
    {
        "code": "2",
        "title": "Faim zéro",
        "description": "Éliminer la faim et assurer la sécurité alimentaire",
    },
    {
        "code": "3",
        "title": "Bonne santé et bien-être",
        "description": "Assurer la santé et le bien-être pour tous",
    },
    {
        "code": "4",
        "title": "Éducation de qualité",
        "description": "Assurer une éducation de qualité inclusive et équitable",
    },
    {
        "code": "5",
        "title": "Égalité des sexes",
        "description": "Parvenir à l'égalité des sexes",
    },
    {
        "code": "6",
        "title": "Eau propre et assainissement",
        "description": "Assurer l'accès à l'eau et à l'assainissement pour tous",
    },
    {
        "code": "7",
        "title": "Énergie propre et d'un coût abordable",
        "description": "Assurer l'accès à une énergie fiable, durable et moderne",
    },
    {
        "code": "8",
        "title": "Travail décent et croissance économique",
        "description": "Promouvoir une croissance économique durable et inclusive",
    },
    {
        "code": "9",
        "title": "Industrie, innovation et infrastructure",
        "description": "Bâtir une infrastructure résiliente et favoriser l'innovation",
    },
    {
        "code": "10",
        "title": "Inégalités réduites",
        "description": "Réduire les inégalités dans les pays et entre les pays",
    },
    {
        "code": "11",
        "title": "Villes et communautés durables",
        "description": "Faire en sorte que les villes soient ouvertes à tous",
    },
    {
        "code": "12",
        "title": "Consommation et production responsables",
        "description": "Établir les modes de consommation et production durables",
    },
    {
        "code": "13",
        "title": "Mesures relatives à la lutte contre les changements climatiques",
        "description": "Prendre d'urgence des mesures pour lutter contre les changements climatiques",
    },
    {
        "code": "14",
        "title": "Vie aquatique",
        "description": "Conserver et exploiter de manière durable les océans",
    },
    {
        "code": "15",
        "title": "Vie terrestre",
        "description": "Préserver et restaurer les écosystèmes",
    },
    {
        "code": "16",
        "title": "Paix, justice et institutions efficaces",
        "description": "Promouvoir la paix et l'inclusion",
    },
    {
        "code": "17",
        "title": "Partenariats pour la réalisation des objectifs",
        "description": "Partenaire mondial pour la réalisation des objectifs",
    },
]

for data in odds:
    goal = SDGGoal(**data)
    db.add(goal)
db.flush()

# Créer des projets de test avec géolocalisation
projects_data = [
    ("PROJ001", "Vaccination Centre Douala", "SANTE", "Vaccination des enfants", 1, 4.05, 9.75),
    ("PROJ002", "École Bilingue Yaoundé", "EDUCATION", "Construction école", 2, 3.87, 11.53),
    ("PROJ003", "Forage d'eau Kfemen", "EAU", "Accès à l'eau potable", 5, 2.9, 12.4),
    ("PROJ004", "Route Bafoussam-Mbouda", "INFRASTRUCTURE", "Infrastructure routière", 3, 5.76, 10.42),
    ("PROJ005", "Micro-hydro Buea", "ENERGIE", "Énergie renouvelable", 4, 4.15, 9.74),
    ("PROJ006", "Santé maternelle Douala", "SANTE", "Services santé mère-enfant", 1, 4.05, 9.75),
    ("PROJ007", "Agriculture durable Yaoundé", "AGRICULTURE", "Cultures durables", 2, 3.87, 11.53),
    ("PROJ008", "Reforestation Centre", "ENVIRONNEMENT", "Plantation d'arbres", 3, 5.76, 10.42),
]

for code, title, sector, desc, commune_id, lat, lon in projects_data:
    p = Project(
        code=code,
        title=title,
        chapitre=sector,
        objectif_specifique=desc,
        commune_id=commune_id,
        latitude=lat,
        longitude=lon,
    )
    db.add(p)

db.commit()
print(f"✓ Seed completed:")
print(f"  - {len(deps)} departments")
print(f"  - {len(communes_data)} communes with geolocation")
print(f"  - {len(odds)} ODD (SDG Goals)")
print(f"  - {len(projects_data)} projects with geolocation")
db.close()
