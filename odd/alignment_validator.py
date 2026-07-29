"""
Moteur de validation sémantique des alignements ODD / SND30 / PCD-PRD.
Approche : cosine similarity sur vecteurs de fréquence de termes (TF),
sans dépendance externe. Fonctionne entièrement côté backend Django.
"""
import math
import re
from collections import Counter

from .models import SDGIndicator

# ── Paramètres ────────────────────────────────────────────────────────────────
RELEVANCE_THRESHOLD = 0.10   # Score minimal pour qu'un indicateur soit jugé pertinent
MIN_INDICATORS       = 2     # Nombre minimal d'indicateurs ODD requis
TOP_SUGGESTIONS      = 5     # Nombre maximal de suggestions retournées

# ── Stopwords français ────────────────────────────────────────────────────────
_STOPWORDS = {
    'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'et', 'en', 'au', 'aux',
    'a', 'par', 'pour', 'sur', 'dans', 'avec', 'ce', 'qui', 'que', 'ou', 'mais',
    'donc', 'or', 'ni', 'car', 'se', 'sa', 'son', 'ses', 'leur', 'leurs',
    'il', 'elle', 'ils', 'elles', 'nous', 'vous', 'on', 'y', 'est', 'sont',
    'plus', 'tout', 'tous', 'toute', 'toutes', 'tres', 'bien', 'aussi', 'dont',
    'proportion', 'nombre', 'taux', 'part', 'mesure', 'niveau', 'valeur',
    'population', 'pays', 'monde', 'national', 'international', 'entre',
}

# ── Référentiels SND30 et PCD/PRD ─────────────────────────────────────────────
# Piliers et axes d'intervention officiels de la SND30 2020-2030 (cf. « La SND30
# en 30 points », MINEPAT). Le pilier 4 ne dispose pas d'une liste d'axes propre
# dans le document source (section dupliquant par erreur celle du pilier 3) : il
# est représenté ici par un axe unique correspondant à son intitulé.
_PILIER1 = "Transformation structurelle de l'économie"
_PILIER2 = "Développement du capital humain et du bien-être"
_PILIER3 = "Promotion de l'emploi et de l'insertion économique"
_PILIER4 = "Gouvernance, décentralisation et gestion stratégique de l'État"

