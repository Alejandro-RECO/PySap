"""Tests del runtime: conexión + Session.find."""

from __future__ import annotations

import pytest

from pysap.objects import GuiButton, GuiTextField
from pysap.runtime.errors import ComponentNotFoundError


def test_find_devuelve_componente(session):
    comp = session.find("wnd[0]/tbar[0]/btn[0]")
    assert comp.type == "GuiButton"
    assert comp.id == "wnd[0]/tbar[0]/btn[0]"


def test_find_path_inexistente_lanza_error(session):
    with pytest.raises(ComponentNotFoundError):
        session.find("wnd[0]/usr/noExiste")


def test_find_as_devuelve_tipo_concreto(session):
    boton = session.find_as("wnd[0]/tbar[0]/btn[0]", GuiButton)
    assert isinstance(boton, GuiButton)
    boton.press()
    assert boton.com.pressed is True


def test_textfield_set_value(session):
    campo = session.find_as("wnd[0]/usr/txtF1", GuiTextField)
    campo.value = "Hola"
    assert campo.com.Text == "Hola"


def test_start_transaction(session):
    session.start_transaction("SE16")
    okcd = session.find("wnd[0]/tbar[0]/okcd")
    assert okcd.com.Text == "/nSE16"
    assert 0 in session.find("wnd[0]").com.vkeys
