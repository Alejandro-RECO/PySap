# -*- coding: utf-8 -*-
# GENERADO automáticamente por pysap.codegen desde el PDF de la API.
# NO EDITAR A MANO: los cambios se perderán al regenerar.

"""GuiStatusbar — wrapper generado."""

from __future__ import annotations

from pysap.objects.base import GuiComponent


class GuiStatusbar(GuiComponent):
    """GuiStatusbar — objeto SAP (prefijo de tipo 'sbar')."""

    @property
    def handle(self) -> int:
        return self._com.Handle

    @property
    def message_as_popup(self) -> bool:
        return self._com.MessageAsPopup

    @property
    def message_has_long_text(self) -> int:
        return self._com.MessageHasLongText

    @property
    def message_id(self) -> str:
        return self._com.MessageId

    @property
    def message_number(self) -> str:
        return self._com.MessageNumber

    @property
    def message_parameter(self) -> str:
        return self._com.MessageParameter

    @property
    def message_type(self) -> str:
        return self._com.MessageType

    def create_support_message_click(self) -> None:
        self._com.CreateSupportMessageClick()

    def double_click(self) -> None:
        self._com.DoubleClick()

    def service_request_click(self) -> None:
        self._com.ServiceRequestClick()
