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


class WaitTimeoutError(PySapError):
    """Se agotó el tiempo esperando a que una condición se cumpliera."""


class SapMessageError(PySapError):
    """SAP reportó un mensaje de error/aborto en la barra de estado."""

    def __init__(self, message_type: str, text: str) -> None:
        self.message_type = message_type
        self.text = text
        super().__init__(f"SAP [{message_type}]: {text}")
