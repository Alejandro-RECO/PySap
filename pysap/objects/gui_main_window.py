# -*- coding: utf-8 -*-
# GENERADO automáticamente por pysap.codegen desde el PDF de la API.
# NO EDITAR A MANO: los cambios se perderán al regenerar.

"""GuiMainWindow — wrapper generado."""

from __future__ import annotations

from pysap.objects.base import GuiComponent


class GuiMainWindow(GuiComponent):
    """GuiMainWindow — objeto SAP (prefijo de tipo '')."""

    @property
    def buttonbar_visible(self) -> bool:
        return self._com.ButtonbarVisible
    @buttonbar_visible.setter
    def buttonbar_visible(self, value: bool) -> None:
        self._com.ButtonbarVisible = value

    @property
    def statusbar_visible(self) -> bool:
        return self._com.StatusbarVisible
    @statusbar_visible.setter
    def statusbar_visible(self, value: bool) -> None:
        self._com.StatusbarVisible = value

    @property
    def titlebar_visible(self) -> bool:
        return self._com.TitlebarVisible
    @titlebar_visible.setter
    def titlebar_visible(self, value: bool) -> None:
        self._com.TitlebarVisible = value

    @property
    def toolbar_visible(self) -> bool:
        return self._com.ToolbarVisible
    @toolbar_visible.setter
    def toolbar_visible(self, value: bool) -> None:
        self._com.ToolbarVisible = value

    def resize_working_pane(self, width: int, height: int, throw_on_fail: bool) -> None:
        self._com.ResizeWorkingPane(width, height, throw_on_fail)

    def resize_working_pane_ex(self, width: int, height: int, throw_on_fail: bool) -> None:
        self._com.ResizeWorkingPaneEx(width, height, throw_on_fail)

    def by_val(self) -> None:
        self._com.ByVal()

    def the(self) -> None:
        self._com.The()
