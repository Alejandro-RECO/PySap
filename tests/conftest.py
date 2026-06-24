"""Fixtures compartidas: sesión SAP mockeada lista para usar."""

from __future__ import annotations

import pytest

from pysap import connect
from pysap.runtime.session import Session
from tests.mocks.fake_sap import FakeComponent, FakeSession, build_app


@pytest.fixture
def fake_session() -> FakeSession:
    """Sesión falsa con un botón y un campo de texto típicos."""
    session = FakeSession()
    session.add(FakeComponent("wnd[0]/tbar[0]/btn[0]", type="GuiButton", name="btn[0]"))
    session.add(
        FakeComponent("wnd[0]/usr/txtF1", type="GuiTextField", name="txtF1", text="")
    )
    session.add(FakeComponent("wnd[0]/tbar[0]/okcd", type="GuiOkCodeField"))
    session.add(FakeComponent("wnd[0]", type="GuiMainWindow"))
    return session


@pytest.fixture
def session(fake_session: FakeSession) -> Session:
    """Wrapper :class:`Session` de PySap sobre la sesión falsa."""
    app = build_app(fake_session)
    return connect(application=app)
