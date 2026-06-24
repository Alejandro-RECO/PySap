"""Excepciones del marco PySap."""

from __future__ import annotations


class PySapError(Exception):
    """Error base de PySap."""


class SapNotRunningError(PySapError):
    """No se encontró SAP GUI en la Running Object Table.

    Causas típicas: SAP GUI no abierto, sin sesión activa, o scripting
    deshabilitado en cliente/servidor.
    """


class ComponentNotFoundError(PySapError):
    """No existe un componente con el ``id``/``path`` solicitado."""

    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__(f"No se encontró el componente SAP con path: {path!r}")


class StepError(PySapError):
    """Falló la ejecución o la verificación de un Step."""
