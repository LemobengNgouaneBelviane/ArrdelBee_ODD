from __future__ import annotations

from datetime import datetime

from rapidfuzz import fuzz
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.matching import suggest_alignment
from app.models import (
    AlignStatus,
    AlignmentODD,
    Commune,
    Department,
    Evidence,
    ProblemSolution,
    Project,
    ProjectKPI,
    SDGGoal,
    SDGTarget,
    UNIndicator,
)


def list_unaligned_projects(db: Session, limit: int = 200) -> list[dict]:
    """
    Projet "non aligné" = aucun alignement VALIDATED.
    """
    stmt = (
        select(Project)
        .where(~Project.alignments.any(AlignmentODD.status == AlignStatus.validated))
        .limit(limit)
    )
    projects = db.scalars(stmt).all()
    out: list[dict] = []
    for p in projects:
        out.append(
            {
                "project": p,
                "suggested_sdg_codes": suggest_alignment(p.chapitre),
            }
        )
    return out


def validate_alignment(
    db: Session,
    project_id: int,
    indicator_id: int,
    validated_by: str | None,
    justification: str | None,
    status: AlignStatus,
) -> AlignmentODD:
    stmt = select(AlignmentODD).where(
        AlignmentODD.project_id == project_id,
        AlignmentODD.indicator_id == indicator_id,
    )
    alignment = db.scalars(stmt).first()
    if alignment is None:
        alignment = AlignmentODD(
            project_id=project_id,
            indicator_id=indicator_id,
            suggested=False,
        )
        db.add(alignment)

    alignment.status = status
    alignment.validated_at = datetime.utcnow() if status == AlignStatus.validated else None
    alignment.validated_by = validated_by
    alignment.justification = justification
    db.commit()
    db.refresh(alignment)
    return alignment


def get_collection_config(db: Session, project_id: int) -> str | None:
    project = db.get(Project, project_id)
    if project is None:
        return None
    return project.source_verification


def upsert_evidence_snapshot(db: Session, project_id: int, alignment_id: int | None = None) -> Evidence:
    stmt = select(Evidence).where(Evidence.project_id == project_id, Evidence.alignment_id == alignment_id)
    ev = db.scalars(stmt).first()
    if ev is None:
        project = db.get(Project, project_id)
        ev = Evidence(
            project_id=project_id,
            alignment_id=alignment_id,
            required_list=project.source_verification if project else None,
        )
        db.add(ev)
        db.commit()
        db.refresh(ev)
    return ev


def update_evidence(db: Session, evidence_id: int, provided_list: str | None, workflow_level, updated_by: str | None) -> Evidence:
    ev = db.get(Evidence, evidence_id)
    if ev is None:
        raise ValueError("Evidence not found")
    ev.provided_list = provided_list
    ev.workflow_level = workflow_level
    ev.updated_by = updated_by
    ev.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(ev)
    return ev


def get_justification(db: Session, project_id: int) -> str | None:
    """
    Cherche dans ProblemSolution le meilleur texte expliquant "pourquoi" le projet aide un ODD.
    Heuristique: fuzzy match sur chapter_hint + titre/objectif du projet, puis retourne un texte synthétique.
    """
    project = db.get(Project, project_id)
    if project is None:
        return None

    candidates = db.scalars(select(ProblemSolution)).all()
    if not candidates:
        return None

    proj_text = " ".join(
        [
            (project.chapitre or ""),
            project.title or "",
            (project.objectif_specifique or ""),
            (project.iov or ""),
        ]
    ).strip()
    if not proj_text:
        return None

    best = None
    best_score = 0
    for c in candidates:
        cand_text = " ".join([(c.chapter_hint or ""), c.probleme, (c.solution or "")]).strip()
        score = fuzz.token_set_ratio(proj_text, cand_text)
        if score > best_score:
            best_score = score
            best = c

    if best is None or best_score < 55:
        return None

    parts = [f"Problème: {best.probleme}"]
    if best.cause:
        parts.append(f"Cause: {best.cause}")
    if best.effet:
        parts.append(f"Effet: {best.effet}")
    if best.solution:
        parts.append(f"Solution: {best.solution}")
    return " | ".join(parts)


def find_indicators_for_goal_codes(db: Session, goal_codes: list[str], limit_per_goal: int = 5) -> list[UNIndicator]:
    if not goal_codes:
        return []
    stmt = (
        select(UNIndicator)
        .join(SDGTarget, UNIndicator.target_id == SDGTarget.id)
        .join(SDGGoal, SDGTarget.goal_id == SDGGoal.id)
        .where(SDGGoal.code.in_(goal_codes))
        .limit(max(1, limit_per_goal * len(goal_codes)))
    )
    return db.scalars(stmt).all()


