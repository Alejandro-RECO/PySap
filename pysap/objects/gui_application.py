# -*- coding: utf-8 -*-
# GENERADO automáticamente por pysap.codegen desde el PDF de la API.
# NO EDITAR A MANO: los cambios se perderán al regenerar.

"""GuiApplication — wrapper generado."""

from __future__ import annotations

from typing import Any
from pysap.objects.base import GuiComponent


class GuiApplication(GuiComponent):
    """GuiApplication — objeto SAP (prefijo de tipo '')."""

    @property
    def active_session(self) -> Any:
        return self._com.ActiveSession

    @property
    def allow_system_messages(self) -> bool:
        return self._com.AllowSystemMessages
    @allow_system_messages.setter
    def allow_system_messages(self, value: bool) -> None:
        self._com.AllowSystemMessages = value

    @property
    def buttonbar_visible(self) -> bool:
        return self._com.ButtonbarVisible
    @buttonbar_visible.setter
    def buttonbar_visible(self, value: bool) -> None:
        self._com.ButtonbarVisible = value

    @property
    def children(self) -> Any:
        return self._com.Children

    @property
    def connection_error_text(self) -> str:
        return self._com.ConnectionErrorText

    @property
    def connections(self) -> Any:
        return self._com.Connections

    @property
    def history_enabled(self) -> bool:
        return self._com.HistoryEnabled
    @history_enabled.setter
    def history_enabled(self, value: bool) -> None:
        self._com.HistoryEnabled = value

    @property
    def major_version(self) -> int:
        return self._com.MajorVersion

    @property
    def minor_version(self) -> int:
        return self._com.MinorVersion

    @property
    def new_visual_design(self) -> bool:
        return self._com.NewVisualDesign

    @property
    def patchlevel(self) -> int:
        return self._com.Patchlevel

    @property
    def revision(self) -> int:
        return self._com.Revision

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

    @property
    def utils(self) -> Any:
        return self._com.Utils

    def add_history_entry(self, fieldname: str, value: str) -> bool:
        return self._com.AddHistoryEntry(fieldname, value)

    def create_gui_collection(self) -> Any:
        return self._com.CreateGuiCollection()

    def drop_history(self) -> bool:
        return self._com.DropHistory()

    def ignore(self, window_handle: int) -> None:
        self._com.Ignore(window_handle)

    def open_connection(self, description: str, sync: Any, raise_: Any) -> Any:
        return self._com.OpenConnection(description, sync, raise_)

    def open_connection_by_connection_string(self, connect_string: str, sync: Any, raise_: Any) -> Any:
        return self._com.OpenConnectionByConnectionString(connect_string, sync, raise_)

    def register_rot(self) -> bool:
        return self._com.RegisterROT()

    def revoke_rot(self) -> None:
        self._com.RevokeROT()

    def as_(self) -> None:
        self._com.As()

    def optional(self) -> None:
        self._com.Optional()
