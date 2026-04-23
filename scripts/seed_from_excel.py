from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd
from sqlalchemy import select

from app.database import SessionLocal
from app.models import Commune, Department, ProblemSolution, Project, SDGGoal, SDGTarget, UNIndicator


def _norm(s: str) -> str:
    s = re.sub(r"\s+", " ", str(s or "")).strip().lower()
    s = s.replace("é", "e").replace("è", "e").replace("ê", "e").replace("à", "a").replace("ù", "u")
    s = s.replace("’", "'")
    return s


def _pick_col(df: pd.DataFrame, *needles: str) -> str | None:
    needles_n = [_norm(n) for n in needles]
    best = None
    for c in df.columns:
        cn = _norm(c)
        if all(n in cn for n in needles_n):
            best = c
            break
    return best


def _read_excel_any(path: str) -> pd.ExcelFile:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    # pandas choisit engine selon extension; .xls => xlrd, .xlsx => openpyxl
    return pd.ExcelFile(p)


def import_pcd(db, path: str) -> None:
    xf = _read_excel_any(path)
    sheet = xf.sheet_names[0]
    # Le fichier utilise des cellules fusionnées: la lecture par colonnes nommées est peu fiable.
    # On lit brut et on interprète: dept en col0, commune en col1 (observé sur Feuil1).
    raw = xf.parse(sheet_name=sheet, header=None)
    current_department: Department | None = None
    for i in range(2, len(raw)):  # saute le titre + ligne d'en-têtes
        dept_raw = str(raw.iat[i, 0]).strip() if raw.shape[1] > 0 else ""
        com_raw = str(raw.iat[i, 1]).strip() if raw.shape[1] > 1 else ""

        # ignore NaN
        dept_raw = "" if dept_raw.lower() == "nan" else dept_raw
        com_raw = "" if com_raw.lower() == "nan" else com_raw

        # ignore sections/numérotations (I, II, III...)
        if dept_raw in {"I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"}:
            continue

        # Nouveau département si col0 non vide
        if dept_raw:
            # Filtrage: dans le fichier, certaines cellules contiennent du texte long (notes) -> on ignore.
            # On garde principalement des libellés courts en majuscules (ex: HAUT-NKAM, NDE).
            if len(dept_raw) > 40:
                continue
            if not any(ch.isalpha() for ch in dept_raw):
                continue
            # tolère espaces et tirets, mais refuse les phrases (minuscules/mots longs)
            if dept_raw != dept_raw.upper():
                continue
            dept_obj = db.scalars(select(Department).where(Department.name == dept_raw)).first()
            if dept_obj is None:
                dept_obj = Department(name=dept_raw)
                db.add(dept_obj)
                db.flush()
            current_department = dept_obj
            continue

        # Commune sous le département courant si col1 non vide
        if com_raw and current_department is not None:
            com_obj = db.scalars(
                select(Commune).where(
                    Commune.department_id == current_department.id,
                    Commune.name == com_raw,
                )
            ).first()
            if com_obj is None:
                db.add(Commune(name=com_raw, department_id=current_department.id))

    db.commit()


