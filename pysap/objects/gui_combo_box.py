# -*- coding: utf-8 -*-
# GENERADO automáticamente por pysap.codegen desde el PDF de la API.
# NO EDITAR A MANO: los cambios se perderán al regenerar.

"""GuiComboBox — wrapper generado."""

from __future__ import annotations

from typing import Any
from pysap.objects.base import GuiComponent


class GuiComboBox(GuiComponent):
    """GuiComboBox — objeto SAP (prefijo de tipo 'cmb')."""

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
    def cur_list_box_entry(self) -> Any:
        return self._com.CurListBoxEntry

    @property
    def flushing(self) -> bool:
        return self._com.Flushing

    @property
    def highlighted(self) -> bool:
        return self._com.Highlighted

    @property
    def is_left_label(self) -> bool:
        return self._com.IsLeftLabel

    @property
    def is_list_box_active(self) -> bool:
        return self._com.IsListBoxActive

    @property
    def is_right_label(self) -> bool:
        return self._com.IsRightLabel

    @property
    def key(self) -> str:
        return self._com.Key

    @property
    def modified(self) -> bool:
        return self._com.Modified
    @modified.setter
    def modified(self, value: bool) -> None:
        self._com.Modified = value

    @property
    def required(self) -> bool:
        return self._com.Required

    @property
    def right_label(self) -> Any:
        return self._com.RightLabel

    @property
    def show_key(self) -> bool:
        return self._com.ShowKey

    @property
    def value(self) -> str:
        return self._com.Value
    @value.setter
    def value(self, value: str) -> None:
        self._com.Value = value

    def set_key_space(self) -> None:
        self._com.SetKeySpace()
