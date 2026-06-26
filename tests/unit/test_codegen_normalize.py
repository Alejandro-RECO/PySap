"""TDD Fase 3: limpieza del texto crudo extraído del PDF."""

from __future__ import annotations

from pysap.codegen.normalize import despace, normalize


def test_despace_une_mayuscula_partida_dentro_de_palabra() -> None:
    # El PDF parte "GuiTextField" como "GuiT extField"; debe reunirse.
    # Solo aplica con minúscula antes (evita corromper artículos sueltos).
    assert despace("GuiT extField") == "GuiTextField"
    assert despace("the GuiC heckBox") == "the GuiCheckBox"


def test_despace_no_toca_articulos() -> None:
    # "A tree" / "I see": mayúscula suelta seguida de palabra, no es artefacto.
    assert despace("A tree control") == "A tree control"


def test_normalize_quita_guion_suave() -> None:
    # El PDF parte palabras con guion suave (­) al final de línea.
    crudo = "informa­tion"
    assert normalize(crudo) == "information"


def test_normalize_quita_glifos_privados() -> None:
    # Glifos de área de uso privado (p.ej. ) deben desaparecer.
    crudo = "session.findById(path)"
    assert "" not in normalize(crudo)


def test_normalize_colapsa_espacios_y_saltos() -> None:
    crudo = "Public   Function\n   GetLineText"
    assert normalize(crudo) == "Public Function GetLineText"
