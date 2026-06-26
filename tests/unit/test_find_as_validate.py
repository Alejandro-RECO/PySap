"""TDD Fase 4: validación de tipo opcional en Session.find_as (ADR-0005)."""

from __future__ import annotations

import pytest

from pysap.objects import GuiButton, GuiComponent
from pysap.runtime.errors import ComponentTypeError


def test_find_as_sin_validar_no_comprueba_tipo(session):
    # Por defecto (validate=False) envuelve aunque el tipo no coincida.
    comp = session.find_as("wnd[0]/usr/txtF1", GuiButton)
    assert isinstance(comp, GuiButton)


def test_find_as_validate_ok_cuando_tipo_coincide(session):
    boton = session.find_as("wnd[0]/tbar[0]/btn[0]", GuiButton, validate=True)
    assert isinstance(boton, GuiButton)


def test_find_as_validate_lanza_si_tipo_no_coincide(session):
    # txtF1 es GuiTextField; pedirlo como GuiButton con validate debe fallar.
    with pytest.raises(ComponentTypeError):
        session.find_as("wnd[0]/usr/txtF1", GuiButton, validate=True)


def test_find_as_validate_con_componente_generico_no_valida(session):
    # GuiComponent es genérico: validate=True no debe rechazar ningún tipo.
    comp = session.find_as("wnd[0]/usr/txtF1", GuiComponent, validate=True)
    assert isinstance(comp, GuiComponent)
