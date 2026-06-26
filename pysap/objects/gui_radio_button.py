# -*- coding: utf-8 -*-
# GENERADO automáticamente por pysap.codegen desde el PDF de la API.
# NO EDITAR A MANO: los cambios se perderán al regenerar.

"""GuiRadioButton — wrapper generado."""

from __future__ import annotations

from typing import Any
from pysap.objects.base import GuiComponent


class GuiRadioButton(GuiComponent):
    """GuiRadioButton — objeto SAP (prefijo de tipo 'rad')."""

    @property
    def char_height(self) -> int:
        return self._com.CharHeight

    @property
    def char_left(self) -> int:
        return self._com.CharLeft

    @property
    def char_top(self) -> int:
        return self._com.CharTop

    @property
    def char_width(self) -> int:
        return self._com.CharWidth

    @property
    def flushing(self) -> bool:
        return self._com.Flushing

    @property
    def group_count(self) -> int:
        return self._com.GroupCount

    @property
    def group_members(self) -> Any:
        return self._com.GroupMembers

    @property
    def group_pos(self) -> int:
        return self._com.GroupPos

    @property
    def is_left_label(self) -> bool:
        return self._com.IsLeftLabel

    @property
    def is_right_label(self) -> bool:
        return self._com.IsRightLabel

    @property
    def left_label(self) -> Any:
        return self._com.LeftLabel

    @property
    def right_label(self) -> Any:
        return self._com.RightLabel

    @property
    def selected(self) -> bool:
        return self._com.Selected
    @selected.setter
    def selected(self, value: bool) -> None:
        self._com.Selected = value

    def select(self) -> None:
        self._com.Select()
