# -*- coding: utf-8 -*-
# GENERADO automáticamente por pysap.codegen desde el PDF de la API.
# NO EDITAR A MANO: los cambios se perderán al regenerar.

"""GuiCheckBox — wrapper generado."""

from __future__ import annotations

from typing import Any
from pysap.objects.base import GuiComponent


class GuiCheckBox(GuiComponent):
    """GuiCheckBox — objeto SAP (prefijo de tipo 'chk')."""

    @property
    def color_index(self) -> int:
        return self._com.ColorIndex

    @property
    def color_intensified(self) -> bool:
        return self._com.ColorIntensified

    @property
    def color_inverse(self) -> bool:
        return self._com.ColorInverse

    @property
    def flushing(self) -> bool:
        return self._com.Flushing

    @property
    def is_left_label(self) -> bool:
        return self._com.IsLeftLabel

    @property
    def is_list_element(self) -> bool:
        return self._com.IsListElement

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
    def row_text(self) -> str:
        return self._com.RowText

    @property
    def selected(self) -> bool:
        return self._com.Selected
    @selected.setter
    def selected(self, value: bool) -> None:
        self._com.Selected = value

    @property
    def count(self) -> int:
        return self._com.Count

    @property
    def length(self) -> int:
        return self._com.Length

    @property
    def new_enum(self) -> Any:
        return self._com.NewEnum

    @property
    def type_(self) -> str:
        return self._com.Type

    @property
    def type_as_number(self) -> int:
        return self._com.TypeAsNumber

    def get_list_property(self, property: str) -> str:
        return self._com.GetListProperty(property)

    def get_list_property_non_rec(self, property: str) -> str:
        return self._com.GetListPropertyNonRec(property)
