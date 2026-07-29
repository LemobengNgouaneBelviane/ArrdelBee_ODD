from rest_framework import serializers
from .models import (
    Project, Sector, SDG, SDGTarget, SDGIndicator,
    ProjectSDGAlignment, SND30Axis, ProjectSND30Alignment,
    ProjectWorkflowTrace, OddRoleRequest, Preuve,
    Period, MesureKPI, CampagneReporting, Rapport,
    PCDObjective,
    GaddDimension, GaddTheme, GaddObjective, GaddEvaluation, GaddObjectiveAnswer,
)


class PreuveSerializer(serializers.ModelSerializer):
    uploaded_by_email  = serializers.ReadOnlyField(source='uploaded_by.email')
    fichier_url        = serializers.SerializerMethodField()
    taille_lisible     = serializers.SerializerMethodField()
    type_document_label = serializers.ReadOnlyField(source='get_type_document_display')

    class Meta:
        model  = Preuve
        fields = [
            'id', 'project', 'titre', 'description', 'type_document', 'type_document_label',
            'fichier', 'fichier_url', 'hash_sha256', 'taille', 'taille_lisible',
            'uploaded_by', 'uploaded_by_email', 'date_depot',
        ]
        read_only_fields = ['hash_sha256', 'taille', 'uploaded_by', 'date_depot']

    def get_fichier_url(self, obj):
        request = self.context.get('request')
        if obj.fichier and request:
            return request.build_absolute_uri(obj.fichier.url)
        return None

    def get_taille_lisible(self, obj):
        t = obj.taille
        if t < 1024:        return f"{t} o"
        if t < 1024**2:     return f"{t/1024:.1f} Ko"
        if t < 1024**3:     return f"{t/1024**2:.1f} Mo"
        return f"{t/1024**3:.1f} Go"


class OddRoleRequestSerializer(serializers.ModelSerializer):
    user_email      = serializers.ReadOnlyField(source='user.email')
    user_full_name  = serializers.ReadOnlyField(source='user.full_name')
    reviewed_by_email = serializers.ReadOnlyField(source='reviewed_by.email')

    class Meta:
        model = OddRoleRequest
        fields = [
            'id', 'user', 'user_email', 'user_full_name',
            'requested_role', 'motivation', 'status',
            'created_at', 'reviewed_at', 'reviewed_by_email', 'review_comment',
        ]
        read_only_fields = ['user', 'status', 'reviewed_at', 'reviewed_by', 'review_comment']


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['id', 'name', 'description']


class SDGIndicatorSerializer(serializers.ModelSerializer):
    frequency_label = serializers.ReadOnlyField(source='get_frequency_display')

    class Meta:
        model = SDGIndicator
        fields = ['id', 'code', 'description', 'unit', 'frequency', 'frequency_label']


class SDGTargetSerializer(serializers.ModelSerializer):
    indicators = SDGIndicatorSerializer(many=True, read_only=True)

    class Meta:
        model = SDGTarget
        fields = ['id', 'code', 'description', 'indicators']


class SDGSerializer(serializers.ModelSerializer):
    targets = SDGTargetSerializer(many=True, read_only=True)

    class Meta:
        model = SDG
        fields = ['id', 'number', 'name', 'color', 'targets']


class SND30AxisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SND30Axis
        fields = ['id', 'number', 'name', 'description', 'pilier_number', 'pilier_title']


class ProjectSDGAlignmentSerializer(serializers.ModelSerializer):
    indicator_code        = serializers.ReadOnlyField(source='indicator.code')
    indicator_description = serializers.ReadOnlyField(source='indicator.description')
    target_code           = serializers.ReadOnlyField(source='indicator.target.code')
    target_description    = serializers.ReadOnlyField(source='indicator.target.description')
    sdg_number            = serializers.ReadOnlyField(source='indicator.target.sdg.number')
    sdg_name              = serializers.ReadOnlyField(source='indicator.target.sdg.name')

    class Meta:
        model = ProjectSDGAlignment
        fields = [
            'id', 'project', 'indicator',
            'indicator_code', 'indicator_description',
            'target_code', 'target_description',
            'sdg_number', 'sdg_name', 'created_at',
        ]


