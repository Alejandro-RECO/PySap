"""Smoke test de los wrappers generados (ADR-0004): importan y delegan al COM."""

from __future__ import annotations

import pysap.objects as objects
from pysap.objects.gui_button import GuiButton
from pysap.objects.gui_statusbar import GuiStatusbar
from tests.mocks.fake_sap import FakeComponent


def test_todos_los_wrappers_se_exportan() -> None:
    # Los 14 objetos núcleo + GuiComponent deben estar disponibles.
    esperados = {
        "GuiComponent", "GuiApplication", "GuiButton", "GuiCTextField",
        "GuiCheckBox", "GuiComboBox", "GuiConnection", "GuiGridView",
        "GuiMainWindow", "GuiPasswordField", "GuiRadioButton", "GuiSession",
        "GuiStatusbar", "GuiTextField", "GuiTree",
    }
    assert esperados <= set(objects.__all__)
    for nombre in esperados:
        assert hasattr(objects, nombre)


def test_guibutton_press_delega_al_com() -> None:
    com = FakeComponent("wnd[0]/tbar[0]/btn[0]", type="GuiButton")
    boton = GuiButton(com)
    boton.press()
    assert com.pressed is True


def test_guistatusbar_message_type_lee_del_com() -> None:
    com = FakeComponent("wnd[0]/sbar", type="GuiStatusbar", message_type="S")
    sbar = GuiStatusbar(com)
    assert sbar.message_type == "S"
