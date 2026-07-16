from django.db import models
from django.conf import settings
from django.utils import timezone


class Sector(models.Model):
    """Secteur thématique d'un projet (Santé, Eau, Éducation…)."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ('draft',              'Brouillon'),
        ('submitted',          'Soumis'),
        ('controlling_ctd',    'En contrôle CTD'),
        ('validated_ctd',      'Validé CTD'),
        ('controlling_arrdel', 'En contrôle ARRDEL'),
        ('validated',          'Validé'),
        ('rejected',           'Rejeté'),
        ('needs_completion',   'À compléter'),
    ]

    name        = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    # Dates
    start_date  = models.DateField(null=True, blank=True)
    end_date    = models.DateField(null=True, blank=True)

    # Territoire — CharField libre + FK Commune (optionnel)
    territory   = models.CharField(max_length=255, blank=True)
    commune     = models.ForeignKey(
        'locations.Commune', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='odd_projects',
    )

    # Secteur
    sector = models.ForeignKey(
        Sector, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='projects',
    )

    # Financier
    budget             = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    beneficiaries_count = models.IntegerField(null=True, blank=True)

    # Alignement local (priorités PCD/PRD)
    local_priorities = models.JSONField(default=list, blank=True)

    # Validation
    rejection_reason = models.TextField(blank=True, default='')

    # Publication Open Data
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)

    # Scores (Snapshots lors de la certification/validation)
    score_odd    = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    score_snd30  = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    score_local  = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    score_global = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    grade        = models.CharField(max_length=2, blank=True, default='')

    # Relations
    owner      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def update_scores(self, save=True):
        """
        Calcule les scores d'alignement ODD, SND30 et Local.
        Logique alignée sur le frontend (oddScores.ts).
        """
        # 1. Score ODD
        # Logic: Math.min(100, oddNumbers.size * 12 + indicators * 4)
        alignments = self.sdg_alignments.select_related('indicator__target__sdg')
        indicators_count = alignments.count()
        odd_numbers = set(a.indicator.target.sdg.number for a in alignments)
        
        self.score_odd = min(100, len(odd_numbers) * 12 + indicators_count * 4)

        # 2. Score SND30
        # Logic: Math.min(100, snd30 * 20)
        snd30_count = self.snd30_alignments.count()
        self.score_snd30 = min(100, snd30_count * 20)

        # 3. Score Local
        # Logic: Math.min(100, local * 20)
        local_count = len(self.local_priorities) if isinstance(self.local_priorities, list) else 0
        self.local_local = min(100, local_count * 20) # Oops, typo in plan? Plan said score_local
        self.score_local = min(100, local_count * 20)

        # 4. Score Global
        # Logic: Math.round(odd * 0.45 + snd30Score * 0.3 + localScore * 0.25)
        global_val = (
            float(self.score_odd) * 0.45 +
            float(self.score_snd30) * 0.3 +
            float(self.score_local) * 0.25
        )
        self.score_global = round(global_val)

        # 5. Grade
        g = self.score_global
        if g >= 90: self.grade = 'A'
        elif g >= 80: self.grade = 'B'
        elif g >= 70: self.grade = 'C'
        elif g >= 60: self.grade = 'D'
        else: self.grade = 'E'

        if save:
            self.save(update_fields=[
                'score_odd', 'score_snd30', 'score_local', 'score_global', 'grade'
            ])
        return self.score_global


class SDG(models.Model):
    number = models.IntegerField(unique=True)
    name   = models.TextField()
    color  = models.CharField(max_length=20)

    def __str__(self):
        return f"ODD {self.number}: {self.name}"


class SDGTarget(models.Model):
    sdg         = models.ForeignKey(SDG, on_delete=models.CASCADE, related_name='targets')
    code        = models.CharField(max_length=10, unique=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.code}: {self.description[:50]}..."


class SDGIndicator(models.Model):
    FREQUENCY_CHOICES = [
        ('annuelle',      'Annuelle'),
        ('semestrielle',  'Semestrielle'),
        ('trimestrielle', 'Trimestrielle'),
        ('mensuelle',     'Mensuelle'),
        ('ponctuelle',    'Ponctuelle'),
    ]

    target      = models.ForeignKey(SDGTarget, on_delete=models.CASCADE, related_name='indicators')
    code        = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    unit        = models.CharField(max_length=100, default='Proportion/Count')
    frequency   = models.CharField(max_length=15, choices=FREQUENCY_CHOICES, default='annuelle')

    def __str__(self):
        return f"{self.code}: {self.description[:50]}..."


class ProjectSDGAlignment(models.Model):
    project    = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sdg_alignments')
    indicator  = models.ForeignKey(SDGIndicator, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'indicator')


class SND30Axis(models.Model):
    number      = models.IntegerField(unique=True)
    name        = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"Axe {self.number}: {self.name}"


class ProjectSND30Alignment(models.Model):
    project    = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='snd30_alignments')
    axis       = models.ForeignKey(SND30Axis, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'axis')


def preuve_upload_path(instance, filename):
    return f"preuves/project_{instance.project_id}/{filename}"


class Preuve(models.Model):
    TYPE_CHOICES = [
        ('pdf',   'Document PDF'),
        ('image', 'Image / Photo / Scan'),
        ('excel', 'Tableur Excel / CSV'),
        ('word',  'Document Word'),
        ('autre', 'Autre'),
    ]

    project       = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='preuves',
    )
    titre         = models.CharField(max_length=255)
    description   = models.TextField(blank=True, default='')
    type_document = models.CharField(max_length=10, choices=TYPE_CHOICES, default='pdf')
    fichier       = models.FileField(upload_to=preuve_upload_path)
    hash_sha256   = models.CharField(max_length=64, blank=True, default='')
    taille        = models.BigIntegerField(default=0)
    uploaded_by   = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='preuves_deposees',
    )
    date_depot = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_depot']

    def __str__(self):
        return f"{self.titre} ({self.get_type_document_display()})"


class OddRoleRequest(models.Model):
    """Demande de rôle ODD soumise par un utilisateur, validée par un admin."""

    ROLE_CHOICES = [
        ('Responsable Projet',    'Responsable Projet'),
        ('Point Focal ODD',       'Point Focal ODD'),
        ('Validateur CTD',        'Validateur CTD'),
        ('Validateur ARRDEL',     'Validateur ARRDEL'),
        ('Admin CTD',             'Admin CTD'),
        ('Admin ARRDEL',          'Admin ARRDEL'),
        ('Responsable Sectoriel', 'Responsable Sectoriel'),
        ('Décideur',              'Décideur'),
        ('Partenaire',            'Partenaire'),
        ('Citoyen',               'Citoyen'),
    ]
    STATUS_CHOICES = [
        ('pending',  'En attente'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='odd_role_request',
    )
    requested_role = models.CharField(max_length=60, choices=ROLE_CHOICES)
    motivation     = models.TextField(blank=True, default='')
    status         = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    created_at    = models.DateTimeField(auto_now_add=True)
    reviewed_at   = models.DateTimeField(null=True, blank=True)
    reviewed_by   = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='odd_role_reviews',
    )
    review_comment = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} → {self.requested_role} ({self.status})"


class Period(models.Model):
    QUARTER_CHOICES = [(1, 'T1'), (2, 'T2'), (3, 'T3'), (4, 'T4')]

    label    = models.CharField(max_length=100)
    year     = models.IntegerField()
    quarter  = models.IntegerField(choices=QUARTER_CHOICES, null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year', '-quarter']
        constraints = [
            models.UniqueConstraint(fields=['year', 'quarter'], name='unique_year_quarter'),
        ]

    def __str__(self):
        return self.label


class MesureKPI(models.Model):
    STATUS_CHOICES = [
        ('draft',     'Brouillon'),
        ('submitted', 'Soumis'),
        ('validated', 'Validé'),
        ('rejected',  'Rejeté'),
    ]

    project   = models.ForeignKey(Project,       on_delete=models.CASCADE, related_name='mesures_kpi')
    indicator = models.ForeignKey(SDGIndicator,  on_delete=models.CASCADE, related_name='mesures')
    period    = models.ForeignKey(Period,        on_delete=models.CASCADE, related_name='mesures')

    valeur        = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    valeur_cible  = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    statut        = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    commentaire   = models.TextField(blank=True, default='')

    saisi_par  = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='mesures_saisies',
    )
    date_saisie = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_saisie']
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'indicator', 'period'],
                name='unique_project_indicator_period',
            ),
        ]

    def __str__(self):
        return f"{self.project.name} / {self.indicator.code} / {self.period.label}: {self.valeur}"


class ProjectWorkflowTrace(models.Model):
    """Journal immuable de toutes les transitions de statut d'un projet."""
    project     = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='workflow_history')
    actor       = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='odd_workflow_actions',
    )
    from_status = models.CharField(max_length=30)
    to_status   = models.CharField(max_length=30)
    comment     = models.TextField(blank=True, default='')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.project.name}: {self.from_status} → {self.to_status}"


