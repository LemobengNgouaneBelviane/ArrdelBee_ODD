from __future__ import annotations

from rapidfuzz import fuzz


DEFAULT_CHAPTER_TO_SDG = {
    # Santé
    "MINSANTE": ["3"],
    "SANTE": ["3"],
    "SANTÉ": ["3"],
    "HEALTH": ["3"],
    # Education
    "MINEDUB": ["4"],
    "MINESEC": ["4"],
    "EDUCATION": ["4"],
    "ÉDUCATION": ["4"],
    # Eau/assainissement
    "MINEE": ["6", "7"],
    "EAU": ["6"],
    "ASSAINISSEMENT": ["6"],
    "WATER": ["6"],
    # Agriculture / faim
    "MINADER": ["2"],
    "AGRICULTURE": ["2", "15"],
    "ELEVAGE": ["2"],
    "FARMING": ["2", "15"],
    # Environnement / climat
    "MINEPDED": ["13", "15"],
    "ENVIRONNEMENT": ["13", "15"],
    "ENVIRONMENT": ["13", "15"],
    # Infrastructures / villes
    "MINTP": ["9", "11"],
    "INFRASTRUCTURE": ["9", "11"],
    "INFRASTRUCTURES": ["9", "11"],
    "URBANISME": ["11"],
    "TRANSPORT": ["9"],
    # Gouvernance / institutions
    "MINAT": ["16"],
    "GOUVERNANCE": ["16"],
    "INSTITUTION": ["16"],
    # Économie / travail
    "MINCOMMERCE": ["8"],
    "ECONOMIE": ["8"],
    "ÉCONOMIE": ["8"],
    "EMPLOI": ["8"],
    "TRAVAIL": ["8"],
    # Énergie
    "MINEE_ENERGIE": ["7"],
    "ENERGIE": ["7"],
    "ÉNERGIE": ["7"],
    "ENERGY": ["7"],
}


def suggest_alignment(chapitre_projet: str | None) -> list[str]:
    """
    Propose automatiquement des codes ODD (objectifs) à partir du chapitre/secteur.
    Retourne une liste de codes (strings) ex: ["3"].
    Compatible avec secteurs en minuscules (français et anglais).
    """
    if not chapitre_projet:
        return []

    raw = chapitre_projet.strip().upper()
    if raw in DEFAULT_CHAPTER_TO_SDG:
        return DEFAULT_CHAPTER_TO_SDG[raw]

    # Fallback fuzzy sur les clés connues
    best_key = None
    best_score = 0
    for k in DEFAULT_CHAPTER_TO_SDG.keys():
        score = fuzz.partial_ratio(raw, k)
        if score > best_score:
            best_score = score
            best_key = k

    if best_key and best_score >= 70:  # Seuil baissé pour plus de flexibilité
        return DEFAULT_CHAPTER_TO_SDG[best_key]
    return []

