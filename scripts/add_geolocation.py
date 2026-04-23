"""
Script pour ajouter les coordonnées géographiques aux projets et communes.

Coordonnées réalistes pour les principales communes du Cameroun.
"""
import sys
from pathlib import Path

# Ajouter le chemin du projet
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import engine
from app.models import Commune, Project

# Coordonnées des communes principales (latitude, longitude)
COMMUNE_COORDS = {
    # Littoral
    "Douala": (4.0511, 9.7679),
    "Edéa": (3.8063, 10.1269),
    "Manenguba": (4.8, 9.6),
    "Nkongsamba": (4.9494, 9.9347),
    
    # Centre
    "Yaoundé": (3.8480, 11.5021),
    "Obala": (3.6433, 11.4033),
    "Abong-Mbang": (4.0769, 12.7128),
    "Ayos": (3.3344, 11.6139),
    
    # Sud
    "Ebolowa": (2.9239, 11.1542),
    "Kribi": (2.9388, 9.9155),
    "Dja": (3.35, 12.5),
    "Sangmelima": (2.9422, 11.9803),
    
    # Extrême-Nord
    "Maroua": (10.5929, 14.3158),
    "Kousseri": (12.0833, 15.0167),
    "Garoua": (9.3022, 13.3972),
    "Mora": (11.7228, 13.9858),
    
    # Nord
    "Garoua": (9.3022, 13.3972),
    "Meiganga": (6.5172, 12.1342),
    "Ngooundéré": (7.3226, 13.5781),
    "Gaoua": (6.3, 11.5),
    
    # Nord-Ouest
    "Bamenda": (5.9631, 10.1591),
    "Kumbo": (6.1833, 10.2333),
    "Menchum": (6.15, 10.15),
    "Santa": (5.7333, 10.05),
    
    # Sud-Ouest
    "Buea": (4.1551, 9.2414),
    "Kumba": (4.6396, 9.4469),
    "Limbe": (4.0211, 9.2387),
    "Mamfe": (5.7833, 8.9),
    
    # Ouest
    "Bafoussam": (5.7626, 10.4169),
    "Mbouda": (5.6333, 10.3),
    "Dschang": (5.6431, 10.0516),
    "Foumban": (6.0833, 10.6),
}

def add_geolocation():
    """Ajouter les coordonnées aux communes et projets."""
    
    with Session(engine) as db:
        # 1. Mettre à jour les communes
        communes = db.query(Commune).all()
        updated_count = 0
        
        for commune in communes:
            if commune.name in COMMUNE_COORDS:
                lat, lon = COMMUNE_COORDS[commune.name]
                commune.latitude = lat
                commune.longitude = lon
                updated_count += 1
            else:
                # Coordonnées par défaut (centre du Cameroun)
                commune.latitude = 3.8480
                commune.longitude = 11.5021
                updated_count += 1
        
        db.commit()
        print(f"✓ {updated_count} communes mises à jour avec coordonnées")
        
        # 2. Mettre à jour les projets (copier des communes)
        projects = db.query(Project).all()
        updated_projects = 0
        
        for project in projects:
            if project.commune and project.commune.latitude and project.commune.longitude:
                # Ajouter une petite variation aléatoire pour ne pas avoir tous les projets au même point
                import random
                offset = random.uniform(-0.01, 0.01)
                project.latitude = project.commune.latitude + offset
                project.longitude = project.commune.longitude + offset
                updated_projects += 1
        
        db.commit()
        print(f"✓ {updated_projects} projets mises à jour avec coordonnées")
        print("\n✅ Géolocalisation complète!")


if __name__ == "__main__":
    add_geolocation()
