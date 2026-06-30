"""Tests de búsqueda robusta de componentes: por nombre y por sufijo de id."""

from __future__ import annotations

import pytest

from pysap.objects import GuiButton, GuiTextField
from pysap.runtime.errors import ComponentNotFoundError, ComponentTypeError
from tests.mocks.fake_sap import FakeComponent

# --- find_by_name -----------------------------------------------------------


def test_find_by_name_devuelve_primer_match(session):
    comp = session.find_by_name("btn[0]", "GuiButton")
    assert comp.id == "wnd[0]/tbar[0]/btn[0]"


def test_find_by_name_inexistente_lanza_error(session):
    with pytest.raises(ComponentNotFoundError):
        session.find_by_name("noExiste", "GuiButton")


def test_find_by_name_inexistente_sin_raise_devuelve_none(session):
    assert session.find_by_name("noExiste", "GuiButton", raise_=False) is None


def test_find_by_name_tipo_no_coincide_no_match(session):
    # El name existe (btn[0]) pero con otro tipo: no debe coincidir.
    assert session.find_by_name("btn[0]", "GuiTextField", raise_=False) is None


# --- find_all_by_name -------------------------------------------------------


def test_find_all_by_name_devuelve_todas(fake_session, session):
    fake_session.add(
        FakeComponent("wnd[0]/usr/txtF2", type="GuiTextField", name="dup")
    )
    fake_session.add(
        FakeComponent("wnd[0]/usr/txtF3", type="GuiTextField", name="dup")
    )
    comps = session.find_all_by_name("dup", "GuiTextField")
    assert [c.id for c in comps] == ["wnd[0]/usr/txtF2", "wnd[0]/usr/txtF3"]


def test_find_all_by_name_vacio(session):
    assert session.find_all_by_name("nada", "GuiButton") == []


# --- find_by_id_suffix ------------------------------------------------------


def test_find_by_id_suffix_raiz_por_defecto(session):
    # Path completo cambiante, sufijo estable.
    comp = session.find_by_id_suffix("tbar[0]/btn[0]")
    assert comp.id == "wnd[0]/tbar[0]/btn[0]"


def test_find_by_id_suffix_recursivo_en_arbol(session):
    raiz = FakeComponent("wnd[0]", type="GuiMainWindow")
    usr = FakeComponent("wnd[0]/usr", type="GuiUserArea")
    # Prefijo dinámico (subscreen con índice variable), sufijo estable.
    boton = FakeComponent(
        "wnd[0]/usr/subSUB:SAPLXXXX:0100/btnGUARDAR",
        type="GuiButton",
        name="btnGUARDAR",
    )
    usr.add_child(boton)
    raiz.add_child(usr)
    comp = session.find_by_id_suffix("btnGUARDAR", root=raiz)
    assert comp.id.endswith("btnGUARDAR")


def test_find_by_id_suffix_inexistente_lanza_error(session):
    with pytest.raises(ComponentNotFoundError):
        session.find_by_id_suffix("noExisteJamas")


def test_find_by_id_suffix_inexistente_sin_raise_devuelve_none(session):
    assert session.find_by_id_suffix("noExisteJamas", raise_=False) is None


# --- find_by_id_suffix con kind tipado (ADR-0006) ---------------------------


def test_find_by_id_suffix_kind_devuelve_wrapper_tipado(session):
    campo = session.find_by_id_suffix("txtF1", GuiTextField)  # Arrange + Act
    assert isinstance(campo, GuiTextField)  # Assert
    assert campo.id == "wnd[0]/usr/txtF1"


def test_find_by_id_suffix_kind_tipo_erroneo_lanza_error(session):
    # txtF1 es GuiTextField; pedir GuiButton con validación debe fallar.
    with pytest.raises(ComponentTypeError):
        session.find_by_id_suffix("txtF1", GuiButton)


def test_find_by_id_suffix_kind_sin_validar_no_comprueba_tipo(session):
    campo = session.find_by_id_suffix("txtF1", GuiButton, validate=False)
    assert isinstance(campo, GuiButton)  # se envuelve sin validar el tipo SAP


def test_find_by_id_suffix_kind_con_root_y_validacion(session):
    raiz = FakeComponent("wnd[0]", type="GuiMainWindow")
    boton = FakeComponent(
        "wnd[0]/usr/subSUB:SAPLXXXX:0100/btnGUARDAR",
        type="GuiButton",
        name="btnGUARDAR",
    )
    raiz.add_child(boton)
    comp = session.find_by_id_suffix("btnGUARDAR", GuiButton, root=raiz)
    assert isinstance(comp, GuiButton)
    comp.press()
    assert comp.com.pressed is True
