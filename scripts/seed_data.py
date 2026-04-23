#!/usr/bin/env python3
"""
Script pour pré-remplir la base de données avec des données de test.
"""

from sqlalchemy import select
from app.database import SessionLocal
from app.models import (
    Commune,
    Department,
    Project,
    SDGGoal,
    SDGTarget,
    UNIndicator,
    AlignmentODD,
    AlignStatus,
)

# Données de test
DEPARTMENTS = [
    "RÉGION 1",
    "RÉGION 2",
    "RÉGION 3",
    "RÉGION 4",
    "RÉGION 5",
]

COMMUNES_BY_DEPT = {
    "RÉGION 1": ["Commune A", "Commune B", "Commune C"],
    "RÉGION 2": ["Commune D", "Commune E"],
    "RÉGION 3": ["Commune F", "Commune G"],
    "RÉGION 4": ["Commune H"],
    "RÉGION 5": ["Commune I", "Commune J"],
}

SECTORS = [
    "Santé",
    "Éducation",
    "Eau",
    "Infrastructure",
    "Énergie",
    "Économie",
    "Environnement",
    "Agriculture",
]

SAMPLE_PROJECTS = [
    {"title": "Programme d'immunisation", "sector": "Santé", "description": "Augmenter la couverture vaccinale"},
    {"title": "Construction école primaire", "sector": "Éducation", "description": "Accès à l'éducation"},
    {"title": "Forage d'eau potable", "sector": "Eau", "description": "Accès à l'eau propre"},
    {"title": "Route rurale", "sector": "Infrastructure", "description": "Amélioration infrastructures"},
    {"title": "Panneaux solaires", "sector": "Énergie", "description": "Énergie renouvelable"},
    {"title": "Coopérative agricole", "sector": "Agriculture", "description": "Support agriculteurs"},
    {"title": "Réserve naturelle", "sector": "Environnement", "description": "Protection biodiversité"},
    {"title": "Micro-crédit femmes", "sector": "Économie", "description": "Entrepreneuriat féminin"},
    {"title": "Centre de santé rural", "sector": "Santé", "description": "Services de santé"},
    {"title": "École secondaire", "sector": "Éducation", "description": "Formation jeunes"},
]

# Mapping secteur -> ODD codes
SECTOR_TO_ODD = {
    "Santé": ["3"],
    "Éducation": ["4"],
    "Eau": ["6"],
    "Infrastructure": ["9", "11"],
    "Énergie": ["7"],
    "Économie": ["8"],
    "Environnement": ["13", "15"],
    "Agriculture": ["2", "15"],
}

# 17 ODD avec targets et indicateurs basiques
ODD_DATA = {
    "1": {
        "title": "Pas de pauvreté",
        "targets": [
            {"code": "1.1", "title": "Éradiquer extrême pauvreté"},
            {"code": "1.2", "title": "Réduire pauvreté relative"},
        ],
    },
    "2": {
        "title": "Zéro faim",
        "targets": [
            {"code": "2.1", "title": "Éliminer faim"},
            {"code": "2.2", "title": "Nutrition"},
        ],
    },
    "3": {
        "title": "Bonne santé",
        "targets": [
            {"code": "3.1", "title": "Santé maternelle"},
            {"code": "3.3", "title": "Lutte épidémies"},
            {"code": "3.8", "title": "Couverture sanitaire"},
        ],
    },
    "4": {
        "title": "Éducation de qualité",
        "targets": [
            {"code": "4.1", "title": "Éducation primaire"},
            {"code": "4.2", "title": "Éducation préscolaire"},
        ],
    },
    "5": {
        "title": "Égalité des genres",
        "targets": [
            {"code": "5.1", "title": "Fin discriminations"},
            {"code": "5.2", "title": "Fin violences"},
        ],
    },
    "6": {
        "title": "Eau propre",
        "targets": [
            {"code": "6.1", "title": "Eau potable"},
            {"code": "6.2", "title": "Assainissement"},
        ],
    },
    "7": {
        "title": "Énergie propre",
        "targets": [
            {"code": "7.1", "title": "Accès électricité"},
            {"code": "7.2", "title": "Énergies renouvelables"},
        ],
    },
    "8": {
        "title": "Travail décent",
        "targets": [
            {"code": "8.1", "title": "Croissance économique"},
            {"code": "8.3", "title": "Entrepreneuriat"},
        ],
    },
    "9": {
        "title": "Industrie et Innovation",
        "targets": [
            {"code": "9.1", "title": "Infrastructure"},
            {"code": "9.3", "title": "Accès technologie"},
        ],
    },
    "10": {
        "title": "Inégalités réduites",
        "targets": [
            {"code": "10.1", "title": "Revenus croissants"},
        ],
    },
    "11": {
        "title": "Villes durables",
        "targets": [
            {"code": "11.1", "title": "Logement adéquat"},
            {"code": "11.2", "title": "Transport durable"},
        ],
    },
    "12": {
        "title": "Consommation responsable",
        "targets": [
            {"code": "12.2", "title": "Gestion déchets"},
        ],
    },
    "13": {
        "title": "Lutte changement climatique",
        "targets": [
            {"code": "13.1", "title": "Résilience climatique"},
        ],
    },
    "14": {
        "title": "Vie aquatique",
        "targets": [
            {"code": "14.1", "title": "Écosystèmes marins"},
        ],
    },
    "15": {
        "title": "Vie terrestre",
        "targets": [
            {"code": "15.1", "title": "Écosystèmes terrestres"},
            {"code": "15.2", "title": "Déforestation"},
        ],
    },
    "16": {
        "title": "Paix et justice",
        "targets": [
            {"code": "16.1", "title": "Violence réduite"},
        ],
    },
    "17": {
        "title": "Partenariats",
        "targets": [
            {"code": "17.1", "title": "Ressources financières"},
        ],
    },
}


