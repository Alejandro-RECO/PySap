"""TDD: barra de estado, detección de errores y popups."""

from __future__ import annotations

import pytest

from pysap import connect
from pysap.runtime.errors import SapMessageError
from tests.mocks.fake_sap import FakeComponent, FakeSession, build_app


def _session_with(*components: FakeComponent):
    fs = FakeSession()
    fs.add(FakeComponent("wnd[0]", type="GuiMainWindow"))
    for c in components:
        fs.add(c)
    return connect(application=build_app(fs))


def test_status_lee_tipo_y_texto():
    s = _session_with(
        FakeComponent("wnd[0]/sbar", type="GuiStatusbar", text="Documento creado", message_type="S")
    )
    status = s.status()
    assert status.type == "S"
    assert status.text == "Documento creado"
    assert status.is_error is False


def test_status_sin_sbar_es_vacio():
    s = _session_with()
    status = s.status()
    assert status.type == ""
    assert status.is_error is False


def test_raise_on_error_lanza_en_tipo_E():
    s = _session_with(
        FakeComponent("wnd[0]/sbar", type="GuiStatusbar", text="Campo obligatorio", message_type="E")
    )
    with pytest.raises(SapMessageError, match="Campo obligatorio"):
        s.raise_on_error()


def test_raise_on_error_no_lanza_en_tipo_S():
    s = _session_with(
        FakeComponent("wnd[0]/sbar", type="GuiStatusbar", text="OK", message_type="S")
    )
    s.raise_on_error()  # no debe lanzar


def test_has_popup_detecta_wnd1():
    s = _session_with(FakeComponent("wnd[1]", type="GuiModalWindow"))
    assert s.has_popup() is True


def test_has_popup_falso_sin_wnd1():
    s = _session_with()
    assert s.has_popup() is False


def test_confirm_popup_envia_enter():
    popup = FakeComponent("wnd[1]", type="GuiModalWindow")
    s = _session_with(popup)
    s.confirm_popup()
    assert 0 in popup.vkeys


def test_cancel_popup_envia_f12():
    popup = FakeComponent("wnd[1]", type="GuiModalWindow")
    s = _session_with(popup)
    s.cancel_popup()
    assert 12 in popup.vkeys
