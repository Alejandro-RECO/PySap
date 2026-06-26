"""Emisor: convierte un :class:`ObjectSpec` en código ``.py`` y stub ``.pyi``.

ADR-0004. Los archivos llevan cabecera "GENERADO — NO EDITAR" y se regeneran
desde el PDF. Todos los wrappers heredan de :class:`GuiComponent` (delegación
COM para los miembros heredados que no se emiten).
"""

from __future__ import annotations

import keyword
import re

from pysap.codegen.pdf_parser import MethodSpec, ObjectSpec, Param, PropertySpec
from pysap.codegen.typemap import vb_to_python

# Miembros que ya provee la base GuiComponent: no se reemiten.
_RESERVADOS = frozenset({"id", "type", "name", "text", "com"})

_CABECERA = (
    "# -*- coding: utf-8 -*-\n"
    "# GENERADO automáticamente por pysap.codegen desde el PDF de la API.\n"
    "# NO EDITAR A MANO: los cambios se perderán al regenerar.\n"
)

_RE_S1 = re.compile(r"(.)([A-Z][a-z]+)")
_RE_S2 = re.compile(r"([a-z0-9])([A-Z])")


def snake_case(name: str) -> str:
    """``LeftLabel`` -> ``left_label``; ``Press`` -> ``press``."""
    s1 = _RE_S1.sub(r"\1_\2", name)
    return _RE_S2.sub(r"\1_\2", s1).lower()


def _py_ident(name: str) -> str:
    """Identificador Python válido: snake_case sin colisionar con palabras clave."""
    ident = snake_case(name)
    if keyword.iskeyword(ident) or keyword.issoftkeyword(ident):
        ident += "_"
    return ident


def _unique_params(params: list[Param]) -> list[tuple[str, str]]:
    """Devuelve (nombre_py único, tipo_py) por parámetro, evitando duplicados."""
    salida: list[tuple[str, str]] = []
    vistos: set[str] = set()
    for p in params:
        base = _py_ident(p.name)
        nombre = base
        i = 2
        while nombre in vistos:
            nombre = f"{base}{i}"
            i += 1
        vistos.add(nombre)
        salida.append((nombre, vb_to_python(p.vb_type)))
    return salida


def _usa_any(spec: ObjectSpec) -> bool:
    tipos = [vb_to_python(p.vb_type) for p in spec.properties]
    for m in spec.methods:
        tipos.append(vb_to_python(m.return_type))
        tipos.extend(vb_to_python(p.vb_type) for p in m.params)
    return "Any" in tipos


def _firma_metodo(m: MethodSpec) -> tuple[str, str, str, list[str]]:
    """Devuelve (nombre_py, firma_de_args, tipo_retorno_py, nombres_param)."""
    py_name = _py_ident(m.name)
    params = _unique_params(m.params)
    args = ["self"] + [f"{n}: {t}" for n, t in params]
    ret = vb_to_python(m.return_type)
    return py_name, ", ".join(args), ret, [n for n, _ in params]


def _emit_property(p: PropertySpec) -> list[str]:
    py_name = _py_ident(p.name)
    if py_name in _RESERVADOS:
        return []
    ret = vb_to_python(p.vb_type)
    lineas = [
        "    @property",
        f"    def {py_name}(self) -> {ret}:",
        f"        return self._com.{p.name}",
    ]
    if not p.readonly:
        py_set = vb_to_python(p.vb_type)
        lineas += [
            f"    @{py_name}.setter",
            f"    def {py_name}(self, value: {py_set}) -> None:",
            f"        self._com.{p.name} = value",
        ]
    return lineas


def _emit_method(m: MethodSpec) -> list[str]:
    py_name, args, ret, nombres = _firma_metodo(m)
    if py_name in _RESERVADOS:
        return []
    call_args = ", ".join(nombres)
    llamada = f"self._com.{m.name}({call_args})"
    cuerpo = f"        {llamada}" if ret == "None" else f"        return {llamada}"
    return [f"    def {py_name}({args}) -> {ret}:", cuerpo]


def emit_module(spec: ObjectSpec) -> str:
    """Emite el código fuente ``.py`` del wrapper."""
    out: list[str] = [_CABECERA, '"""' + f"{spec.name} — wrapper generado." + '"""', ""]
    out.append("from __future__ import annotations")
    out.append("")
    if _usa_any(spec):
        out.append("from typing import Any")
    out.append("from pysap.objects.base import GuiComponent")
    out.append("")
    out.append("")
    doc = f"{spec.name} — objeto SAP (prefijo de tipo {spec.prefix!r})."
    out.append(f"class {spec.name}(GuiComponent):")
    out.append(f'    """{doc}"""')

    cuerpo: list[str] = []
    emitidos: set[str] = set()
    for p in spec.properties:
        key = _py_ident(p.name)
        if key in emitidos:
            continue
        lineas = _emit_property(p)
        if lineas:
            cuerpo += [""] + lineas
            emitidos.add(key)
    for m in spec.methods:
        key = _py_ident(m.name)
        if key in emitidos:
            continue
        lineas = _emit_method(m)
        if lineas:
            cuerpo += [""] + lineas
            emitidos.add(key)

    if not cuerpo:
        cuerpo = ["", "    pass"]

    out += cuerpo
    out.append("")
    return "\n".join(out)


def emit_stub(spec: ObjectSpec) -> str:
    """Emite el stub ``.pyi`` (firmas sin cuerpo) del wrapper."""
    out: list[str] = [_CABECERA]
    if _usa_any(spec):
        out.append("from typing import Any")
    out.append("from pysap.objects.base import GuiComponent")
    out.append("")
    out.append("")
    out.append(f"class {spec.name}(GuiComponent):")

    cuerpo: list[str] = []
    emitidos: set[str] = set()
    for p in spec.properties:
        py_name = _py_ident(p.name)
        if py_name in _RESERVADOS or py_name in emitidos:
            continue
        ret = vb_to_python(p.vb_type)
        cuerpo.append("    @property")
        cuerpo.append(f"    def {py_name}(self) -> {ret}: ...")
        if not p.readonly:
            cuerpo.append(f"    @{py_name}.setter")
            cuerpo.append(f"    def {py_name}(self, value: {ret}) -> None: ...")
        emitidos.add(py_name)
    for m in spec.methods:
        py_name, args, ret, _ = _firma_metodo(m)
        if py_name in _RESERVADOS or py_name in emitidos:
            continue
        cuerpo.append(f"    def {py_name}({args}) -> {ret}: ...")
        emitidos.add(py_name)

    if not cuerpo:
        cuerpo = ["    ..."]

    out += cuerpo
    out.append("")
    return "\n".join(out)