class ProjectSND30AlignmentSerializer(serializers.ModelSerializer):
    axis_number = serializers.ReadOnlyField(source='axis.number')
    axis_name   = serializers.ReadOnlyField(source='axis.name')

    class Meta:
        model = ProjectSND30Alignment
        fields = ['id', 'project', 'axis', 'axis_number', 'axis_name', 'created_at']


class WorkflowTraceSerializer(serializers.ModelSerializer):
    actor_email = serializers.ReadOnlyField(source='actor.email')

    class Meta:
        model = ProjectWorkflowTrace
        fields = ['id', 'from_status', 'to_status', 'comment', 'actor_email', 'created_at']


class ProjectSerializer(serializers.ModelSerializer):
    sdg_alignments   = ProjectSDGAlignmentSerializer(many=True, read_only=True)
    snd30_alignments = ProjectSND30AlignmentSerializer(many=True, read_only=True)
    workflow_history = WorkflowTraceSerializer(many=True, read_only=True)

    sector_name    = serializers.ReadOnlyField(source='sector.name')
    commune_name   = serializers.ReadOnlyField(source='commune.name')
    owner_email    = serializers.ReadOnlyField(source='owner.email')
    preuves_count  = serializers.SerializerMethodField()
    gadd_evaluated = serializers.SerializerMethodField()
    gadd_status    = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'status',
            'start_date', 'end_date',
            'territory', 'commune', 'commune_name',
            'sector', 'sector_name',
            'budget', 'beneficiaries_count',
            'local_priorities', 'rejection_reason',
            'is_published', 'published_at',
            'score_odd', 'score_snd30', 'score_local', 'score_global', 'grade',
            'owner', 'owner_email',
            'sdg_alignments', 'snd30_alignments',
            'workflow_history',
            'preuves_count', 'gadd_evaluated', 'gadd_status',
            'created_at', 'updated_at',
        ]
        read_only_fields = [
            'owner', 'updated_at',
            'score_odd', 'score_snd30', 'score_local', 'score_global', 'grade',
            'is_published', 'published_at',
        ]

    def get_preuves_count(self, obj):
        return obj.preuves.count()

    def get_gadd_evaluated(self, obj):
        return hasattr(obj, 'gadd_evaluation')

    def get_gadd_status(self, obj):
        evaluation = getattr(obj, 'gadd_evaluation', None)
        return evaluation.compute_status() if evaluation else 'not_started'

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class PublicProjectDetailSerializer(serializers.ModelSerializer):
    """Fiche détaillée d'un projet publié, exposée sans authentification sur le portail public."""
    sdg_alignments   = ProjectSDGAlignmentSerializer(many=True, read_only=True)
    snd30_alignments = ProjectSND30AlignmentSerializer(many=True, read_only=True)
    sector_name      = serializers.ReadOnlyField(source='sector.name')
    commune_name     = serializers.ReadOnlyField(source='commune.name')
    status_label     = serializers.ReadOnlyField(source='get_status_display')

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'status', 'status_label',
            'start_date', 'end_date',
            'territory', 'commune_name', 'sector_name',
            'budget', 'beneficiaries_count',
            'is_published', 'published_at',
            'score_odd', 'score_snd30', 'score_local', 'score_global', 'grade',
            'sdg_alignments', 'snd30_alignments',
            'created_at', 'updated_at',
        ]