def import_sdg_reference(db, path: str) -> None:
    xf = _read_excel_any(path)
    # Certains fichiers ont du texte/merge cells au début; on détecte une ligne d'en-tête plausible.
    sheet = "ODD, Cibles & Indicateurs" if "ODD, Cibles & Indicateurs" in xf.sheet_names else xf.sheet_names[0]

    raw = xf.parse(sheet_name=sheet, header=None)
    header_row = None
    needles = ["odd", "cible", "indicateur"]
    for i in range(min(50, len(raw))):
        joined = " | ".join([str(x).lower() for x in raw.iloc[i].tolist()])
        if all(n in joined for n in needles):
            header_row = i
            break
    if header_row is None:
        header_row = 0

    df = xf.parse(sheet_name=sheet, header=header_row)
    df.columns = [str(c).strip() for c in df.columns]

    goal_col = (
        _pick_col(df, "code", "odd")
        or _pick_col(df, "odd")
        or _pick_col(df, "objectif")
        or _pick_col(df, "goal")
    )
    target_col = _pick_col(df, "code", "cible") or _pick_col(df, "cible") or _pick_col(df, "target")
    ind_col = (
        _pick_col(df, "code", "indicateur")
        or _pick_col(df, "indicateur")
        or _pick_col(df, "indicator")
    )
    ind_name_col = _pick_col(df, "indicateurs") or _pick_col(df, "intit") or _pick_col(df, "libell") or _pick_col(df, "nom")

    if goal_col is None or target_col is None or ind_col is None:
        raise ValueError(f"Colonnes non trouvées dans {path}: goal={goal_col}, target={target_col}, indicator={ind_col}")

    def get_or_create_goal(code: str) -> SDGGoal:
        code = str(code).strip()
        g = db.scalars(select(SDGGoal).where(SDGGoal.code == code)).first()
        if g is None:
            g = SDGGoal(code=code)
            db.add(g)
            db.flush()
        return g

    def get_or_create_target(goal_id: int, code: str) -> SDGTarget:
        code = str(code).strip()
        t = db.scalars(select(SDGTarget).where(SDGTarget.goal_id == goal_id, SDGTarget.code == code)).first()
        if t is None:
            t = SDGTarget(goal_id=goal_id, code=code)
            db.add(t)
            db.flush()
        return t

    def get_or_create_indicator(target_id: int, code: str) -> UNIndicator:
        code = str(code).strip()
        ind = db.scalars(select(UNIndicator).where(UNIndicator.target_id == target_id, UNIndicator.code == code)).first()
        if ind is None:
            ind = UNIndicator(target_id=target_id, code=code)
            db.add(ind)
            db.flush()
        return ind

    seen_goal = set()
    for _, row in df.iterrows():
        goal = str(row.get(goal_col, "")).strip()
        target = str(row.get(target_col, "")).strip()
        indicator = str(row.get(ind_col, "")).strip()
        if not goal or goal.lower() == "nan":
            continue

        # nettoyage doublons: "ODD 3" -> "3"
        m = re.search(r"(\d+)", goal)
        goal_code = m.group(1) if m else goal

        g = get_or_create_goal(goal_code)
        if g.code not in seen_goal:
            seen_goal.add(g.code)
            # optionnel: titre/description si présent dans les colonnes
            title_col = _pick_col(df, "objectif", "intit") or _pick_col(df, "objectif", "titre")
            if title_col:
                g.title = str(row.get(title_col, "")).strip() or g.title

        if not target or target.lower() == "nan":
            continue
        t = get_or_create_target(g.id, target)

        if not indicator or indicator.lower() == "nan":
            continue
        ind = get_or_create_indicator(t.id, indicator)
        if ind_name_col:
            ind.name = str(row.get(ind_name_col, "")).strip() or ind.name

    db.commit()


