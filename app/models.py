from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class WorkflowLevel(str, enum.Enum):
    saisie = "SAISIE"
    verification = "VERIFICATION"
    validation_ctd = "VALIDATION_CTD"
    certification_arrdel = "CERTIFICATION_ARRDEL"


class AlignStatus(str, enum.Enum):
    proposed = "PROPOSED"
    validated = "VALIDATED"
    rejected = "REJECTED"


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    communes: Mapped[list[Commune]] = relationship(back_populates="department")  # type: ignore[name-defined]


class Commune(Base):
    __tablename__ = "communes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), index=True)
    latitude: Mapped[float | None] = mapped_column(Float)  # coordonnées centre commune
    longitude: Mapped[float | None] = mapped_column(Float)

    department: Mapped[Department] = relationship(back_populates="communes")
    projects: Mapped[list[Project]] = relationship(back_populates="commune")  # type: ignore[name-defined]

    __table_args__ = (UniqueConstraint("department_id", "name", name="uq_commune_department_name"),)


class SDGGoal(Base):
    __tablename__ = "sdg_goals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True, index=True)  # ex: "3"
    title: Mapped[str | None] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)

    targets: Mapped[list[SDGTarget]] = relationship(back_populates="goal")  # type: ignore[name-defined]


class SDGTarget(Base):
    __tablename__ = "sdg_targets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    goal_id: Mapped[int] = mapped_column(ForeignKey("sdg_goals.id"), index=True)
    code: Mapped[str] = mapped_column(String(20), index=True)  # ex: "3.1"
    title: Mapped[str | None] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)

    goal: Mapped[SDGGoal] = relationship(back_populates="targets")
    indicators: Mapped[list[UNIndicator]] = relationship(back_populates="target")  # type: ignore[name-defined]

    __table_args__ = (UniqueConstraint("goal_id", "code", name="uq_target_goal_code"),)


class UNIndicator(Base):
    __tablename__ = "un_indicators"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    target_id: Mapped[int] = mapped_column(ForeignKey("sdg_targets.id"), index=True)
    code: Mapped[str] = mapped_column(String(50), index=True)  # ex: "3.1.1"
    name: Mapped[str | None] = mapped_column(String(1000))
    definition: Mapped[str | None] = mapped_column(Text)

    target: Mapped[SDGTarget] = relationship(back_populates="indicators")
    alignments: Mapped[list[AlignmentODD]] = relationship(back_populates="indicator")  # type: ignore[name-defined]

    __table_args__ = (UniqueConstraint("target_id", "code", name="uq_indicator_target_code"),)


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str | None] = mapped_column(String(100), index=True)  # si disponible
    title: Mapped[str] = mapped_column(String(500), index=True)
    chapitre: Mapped[str | None] = mapped_column(String(255), index=True)  # ex: MINSANTE
    objectif_specifique: Mapped[str | None] = mapped_column(Text)
    iov: Mapped[str | None] = mapped_column(Text)  # Indicateur Objectivement Vérifiable
    source_verification: Mapped[str | None] = mapped_column(Text)  # preuves obligatoires (cadre logique)

    commune_id: Mapped[int | None] = mapped_column(ForeignKey("communes.id"), index=True)
    latitude: Mapped[float | None] = mapped_column(Float)  # localisation du projet
    longitude: Mapped[float | None] = mapped_column(Float)

    commune: Mapped[Commune | None] = relationship(back_populates="projects")

    kpis: Mapped[list[ProjectKPI]] = relationship(back_populates="project")  # type: ignore[name-defined]
    alignments: Mapped[list[AlignmentODD]] = relationship(back_populates="project")  # type: ignore[name-defined]


class ProjectKPI(Base):
    __tablename__ = "project_kpis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    name: Mapped[str] = mapped_column(String(500))
    unit: Mapped[str | None] = mapped_column(String(50))
    target_value: Mapped[float | None] = mapped_column(Float)
    realized_value: Mapped[float | None] = mapped_column(Float)

    project: Mapped[Project] = relationship(back_populates="kpis")

    __table_args__ = (UniqueConstraint("project_id", "name", name="uq_project_kpi_name"),)


class AlignmentODD(Base):
    __tablename__ = "alignments_odd"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    indicator_id: Mapped[int] = mapped_column(ForeignKey("un_indicators.id"), index=True)

    status: Mapped[AlignStatus] = mapped_column(Enum(AlignStatus), default=AlignStatus.proposed, index=True)
    suggested: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    justification: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    validated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    validated_by: Mapped[str | None] = mapped_column(String(255))

    project: Mapped[Project] = relationship(back_populates="alignments")
    indicator: Mapped[UNIndicator] = relationship(back_populates="alignments")

    __table_args__ = (UniqueConstraint("project_id", "indicator_id", name="uq_alignment_project_indicator"),)


class ProblemSolution(Base):
    __tablename__ = "problem_solutions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    probleme: Mapped[str] = mapped_column(Text)
    cause: Mapped[str | None] = mapped_column(Text)
    effet: Mapped[str | None] = mapped_column(Text)
    solution: Mapped[str | None] = mapped_column(Text)

    chapter_hint: Mapped[str | None] = mapped_column(String(255), index=True)  # ex: MINSANTE / secteur
    commune_id: Mapped[int | None] = mapped_column(ForeignKey("communes.id"), index=True)


class Evidence(Base):
    __tablename__ = "evidences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    alignment_id: Mapped[int | None] = mapped_column(ForeignKey("alignments_odd.id"), index=True)

    required_list: Mapped[str | None] = mapped_column(Text)  # snapshot des "source_verification"
    provided_list: Mapped[str | None] = mapped_column(Text)  # liens/ids docs ou texte

    workflow_level: Mapped[WorkflowLevel] = mapped_column(Enum(WorkflowLevel), default=WorkflowLevel.saisie, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_by: Mapped[str | None] = mapped_column(String(255))