def create_project(
    db: Session,
    title: str,
    description: str | None = None,
    sector: str | None = None,
    department_name: str | None = None,
    commune_name: str | None = None,
    budget: float | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> Project:
    """Créer un nouveau projet avec commune si fournie."""
    
    commune = None
    if department_name and commune_name:
        # Chercher ou créer le département
        dept = db.scalars(select(Department).where(Department.name == department_name)).first()
        if dept is None:
            dept = Department(name=department_name)
            db.add(dept)
            db.flush()
        
        # Chercher ou créer la commune
        comm = db.scalars(
            select(Commune).where(
                Commune.department_id == dept.id,
                Commune.name == commune_name,
            )
        ).first()
        if comm is None:
            comm = Commune(name=commune_name, department_id=dept.id)
            db.add(comm)
            db.flush()
        commune = comm
    
    project = Project(
        title=title,
        chapitre=sector,
        objectif_specifique=description,
        commune_id=commune.id if commune else None,
    )
    db.add(project)
    db.flush()
    
    # Ajouter un KPI par défaut si budget fourni
    if budget and budget > 0:
        kpi = ProjectKPI(
            project_id=project.id,
            name="Budget alloué",
            unit="USD",
            target_value=budget,
            realized_value=None,
        )
        db.add(kpi)
    
    db.commit()
    db.refresh(project)
    return project


def validate_alignment_multi_odds(
    db: Session,
    project_id: int,
    selected_odds: list[int],
    baseline: float | None = None,
    target: float | None = None,
    justification: str | None = None,
    validated_by: str | None = None,
    status: AlignStatus = AlignStatus.validated,
) -> list[AlignmentODD]:
    """
    Créer des alignements pour plusieurs ODD.
    Pour chaque ODD, on prend le premier indicateur.
    """
    project = db.get(Project, project_id)
    if project is None:
        raise ValueError(f"Project {project_id} not found")
    
    alignments = []
    
    for odd_code in selected_odds:
        # Trouver le premier indicateur pour cet ODD
        stmt = (
            select(UNIndicator)
            .join(SDGTarget, UNIndicator.target_id == SDGTarget.id)
            .join(SDGGoal, SDGTarget.goal_id == SDGGoal.id)
            .where(SDGGoal.code == str(odd_code))
            .limit(1)
        )
        indicator = db.scalars(stmt).first()
        
        if indicator is None:
            # Créer un ODD factice si không exist
            goal = db.scalars(select(SDGGoal).where(SDGGoal.code == str(odd_code))).first()
            if goal is None:
                goal = SDGGoal(code=str(odd_code), title=f"ODD {odd_code}")
                db.add(goal)
                db.flush()
            
            target = db.scalars(select(SDGTarget).where(SDGTarget.goal_id == goal.id)).first()
            if target is None:
                sdg_target = SDGTarget(goal_id=goal.id, code=f"{odd_code}.1", title=f"Target {odd_code}.1")
                db.add(sdg_target)
                db.flush()
            else:
                sdg_target = target
            
            indicator = UNIndicator(target_id=sdg_target.id, code=f"{odd_code}.1.1", name=f"Indicator {odd_code}")
            db.add(indicator)
            db.flush()
        
        # Créer ou mettre à jour l'alignement
        alignment = db.scalars(
            select(AlignmentODD).where(
                AlignmentODD.project_id == project_id,
                AlignmentODD.indicator_id == indicator.id,
            )
        ).first()
        
        if alignment is None:
            alignment = AlignmentODD(
                project_id=project_id,
                indicator_id=indicator.id,
                suggested=False,
            )
            db.add(alignment)
        
        alignment.status = status
        alignment.validated_at = datetime.utcnow() if status == AlignStatus.validated else None
        alignment.validated_by = validated_by
        alignment.justification = justification
        alignments.append(alignment)
        
        # Ajouter le KPI si fourni
        if baseline is not None and target is not None:
            project_kpi = db.scalars(
                select(ProjectKPI).where(ProjectKPI.project_id == project_id)
            ).first()
            if project_kpi is None:
                project_kpi = ProjectKPI(
                    project_id=project_id,
                    name=f"KPI ODD {odd_code}",
                    unit="percent",
                    target_value=target,
                    realized_value=baseline,
                )
                db.add(project_kpi)
            else:
                project_kpi.target_value = target
                project_kpi.realized_value = baseline
    
    db.commit()
    for a in alignments:
        db.refresh(a)
    return alignments

