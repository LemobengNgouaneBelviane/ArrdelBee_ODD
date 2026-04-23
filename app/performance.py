from __future__ import annotations

from dataclasses import dataclass


class PerformanceColor:
    GREEN = "VERT"
    ORANGE = "ORANGE"
    RED = "ROUGE"
    UNKNOWN = "INCONNU"


@dataclass(frozen=True)
class PerformanceResult:
    success_pct: float | None
    color: str


def compute_performance(target_value: float | None, realized_value: float | None) -> PerformanceResult:
    """
    Compare Valeur Cible (prévue) vs Valeur Réalisée (collectée).
    - % réussite = (réalisée / cible) * 100
    - Couleur: Vert >= 90%, Orange >= 50%, Rouge < 50%
    """
    if target_value is None or realized_value is None or target_value == 0:
        return PerformanceResult(success_pct=None, color=PerformanceColor.UNKNOWN)

    pct = (realized_value / target_value) * 100.0
    if pct >= 90.0:
        color = PerformanceColor.GREEN
    elif pct >= 50.0:
        color = PerformanceColor.ORANGE
    else:
        color = PerformanceColor.RED
    return PerformanceResult(success_pct=pct, color=color)

