"""Step: unidad atómica de automatización, medible, esperable y reintentable."""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass

from pysap.runtime.errors import WaitTimeoutError
from pysap.runtime.session import Session

# Acción: recibe la sesión, ejecuta una interacción SAP.
Action = Callable[[Session], None]
# Verificación / condición: devuelve True si el estado es el esperado.
Check = Callable[[Session], bool]
# Dependencias inyectables (para tests deterministas).
Sleeper = Callable[[float], None]
Clock = Callable[[], float]


@dataclass
class Step:
    """Paso individual de un proceso.

    Args:
        name: nombre legible (aparece en métricas/logs).
        action: interacción con SAP a ejecutar.
        verify: comprobación posterior opcional; si devuelve False, el step falla.
        retries: reintentos extra si la acción/verificación falla (0 = un intento).
        retry_delay: segundos a esperar entre reintentos.
        wait_for: condición a cumplir ANTES de la acción (p.ej. pantalla lista).
        wait_timeout: segundos máximos esperando ``wait_for``.
        wait_poll: segundos entre sondeos de ``wait_for``.
    """

    name: str
    action: Action
    verify: Check | None = None
    retries: int = 0
    retry_delay: float = 0.0
    wait_for: Check | None = None
    wait_timeout: float = 10.0
    wait_poll: float = 0.2

    def run(
        self,
        session: Session,
        *,
        sleep: Sleeper = time.sleep,
        clock: Clock = time.perf_counter,
    ) -> None:
        """Espera la condición (si hay), ejecuta la acción con reintentos y verifica."""
        if self.wait_for is not None:
            self._await_condition(session, sleep, clock)

        attempts = self.retries + 1
        last_exc: Exception | None = None
        for i in range(attempts):
            try:
                self.action(session)
                if self.verify is not None and not self.verify(session):
                    raise AssertionError(f"Verificación fallida en step: {self.name}")
                return
            except Exception as exc:  # noqa: BLE001 - se reintenta y se re-lanza
                last_exc = exc
                if i < attempts - 1:
                    sleep(self.retry_delay)
        assert last_exc is not None  # invariante: el bucle corrió al menos una vez
        raise last_exc

    def _await_condition(self, session: Session, sleep: Sleeper, clock: Clock) -> None:
        assert self.wait_for is not None
        start = clock()
        while True:
            if self.wait_for(session):
                return
            if clock() - start >= self.wait_timeout:
                raise WaitTimeoutError(
                    f"Timeout ({self.wait_timeout}s) esperando condición en step: {self.name}"
                )
            sleep(self.wait_poll)