class CampagneReporting(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planifiée'),
        ('open',    'Ouverte'),
        ('closed',  'Clôturée'),
    ]

    label       = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    year        = models.IntegerField()
    quarter     = models.IntegerField(choices=Period.QUARTER_CHOICES, null=True, blank=True)
    start_date  = models.DateField()
    end_date    = models.DateField()
    deadline    = models.DateField()
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='planned')
    created_by  = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='campagnes_creees',
    )
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.label

    @property
    def is_active(self):
        from django.utils import timezone
        today = timezone.now().date()
        return self.status == 'open' and self.start_date <= today <= self.end_date


class Rapport(models.Model):
    TYPE_CHOICES = [
        ('trimestriel', 'Rapport trimestriel'),
        ('annuel',      'Rapport annuel'),
        ('portefeuille','Rapport portefeuille'),
        ('synthese',    'Note de synthèse décisionnelle'),
    ]
    STATUS_CHOICES = [
        ('generated', 'Généré'),
        ('validated', 'Validé'),
        ('archived',  'Archivé'),
    ]

    type         = models.CharField(max_length=15, choices=TYPE_CHOICES)
    title        = models.CharField(max_length=255)
    period       = models.ForeignKey(
        Period, on_delete=models.SET_NULL, null=True, blank=True, related_name='rapports',
    )
    campagne     = models.ForeignKey(
        CampagneReporting, on_delete=models.SET_NULL, null=True, blank=True, related_name='rapports',
    )
    content      = models.JSONField(default=dict)
    status       = models.CharField(max_length=10, choices=STATUS_CHOICES, default='generated')
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='rapports_generes',
    )
    generated_at = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.get_type_display()} — {self.title}"


