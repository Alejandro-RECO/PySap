# -*- coding: utf-8 -*-
# GENERADO automáticamente por pysap.codegen desde el PDF de la API.
# NO EDITAR A MANO: los cambios se perderán al regenerar.

"""GuiButton — wrapper generado."""

from __future__ import annotations

from typing import Any
from pysap.objects.base import GuiComponent


class GuiButton(GuiComponent):
    """GuiButton — objeto SAP (prefijo de tipo 'btn')."""

    @property
    def emphasized(self) -> bool:
        return self._com.Emphasized

    @property
    def left_label(self) -> Any:
        return self._com.LeftLabel
    @left_label.setter
    def left_label(self, value: Any) -> None:
        self._com.LeftLabel = value

    @property
    def right_label(self) -> Any:
        return self._com.RightLabel
    @right_label.setter
    def right_label(self, value: Any) -> None:
        self._com.RightLabel = value

    def press(self) -> None:
        self._com.Press()