class CampagneReportingSerializer(serializers.ModelSerializer):
    created_by_email = serializers.ReadOnlyField(source='created_by.email')
    is_active        = serializers.ReadOnlyField()

    class Meta:
        model = CampagneReporting
        fields = [
            'id', 'label', 'description', 'year', 'quarter',
            'start_date', 'end_date', 'deadline', 'status',
            'is_active', 'created_by', 'created_by_email', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class RapportSerializer(serializers.ModelSerializer):
    generated_by_email = serializers.ReadOnlyField(source='generated_by.email')
    period_label       = serializers.ReadOnlyField(source='period.label')
    campagne_label     = serializers.ReadOnlyField(source='campagne.label')
    type_label         = serializers.ReadOnlyField(source='get_type_display')
    status_label       = serializers.ReadOnlyField(source='get_status_display')

    class Meta:
        model = Rapport
        fields = [
            'id', 'type', 'type_label', 'title',
            'period', 'period_label', 'campagne', 'campagne_label',
            'content', 'status', 'status_label',
            'generated_by', 'generated_by_email',
            'generated_at', 'updated_at',
        ]
        read_only_fields = ['generated_by', 'generated_at', 'updated_at']


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ['id', 'label', 'year', 'quarter', 'is_closed', 'created_at']
        read_only_fields = ['created_at']


class MesureKPISerializer(serializers.ModelSerializer):
    indicator_code        = serializers.ReadOnlyField(source='indicator.code')
    indicator_description = serializers.ReadOnlyField(source='indicator.description')
    indicator_unit        = serializers.ReadOnlyField(source='indicator.unit')
    target_code           = serializers.ReadOnlyField(source='indicator.target.code')
    sdg_number            = serializers.ReadOnlyField(source='indicator.target.sdg.number')
    period_label          = serializers.ReadOnlyField(source='period.label')
    saisi_par_email       = serializers.ReadOnlyField(source='saisi_par.email')
    taux_realisation      = serializers.SerializerMethodField()

    class Meta:
        model = MesureKPI
        fields = [
            'id', 'project', 'indicator',
            'indicator_code', 'indicator_description', 'indicator_unit',
            'target_code', 'sdg_number',
            'period', 'period_label',
            'valeur', 'valeur_cible', 'taux_realisation',
            'statut', 'commentaire',
            'saisi_par', 'saisi_par_email',
            'date_saisie', 'updated_at',
        ]
        read_only_fields = ['saisi_par', 'date_saisie', 'updated_at']

    def get_taux_realisation(self, obj):
        if obj.valeur is not None and obj.valeur_cible and float(obj.valeur_cible) != 0:
            return round((float(obj.valeur) / float(obj.valeur_cible)) * 100, 1)
        return None


class PCDObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PCDObjective
        fields = [
            'id', 'commune_nom', 'secteur', 'programme',
            'objectif_global', 'code_objectif_global',
            'objectif_specifique', 'resultats', 'budget',
        ]


# ──────────────────────────────────────────────────────────────────────────
# GADD — Référentiel (lecture seule) + fiche d'évaluation d'un projet
# ──────────────────────────────────────────────────────────────────────────

class GaddObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model  = GaddObjective
        fields = ['id', 'code', 'label']


class GaddThemeSerializer(serializers.ModelSerializer):
    objectives = GaddObjectiveSerializer(many=True, read_only=True)

    class Meta:
        model  = GaddTheme
        fields = ['id', 'number', 'label', 'objectives']


class GaddDimensionSerializer(serializers.ModelSerializer):
    themes = GaddThemeSerializer(many=True, read_only=True)

    class Meta:
        model  = GaddDimension
        fields = ['id', 'key', 'label', 'description', 'order', 'themes']


class GaddObjectiveAnswerSerializer(serializers.ModelSerializer):
    objective_code  = serializers.ReadOnlyField(source='objective.code')
    objective_label = serializers.ReadOnlyField(source='objective.label')
    theme_number    = serializers.ReadOnlyField(source='objective.theme.number')
    dimension_key   = serializers.ReadOnlyField(source='objective.theme.dimension.key')

    class Meta:
        model  = GaddObjectiveAnswer
        fields = [
            'id', 'objective', 'objective_code', 'objective_label',
            'theme_number', 'dimension_key',
            'importance', 'evaluation_pct', 'justification', 'actions',
            'updated_at',
        ]


class GaddEvaluationSerializer(serializers.ModelSerializer):
    answers           = GaddObjectiveAnswerSerializer(many=True, read_only=True)
    evaluated_by_email = serializers.ReadOnlyField(source='evaluated_by.email')
    dimension_scores  = serializers.SerializerMethodField()
    score_global      = serializers.SerializerMethodField()

    class Meta:
        model  = GaddEvaluation
        fields = [
            'id', 'project', 'evaluated_by', 'evaluated_by_email', 'evaluated_at',
            'relevant_theme_ids', 'answers', 'dimension_scores', 'score_global',
        ]
        read_only_fields = ['project', 'evaluated_by', 'evaluated_at']

    def get_dimension_scores(self, obj):
        return obj.compute_dimension_scores()

    def get_score_global(self, obj):
        return obj.compute_global_score()