class PCDObjective(models.Model):
    """Objectif extrait des Cadres Logiques PCD des communes (Bafoussam I/II/III)."""
    commune_nom          = models.CharField(max_length=100)
    commune              = models.ForeignKey(
        'locations.Commune', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='pcd_objectives',
    )
    secteur              = models.CharField(max_length=200, blank=True)
    programme            = models.CharField(max_length=300, blank=True)
    objectif_global      = models.TextField()
    code_objectif_global = models.CharField(max_length=20, blank=True)
    objectif_specifique  = models.TextField(blank=True)
    resultats            = models.TextField(blank=True)
    budget               = models.BigIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['commune_nom', 'secteur', 'code_objectif_global']

    def __str__(self):
        return f"[{self.commune_nom}] {self.objectif_global[:60]}"


# ──────────────────────────────────────────────────────────────────────────
# GADD — Grille d'Analyse de Développement Durable
# Référentiel officiel : 6 dimensions, thèmes, 166 objectifs.
# ──────────────────────────────────────────────────────────────────────────

class GaddDimension(models.Model):
    KEY_CHOICES = [
        ('sociale',       'Sociale'),
        ('ecologique',    'Écologique'),
        ('economique',    'Économique'),
        ('culturelle',    'Culturelle'),
        ('ethique',       'Éthique'),
        ('gouvernance',   'Gouvernance'),
    ]

    key         = models.CharField(max_length=20, choices=KEY_CHOICES, unique=True)
    label       = models.CharField(max_length=50)
    description = models.TextField(blank=True, default='')
    order       = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label


