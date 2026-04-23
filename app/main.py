from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.models import AlignStatus, AlignmentODD
from app.performance import compute_performance
from app.models import Commune, Department, Project
from app.schemas import (
    AlignmentCreateIn,
    AlignmentOut,
    AlignmentValidateIn,
    CollectionConfigOut,
    DashboardProjectImpactOut,
    DepartmentOut,
    EvidenceOut,
    EvidenceUpdateIn,
    CommuneOut,
    ProjectCreateIn,
    ProjectListOut,
    ProjectGeoOut,
    UnalignedProjectOut,
)


app = FastAPI(title="ODD ARRDEL API", version="0.1.0")

# Configurer CORS pour permettre au frontend de se connecter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Endpoints FR (officiels) ---
@app.get("/projets/non-alignes", response_model=list[UnalignedProjectOut], tags=["Projets"])
def api_list_unaligned_projects(limit: int = 200, db: Session = Depends(get_db)):
    rows = crud.list_unaligned_projects(db, limit=limit)
    out: list[UnalignedProjectOut] = []
    for r in rows:
        p = r["project"]
        out.append(
            UnalignedProjectOut(
                id=p.id,
                code=p.code,
                title=p.title,
                chapitre=p.chapitre,
                commune=p.commune.name if p.commune else None,
                department=p.commune.department.name if (p.commune and p.commune.department) else None,
                suggested_sdg_codes=r["suggested_sdg_codes"],
            )
        )
    return out


@app.post("/alignements/valider", response_model=list[AlignmentOut], tags=["Alignements"])
def api_validate_alignment(payload: AlignmentValidateIn | AlignmentCreateIn, db: Session = Depends(get_db)):
    """
    Valider un alignement (ancien format) ou créer des alignements multiples (nouveau format).
    """
    if isinstance(payload, AlignmentCreateIn) or hasattr(payload, "selected_odds"):
        # Nouveau format: ODD multiples
        payload = AlignmentCreateIn(**payload.dict()) if hasattr(payload, "dict") else payload
        alignments = crud.validate_alignment_multi_odds(
            db=db,
            project_id=payload.project_id,
            selected_odds=payload.selected_odds,
            baseline=payload.baseline,
            target=payload.target,
            justification=payload.justification,
            validated_by=payload.validated_by,
            status=payload.status,
        )
        return [AlignmentOut.model_validate(a, from_attributes=True) for a in alignments]
    else:
        # Ancien format: un seul ODD/indicateur
        alignment = crud.validate_alignment(
            db=db,
            project_id=payload.project_id,
            indicator_id=payload.indicator_id,
            validated_by=payload.validated_by,
            justification=payload.justification,
            status=payload.status,
        )
        return [AlignmentOut.model_validate(alignment, from_attributes=True)]


@app.get(
    "/projets/{project_id}/configuration-collecte",
    response_model=CollectionConfigOut,
    tags=["Collecte"],
)
def api_collection_config(project_id: int, db: Session = Depends(get_db)):
    req = crud.get_collection_config(db, project_id=project_id)
    if req is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return CollectionConfigOut(project_id=project_id, required_proofs=req)


@app.post("/projets/{project_id}/preuves", response_model=EvidenceOut, tags=["Collecte"])
def api_create_or_get_evidence(project_id: int, alignment_id: int | None = None, db: Session = Depends(get_db)):
    ev = crud.upsert_evidence_snapshot(db, project_id=project_id, alignment_id=alignment_id)
    return EvidenceOut.model_validate(ev, from_attributes=True)


