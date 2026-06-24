"""TDD: abrir conexión y login por código."""

from __future__ import annotations

from pysap import connect
from pysap.runtime.connector import open_connection
from tests.mocks.fake_sap import FakeApplication


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
