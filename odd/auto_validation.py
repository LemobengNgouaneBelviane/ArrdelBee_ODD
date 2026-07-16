"""
Moteur de vérification automatique de complétude d'un projet ODD.

Déclenché à la demande par un Validateur CTD/ARRDEL ou un Administrateur
(cf. ProjectViewSet.check_completeness dans views.py) — pas automatiquement
à l'instant de la soumission, afin de laisser le projet visible au statut
'submitted' en attente de revue humaine.

Rôle unique : vérifier la COMPLÉTUDE du dossier.
La cohérence sémantique des alignements (ODD, SND30, PCD/PRD) est désormais
garantie en amont par alignment_validator.py au moment du sync_alignments.
Ce module ne revalide donc plus cette cohérence pour éviter tout double emploi.

Niveaux :
  Niveau 1 — Rejet immédiat  : éléments obligatoires manquants
  Niveau 2 — À compléter    : éléments recommandés manquants
  Niveau 3 — Validé         : dossier complet
"""
from .models import Project, ProjectSDGAlignment, ProjectSND30Alignment, ProjectWorkflowTrace


def _record_trace(project: Project, from_s: str, to_s: str, comment: str, actor=None):
    ProjectWorkflowTrace.objects.create(
        project=project,
        actor=actor,
        from_status=from_s,
        to_status=to_s,
        comment=comment,
    )


def auto_validate(project: Project, actor=None) -> tuple:
    """
    Retourne (new_status: str, reason: str).
    new_status : 'validated' | 'rejected' | 'needs_completion'
    """
    from_status = project.status

    # ── Niveau 1 : Complétude obligatoire — bloquant ──────────────────────
    errors = []

    if not project.description or len(project.description.strip()) < 20:
        errors.append(
            f"• Description insuffisante ({len((project.description or '').strip())} car.) "
            "— minimum 20 caractères requis pour caractériser le projet."
        )

    if not project.start_date:
        errors.append(
            "• Date de début manquante — obligatoire pour le suivi temporel du projet."
        )

    if not project.budget or float(project.budget) <= 0:
        errors.append(
            "• Budget manquant ou nul — renseignez le coût prévisionnel du projet."
        )

    sdg_alignments = list(
        ProjectSDGAlignment.objects
        .filter(project=project)
        .select_related('indicator__target__sdg')
    )
    if len(sdg_alignments) == 0:
        errors.append(
            "• Aucun indicateur ODD aligné — retournez à l'étape « Mapping ODD » "
            "et sélectionnez au moins un indicateur."
        )

    if project.preuves.count() == 0:
        errors.append(
            "• Aucune preuve documentaire jointe — déposez au moins un document "
            "(rapport, photo, procès-verbal, délibération…) pour justifier le projet."
        )

    if errors:
        reason = (
            "❌ REJET — Dossier incomplet.\n\n"
            "Le projet a été rejeté pour les raisons suivantes :\n\n"
            + "\n".join(errors)
            + "\n\nCorrigez ces points et soumettez à nouveau."
        )
        _record_trace(project, from_status, 'rejected', reason, actor)
        return 'rejected', reason

    # ── Niveau 2 : Recommandations — non bloquant ────────────────────────
    warnings = []

    snd30_count = ProjectSND30Alignment.objects.filter(project=project).count()
    if snd30_count == 0:
        warnings.append(
            "• Aucun axe SND30 aligné — l'alignement sur la Stratégie Nationale "
            "de Développement 2030 est requis pour une certification complète."
        )

    if not project.local_priorities:
        warnings.append(
            "• Aucune priorité PCD/PRD renseignée — alignez le projet sur les plans "
            "locaux de développement (PCD/PRD) pour renforcer sa légitimité territoriale."
        )

    if len(sdg_alignments) < 3:
        warnings.append(
            f"• Seulement {len(sdg_alignments)} indicateur(s) ODD sélectionné(s) — "
            "un alignement sur 3 indicateurs ou plus renforce la crédibilité du dossier."
        )

    if not project.beneficiaries_count:
        warnings.append(
            "• Nombre de bénéficiaires non renseigné — "
            "cette donnée est utile pour mesurer l'impact social du projet."
        )

    if warnings:
        reason = (
            "⚠️ À COMPLÉTER — Le projet est partiellement conforme.\n\n"
            "Les éléments suivants doivent être complétés avant la certification finale :\n\n"
            + "\n".join(warnings)
            + "\n\nComplétez ces points et soumettez à nouveau."
        )
        # On calcule quand même les scores pour donner une idée de l'avancement
        project.update_scores()
        _record_trace(project, from_status, 'needs_completion', reason, actor)
        return 'needs_completion', reason

    # ── Niveau 3 : Validé ─────────────────────────────────────────────────
    # On fige les scores définitifs lors de la validation réussie
    project.update_scores()
    _record_trace(
        project,
        from_status,
        'validated',
        "✅ Validation automatique réussie — dossier complet, alignements ODD/SND30/PCD-PRD conformes.",
        actor,
    )
    return 'validated', ''
