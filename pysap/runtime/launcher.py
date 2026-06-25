"""Arranque de SAP GUI: lanza ``saplogon.exe`` y espera al scripting engine.

ADR-0003: "abrir SAP" cubre el caso de SAP cerrado. Si la Running Object Table
(ROT) ya expone el engine, se engancha sin relanzar; si no, se lanza el binario
y se sondea hasta que la ROT responda o se agote el tiempo.

Las dependencias del SO (``opener``, ``get_engine``, ``sleep``, ``clock``) son
inyectables para poder testear el arranque sin SAP ni proceso real.
"""

from __future__ import annotations

import subprocess
import time
from typing import Any, Callable

from pysap.runtime.connector import _get_scripting_engine
from pysap.runtime.errors import SapLaunchError, SapNotRunningError

# Lanza el ejecutable de SAP Logon (recibe la ruta, devuelve el proceso).
Opener = Callable[[str], Any]
# Devuelve el GuiApplication desde la ROT o lanza SapNotRunningError.
EngineGetter = Callable[[], Any]
Sleeper = Callable[[float], None]
Clock = Callable[[], float]


def launch_sap(
    logon_path: str,
    *,
    opener: Opener = subprocess.Popen,
    get_engine: EngineGetter = _get_scripting_engine,
    sleep: Sleeper = time.sleep,
    clock: Clock = time.perf_counter,
    timeout: float = 30.0,
    poll: float = 0.5,
) -> Any:
    """Garantiza que SAP GUI esté disponible y devuelve el ``GuiApplication``.

    Args:
        logon_path: ruta a ``saplogon.exe`` (necesaria solo si hay que lanzarlo).
        opener: callable que lanza el binario.
        get_engine: callable que obtiene el engine desde la ROT.
        sleep/clock: dependencias de tiempo (inyectables en tests).
        timeout: segundos máximos esperando a que la ROT responda tras lanzar.
        poll: segundos entre sondeos.

    Raises:
        SapLaunchError: si no hay ROT ni ruta para lanzar, o se agota el tiempo.
    """
    # 1) ¿La ROT ya responde? Enganchar sin relanzar.
    try:
        return get_engine()
    except SapNotRunningError:
        pass

    # 2) No responde: hace falta lanzar el binario.
    if not logon_path:
        raise SapLaunchError(
            "SAP GUI no está corriendo y no se indicó 'logon_path' para lanzarlo."
        )
    opener(logon_path)

    # 3) Sondear hasta que el scripting engine esté disponible o expire el tiempo.
    start = clock()
    while True:
        try:
            return get_engine()
        except SapNotRunningError:
            if clock() - start >= timeout:
                raise SapLaunchError(
                    f"Timeout ({timeout}s) esperando a que SAP GUI exponga el "
                    "scripting engine tras lanzar saplogon.exe."
                ) from None
            sleep(poll)
