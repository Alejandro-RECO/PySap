"""PySap — marco Python para SAP GUI Scripting API."""

from pysap.runtime.connector import connect
from pysap.runtime.session import Session
from pysap.runtime.errors import (
    PySapError,
    SapNotRunningError,
    ComponentNotFoundError,
)

__version__ = "0.1.0"

__all__ = [
    "connect",
    "Session",
    "PySapError",
    "SapNotRunningError",
    "ComponentNotFoundError",
]
