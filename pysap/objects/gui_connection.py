# -*- coding: utf-8 -*-
# GENERADO automáticamente por pysap.codegen desde el PDF de la API.
# NO EDITAR A MANO: los cambios se perderán al regenerar.

"""GuiConnection — wrapper generado."""

from __future__ import annotations

from typing import Any
from pysap.objects.base import GuiComponent


class GuiConnection(GuiComponent):
    """GuiConnection — objeto SAP (prefijo de tipo '')."""

    @property
    def children(self) -> Any:
        return self._com.Children

    @property
    def connection_string(self) -> str:
        return self._com.ConnectionString

    @property
    def description(self) -> str:
        return self._com.Description

    @property
    def disabled_by_server(self) -> bool:
        return self._com.DisabledByServer

    @property
    def sessions(self) -> Any:
        return self._com.Sessions

    def close_connection(self) -> None:
        self._com.CloseConnection()

    def close_session(self, id: str) -> None:
        self._com.CloseSession(id)
