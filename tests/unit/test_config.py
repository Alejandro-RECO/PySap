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


# --- from_settings: credenciales desde una clase Settings (ADR-0007) ---------


class FakeSettings:
    """Imita una clase Settings (pydantic BaseSettings) con atributos sap_*."""

    def __init__(self, **valores):
        # Valores por defecto completos; los kwargs sobrescriben o eliminan.
        defaults = {
            "sap_connection": "PRD - Producción",
            "sap_client": "100",
            "sap_user": "USUARIO",
            "sap_password": "secreto",
            "sap_lang": "ES",
            "sap_logon_path": r"C:\SAP\saplogon.exe",
        }
        defaults.update(valores)
        for clave, valor in defaults.items():
            setattr(self, clave, valor)


def test_from_settings_mapeo_por_defecto_construye_config():
    cfg = SapConfig.from_settings(FakeSettings())  # Arrange + Act
    assert cfg.connection == "PRD - Producción"  # Assert
    assert cfg.client == "100"
    assert cfg.user == "USUARIO"
    assert cfg.password == "secreto"
    assert cfg.language == "ES"
    assert cfg.logon_path == r"C:\SAP\saplogon.exe"


def test_from_settings_falta_obligatoria_lanza_error():
    settings = FakeSettings(sap_password="")  # obligatoria vacía
    with pytest.raises(MissingConfigError) as exc:
        SapConfig.from_settings(settings)
    assert "sap_password" in str(exc.value)


def test_from_settings_opcionales_ausentes_quedan_vacias():
    settings = FakeSettings(sap_lang="", sap_logon_path="")
    cfg = SapConfig.from_settings(settings)
    assert cfg.language == ""
    assert cfg.logon_path == ""


def test_from_settings_mapeo_a_medida():
    class SettingsPropia:
        conexion = "QAS - Calidad"
        mandante = "200"
        usuario = "OTRO"
        clave = "pwd"

    mapping = {
        "connection": "conexion",
        "client": "mandante",
        "user": "usuario",
        "password": "clave",
    }
    cfg = SapConfig.from_settings(SettingsPropia(), mapping=mapping)
    assert cfg.connection == "QAS - Calidad"
    assert cfg.client == "200"
    assert cfg.user == "OTRO"
    assert cfg.password == "pwd"
    assert cfg.language == ""  # no mapeada -> vacía