def seed_database():
    db = SessionLocal()
    
    try:
        # 1. Créer les ODD, targets et indicateurs
        for odd_code, odd_info in ODD_DATA.items():
            goal = db.scalars(select(SDGGoal).where(SDGGoal.code == odd_code)).first()
            if goal is None:
                goal = SDGGoal(code=odd_code, title=odd_info["title"])
                db.add(goal)
                db.flush()
                
                # Créer les targets
                for target_info in odd_info["targets"]:
                    target = SDGTarget(
                        goal_id=goal.id,
                        code=target_info["code"],
                        title=target_info["title"],
                    )
                    db.add(target)
                    db.flush()
                    
                    # Créer les indicateurs
                    indicator = UNIndicator(
                        target_id=target.id,
                        code=f"{target_info['code']}.1",
                        name=f"Indicateur {target_info['code']}",
                    )
                    db.add(indicator)
        
        db.commit()
        print("✓ ODD, targets et indicateurs créés")
        
        # 2. Créer les départements et communes
        for dept_name in DEPARTMENTS:
            dept = db.scalars(select(Department).where(Department.name == dept_name)).first()
            if dept is None:
                dept = Department(name=dept_name)
                db.add(dept)
                db.flush()
                
                # Créer les communes
                for comm_name in COMMUNES_BY_DEPT.get(dept_name, []):
                    comm = db.scalars(
                        select(Commune).where(
                            Commune.department_id == dept.id,
                            Commune.name == comm_name,
                        )
                    ).first()
                    if comm is None:
                        comm = Commune(name=comm_name, department_id=dept.id)
                        db.add(comm)
        
        db.commit()
        print("✓ Départements et communes créés")
        
        # 3. Créer les projets
        all_comms = db.query(Commune).all()
        comm_idx = 0
        
        for proj_data in SAMPLE_PROJECTS:
            # Chercher une commune pour ce projet
            if comm_idx >= len(all_comms):
                comm_idx = 0
            commune = all_comms[comm_idx]
            comm_idx += 1
            
            project = db.scalars(
                select(Project).where(Project.title == proj_data["title"])
            ).first()
            if project is None:
                project = Project(
                    title=proj_data["title"],
                    chapitre=proj_data["sector"],
                    objectif_specifique=proj_data["description"],
                    commune_id=commune.id,
                )
                db.add(project)
                db.flush()
                
                # Sugérer les ODD pour ce secteur
                odd_codes = SECTOR_TO_ODD.get(proj_data["sector"], [])
                for odd_code in odd_codes:
                    # Prendre le premier indicateur de cet ODD
                    stmt = (
                        select(UNIndicator)
                        .join(SDGTarget, UNIndicator.target_id == SDGTarget.id)
                        .join(SDGGoal, SDGTarget.goal_id == SDGGoal.id)
                        .where(SDGGoal.code == odd_code)
                        .limit(1)
                    )
                    indicator = db.scalars(stmt).first()
                    if indicator:
                        alignment = AlignmentODD(
                            project_id=project.id,
                            indicator_id=indicator.id,
                            suggested=True,
                            status=AlignStatus.proposed,
                        )
                        db.add(alignment)
        
        db.commit()
        print(f"✓ {len(SAMPLE_PROJECTS)} projets créés")
        
        # Résumé
        dept_count = db.query(Department).count()
        comm_count = db.query(Commune).count()
        goal_count = db.query(SDGGoal).count()
        proj_count = db.query(Project).count()
        align_count = db.query(AlignmentODD).count()
        
        print("\n✅ Base de données pré-remplie:")
        print(f"  - {dept_count} départements")
        print(f"  - {comm_count} communes")
        print(f"  - {goal_count} ODD")
        print(f"  - {proj_count} projets")
        print(f"  - {align_count} alignements suggérés")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
