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

# Campos de SapConfig, derivados de los mapeos anteriores (sin duplicar).
_CAMPOS_OBLIGATORIOS = tuple(_OBLIGATORIAS.values())
_CAMPOS_OPCIONALES = tuple(_OPCIONALES.values())

# Mapeo por defecto campo de SapConfig -> atributo en la clase Settings
# (convención sap_* snake_case, la típica de pydantic BaseSettings sobre SAP_*).
_SETTINGS_MAP = {
    "connection": "sap_connection",
    "client": "sap_client",
    "user": "sap_user",
    "password": "sap_password",
    "language": "sap_lang",
    "logon_path": "sap_logon_path",
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

    @classmethod
    def from_settings(
        cls,
        settings: object,
        *,
        mapping: Mapping[str, str] | None = None,
    ) -> SapConfig:
        """Construye la config desde un objeto de settings (p.ej. pydantic
        ``BaseSettings``).

        Lee los valores por atributo (duck typing): no acopla PySap a pydantic
        ni a ninguna librería; sirve cualquier objeto con los atributos
        esperados (ver ADR-0007).

        Args:
            settings: objeto cuyos atributos contienen la configuración SAP.
            mapping: mapa ``{campo_SapConfig: atributo_en_settings}``; por
                defecto :data:`_SETTINGS_MAP` (convención ``sap_*``). Pásalo si
                tu ``Settings`` usa otros nombres.

        Raises:
            MissingConfigError: si falta alguna variable obligatoria.
        """
        m = mapping or _SETTINGS_MAP
        valores: dict[str, str] = {}
        for campo, attr in m.items():
            valor = getattr(settings, attr, None)
            # pydantic puede entregar SecretStr/int: se normaliza a str.
            if valor is not None and str(valor) != "":
                valores[campo] = str(valor)

        faltantes = [m.get(campo, campo) for campo in _CAMPOS_OBLIGATORIOS if not valores.get(campo)]
        if faltantes:
            raise MissingConfigError(faltantes)

        campos = {c: valores.get(c, "") for c in (*_CAMPOS_OBLIGATORIOS, *_CAMPOS_OPCIONALES)}
        return cls(**campos)
