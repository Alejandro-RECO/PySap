"""Estructuras de medición: por Step y agregado por Process."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class StepMetric:
    """Resultado medible de un Step."""

    name: str
    ok: bool
    duration_s: float
    error: str | None = None


@dataclass
class ProcessReport:
    """Reporte agregado de un Process."""

    process_name: str
    steps: list[StepMetric] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True si todos los steps tuvieron éxito."""
        return all(s.ok for s in self.steps)

    @property
    def total_duration_s(self) -> float:
        return sum(s.duration_s for s in self.steps)

    @property
    def failed(self) -> list[StepMetric]:
        return [s for s in self.steps if not s.ok]

    def add(self, metric: StepMetric) -> None:
        self.steps.append(metric)
