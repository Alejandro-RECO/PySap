"""Parser del texto del PDF -> especificaciones de objetos SAP (ADR-0004).

Trabaja sobre el texto ya extraído (ver :mod:`text_extract`). Por cada objeto
``GuiX`` extrae su clase base, su prefijo de tipo y SOLO sus miembros propios
(propiedades y métodos declarados en su sección). Los miembros heredados (que el
PDF lista como viñetas ``•``) los cubre la herencia/delegación COM, no se emiten.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from pysap.codegen.normalize import despace, normalize

# Tokens que parecen un método "solo-nombre" pero son encabezados/ruido del PDF.
_NO_METODOS = frozenset(
    {
        "Method", "Methods", "Syntax", "Description", "Property", "Properties",
        "Event", "Events", "Public", "All", "Note", "See", "Sap", "Gui",
    }
)

_RE_BASE = re.compile(r"extends the (Gui[A-Za-z]+) Object")
_RE_PREFIX = re.compile(r"type prefix is (\w+)")
_RE_PROP = re.compile(r"Public Property (\w+) As (\w+)")
_RE_SIG = re.compile(
    r"Public (Sub|Function)\s+(\w+)\s*\(([^)]*)\)(?:\s*As\s+(\w+))?"
)
_RE_PARAM = re.compile(r"By(?:Val|Ref)\s+(\w+)\s+As\s+(\w+)")
# Método solo-nombre: PascalCase (2º carácter minúscula) + descripción Capitalizada.
_RE_NAME_ONLY = re.compile(r"^([A-Z][a-z][A-Za-z0-9]*) [A-Z][a-z]")
# Cabecera de definición: una línea que TERMINA en "GuiX Object". Las entradas del
# índice terminan en un número ("... 53") y las referencias cruzadas continúan tras
# "Object" ("[page 53])"), así que solo la definición real queda anclada al final.
_RE_OBJECT_HEADER = re.compile(r"(Gui[A-Za-z]+) Object$")
# Caracteres que delatan una línea de código de ejemplo (no un método).
_CODE_CHARS = set("=(){}/")


@dataclass
class Param:
    """Parámetro de un método."""

    name: str
    vb_type: str


@dataclass
class MethodSpec:
    """Método propio de un objeto. ``return_type`` vacío = Sub (sin retorno)."""

    name: str
    params: list[Param] = field(default_factory=list)
    return_type: str = ""
    doc: str = ""


@dataclass
class PropertySpec:
    """Propiedad propia de un objeto."""

    name: str
    vb_type: str
    readonly: bool = False
    doc: str = ""


@dataclass
class ObjectSpec:
    """Especificación completa de un objeto SAP a generar."""

    name: str
    base: str = "GuiComponent"
    prefix: str = ""
    doc: str = ""
    properties: list[PropertySpec] = field(default_factory=list)
    methods: list[MethodSpec] = field(default_factory=list)


def _clean_lines(text: str) -> list[str]:
    """Limpia cada línea física (sin colapsar los saltos entre líneas)."""
    return [normalize(linea) for linea in text.splitlines()]


def _region(lines: list[str], start_kw: str, end_kw: str | None) -> list[str]:
    """Devuelve las líneas entre el primer ``start_kw`` y el primer ``end_kw``."""
    try:
        i = next(n for n, ln in enumerate(lines) if ln == start_kw)
    except StopIteration:
        return []
    resto = lines[i + 1 :]
    if end_kw is not None:
        for n, ln in enumerate(resto):
            if ln == end_kw:
                return resto[:n]
    return resto


def _parse_properties(region: list[str]) -> list[PropertySpec]:
    props: list[PropertySpec] = []
    blob = " ".join(region)
    for m in _RE_PROP.finditer(blob):
        name, vb = m.group(1), m.group(2)
        # Read-only si aparece "Nombre (Read-only)" antes de la declaración.
        readonly = f"{name} (Read-only)" in blob
        props.append(PropertySpec(name=name, vb_type=vb, readonly=readonly))
    return props


def _parse_methods(region: list[str]) -> list[MethodSpec]:
    methods: list[MethodSpec] = []
    vistos: set[str] = set()

    # 1) Métodos con firma explícita (pueden abarcar varias líneas: se unen).
    blob = " ".join(region)
    for m in _RE_SIG.finditer(blob):
        nombre, dentro, retorno = m.group(2), m.group(3), m.group(4) or ""
        params = [Param(name=n, vb_type=t) for n, t in _RE_PARAM.findall(dentro)]
        methods.append(MethodSpec(name=nombre, params=params, return_type=retorno))
        vistos.add(nombre)

    # 2) Métodos solo-nombre (p.ej. "Press This emulates ..."), sin firma.
    for linea in region:
        if linea.startswith("•") or linea.startswith("Public "):
            continue
        if any(c in _CODE_CHARS for c in linea):  # línea de ejemplo de código
            continue
        m = _RE_NAME_ONLY.match(linea)
        if not m:
            continue
        nombre = m.group(1)
        if nombre in _NO_METODOS or nombre in vistos:
            continue
        methods.append(MethodSpec(name=nombre, params=[], return_type=""))
        vistos.add(nombre)

    return methods


def parse_object(text: str, name: str) -> ObjectSpec:
    """Parsea la sección de un objeto y devuelve su :class:`ObjectSpec`."""
    lines = _clean_lines(despace(text))
    blob = " ".join(lines)

    base_m = _RE_BASE.search(blob)
    prefix_m = _RE_PREFIX.search(blob)

    metodos_region = _region(lines, "Methods", "Properties")
    props_region = _region(lines, "Properties", None)

    return ObjectSpec(
        name=name,
        base=base_m.group(1) if base_m else "GuiComponent",
        prefix=prefix_m.group(1) if prefix_m else "",
        properties=_parse_properties(props_region),
        methods=_parse_methods(metodos_region),
    )


def _split_sections(text: str) -> dict[str, str]:
    """Parte el documento en secciones de definición por objeto.

    Una cabecera de definición es una **línea que es exactamente** ``GuiX Object``.
    Las referencias cruzadas (``GuiX Object [page N]``) y las entradas del índice
    (``GuiX Object....... 53``) no son líneas exactas, así que quedan fuera.
    """
    text = despace(text)
    headers: list[tuple[str, int]] = []  # (nombre, offset de carácter)
    offset = 0
    for linea in text.splitlines(keepends=True):
        norm = normalize(linea)
        m = _RE_OBJECT_HEADER.search(norm)
        if m:
            headers.append((m.group(1), offset))
        offset += len(linea)

    secciones: dict[str, str] = {}
    for i, (nombre, start) in enumerate(headers):
        fin = headers[i + 1][1] if i + 1 < len(headers) else len(text)
        # La primera definición de cada objeto gana (evita pisar con duplicados).
        secciones.setdefault(nombre, text[start:fin])
    return secciones


def parse_all(text: str, objetos: list[str]) -> list[ObjectSpec]:
    """Parsea del texto completo solo los ``objetos`` pedidos, en ese orden."""
    secciones = _split_sections(text)
    specs: list[ObjectSpec] = []
    for nombre in objetos:
        seccion = secciones.get(nombre)
        if seccion is not None:
            specs.append(parse_object(seccion, nombre))
    return specs
