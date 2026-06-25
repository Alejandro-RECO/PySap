"""Tests de SapConfig: carga desde entorno y .env, validación de obligatorias."""

from __future__ import annotations

import pytest

from pysap.config import SapConfig
from pysap.runtime.errors import MissingConfigError

ENV_COMPLETO = {
    "SAP_CONNECTION": "PRD - Producción",
    "SAP_CLIENT": "100",
    "SAP_USER": "USUARIO",
    "SAP_PASSWORD": "secreto",
    "SAP_LANG": "ES",
    "SAP_LOGON_PATH": r"C:\SAP\saplogon.exe",
}


def test_from_env_lee_todas_las_variables():
    cfg = SapConfig.from_env(env=ENV_COMPLETO)  # Arrange + Act
    assert cfg.connection == "PRD - Producción"  # Assert
    assert cfg.client == "100"
    assert cfg.user == "USUARIO"
    assert cfg.password == "secreto"
    assert cfg.language == "ES"
    assert cfg.logon_path == r"C:\SAP\saplogon.exe"


def test_from_env_opcionales_por_defecto_vacias():
    env = {k: v for k, v in ENV_COMPLETO.items() if k not in ("SAP_LANG", "SAP_LOGON_PATH")}
    cfg = SapConfig.from_env(env=env)
    assert cfg.language == ""
    assert cfg.logon_path == ""


def test_from_env_falta_obligatoria_lanza_error():
    env = {k: v for k, v in ENV_COMPLETO.items() if k != "SAP_PASSWORD"}
    with pytest.raises(MissingConfigError) as exc:
        SapConfig.from_env(env=env)
    assert "SAP_PASSWORD" in str(exc.value)


def test_from_env_dotenv_rellena_valores(tmp_path):
    dotenv = tmp_path / ".env"
    dotenv.write_text(
        "\n".join(
            [
                "# credenciales de prueba",
                'SAP_CONNECTION="PRD - Producción"',
                "SAP_CLIENT=100",
                "SAP_USER=USUARIO",
                "SAP_PASSWORD=secreto",
                "",
            ]
        ),
        encoding="utf-8",
    )
    cfg = SapConfig.from_env(env={}, dotenv_path=str(dotenv))
    assert cfg.user == "USUARIO"
    assert cfg.password == "secreto"


def test_from_env_el_entorno_pisa_al_dotenv(tmp_path):
    dotenv = tmp_path / ".env"
    dotenv.write_text("SAP_USER=DESDE_ENV_FILE\n", encoding="utf-8")
    env = dict(ENV_COMPLETO, SAP_USER="DESDE_ENTORNO")
    cfg = SapConfig.from_env(env=env, dotenv_path=str(dotenv))
    assert cfg.user == "DESDE_ENTORNO"