_SND30_AXES = {
    1: {
        'title': 'Développement des industries et des services', 'pilier': _PILIER1,
        'desc': "Promotion de l'industrie manufacturière et rattrapage technologique ; filières prioritaires (énergie, agro-industrie, numérique, forêt-bois, textile, mines, hydrocarbures, chimie-pharmacie, construction-services)",
        'keywords': ['industrie', 'usine', 'manufacture', 'production', 'transformation', 'fabrication', 'filiere', 'technologie', 'numerique', 'manufacturier'],
    },
    2: {
        'title': 'Développement de la productivité et de la production agricoles', 'pilier': _PILIER1,
        'desc': "Amélioration des rendements agricoles, de la production vivrière et de l'agro-industrie",
        'keywords': ['agriculture', 'agricole', 'rendement', 'culture', 'elevage', 'semence', 'engrais', 'recolte', 'vivrier', 'exploitation', 'ferme'],
    },
    3: {
        'title': 'Développement des infrastructures productives', 'pilier': _PILIER1,
        'desc': "Infrastructures de transport, d'énergie et de numérique au service de la production",
        'keywords': ['infrastructure', 'route', 'transport', 'energie', 'port', 'aeroport', 'chemin', 'reseau', 'electrification', 'barrage', 'pont'],
    },
    4: {
        'title': "Intégration régionale et facilitation des échanges", 'pilier': _PILIER1,
        'desc': "Renforcement des échanges commerciaux régionaux et de l'intégration économique sous-régionale",
        'keywords': ['commerce', 'echange', 'exportation', 'importation', 'frontiere', 'regional', 'integration', 'douane', 'marche', 'commercial'],
    },
    5: {
        'title': 'Dynamisation du secteur privé', 'pilier': _PILIER1,
        'desc': "Amélioration du climat des affaires et soutien à l'investissement privé",
        'keywords': ['entreprise', 'investissement', 'prive', 'affaires', 'pme', 'entrepreneuriat', 'competitivite', 'investisseur', 'societe'],
    },
    6: {
        'title': "Préservation de l'environnement et protection de la nature", 'pilier': _PILIER1,
        'desc': "Gestion durable des ressources naturelles et lutte contre les changements climatiques",
        'keywords': ['environnement', 'foret', 'biodiversite', 'climat', 'pollution', 'dechet', 'ecosysteme', 'reboisement', 'nature', 'ressource'],
    },
    7: {
        'title': 'Transformation du système financier', 'pilier': _PILIER1,
        'desc': "Modernisation du secteur financier et amélioration de l'accès au financement",
        'keywords': ['banque', 'financement', 'credit', 'microfinance', 'epargne', 'assurance', 'bourse', 'financier', 'pret'],
    },
    8: {
        'title': "Amélioration de l'éducation, formation et employabilité", 'pilier': _PILIER2,
        'desc': "Accès à une éducation de qualité et adéquation formation-emploi",
        'keywords': ['education', 'ecole', 'formation', 'employabilite', 'competence', 'alphabetisation', 'enseignement', 'apprentissage', 'scolarisation', 'universite'],
    },
    9: {
        'title': 'Santé et nutrition', 'pilier': _PILIER2,
        'desc': "Amélioration de l'état de santé et nutritionnel des populations, couverture santé universelle",
        'keywords': ['sante', 'hopital', 'nutrition', 'maladie', 'vaccination', 'soins', 'medecin', 'dispensaire', 'maternite'],
    },
    10: {
        'title': "Promotion de l'accès aux facilités sociales de base", 'pilier': _PILIER2,
        'desc': "Accès à l'eau, à l'assainissement, au logement et aux services sociaux essentiels",
        'keywords': ['eau', 'assainissement', 'logement', 'potable', 'latrine', 'habitat', 'hygiene', 'adduction'],
    },
    11: {
        'title': 'Amélioration de la protection sociale', 'pilier': _PILIER2,
        'desc': "Renforcement des dispositifs de protection sociale et d'assistance aux populations vulnérables",
        'keywords': ['protection', 'social', 'vulnerable', 'assistance', 'handicap', 'indigent', 'filet'],
    },
    12: {
        'title': 'Promotion de la recherche-développement et de l\'innovation', 'pilier': _PILIER2,
        'desc': "Développement de la recherche scientifique et de l'innovation technologique",
        'keywords': ['recherche', 'innovation', 'technologie', 'laboratoire', 'scientifique', 'brevet', 'incubateur'],
    },
    13: {
        'title': "Promotion de l'emploi dans les projets d'investissement public", 'pilier': _PILIER3,
        'desc': "Création d'emplois locaux à travers les projets d'investissement public",
        'keywords': ['emploi', 'investissement', 'chantier', 'recrutement', 'travailleur', 'embauche', 'main'],
    },
    14: {
        'title': "Amélioration de la productivité agricole, de l'emploi et des revenus en milieu rural", 'pilier': _PILIER3,
        'desc': "Développement économique rural et amélioration des revenus agricoles",
        'keywords': ['rural', 'agricole', 'revenu', 'paysan', 'cooperative', 'campagne', 'agriculteur'],
    },
    15: {
        'title': "Promotion de la migration de l'informel vers le formel", 'pilier': _PILIER3,
        'desc': "Formalisation des activités économiques informelles",
        'keywords': ['informel', 'formel', 'formalisation', 'artisan', 'micro'],
    },
    16: {
        'title': "Création et préservation de l'emploi décent dans les grandes entreprises", 'pilier': _PILIER3,
        'desc': "Emploi décent et stable dans le secteur formel",
        'keywords': ['emploi', 'decent', 'entreprise', 'salarie', 'travail', 'contrat'],
    },
    17: {
        'title': "Mise en adéquation formation-emploi et insertion professionnelle", 'pilier': _PILIER3,
        'desc': "Adaptation des formations aux besoins du marché du travail",
        'keywords': ['formation', 'insertion', 'professionnelle', 'stage', 'apprentissage', 'orientation', 'qualification'],
    },
    18: {
        'title': 'Régulation du marché du travail', 'pilier': _PILIER3,
        'desc': "Encadrement et régulation des relations et conditions de travail",
        'keywords': ['travail', 'syndicat', 'chomage', 'contrat', 'reglementation', 'inspection'],
    },
    19: {
        'title': 'Gouvernance, décentralisation et gestion stratégique de l\'État', 'pilier': _PILIER4,
        'desc': "Renforcement de la gouvernance publique, décentralisation et transferts de compétences aux CTD",
        'keywords': ['gouvernance', 'decentralisation', 'institution', 'administration', 'etat', 'transparence', 'commune', 'collectivite', 'maire', 'conseil'],
    },
}

