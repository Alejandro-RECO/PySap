"""Tests de launch_sap: engancha si la ROT responde, si no lanza saplogon y sondea."""

from __future__ import annotations

import pytest

from pysap.runtime.errors import SapLaunchError, SapNotRunningError
from pysap.runtime.launcher import launch_sap


class EngineStub:
    """get_engine falso: falla ``fail_times`` veces y luego devuelve la app."""

    def __init__(self, fail_times: int) -> None:
        self.fail_times = fail_times
        self.calls = 0
        self.app = object()

    def __call__(self):
        self.calls += 1
        if self.calls <= self.fail_times:
            raise SapNotRunningError("ROT vacía")
        return self.app


class OpenerSpy:
    def __init__(self) -> None:
        self.paths: list[str] = []

    def __call__(self, path: str):
        self.paths.append(path)
        return object()


class Clock:
    """Reloj falso monótono: avanza ``step`` segundos en cada llamada."""

    def __init__(self, step: float) -> None:
        self.t = 0.0
        self.step = step

    def __call__(self) -> float:
        t = self.t
        self.t += self.step
        return t


def test_launch_engancha_sin_lanzar_si_rot_responde():
    engine = EngineStub(fail_times=0)
    opener = OpenerSpy()
    app = launch_sap("ruta.exe", opener=opener, get_engine=engine, sleep=lambda _: None)
    assert app is engine.app
    assert opener.paths == []  # no relanzó SAP


def test_launch_lanza_saplogon_y_engancha_tras_sondeo():
    engine = EngineStub(fail_times=1)  # primer intento falla; tras lanzar, conecta
    opener = OpenerSpy()
    sleeps: list[float] = []
    app = launch_sap(
        r"C:\SAP\saplogon.exe",
        opener=opener,
        get_engine=engine,
        sleep=sleeps.append,
        clock=Clock(step=1.0),
        timeout=30.0,
        poll=0.5,
    )
    assert app is engine.app
    assert opener.paths == [r"C:\SAP\saplogon.exe"]


def test_launch_timeout_lanza_saplaunch_error():
    engine = EngineStub(fail_times=999)  # nunca conecta
    opener = OpenerSpy()
    with pytest.raises(SapLaunchError):
        launch_sap(
            "ruta.exe",
            opener=opener,
            get_engine=engine,
            sleep=lambda _: None,
            clock=Clock(step=10.0),
            timeout=30.0,
            poll=0.5,
        )
    assert opener.paths == ["ruta.exe"]  # intentó lanzar


def test_launch_sin_path_y_sin_rot_lanza_error():
    engine = EngineStub(fail_times=999)
    opener = OpenerSpy()
    with pytest.raises(SapLaunchError):
        launch_sap("", opener=opener, get_engine=engine, sleep=lambda _: None)
    assert opener.paths == []  # no hay binario que lanzar
