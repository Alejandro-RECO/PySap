"""Tests de start_session: orquesta arranque -> open_connection -> login -> Session."""

from __future__ import annotations


from pysap.config import SapConfig
from pysap.runtime.bootstrap import start_session
from pysap.runtime.session import Session
from tests.mocks.fake_sap import FakeApplication

CFG = SapConfig(
    connection="PRD - Producción",
    client="100",
    user="USUARIO",
    password="secreto",
    language="ES",
    logon_path=r"C:\SAP\saplogon.exe",
)


def test_start_session_con_app_abre_conexion_y_loguea():
    app = FakeApplication([])  # Arrange: sin conexiones; OpenConnection creará una
    session = start_session(CFG, application=app)  # Act
    assert isinstance(session, Session)  # Assert
    assert app.opened == ["PRD - Producción"]  # abrió la conexión por nombre


def test_start_session_rellena_credenciales_de_login():
    app = FakeApplication([])
    session = start_session(CFG, application=app)
    com = session.com
    assert com.findById("wnd[0]/usr/txtRSYST-MANDT").Text == "100"
    assert com.findById("wnd[0]/usr/txtRSYST-BNAME").Text == "USUARIO"
    assert com.findById("wnd[0]/usr/pwdRSYST-BCODE").Text == "secreto"
    assert com.findById("wnd[0]/usr/txtRSYST-LANGU").Text == "ES"


def test_start_session_confirma_login_con_enter():
    app = FakeApplication([])
    session = start_session(CFG, application=app)
    assert session.com.findById("wnd[0]").vkeys == [0]  # Enter tras login


def test_start_session_sin_app_usa_el_launcher():
    app = FakeApplication([])
    rutas: list[str] = []

    def launcher(path: str):
        rutas.append(path)
        return app

    session = start_session(CFG, launcher=launcher)
    assert rutas == [r"C:\SAP\saplogon.exe"]  # usó el launcher con el path de config
    assert isinstance(session, Session)


def test_start_session_no_usa_launcher_si_recibe_app():
    app = FakeApplication([])

    def launcher(path: str):  # pragma: no cover - no debe llamarse
        raise AssertionError("no debe lanzarse SAP cuando se pasa application")

    session = start_session(CFG, application=app, launcher=launcher)
    assert isinstance(session, Session)
