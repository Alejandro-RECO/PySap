"""TDD: espera (wait_for) y reintentos (retries) en Step."""

from __future__ import annotations

import pytest

from pysap.process import Step
from pysap.runtime.errors import WaitTimeoutError


def _no_sleep(_seconds: float) -> None:
    """Sleep falso: no espera de verdad."""


class FakeClock:
    """Reloj controlable: avanza un tick por llamada."""

    def __init__(self, step: float = 1.0) -> None:
        self.t = 0.0
        self.step = step

    def __call__(self) -> float:
        self.t += self.step
        return self.t


def test_retry_reintenta_hasta_exito(session):
    intentos = {"n": 0}

    def accion(_s):
        intentos["n"] += 1
        if intentos["n"] < 3:
            raise RuntimeError("aún no")

    step = Step("flaky", action=accion, retries=3, retry_delay=0.0)
    step.run(session, sleep=_no_sleep)

    assert intentos["n"] == 3


def test_retry_agotado_propaga_ultimo_error(session):
    def accion(_s):
        raise RuntimeError("siempre falla")

    step = Step("flaky", action=accion, retries=2, retry_delay=0.0)
    with pytest.raises(RuntimeError, match="siempre falla"):
        step.run(session, sleep=_no_sleep)


def test_wait_for_espera_a_condicion(session):
    estado = {"listo": False}
    llamadas = {"n": 0}

    def cond(_s):
        llamadas["n"] += 1
        if llamadas["n"] >= 2:
            estado["listo"] = True
        return estado["listo"]

    ejecutado = {"ok": False}
    step = Step(
        "espera",
        action=lambda _s: ejecutado.__setitem__("ok", True),
        wait_for=cond,
    )
    step.run(session, sleep=_no_sleep, clock=FakeClock())

    assert ejecutado["ok"] is True
    assert llamadas["n"] >= 2


def test_wait_for_timeout_lanza_error(session):
    step = Step(
        "espera",
        action=lambda _s: None,
        wait_for=lambda _s: False,
        wait_timeout=3.0,
    )
    with pytest.raises(WaitTimeoutError):
        step.run(session, sleep=_no_sleep, clock=FakeClock(step=1.0))
