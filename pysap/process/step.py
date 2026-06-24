"""Step: unidad atómica de automatización, medible y verificable."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from pysap.runtime.session import Session

# Acción: recibe la sesión, ejecuta una interacción SAP.
Action = Callable[[Session], None]
# Verificación opcional: devuelve True si el estado posterior es correcto.
Check = Callable[[Session], bool]


@dataclass
class Step:
    """Paso individual de un proceso.

    Args:
        name: nombre legible (aparece en métricas/logs).
        action: interacción con SAP a ejecutar.
        verify: comprobación posterior opcional; si devuelve False, el step falla.
    """

    name: str
    action: Action
    verify: Check | None = None

    def run(self, session: Session) -> None:
        """Ejecuta la acción y, si hay verify, valida el resultado."""
        self.action(session)
        if self.verify is not None and not self.verify(session):
            raise AssertionError(f"Verificación fallida en step: {self.name}")
