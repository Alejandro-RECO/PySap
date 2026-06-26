"""TDD Fase 3: mapeo de tipos VB del PDF a tipos Python."""

from __future__ import annotations

import pytest

from pysap.codegen.typemap import vb_to_python


@pytest.mark.parametrize(
    "vb, esperado",
    [
        ("String", "str"),
        ("Long", "int"),
        ("Integer", "int"),
        ("Short", "int"),
        ("Byte", "bool"),
        ("Boolean", "bool"),
        ("Double", "float"),
        ("Single", "float"),
        ("Variant", "Any"),
        ("Object", "Any"),
        ("GuiVComponent", "Any"),
        ("GuiComponentCollection", "Any"),
    ],
)
def test_vb_to_python_mapea_tipos(vb: str, esperado: str) -> None:
    assert vb_to_python(vb) == esperado


def test_vb_to_python_tipo_desconocido_es_any() -> None:
    assert vb_to_python("LoQueSea") == "Any"


def test_vb_to_python_vacio_es_none() -> None:
    # Sin tipo de retorno (Sub) -> None.
    assert vb_to_python("") == "None"
