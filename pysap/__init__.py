"""PySap — marco Python para SAP GUI Scripting API."""

from pysap.runtime.connector import connect, open_connection
from pysap.runtime.session import Session
from pysap.runtime.errors import (
    PySapError,
    SapNotRunningError,
    ComponentNotFoundError,
    WaitTimeoutError,
    SapMessageError,
)

__version__ = "0.1.0"

__all__ = [
    "connect",
    "open_connection",
    "Session",
    "PySapError",
    "SapNotRunningError",
    "ComponentNotFoundError",
    "WaitTimeoutError",
    "SapMessageError",
]
