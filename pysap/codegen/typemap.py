"""Mapeo de tipos VB (los que usa el PDF) a anotaciones Python (ADR-0004)."""

from __future__ import annotations

# Tipo VB -> tipo Python. Lo no listado cae a "Any".
_MAPA = {
    "String": "str",
    "Long": "int",
    "Integer": "int",
    "Short": "int",
    "Byte": "bool",  # SAP usa Byte como booleano (True/False) en sus props.
    "Boolean": "bool",
    "Double": "float",
    "Single": "float",
    "Variant": "Any",
    "Object": "Any",
}


def vb_to_python(vb_type: str) -> str:
    """Traduce un tipo VB a Python. Vacío -> ``None`` (Sub sin retorno)."""
    vb = vb_type.strip()
    if not vb:
        return "None"
    return _MAPA.get(vb, "Any")
