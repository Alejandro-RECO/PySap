"""TDD Fase 4: Page Objects sobre PathRegistry (ADR-0005)."""

from __future__ import annotations

import pytest

from pysap.mapping import Field, PageObject, PathRegistry
from pysap.objects import GuiButton, GuiTextField
from pysap.runtime.errors import ComponentTypeError


@pytest.fixture
def registry() -> PathRegistry:
    reg = PathRegistry()
    reg.register("boton", "wnd[0]/tbar[0]/btn[0]")
    reg.register("campo", "wnd[0]/usr/txtF1")
    return reg


def test_page_object_find_resuelve_nombre_logico(session, registry):
    page = PageObject(session, registry)
    comp = page.find("boton")
    assert comp.id == "wnd[0]/tbar[0]/btn[0]"


def test_page_object_find_as_devuelve_tipo(session, registry):
    page = PageObject(session, registry)
    boton = page.find_as("boton", GuiButton)
    assert isinstance(boton, GuiButton)
    boton.press()
    assert boton.com.pressed is True


def test_page_object_find_as_valida_por_defecto(session, registry):
    page = PageObject(session, registry)
    with pytest.raises(ComponentTypeError):
        page.find_as("campo", GuiButton)  # campo es GuiTextField


def test_page_object_nombre_no_registrado_lanza(session, registry):
    page = PageObject(session, registry)
    with pytest.raises(KeyError):
        page.find("inexistente")


def test_field_descriptor_resuelve_typed(session, registry):
    class Pantalla(PageObject):
        boton = Field("boton", GuiButton)
        campo = Field("campo", GuiTextField)

    page = Pantalla(session, registry)
    assert isinstance(page.boton, GuiButton)
    assert isinstance(page.campo, GuiTextField)
    page.campo.value = "Hola"
    assert page.campo.com.Text == "Hola"


def test_field_descriptor_sin_kind_devuelve_generico(session, registry):
    class Pantalla(PageObject):
        boton = Field("boton")

    page = Pantalla(session, registry)
    assert page.boton.id == "wnd[0]/tbar[0]/btn[0]"
