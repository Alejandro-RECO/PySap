"""TDD Fase 3: emisor de código (.py y .pyi) desde las especificaciones."""

from __future__ import annotations

from pysap.codegen.emitter import emit_module, emit_stub, snake_case
from pysap.codegen.pdf_parser import MethodSpec, ObjectSpec, Param, PropertySpec


def _spec() -> ObjectSpec:
    return ObjectSpec(
        name="GuiButton",
        base="GuiVComponent",
        prefix="btn",
        doc="GuiButton representa botones.",
        properties=[
            PropertySpec(name="Emphasized", vb_type="Byte", readonly=True, doc="Resaltado."),
            PropertySpec(name="LeftLabel", vb_type="GuiVComponent", readonly=True, doc="Etiqueta."),
        ],
        methods=[
            MethodSpec(name="Press", params=[], return_type="", doc="Pulsa el botón."),
            MethodSpec(
                name="GetListProperty",
                params=[Param(name="Property", vb_type="String")],
                return_type="String",
                doc="Lee una propiedad.",
            ),
        ],
    )


def test_snake_case_convierte_pascal() -> None:
    assert snake_case("LeftLabel") == "left_label"
    assert snake_case("Press") == "press"
    assert snake_case("GetListProperty") == "get_list_property"
    assert snake_case("MaxLength") == "max_length"


def test_emit_module_tiene_cabecera_generado() -> None:
    code = emit_module(_spec())
    assert "GENERADO" in code
    assert "NO EDITAR" in code.upper()


def test_emit_module_clase_hereda_de_guicomponent() -> None:
    code = emit_module(_spec())
    assert "class GuiButton(GuiComponent):" in code
    assert "from pysap.objects.base import GuiComponent" in code


def test_emit_module_propiedad_readonly_sin_setter() -> None:
    code = emit_module(_spec())
    assert "def emphasized(self) -> bool:" in code
    assert "return self._com.Emphasized" in code
    # Read-only: no debe generar setter.
    assert "@emphasized.setter" not in code


def test_emit_module_metodo_sub_devuelve_none() -> None:
    code = emit_module(_spec())
    assert "def press(self) -> None:" in code
    assert "self._com.Press()" in code


def test_emit_module_metodo_con_param_tipado() -> None:
    code = emit_module(_spec())
    assert "def get_list_property(self, property: str) -> str:" in code
    assert "return self._com.GetListProperty(property)" in code


def test_emit_stub_es_pyi_sin_cuerpos() -> None:
    stub = emit_stub(_spec())
    assert "class GuiButton(GuiComponent):" in stub
    assert "def press(self) -> None: ..." in stub
    assert "def emphasized(self) -> bool: ..." in stub
