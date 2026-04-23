from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.models import AlignStatus, WorkflowLevel


class ProjectOut(BaseModel):
    id: int
    code: str | None = None
    title: str
    chapitre: str | None = None
    commune: str | None = None
    department: str | None = None


class UnalignedProjectOut(ProjectOut):
    suggested_sdg_codes: list[str] = Field(default_factory=list)


class AlignmentValidateIn(BaseModel):
    project_id: int
    indicator_id: int
    validated_by: str | None = None
    justification: str | None = None
    status: AlignStatus = AlignStatus.validated


class AlignmentOut(BaseModel):
    id: int
    project_id: int
    indicator_id: int
    status: AlignStatus
    suggested: bool
    justification: str | None = None
    created_at: datetime
    validated_at: datetime | None = None
    validated_by: str | None = None


class CollectionConfigOut(BaseModel):
    project_id: int
    required_proofs: str | None = None


class EvidenceUpdateIn(BaseModel):
    provided_list: str | None = None
    workflow_level: WorkflowLevel
    updated_by: str | None = None


class EvidenceOut(BaseModel):
    id: int
    project_id: int
    alignment_id: int | None = None
    required_list: str | None = None
    provided_list: str | None = None
    workflow_level: WorkflowLevel
    updated_at: datetime
    updated_by: str | None = None


class DashboardProjectImpactOut(BaseModel):
    project: ProjectOut
    sdg_goal_code: str | None = None
    un_indicator_code: str | None = None
    success_pct: float | None = None
    color: str
    proofs: str | None = None
    sdg_logo_ref: str | None = None  # ex: chemin/URL d’asset logo


class DepartmentOut(BaseModel):
    id: int
    name: str


class CommuneOut(BaseModel):
    id: int
    name: str
    department_id: int
    latitude: float | None = None
    longitude: float | None = None
    department_name: str | None = None


class ProjectListOut(BaseModel):
    id: int
    title: str
    chapitre: str | None = None
    commune_id: int | None = None
    commune: str | None = None
    department: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class ProjectGeoOut(BaseModel):
    """Projet avec coordonnées pour la cartographie"""
    id: int
    title: str
    chapitre: str | None = None
    commune: str | None = None
    latitude: float
    longitude: float
    is_aligned: bool = False
    alignment_count: int = 0


class ProjectCreateIn(BaseModel):
    title: str
    description: str | None = None
    sector: str | None = None  # Equivalent to chapitre
    department: str | None = None
    commune: str | None = None
    budget: float | None = None
    start_date: str | None = None
    end_date: str | None = None


class AlignmentCreateIn(BaseModel):
    project_id: int
    selected_odds: list[int] = []  # List of ODD (SDG) codes
    baseline: float | None = None
    target: float | None = None
    justification: str | None = None
    validated_by: str | None = None
    status: AlignStatus = AlignStatus.validated

