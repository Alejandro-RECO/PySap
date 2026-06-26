"""TDD Fase 3: parser del texto del PDF -> especificaciones de objetos."""

from __future__ import annotations

from pysap.codegen.pdf_parser import parse_all, parse_object

# Fragmento representativo del texto extraído (limpio) de un objeto.
GUIBUTTON = """GuiButton Object
Description
GuiButton represents all push buttons. GuiButton extends the GuiVComponent Object [page 279]. The type prefix is btn, the name property is the fieldname.
Methods
All methods of the GuiVComponent Object [page 279]:
DumpState
SetFocus
Press This emulates manually pressing a button.
Properties
All properties of the GuiComponent Object [page 81]:
Id
Name
Emphasized (Read-only)
Public Property Emphasized As Byte
This property is True if the button is displayed emphasized.
LeftLabel (Read-only)
Public Property LeftLabel As GuiVComponent
Left label of the GuiButton.
"""

GUITEXTFIELD = """GuiTextField Object
Description
GuiTextField extends the GuiVComponent Object [page 279]. The type prefix is txt.
Methods
All methods of the GuiVComponent Object [page 279]:
SetFocus
Properties
MaxLength (Read-only)
Public Property MaxLength As Long
Maximum number of characters.
Required (Read-only)
Public Property Required As Byte
True if the field is mandatory.
"""

GUIEDIT = """GuiShell Object
Description
GuiShell extends the GuiVContainer Object [page 281]. The type prefix is shell.
Methods
DeleteRange( _ ByVal LineStart As Long, _ ByVal ColumnStart As Long _ )
Public Sub DeleteRange( _ ByVal LineStart As Long, _ ByVal ColumnStart As Long _ )
Deletes a range of text.
GetLineText( _ ByVal Line As Long _ )
Public Function GetLineText( _ ByVal Line As Long _ ) As String
Returns the text of a line.
"""


def test_parse_object_extrae_nombre_base_y_prefijo() -> None:
    spec = parse_object(GUIBUTTON, "GuiButton")
    assert spec.name == "GuiButton"
    assert spec.base == "GuiVComponent"
    assert spec.prefix == "btn"


def test_parse_object_extrae_propiedades_propias() -> None:
    spec = parse_object(GUIBUTTON, "GuiButton")
    nombres = {p.name for p in spec.properties}
    assert nombres == {"Emphasized", "LeftLabel"}


def test_parse_object_propiedad_tiene_tipo_y_readonly() -> None:
    spec = parse_object(GUIBUTTON, "GuiButton")
    emph = next(p for p in spec.properties if p.name == "Emphasized")
    assert emph.vb_type == "Byte"
    assert emph.readonly is True


def test_parse_object_extrae_metodo_propio_sin_params() -> None:
    spec = parse_object(GUIBUTTON, "GuiButton")
    nombres = {m.name for m in spec.methods}
    assert "Press" in nombres
    press = next(m for m in spec.methods if m.name == "Press")
    assert press.params == []
    assert press.return_type == ""  # Sub: sin retorno


def test_parse_object_no_incluye_miembros_heredados() -> None:
    # SetFocus/DumpState son heredados (bullets), no deben emitirse como propios.
    spec = parse_object(GUIBUTTON, "GuiButton")
    nombres = {m.name for m in spec.methods}
    assert "SetFocus" not in nombres
    assert "DumpState" not in nombres


def test_parse_object_metodo_con_params_y_retorno() -> None:
    spec = parse_object(GUIEDIT, "GuiShell")
    get_line = next(m for m in spec.methods if m.name == "GetLineText")
    assert [p.name for p in get_line.params] == ["Line"]
    assert get_line.params[0].vb_type == "Long"
    assert get_line.return_type == "String"


def test_parse_object_metodo_sub_con_varios_params() -> None:
    spec = parse_object(GUIEDIT, "GuiShell")
    rng = next(m for m in spec.methods if m.name == "DeleteRange")
    assert [p.name for p in rng.params] == ["LineStart", "ColumnStart"]
    assert rng.return_type == ""


def test_parse_all_devuelve_solo_objetos_pedidos() -> None:
    texto = GUIBUTTON + "\n" + GUITEXTFIELD
    specs = parse_all(texto, objetos=["GuiButton", "GuiTextField"])
    assert {s.name for s in specs} == {"GuiButton", "GuiTextField"}
