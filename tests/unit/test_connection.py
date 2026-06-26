"""TDD: abrir conexión y login por código."""

from __future__ import annotations

import pytest

from pysap.runtime.connector import open_connection
from pysap.runtime.errors import WaitTimeoutError
from tests.mocks.fake_sap import (
    FakeApplication,
    FakeChildren,
    FakeComponent,
    FakeConnection,
    FakeSession,
)


def test_open_connection_crea_sesion():
    app = FakeApplication([])
    session = open_connection("SERVIDOR PRD", application=app)
    assert app.opened == ["SERVIDOR PRD"]
    assert session.find("wnd[0]").type == "GuiMainWindow"


def test_login_rellena_campos_y_confirma():
    app = FakeApplication([])
    session = open_connection("SERVIDOR PRD", application=app)

    session.login(client="100", user="USR", password="secreto", language="ES")

    assert session.find("wnd[0]/usr/txtRSYST-MANDT").com.Text == "100"
    assert session.find("wnd[0]/usr/txtRSYST-BNAME").com.Text == "USR"
    assert session.find("wnd[0]/usr/pwdRSYST-BCODE").com.Text == "secreto"
    assert session.find("wnd[0]/usr/txtRSYST-LANGU").com.Text == "ES"
    assert 0 in session.find("wnd[0]").com.vkeys


class _DelayedChildren:
    """Colección cuya sesión aparece tras ``aparece_en`` consultas (SAP async)."""

    def __init__(self, session: FakeSession, aparece_en: int) -> None:
        self._session = session
        self._consultas = 0
        self._aparece_en = aparece_en

    @property
    def Count(self) -> int:
        self._consultas += 1
        return 1 if self._consultas >= self._aparece_en else 0

    def __call__(self, index: int) -> FakeSession:
        return self._session


class _DelayedConnection:
    def __init__(self, children: _DelayedChildren) -> None:
        self.Children = children


class _DelayedApp:
    """App cuya OpenConnection devuelve una conexión con sesión diferida."""

    def __init__(self, aparece_en: int) -> None:
        session = FakeSession()
        session.add(FakeComponent("wnd[0]", type="GuiMainWindow"))
        self._conn = _DelayedConnection(_DelayedChildren(session, aparece_en))
        self.opened: list[str] = []

    def OpenConnection(self, description: str, sync: bool = True):
        self.opened.append(description)
        return self._conn


def test_open_connection_espera_a_que_aparezca_la_sesion():
    app = _DelayedApp(aparece_en=3)  # la sesión no está en los 2 primeros sondeos
    sleeps: list[float] = []
    session = open_connection("PRD", application=app, sleep=sleeps.append, poll=0.5)
    assert session.find("wnd[0]").type == "GuiMainWindow"
    assert sleeps  # tuvo que esperar al menos una vez


def test_open_connection_timeout_si_no_aparece_sesion():
    app = _DelayedApp(aparece_en=999)  # nunca aparece

    class _Clock:
        def __init__(self) -> None:
            self.t = 0.0

        def __call__(self) -> float:
            t = self.t
            self.t += 10.0
            return t

    with pytest.raises(WaitTimeoutError):
        open_connection(
            "PRD", application=app, sleep=lambda _: None, clock=_Clock(), timeout=30.0
        )


class _AppRefSinSesion:
    """OpenConnection devuelve una ref vacía; la sesión cuelga del application.

    Reproduce el caso real (SAP GUI 750): la conexión abre y la sesión existe en
    ``application.Children``, pero la referencia devuelta no la expone.
    """

    def __init__(self) -> None:
        session = FakeSession()
        session.add(FakeComponent("wnd[0]", type="GuiMainWindow"))
        self._ref_vacia = FakeConnection([])  # ref devuelta: Children vacíos
        conn_real = FakeConnection([session])  # sesión real colgando del app
        self.Children = FakeChildren([conn_real])
        self.opened: list[str] = []

    def OpenConnection(self, description: str, sync: bool = True):
        self.opened.append(description)
        return self._ref_vacia


def test_open_connection_resuelve_sesion_desde_application():
    app = _AppRefSinSesion()
    session = open_connection("SALUD CALIDAD", application=app, sleep=lambda _: None)
    assert session.find("wnd[0]").type == "GuiMainWindow"
