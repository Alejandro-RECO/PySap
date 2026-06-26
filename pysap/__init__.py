"""PySap — marco Python para SAP GUI Scripting API."""

from pysap.config import SapConfig
from pysap.runtime.connector import connect, open_connection
from pysap.runtime.bootstrap import start_session
from pysap.runtime.launcher import launch_sap
from pysap.runtime.session import Session
from pysap.runtime.errors import (
    PySapError,
    SapNotRunningError,
    ComponentNotFoundError,
    ComponentTypeError,
    WaitTimeoutError,
    SapMessageError,
    MissingConfigError,
    SapLaunchError,
)

__version__ = "0.1.0"

__all__ = [
    "connect",
    "open_connection",
    "start_session",
    "launch_sap",
    "SapConfig",
    "Session",
    "PySapError",
    "SapNotRunningError",
    "ComponentNotFoundError",
    "ComponentTypeError",
    "WaitTimeoutError",
    "SapMessageError",
    "MissingConfigError",
    "SapLaunchError",
]