_PCD_PRD_PRIORITIES = {
    1: {
        'label': "Accès à l'eau potable et assainissement",
        'plan': 'PCD',
        'keywords': ['eau', 'potable', 'assainissement', 'forage', 'hydraulique',
                     'latrines', 'hygiene', 'puits', 'chateau', 'adduction', 'robinet'],
    },
    2: {
        'label': 'Désenclavement et voirie communale',
        'plan': 'PCD',
        'keywords': ['route', 'pont', 'piste', 'desenclavement', 'voirie',
                     'transport', 'acces', 'bitumage', 'goudronnage', 'chemin', 'troncon'],
    },
    3: {
        'label': 'Santé de proximité',
        'plan': 'PRD',
        'keywords': ['sante', 'hopital', 'centre', 'medecin', 'infirmier',
                     'medicament', 'soins', 'maladie', 'maternite', 'dispensaire', 'clinique'],
    },
    4: {
        'label': 'Électrification et énergies renouvelables',
        'plan': 'PRD',
        'keywords': ['electricite', 'energie', 'solaire', 'eclairage', 'electrification',
                     'renouvelable', 'panneau', 'reseau', 'courant', 'groupe', 'generateur'],
    },
    5: {
        'label': "Protection de l'environnement",
        'plan': 'PCD',
        'keywords': ['environnement', 'foret', 'reboisement', 'dechet', 'nature',
                     'protection', 'ecosysteme', 'plantation', 'bassin', 'erosion'],
    },
}


# ── Correspondance GADD → ODD (BROUILLON — à valider avec le référent GADD/ODD) ─
# Les 6 dimensions de la grille GADD 2016 ne correspondent pas officiellement
# aux 17 ODD (référentiels distincts, d'origines différentes). Cette table est
# une proposition de correspondance thématique, pas une norme. Les chevauche-
# ments entre dimensions sont normaux : les dimensions GADD ne sont pas
# mutuellement exclusives.
GADD_DIMENSION_TO_SDG = {
    'sociale':      [1, 2, 3, 4, 5, 10, 11],
    'ecologique':   [6, 7, 11, 12, 13, 14, 15],
    'economique':   [8, 9, 10, 11, 12],
    'culturelle':   [4, 11, 16],
    'ethique':      [5, 10, 16],
    'gouvernance':  [16, 17],
}

# Score moyen minimal (%) d'une dimension GADD pour que ses ODD associés
# reçoivent un bonus lors des suggestions/validations d'indicateurs.
GADD_RELEVANCE_THRESHOLD = 50
# Bonus additif appliqué au score de similarité texte (échelle 0-1).
GADD_BONUS_WEIGHT = 0.15


