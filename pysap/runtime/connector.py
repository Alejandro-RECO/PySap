"""Conexión a SAP GUI vía COM (Running Object Table).

Modelo de objetos (ver SAP GUI Scripting API):

    GetObject("SAPGUI").GetScriptingEngine
      -> application (GuiApplication)
           -> connection (GuiConnection)   application.Children(n)
                -> session (GuiSession)     connection.Children(n)
                     -> findById(path)
"""

from __future__ import annotations

import time
from typing import Any, Callable

from pysap.runtime.errors import SapNotRunningError, WaitTimeoutError
from pysap.runtime.session import Session

Sleeper = Callable[[float], None]
Clock = Callable[[], float]


def _get_scripting_engine() -> Any:
    """Obtiene el GuiApplication desde la ROT. Aislado para poder mockearlo."""
    try:
        import win32com.client  # import diferido: solo Windows con pywin32
    except ImportError as exc:  # pragma: no cover - entorno sin pywin32
        raise SapNotRunningError(
            "pywin32 no está instalado; no se puede acceder a SAP GUI por COM."
        ) from exc

    try:
        rot = win32com.client.GetObject("SAPGUI")
        return rot.GetScriptingEngine
    except Exception as exc:  # pragma: no cover - requiere SAP real
        raise SapNotRunningError(
            "No se encontró SAP GUI en ejecución. Verifica que esté abierto "
            "y que el scripting esté habilitado."
        ) from exc


def connect(
    connection_index: int = 0,
    session_index: int = 0,
    *,
    application: Any | None = None,
) -> Session:
    """Engancha a una sesión SAP existente y la devuelve envuelta en :class:`Session`.

    Args:
        connection_index: índice de la conexión (``application.Children``).
        session_index: índice de la sesión dentro de la conexión.
        application: GuiApplication ya resuelto (para tests/mock). Si es
            ``None`` se obtiene desde la ROT.
    """
    app = application if application is not None else _get_scripting_engine()

    if app.Children.Count <= connection_index:
        raise SapNotRunningError(
            f"No existe la conexión índice {connection_index} (hay {app.Children.Count})."
        )
    connection = app.Children(connection_index)

    if connection.Children.Count <= session_index:
        raise SapNotRunningError(
            f"No existe la sesión índice {session_index} (hay {connection.Children.Count})."
        )
    com_session = connection.Children(session_index)

    return Session(com_session)


def open_connection(
    description: str,
    *,
    session_index: int = 0,
    sync: bool = True,
    application: Any | None = None,
    sleep: Sleeper = time.sleep,
    clock: Clock = time.perf_counter,
    timeout: float = 30.0,
    poll: float = 0.5,
) -> Session:
    """Abre una conexión nueva por su descripción en SAP Logon y devuelve la sesión.

    SAP puebla la sesión de forma asíncrona: aunque ``OpenConnection`` sea
    síncrona, ``connection.Children`` puede tardar en exponer la sesión. Se
    sondea hasta que aparezca o se agote el tiempo (evita el error COM 614
    "enumerator cannot find element with the specified index").

    Args:
        description: nombre de la entrada en SAP Logon (o cadena de conexión).
        session_index: sesión a usar dentro de la conexión recién abierta.
        sync: abrir de forma síncrona (espera a que esté lista).
        application: GuiApplication ya resuelto (para tests/mock).
        sleep/clock: dependencias de tiempo (inyectables en tests).
        timeout: segundos máximos esperando a que aparezca la sesión.
        poll: segundos entre sondeos.

    Raises:
        WaitTimeoutError: si la sesión no aparece antes de ``timeout``.
    """
    app = application if application is not None else _get_scripting_engine()
    connection = app.OpenConnection(description, sync)

    start = clock()
    while connection.Children.Count <= session_index:
        if clock() - start >= timeout:
            raise WaitTimeoutError(
                f"Timeout ({timeout}s) esperando a que la conexión {description!r} "
                f"exponga la sesión índice {session_index}."
            )
        sleep(poll)

    com_session = connection.Children(session_index)
    return Session(com_session)