class GaddTheme(models.Model):
    dimension = models.ForeignKey(GaddDimension, on_delete=models.CASCADE, related_name='themes')
    number    = models.IntegerField()
    label     = models.CharField(max_length=255)

    class Meta:
        ordering = ['dimension__order', 'number']
        unique_together = ('dimension', 'number')

    def __str__(self):
        return f"{self.dimension.label} — {self.number}. {self.label}"


class GaddObjective(models.Model):
    theme = models.ForeignKey(GaddTheme, on_delete=models.CASCADE, related_name='objectives')
    code  = models.CharField(max_length=10)   # ex: "1.1"
    label = models.TextField()

    class Meta:
        ordering = ['theme__number', 'code']
        unique_together = ('theme', 'code')

    def __str__(self):
        return f"{self.code} — {self.label[:60]}"


class GaddEvaluation(models.Model):
    """Fiche d'évaluation GADD d'un projet — un snapshot courant par projet."""
    project      = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='gadd_evaluation')
    evaluated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='gadd_evaluations',
    )
    evaluated_at = models.DateTimeField(auto_now=True)

    # Portée : thèmes GADD jugés pertinents pour CE projet — chaque projet a ses
    # propres objectifs, plutôt que de forcer la revue des 166 objectifs officiels.
    # Tant que cette liste est vide, aucun thème n'est considéré comme cadré.
    relevant_theme_ids = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Évaluation GADD — {self.project.name}"

    def compute_dimension_scores(self):
        """
        Retourne { dimension_key: moyenne_pct } à partir des réponses renseignées
        (evaluation_pct non nul). Une dimension sans réponse n'apparaît pas.
        """
        answers = list(
            self.answers.filter(evaluation_pct__isnull=False)
            .select_related('objective__theme__dimension')
        )
        buckets = {}
        for a in answers:
            key = a.objective.theme.dimension.key
            buckets.setdefault(key, []).append(float(a.evaluation_pct))
        return {k: round(sum(v) / len(v), 2) for k, v in buckets.items()}

    def compute_global_score(self):
        scores = self.compute_dimension_scores()
        if not scores:
            return 0.0
        return round(sum(scores.values()) / len(scores), 2)

    def compute_status(self) -> str:
        """
        'not_started' — aucun thème retenu et aucune réponse saisie ;
        'done'        — tous les objectifs des thèmes retenus sont évalués ;
        'in_progress' — un début d'évaluation existe mais n'est pas complet.
        """
        total = (
            GaddObjective.objects.filter(theme_id__in=self.relevant_theme_ids).count()
            if self.relevant_theme_ids else 0
        )
        answered = self.answers.filter(evaluation_pct__isnull=False).count()
        if total == 0 and answered == 0:
            return 'not_started'
        if total > 0 and answered >= total:
            return 'done'
        return 'in_progress'


class GaddObjectiveAnswer(models.Model):
    IMPORTANCE_CHOICES = [
        (1, 'Souhaitable'),
        (2, 'Important'),
        (3, 'Indispensable'),
    ]

    evaluation      = models.ForeignKey(GaddEvaluation, on_delete=models.CASCADE, related_name='answers')
    objective       = models.ForeignKey(GaddObjective, on_delete=models.CASCADE, related_name='answers')
    importance      = models.IntegerField(choices=IMPORTANCE_CHOICES, null=True, blank=True)
    evaluation_pct  = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    justification   = models.TextField(blank=True, default='')
    actions         = models.TextField(blank=True, default='')
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('evaluation', 'objective')

    def __str__(self):
        return f"{self.evaluation.project.name} / {self.objective.code}"