def _gadd_relevant_sdgs(project) -> set:
    """
    Numéros d'ODD associés aux dimensions GADD que ce projet couvre bien
    (moyenne des evaluation_pct >= GADD_RELEVANCE_THRESHOLD), d'après sa
    fiche d'évaluation GADD. Set vide si le projet n'a pas encore de fiche
    GADD — dans ce cas le calcul d'indicateurs reste inchangé (texte seul).
    """
    if project is None:
        return set()
    evaluation = getattr(project, 'gadd_evaluation', None)
    if not evaluation:
        return set()
    relevant = set()
    for dim_key, score in evaluation.compute_dimension_scores().items():
        if score >= GADD_RELEVANCE_THRESHOLD:
            relevant.update(GADD_DIMENSION_TO_SDG.get(dim_key, []))
    return relevant


# ── Utilitaires ───────────────────────────────────────────────────────────────

def _normalize(text: str) -> str:
    """Minuscule + suppression des accents pour la recherche de mots-clés."""
    text = text.lower()
    for src, dst in [('é','e'),('è','e'),('ê','e'),('ë','e'),('à','a'),('â','a'),
                     ('î','i'),('ï','i'),('ô','o'),('ù','u'),('û','u'),('ü','u'),('ç','c')]:
        text = text.replace(src, dst)
    return text