def import_logframe_projects(db, path: str) -> None:
    xf = _read_excel_any(path)
    def detect_header_row(raw: pd.DataFrame) -> int | None:
        needles = ["logique", "source", "verif"]
        for i in range(min(60, len(raw))):
            joined = _norm(" | ".join([str(x) for x in raw.iloc[i].tolist()]))
            if all(n in joined for n in needles):
                return i
        return None

    created = 0
    for sheet in xf.sheet_names:
        raw = xf.parse(sheet_name=sheet, header=None)
        header_row = detect_header_row(raw)
        if header_row is None:
            continue
        df = xf.parse(sheet_name=sheet, header=header_row)
        df.columns = [str(c).strip() for c in df.columns]

        chapitre_col = _pick_col(df, "chapitre") or _pick_col(df, "secteur")
        level_col = _pick_col(df, "probleme") or _pick_col(df, "niveau")  # souvent la colonne "Objectif global/spécifique..."
        logique_col = _pick_col(df, "logique", "intervention")
        iov_col = _pick_col(df, "indicateur", "objectiv") or _pick_col(df, "iov") or _pick_col(df, "indicateur")
        src_col = _pick_col(df, "source", "verif")

        if logique_col is None:
            continue

        for _, row in df.iterrows():
            logique = str(row.get(logique_col, "")).strip()
            if not logique or logique.lower() == "nan":
                continue

            chapitre = str(row.get(chapitre_col, "")).strip() if chapitre_col else None
            level = str(row.get(level_col, "")).strip() if level_col else ""
            iov = str(row.get(iov_col, "")).strip() if iov_col else None
            src = str(row.get(src_col, "")).strip() if src_col else None

            # Heuristique: on garde les entrées qui ressemblent à des "projets" (OS/Résultat/Activité)
            level_l = level.lower()
            keep = any(
                k in level_l
                for k in [
                    "objectif specifique",
                    "objectif spécifique",
                    "resultat",
                    "résultat",
                    "activite",
                    "activité",
                    "action",
                ]
            )
            if not keep and len(logique) < 12:
                continue

            titre = logique
            objectif = logique if ("objectif" in level_l) else None

            existing = db.scalars(select(Project).where(Project.title == titre, Project.chapitre == chapitre)).first()
            if existing:
                existing.objectif_specifique = existing.objectif_specifique or (objectif if objectif and objectif.lower() != "nan" else None)
                existing.iov = existing.iov or (iov if iov and iov.lower() != "nan" else None)
                existing.source_verification = existing.source_verification or (src if src and src.lower() != "nan" else None)
                continue

            db.add(
                Project(
                    title=titre,
                    chapitre=chapitre if chapitre and chapitre.lower() != "nan" else None,
                    objectif_specifique=objectif if objectif and objectif.lower() != "nan" else None,
                    iov=iov if iov and iov.lower() != "nan" else None,
                    source_verification=src if src and src.lower() != "nan" else None,
                )
            )
            created += 1

    db.commit()
    if created == 0:
        raise ValueError(f"Aucun projet détecté dans {path} (structure inattendue)")


def import_problem_solution(db, path: str) -> None:
    xf = _read_excel_any(path)
    sheet = xf.sheet_names[0]
    df = xf.parse(sheet_name=sheet)
    df.columns = [str(c).strip() for c in df.columns]

    pb_col = _pick_col(df, "proble") or _pick_col(df, "pb") or _pick_col(df, "problem")
    cause_col = _pick_col(df, "cause")
    effet_col = _pick_col(df, "effet") or _pick_col(df, "impact")
    sol_col = _pick_col(df, "solution") or _pick_col(df, "besoin")
    chap_col = _pick_col(df, "chapitre") or _pick_col(df, "secteur") or _pick_col(df, "minister")

    if pb_col is None:
        raise ValueError(f"Colonne problème non trouvée dans {path}")

    for _, row in df.iterrows():
        pb = str(row.get(pb_col, "")).strip()
        if not pb or pb.lower() == "nan":
            continue
        cause = str(row.get(cause_col, "")).strip() if cause_col else None
        effet = str(row.get(effet_col, "")).strip() if effet_col else None
        sol = str(row.get(sol_col, "")).strip() if sol_col else None
        chap = str(row.get(chap_col, "")).strip() if chap_col else None

        # dédoublonnage basique sur problème+solution
        existing = db.scalars(
            select(ProblemSolution).where(ProblemSolution.probleme == pb, ProblemSolution.solution == (sol if sol and sol.lower() != "nan" else None))
        ).first()
        if existing:
            continue

        db.add(
            ProblemSolution(
                probleme=pb,
                cause=cause if cause and cause.lower() != "nan" else None,
                effet=effet if effet and effet.lower() != "nan" else None,
                solution=sol if sol and sol.lower() != "nan" else None,
                chapter_hint=chap if chap and chap.lower() != "nan" else None,
            )
        )

    db.commit()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--odd", required=True, help="Fichier Matrice ODD (Référentiel mondial)")
    ap.add_argument("--logframe", required=True, help="Fichier Cadre Logique (portefeuille projets)")
    ap.add_argument("--problem_solution", required=True, help="Fichier Matrice Problèmes-Solutions")
    ap.add_argument("--pcd", required=True, help="Fichier Inventaire PCD (Département/Commune)")
    args = ap.parse_args()

    db = SessionLocal()
    try:
        import_pcd(db, args.pcd)
        import_sdg_reference(db, args.odd)
        import_logframe_projects(db, args.logframe)
        import_problem_solution(db, args.problem_solution)
    finally:
        db.close()


if __name__ == "__main__":
    main()

