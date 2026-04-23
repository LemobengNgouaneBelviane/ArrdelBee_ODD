#!/usr/bin/env python3
"""
Ajouter des projets de test avec les bons secteurs pour tester le système d'alignement.
"""

from sqlalchemy import select
from app.database import SessionLocal
from app.models import (
    Commune,
    Department,
    Project,
)

TEST_PROJECTS = [
    {
        "title": "Programme national de vaccination",
        "sector": "SANTE",
        "description": "Augmenter la couverture vaccinale de 50% en 2 ans",
        "dept": "RÉGION 1",
        "commune": "Commune A",
    },
    {
        "title": "Construction de 5 écoles primaires en zone rurale",
        "sector": "EDUCATION",
        "description": "Fournir l'accès à l'éducation primaire aux enfants",
        "dept": "RÉGION 2",
        "commune": "Commune D",
    },
    {
        "title": "Installation de puits forés pour l'eau potable",
        "sector": "EAU",
        "description": "Fournir l'accès à l'eau propre à 1000 ménages",
        "dept": "RÉGION 1",
        "commune": "Commune B",
    },
    {
        "title": "Construction de routes communales",
        "sector": "INFRASTRUCTURE",
        "description": "Améliorer l'accès aux services par le transport",
        "dept": "RÉGION 3",
        "commune": "Commune F",
    },
    {
        "title": "Installation de panneaux solaires",
        "sector": "MINEE_ENERGIE",
        "description": "Accès à l'énergie renouvelable pour 200 ménages",
        "dept": "RÉGION 2",
        "commune": "Commune E",
    },
    {
        "title": "Programme d'entrepreneuriat féminin",
        "sector": "MINCOMMERCE",
        "description": "Soutenir 100 femmes entrepreneurs avec micro-crédit",
        "dept": "RÉGION 4",
        "commune": "Commune H",
    },
    {
        "title": "Création d'une réserve naturelle",
        "sector": "MINEPDED",
        "description": "Protéger 500 hectares de biodiversité",
        "dept": "RÉGION 5",
        "commune": "Commune I",
    },
    {
        "title": "Production agricole durable",
        "sector": "MINADER",
        "description": "Former 200 fermiers à l'agriculture biologique",
        "dept": "RÉGION 1",
        "commune": "Commune C",
    },
]


def add_test_projects():
    db = SessionLocal()
    
    try:
        for proj_data in TEST_PROJECTS:
            # Trouver la commune
            dept = db.scalars(
                select(Department).where(Department.name == proj_data["dept"])
            ).first()
            if not dept:
                continue
            
            commune = db.scalars(
                select(Commune).where(
                    Commune.department_id == dept.id,
                    Commune.name == proj_data["commune"],
                )
            ).first()
            
            if not commune:
                continue
            
            # Vérifier que le projet n'existe pas
            existing = db.scalars(
                select(Project).where(Project.title == proj_data["title"])
            ).first()
            
            if not existing:
                project = Project(
                    title=proj_data["title"],
                    chapitre=proj_data["sector"],  # Le secteur en minuscules
                    objectif_specifique=proj_data["description"],
                    commune_id=commune.id,
                )
                db.add(project)
                print(f"✓ Ajout: {proj_data['title']} (secteur: {proj_data['sector']})")
        
        db.commit()
        
        # Vérifier les projets non-alignés
        unaligned_count = db.query(Project).count()
        print(f"\n✅ {unaligned_count} projets au total dans la base")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    add_test_projects()
