"""Tests de integración contra SAP GUI real.

Marcados con ``@pytest.mark.sap`` — excluidos por defecto (ver pyproject.toml).
Ejecutar con SAP GUI abierto y scripting habilitado::

    pytest -m sap
"""

from __future__ import annotations

import pytest

from pysap import connect
from pysap.runtime.errors import SapNotRunningError


@pytest.mark.sap
def test_conecta_a_sesion_real():
    try:
        session = connect()
    except SapNotRunningError:
        pytest.skip("SAP GUI no está corriendo / scripting deshabilitado")
    assert session.info.User != ""
