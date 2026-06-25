"""Bootstrap: integra arranque, conexión y login en un flujo medible.

ADR-0003 (Fase 5, demo end-to-end). Reúne las piezas existentes:
``launch_sap`` -> ``open_connection`` -> ``Session.login`` ejecutado como un
``Process`` de ``Step``s y verificado con el feedback de la barra de estado.
"""

from __future__ import annotations

from typing import Any, Callable

from pysap.config import SapConfig
from pysap.process.process import Process
from pysap.process.step import Step
from pysap.runtime.connector import open_connection
from pysap.runtime.launcher import launch_sap
from pysap.runtime.session import Session

# Garantiza SAP disponible y devuelve el GuiApplication (recibe el logon_path).
Launcher = Callable[[str], Any]


def start_session(
    config: SapConfig,
    *,
    application: Any | None = None,
    launcher: Launcher = launch_sap,
) -> Session:
    """Abre SAP (si hace falta), abre la conexión y hace login.

    Args:
        config: credenciales y datos de conexión (ver :class:`SapConfig`).
        application: ``GuiApplication`` ya resuelto; si es ``None`` se obtiene
            con ``launcher`` (que arranca SAP si no está corriendo).
        launcher: estrategia de arranque (inyectable en tests).

    Returns:
        La :class:`Session` ya logueada, lista para operar.
    """
    app = application if application is not None else launcher(config.logon_path)
    session = open_connection(config.connection, application=app)

    proceso = Process("login").add(
        Step(
            "login",
            action=lambda s: s.login(
                config.client, config.user, config.password, config.language
            ),
            verify=lambda s: not s.status().is_error,
        )
    )
    proceso.run(session)
    return session