@app.post("/preuves/{evidence_id}", response_model=EvidenceOut, tags=["Collecte"])
def api_update_evidence(evidence_id: int, payload: EvidenceUpdateIn, db: Session = Depends(get_db)):
    try:
        ev = crud.update_evidence(
            db,
            evidence_id=evidence_id,
            provided_list=payload.provided_list,
            workflow_level=payload.workflow_level,
            updated_by=payload.updated_by,
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return EvidenceOut.model_validate(ev, from_attributes=True)


@app.get("/projets/{project_id}/justification", tags=["Justification"])
def api_justification(project_id: int, db: Session = Depends(get_db)):
    txt = crud.get_justification(db, project_id=project_id)
    return {"project_id": project_id, "justification": txt}


@app.get("/tableau-de-bord/impact", response_model=list[DashboardProjectImpactOut], tags=["Restitution"])
def api_dashboard_impact(limit: int = 200, db: Session = Depends(get_db)):
    """
    Sortie agrégée pour tableaux de bord / rapports PDF:
    identité projet + logo ODD (référence) + score d’impact + preuves.
    """
    stmt = (
        db.query(AlignmentODD)
        .filter(AlignmentODD.status == AlignStatus.validated)
        .limit(limit)
    )
    alignments = stmt.all()
    out: list[DashboardProjectImpactOut] = []
    for a in alignments:
        p = a.project
        ind = a.indicator
        goal_code = ind.target.goal.code if (ind and ind.target and ind.target.goal) else None

        # KPI: on prend le premier KPI numérique si disponible
        kpi = p.kpis[0] if p and p.kpis else None
        perf = compute_performance(kpi.target_value if kpi else None, kpi.realized_value if kpi else None)

        proofs = p.source_verification if p else None
        out.append(
            DashboardProjectImpactOut(
                project={
                    "id": p.id,
                    "code": p.code,
                    "title": p.title,
                    "chapitre": p.chapitre,
                    "commune": p.commune.name if p.commune else None,
                    "department": p.commune.department.name if (p.commune and p.commune.department) else None,
                },
                sdg_goal_code=goal_code,
                un_indicator_code=ind.code if ind else None,
                success_pct=perf.success_pct,
                color=perf.color,
                proofs=proofs,
                sdg_logo_ref=(f"sdg-{goal_code}.png" if goal_code else None),
            )
        )
    return out


@app.get("/sante", tags=["Système"])
def health():
    return {"ok": True}


@app.get("/territoire/departements", response_model=list[DepartmentOut], tags=["Territoire"])
def api_list_departements(db: Session = Depends(get_db)):
    deps = db.query(Department).order_by(Department.name.asc()).all()
    return [DepartmentOut(id=d.id, name=d.name) for d in deps]


@app.get("/territoire/departements/{department_id}/communes", response_model=list[CommuneOut], tags=["Territoire"])
def api_list_communes(department_id: int, db: Session = Depends(get_db)):
    comms = (
        db.query(Commune)
        .filter(Commune.department_id == department_id)
        .order_by(Commune.name.asc())
        .all()
    )
    dep = db.get(Department, department_id)
    dep_name = dep.name if dep else None
    return [
        CommuneOut(id=c.id, name=c.name, department_id=c.department_id, department_name=dep_name)
        for c in comms
    ]


@app.get("/territoire/communes", response_model=list[CommuneOut], tags=["Territoire"])
def api_list_all_communes(db: Session = Depends(get_db)):
    comms = db.query(Commune).join(Department).order_by(Department.name.asc(), Commune.name.asc()).all()
    return [
        CommuneOut(
            id=c.id,
            name=c.name,
            department_id=c.department_id,
            department_name=(c.department.name if c.department else None),
        )
        for c in comms
    ]


@app.get("/projets", response_model=list[ProjectListOut], tags=["Projets"])
def api_list_projets(commune_id: int | None = None, limit: int = 500, db: Session = Depends(get_db)):
    q = db.query(Project)
    if commune_id is not None:
        q = q.filter(Project.commune_id == commune_id)
    q = q.limit(limit)
    projects = q.all()
    return [
        ProjectListOut(
            id=p.id,
            title=p.title,
            chapitre=p.chapitre,
            commune_id=p.commune_id,
            commune=(p.commune.name if p.commune else None),
            department=(p.commune.department.name if (p.commune and p.commune.department) else None),
        )
        for p in projects
    ]


@app.post("/projets", response_model=ProjectListOut, tags=["Projets"])
def api_create_project(payload: ProjectCreateIn, db: Session = Depends(get_db)):
    """Créer un nouveau projet."""
    project = crud.create_project(
        db=db,
        title=payload.title,
        description=payload.description,
        sector=payload.sector,
        department_name=payload.department,
        commune_name=payload.commune,
        budget=payload.budget,
        start_date=payload.start_date,
        end_date=payload.end_date,
    )
    return ProjectListOut(
        id=project.id,
        title=project.title,
        chapitre=project.chapitre,
        commune_id=project.commune_id,
        commune=(project.commune.name if project.commune else None),
        department=(project.commune.department.name if (project.commune and project.commune.department) else None),
    )


# --- Aliases EN (compatibilité) ---
@app.get("/projects/unaligned", response_model=list[UnalignedProjectOut], include_in_schema=False)
def alias_list_unaligned_projects(limit: int = 200, db: Session = Depends(get_db)):
    return api_list_unaligned_projects(limit=limit, db=db)


@app.post("/projects/create", response_model=ProjectListOut, include_in_schema=False)
def alias_create_project(payload: ProjectCreateIn, db: Session = Depends(get_db)):
    return api_create_project(payload=payload, db=db)


@app.post("/alignments/validate", response_model=list[AlignmentOut], include_in_schema=False)
def alias_validate_alignment(payload: AlignmentValidateIn | AlignmentCreateIn, db: Session = Depends(get_db)):
    return api_validate_alignment(payload=payload, db=db)


@app.get("/projects/{project_id}/collection-config", response_model=CollectionConfigOut, include_in_schema=False)
def alias_collection_config(project_id: int, db: Session = Depends(get_db)):
    return api_collection_config(project_id=project_id, db=db)


@app.post("/projects/{project_id}/evidence", response_model=EvidenceOut, include_in_schema=False)
def alias_create_or_get_evidence(project_id: int, alignment_id: int | None = None, db: Session = Depends(get_db)):
    return api_create_or_get_evidence(project_id=project_id, alignment_id=alignment_id, db=db)


@app.post("/evidence/{evidence_id}", response_model=EvidenceOut, include_in_schema=False)
def alias_update_evidence(evidence_id: int, payload: EvidenceUpdateIn, db: Session = Depends(get_db)):
    return api_update_evidence(evidence_id=evidence_id, payload=payload, db=db)


@app.get("/projects/{project_id}/justification", include_in_schema=False)
def alias_justification(project_id: int, db: Session = Depends(get_db)):
    return api_justification(project_id=project_id, db=db)


@app.get("/dashboard/impact", response_model=list[DashboardProjectImpactOut], include_in_schema=False)
def alias_dashboard_impact(limit: int = 200, db: Session = Depends(get_db)):
    return api_dashboard_impact(limit=limit, db=db)


@app.get("/health", include_in_schema=False)
def alias_health():
    return health()


# --- ENDPOINTS GEOLOCALISATION ---

@app.get("/projets/geolocalises/alignes", response_model=list[ProjectGeoOut], tags=["Cartographie"])
def api_projects_aligned_geo(commune_id: int | None = None, limit: int = 500, db: Session = Depends(get_db)):
    """
    Retourner projets alignés avec coordonnées géographiques pour la carte.
    Filtre par commune optionnellement.
    """
    q = db.query(Project).join(AlignmentODD).filter(
        AlignmentODD.status == AlignStatus.validated,
        Project.latitude.isnot(None),
        Project.longitude.isnot(None),
    )
    if commune_id is not None:
        q = q.filter(Project.commune_id == commune_id)
    
    projects = q.distinct().limit(limit).all()
    
    return [
        ProjectGeoOut(
            id=p.id,
            title=p.title,
            chapitre=p.chapitre,
            commune=(p.commune.name if p.commune else None),
            latitude=p.latitude,
            longitude=p.longitude,
            is_aligned=bool(p.alignments),
            alignment_count=len([a for a in p.alignments if a.status == AlignStatus.validated]),
        )
        for p in projects
    ]


@app.get("/projets/geolocalises", response_model=list[ProjectGeoOut], tags=["Cartographie"])
def api_projects_geo(commune_id: int | None = None, limit: int = 500, db: Session = Depends(get_db)):
    """
    Retourner tous projets avec coordonnées géographiques pour la carte.
    """
    q = db.query(Project).filter(
        Project.latitude.isnot(None),
        Project.longitude.isnot(None),
    )
    if commune_id is not None:
        q = q.filter(Project.commune_id == commune_id)
    
    projects = q.limit(limit).all()
    
    return [
        ProjectGeoOut(
            id=p.id,
            title=p.title,
            chapitre=p.chapitre,
            commune=(p.commune.name if p.commune else None),
            latitude=p.latitude,
            longitude=p.longitude,
            is_aligned=bool([a for a in p.alignments if a.status == AlignStatus.validated]),
            alignment_count=len([a for a in p.alignments if a.status == AlignStatus.validated]),
        )
        for p in projects
    ]

