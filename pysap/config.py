"""Configuración de PySap: credenciales y datos de conexión desde el entorno.

ADR-0003: las credenciales nunca se versionan. Se leen de variables de entorno
(``SAP_*``), con un archivo ``.env`` opcional para desarrollo. El entorno real
tiene prioridad sobre el ``.env``.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass

from pysap.runtime.errors import MissingConfigError

# Variable de entorno -> atributo y si es obligatoria.
_OBLIGATORIAS = {
    "SAP_CONNECTION": "connection",
    "SAP_CLIENT": "client",
    "SAP_USER": "user",
    "SAP_PASSWORD": "password",
}
_OPCIONALES = {
    "SAP_LANG": "language",
    "SAP_LOGON_PATH": "logon_path",
}


def _read_dotenv(path: str) -> dict[str, str]:
    """Lee un archivo ``.env`` simple (``KEY=VALUE``).

    Ignora líneas vacías y comentarios (``#``); quita comillas envolventes.
    """
    valores: dict[str, str] = {}
    with open(path, encoding="utf-8") as fichero:
        for linea in fichero:
            linea = linea.strip()
            if not linea or linea.startswith("#") or "=" not in linea:
                continue
            clave, _, valor = linea.partition("=")
            valor = valor.strip()
            if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in ("'", '"'):
                valor = valor[1:-1]
            valores[clave.strip()] = valor
    return valores


@dataclass(frozen=True)
class SapConfig:
    """Datos para abrir SAP y hacer login. Cárgalo con :meth:`from_env`."""

    connection: str
    client: str
    user: str
    password: str
    language: str = ""
    logon_path: str = ""

    @classmethod
    def from_env(
        cls,
        env: Mapping[str, str] | None = None,
        *,
        dotenv_path: str | None = None,
    ) -> SapConfig:
        """Construye la config desde el entorno (y un ``.env`` opcional).

        Args:
            env: mapa de variables (por defecto ``os.environ``).
            dotenv_path: ruta a un ``.env`` que rellena valores ausentes; el
                entorno tiene prioridad sobre él.

        Raises:
            MissingConfigError: si falta alguna variable obligatoria.
        """
        valores: dict[str, str] = {}
        if dotenv_path is not None:
            valores.update(_read_dotenv(dotenv_path))
        base = os.environ if env is None else env
        valores.update(base)  # el entorno pisa al .env

        faltantes = [var for var in _OBLIGATORIAS if not valores.get(var)]
        if faltantes:
            raise MissingConfigError(faltantes)

        campos = {attr: valores[var] for var, attr in _OBLIGATORIAS.items()}
        campos.update({attr: valores.get(var, "") for var, attr in _OPCIONALES.items()})
        return cls(**campos)