def _tokenize(text: str) -> list:
    text = _normalize(text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    return [t for t in text.split() if t not in _STOPWORDS and len(t) > 2]


def _cosine(tokens_a: list, tokens_b: list) -> float:
    if not tokens_a or not tokens_b:
        return 0.0
    ca, cb = Counter(tokens_a), Counter(tokens_b)
    vocab  = set(ca) | set(cb)
    na, nb = len(tokens_a), len(tokens_b)
    va = {w: ca[w] / na for w in vocab}
    vb = {w: cb[w] / nb for w in vocab}
    dot  = sum(va[w] * vb[w] for w in vocab)
    mag_a = math.sqrt(sum(v ** 2 for v in va.values()))
    mag_b = math.sqrt(sum(v ** 2 for v in vb.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def _project_text(project) -> str:
    return ' '.join(filter(None, [
        project.name or '',
        project.description or '',
        project.sector.name if project.sector else '',
        project.territory or '',
    ]))


def _fail(rejected, suggestions, message):
    return {'valid': False, 'rejected': rejected, 'suggestions': suggestions, 'message': message}


# ── Validation ODD ────────────────────────────────────────────────────────────

def validate_odd_choices(project, indicator_codes: list) -> dict:
    """
    Vérifie que chaque indicateur choisi est cohérent avec le projet.
    Retourne { valid, rejected, suggestions, message }.
    """
    if not indicator_codes:
        return _fail([], [], 'Aucun indicateur ODD sélectionné.')

    if len(indicator_codes) < MIN_INDICATORS:
        suggestions = _suggest_odd(_tokenize(_project_text(project)), indicator_codes, project=project)
        return _fail(
            [],
            suggestions,
            f'Sélectionnez au moins {MIN_INDICATORS} indicateurs ODD '
            f'(actuellement : {len(indicator_codes)}).',
        )

    proj_tokens = _tokenize(_project_text(project))
    indicators  = list(
        SDGIndicator.objects
        .filter(code__in=indicator_codes)
        .select_related('target__sdg')
    )

    gadd_bonus_sdgs = _gadd_relevant_sdgs(project)

    rejected = []
    for ind in indicators:
        ind_text  = f"{ind.description} {ind.target.description} {ind.target.sdg.name}"
        score     = _cosine(proj_tokens, _tokenize(ind_text))
        if ind.target.sdg.number in gadd_bonus_sdgs:
            score = min(1.0, score + GADD_BONUS_WEIGHT)
        if score < RELEVANCE_THRESHOLD:
            sector_label = project.sector.name if project.sector else 'ce projet'
            rejected.append({
                'code':       ind.code,
                'description': ind.description,
                'sdg_number': ind.target.sdg.number,
                'sdg_name':   ind.target.sdg.name,
                'score_pct':  round(score * 100),
                'reason': (
                    f"Score de pertinence : {round(score * 100)} %. "
                    f"L'indicateur \"{ind.description[:80]}\" "
                    f"ne présente pas de lien thématique suffisant avec le secteur "
                    f"« {sector_label} » et le contenu de ce projet."
                ),
            })

    if not rejected:
        return {'valid': True, 'rejected': [], 'suggestions': [], 'message': ''}

    suggestions = _suggest_odd(proj_tokens, indicator_codes, project=project)
    return _fail(
        rejected,
        suggestions,
        f"{len(rejected)} indicateur(s) rejeté(s) sur {len(indicators)} — "
        "cohérence insuffisante avec le projet. "
        "Consultez les suggestions et ajustez votre sélection.",
    )


def _suggest_odd(proj_tokens: list, exclude_codes: list, project=None) -> list:
    """
    Retourne toujours au moins TOP_SUGGESTIONS indicateurs.
    Les candidats sont triés par score décroissant. Le score de base est la
    similarité texte projet/indicateur ; si `project` a une fiche d'évaluation
    GADD, les indicateurs dont l'ODD est associé à une dimension GADD bien
    couverte par le projet reçoivent un bonus (voir GADD_DIMENSION_TO_SDG).
    Si aucun ne dépasse le seuil, on retourne quand même les meilleurs
    disponibles avec un message adapté.
    """
    gadd_bonus_sdgs = _gadd_relevant_sdgs(project)

    candidates = list(
        SDGIndicator.objects
        .exclude(code__in=exclude_codes)
        .select_related('target__sdg')
    )
    scored = []
    for ind in candidates:
        ind_text = f"{ind.description} {ind.target.description} {ind.target.sdg.name}"
        score    = _cosine(proj_tokens, _tokenize(ind_text))
        gadd_boosted = ind.target.sdg.number in gadd_bonus_sdgs
        if gadd_boosted:
            score = min(1.0, score + GADD_BONUS_WEIGHT)
        scored.append({
            'code':          ind.code,
            'description':   ind.description,
            'sdg_number':    ind.target.sdg.number,
            'sdg_name':      ind.target.sdg.name,
            'target_code':   ind.target.code,
            'score_pct':     round(score * 100),
            '_score':        score,
            '_gadd_boosted': gadd_boosted,
        })

    scored.sort(key=lambda x: x['_score'], reverse=True)
    top = scored[:TOP_SUGGESTIONS]

    for item in top:
        pct = item['score_pct']
        gadd_note = (
            " Ce lien est renforcé par le profil GADD du projet."
            if item['_gadd_boosted'] else ""
        )
        if pct >= 20:
            item['justification'] = (
                f"Score de pertinence : {pct} %. "
                f"Cet indicateur partage des termes thématiques importants "
                f"avec le contenu de votre projet.{gadd_note}"
            )
        elif pct >= RELEVANCE_THRESHOLD * 100:
            item['justification'] = (
                f"Score de pertinence : {pct} %. "
                f"Cet indicateur présente un lien modéré avec votre projet — "
                f"vérifiez s'il correspond bien aux activités prévues.{gadd_note}"
            )
        else:
            item['justification'] = (
                f"Correspondance thématique faible ({pct} %) mais cet indicateur "
                f"est parmi les plus proches disponibles pour l'ODD {item['sdg_number']}. "
                f"Précisez la description de votre projet pour améliorer la détection.{gadd_note}"
            )
        del item['_score']
        del item['_gadd_boosted']

    return top


# ── Validation SND30 ──────────────────────────────────────────────────────────

def validate_snd30_choices(project, axis_numbers: list) -> dict:
    """
    Vérifie que chaque axe SND30 sélectionné est cohérent avec le projet.
    """
    if not axis_numbers:
        return {'valid': True, 'rejected': [], 'suggestions': [], 'message': ''}

    proj_norm = _normalize(_project_text(project))
    rejected  = []

    for num in axis_numbers:
        axis = _SND30_AXES.get(num)
        if not axis:
            continue
        matches = [kw for kw in axis['keywords'] if kw in proj_norm]
        if not matches:
            rejected.append({
                'axis_number': num,
                'title':       axis['title'],
                'reason': (
                    f"Axe SND30 {num} — \"{axis['title']}\" — "
                    f"aucun terme caractéristique de cet axe n'a été trouvé "
                    f"dans le nom, la description ou le secteur du projet. "
                    f"Termes attendus pour cet axe : "
                    f"{', '.join(axis['keywords'][:6])}."
                ),
            })

    if not rejected:
        return {'valid': True, 'rejected': [], 'suggestions': [], 'message': ''}

    # Suggestions : toujours au moins les axes les plus pertinents disponibles
    candidates = []
    for num, axis in _SND30_AXES.items():
        if num in axis_numbers:
            continue
        matches = [kw for kw in axis['keywords'] if kw in proj_norm]
        candidates.append((len(matches), num, axis, matches))
    candidates.sort(reverse=True)

    suggestions = []
    for match_count, num, axis, matches in candidates[:3]:
        if match_count > 0:
            justif = (
                f"Termes communs détectés : {', '.join(matches[:4])}. "
                f"Cet axe correspond mieux aux activités de votre projet."
            )
        else:
            justif = (
                f"Aucun terme commun explicite, mais cet axe ({axis['title']}) "
                f"est proposé en alternative. Précisez la description du projet "
                f"pour affiner la détection."
            )
        suggestions.append({
            'axis_number': num,
            'title':       axis['title'],
            'description': axis['desc'],
            'justification': justif,
        })

    return _fail(
        rejected,
        suggestions,
        f"{len(rejected)} axe(s) SND30 rejeté(s) — "
        "aucun lien thématique avec le projet. "
        "Consultez les suggestions ci-dessous.",
    )


# ── Validation PCD/PRD ────────────────────────────────────────────────────────

def _pcd_text(obj) -> str:
    return ' '.join(filter(None, [
        obj.objectif_global,
        obj.objectif_specifique,
        obj.resultats,
        obj.secteur,
        obj.programme,
    ]))


def validate_pcd_prd_choices(project, priority_ids: list) -> dict:
    """
    Vérifie la cohérence des priorités PCD sélectionnées avec le projet.
    Si des PCDObjective existent pour la commune, on utilise les vraies données PCD.
    Sinon, fallback sur les catégories génériques _PCD_PRD_PRIORITIES.
    """
    if not priority_ids:
        return {'valid': True, 'rejected': [], 'suggestions': [], 'message': ''}

    from .models import PCDObjective

    commune_nom = None
    if project.commune:
        commune_nom = project.commune.name
    elif project.territory:
        commune_nom = project.territory

    use_db = False
    pcd_qs = PCDObjective.objects.none()
    if commune_nom:
        pcd_qs = PCDObjective.objects.filter(commune_nom__icontains=commune_nom.split()[0])
        use_db = pcd_qs.exists()
    if not use_db and project.commune:
        pcd_qs = PCDObjective.objects.filter(commune=project.commune)
        use_db = pcd_qs.exists()

    if use_db:
        return _validate_pcd_db(project, priority_ids, pcd_qs)
    return _validate_pcd_generic(project, priority_ids)


def _validate_pcd_db(project, priority_ids: list, pcd_qs) -> dict:
    """Validation contre les vraies données PCD importées en base."""
    proj_tokens = _tokenize(_project_text(project))
    objectives  = {obj.pk: obj for obj in pcd_qs}
    rejected    = []

    for pid in priority_ids:
        obj = objectives.get(pid)
        if not obj:
            continue
        score = _cosine(proj_tokens, _tokenize(_pcd_text(obj)))
        if score < RELEVANCE_THRESHOLD:
            rejected.append({
                'priority_id': pid,
                'label':       obj.objectif_global[:100],
                'plan':        f"PCD {obj.commune_nom}",
                'reason': (
                    f"Score de pertinence : {round(score * 100)} %. "
                    f"L'objectif PCD « {obj.objectif_global[:80]} » "
                    f"ne présente pas de lien thématique suffisant avec ce projet."
                ),
            })

    if not rejected:
        return {'valid': True, 'rejected': [], 'suggestions': [], 'message': ''}

    suggestions = _suggest_pcd_db(proj_tokens, priority_ids, pcd_qs)
    return _fail(
        rejected,
        suggestions,
        f"{len(rejected)} objectif(s) PCD rejeté(s) — "
        "cohérence insuffisante avec le projet. "
        "Consultez les suggestions.",
    )


def _suggest_pcd_db(proj_tokens: list, exclude_ids: list, pcd_qs) -> list:
    scored = []
    for obj in pcd_qs.exclude(pk__in=exclude_ids):
        score = _cosine(proj_tokens, _tokenize(_pcd_text(obj)))
        scored.append((score, obj))
    scored.sort(key=lambda x: x[0], reverse=True)

    suggestions = []
    for score, obj in scored[:TOP_SUGGESTIONS]:
        pct = round(score * 100)
        suggestions.append({
            'priority_id':   obj.pk,
            'label':         obj.objectif_global[:100],
            'plan':          f"PCD {obj.commune_nom}",
            'secteur':       obj.secteur,
            'score_pct':     pct,
            'justification': (
                f"Score de pertinence : {pct} %. "
                f"Cet objectif PCD de {obj.commune_nom} partage des termes "
                f"thématiques avec votre projet."
            ),
        })
    return suggestions


def suggest_pcd_objectives(project) -> list:
    """
    Retourne les PCDObjective les plus pertinents pour un projet donné.
    Utilisé par l'auto-fill et le frontend pour proposer des priorités locales.
    """
    from .models import PCDObjective

    commune_nom = None
    if project.commune:
        commune_nom = project.commune.name
    elif project.territory:
        commune_nom = project.territory

    if commune_nom:
        pcd_qs = PCDObjective.objects.filter(commune_nom__icontains=commune_nom.split()[0])
    else:
        pcd_qs = PCDObjective.objects.all()

    if not pcd_qs.exists():
        return []

    proj_tokens = _tokenize(_project_text(project))
    return _suggest_pcd_db(proj_tokens, [], pcd_qs)


def _validate_pcd_generic(project, priority_ids: list) -> dict:
    """Fallback : validation contre les catégories génériques codées en dur."""
    proj_norm = _normalize(_project_text(project))
    rejected  = []

    for pid in priority_ids:
        priority = _PCD_PRD_PRIORITIES.get(pid)
        if not priority:
            continue
        matches = [kw for kw in priority['keywords'] if kw in proj_norm]
        if not matches:
            rejected.append({
                'priority_id': pid,
                'label':       priority['label'],
                'plan':        priority['plan'],
                'reason': (
                    f"Priorité {priority['plan']} « {priority['label']} » — "
                    f"aucun terme attendu n'est présent dans le contenu du projet. "
                    f"Termes attendus : {', '.join(priority['keywords'][:6])}."
                ),
            })

    if not rejected:
        return {'valid': True, 'rejected': [], 'suggestions': [], 'message': ''}

    candidates = []
    for pid, priority in _PCD_PRD_PRIORITIES.items():
        if pid in priority_ids:
            continue
        matches = [kw for kw in priority['keywords'] if kw in proj_norm]
        candidates.append((len(matches), pid, priority, matches))
    candidates.sort(reverse=True)

    suggestions = []
    for match_count, pid, priority, matches in candidates[:3]:
        justif = (
            f"Termes communs : {', '.join(matches[:4])}. " if match_count > 0
            else f"Aucun terme commun explicite, mais « {priority['label']} » est proposé en alternative. "
        )
        suggestions.append({
            'priority_id': pid,
            'label':       priority['label'],
            'plan':        priority['plan'],
            'justification': justif,
        })

    return _fail(
        rejected,
        suggestions,
        f"{len(rejected)} priorité(s) PCD/PRD rejetée(s) — "
        "cohérence insuffisante avec le projet. "
        "Consultez les suggestions.",
    )
