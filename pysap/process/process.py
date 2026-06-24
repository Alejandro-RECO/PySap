"""Process: secuencia de Steps con medición y manejo de fallos."""

from __future__ import annotations

import logging
import time
from collections.abc import Iterable

from pysap.process.step import Step
from pysap.runtime.errors import StepError
from pysap.runtime.session import Session
from pysap.telemetry.metrics import ProcessReport, StepMetric

logger = logging.getLogger("pysap.process")


class Process:
    """Orquesta una lista ordenada de :class:`Step`.

    Mide cada step y produce un :class:`ProcessReport`. Por defecto detiene
    la ejecución al primer fallo (``stop_on_error=True``).
    """

    def __init__(self, name: str, steps: Iterable[Step] | None = None) -> None:
        self.name = name
        self.steps: list[Step] = list(steps or [])

    def add(self, step: Step) -> Process:
        """Añade un step y devuelve self (encadenable)."""
        self.steps.append(step)
        return self

    def run(self, session: Session, *, stop_on_error: bool = True) -> ProcessReport:
        """Ejecuta los steps en orden, midiendo cada uno."""
        report = ProcessReport(process_name=self.name)
        for step in self.steps:
            start = time.perf_counter()
            try:
                step.run(session)
                report.add(StepMetric(step.name, ok=True, duration_s=time.perf_counter() - start))
                logger.info("Step OK: %s", step.name)
            except Exception as exc:
                report.add(
                    StepMetric(
                        step.name,
                        ok=False,
                        duration_s=time.perf_counter() - start,
                        error=str(exc),
                    )
                )
                logger.error("Step FALLÓ: %s -> %s", step.name, exc)
                if stop_on_error:
                    raise StepError(f"Proceso {self.name!r} falló en step {step.name!r}: {exc}") from exc
        return report
