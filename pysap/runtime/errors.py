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


class MissingConfigError(PySapError):
    """Faltan variables de configuración obligatorias (credenciales/conexión).

    Ver ADR-0003: la config se carga del entorno; nunca se versiona.
    """

    def __init__(self, missing: list[str]) -> None:
        self.missing = list(missing)
        nombres = ", ".join(self.missing)
        super().__init__(f"Faltan variables de configuración obligatorias: {nombres}")


class SapLaunchError(PySapError):
    """No se pudo arrancar SAP GUI / enganchar la sesión de scripting.

    Causas: ``saplogon.exe`` no se pudo lanzar, no hay ruta y la ROT no responde,
    o se agotó el tiempo esperando a que el scripting engine estuviera disponible.
    """
