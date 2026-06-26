# -*- coding: utf-8 -*-
# GENERADO automáticamente por pysap.codegen desde el PDF de la API.
# NO EDITAR A MANO: los cambios se perderán al regenerar.

"""GuiSession — wrapper generado."""

from __future__ import annotations

from typing import Any
from pysap.objects.base import GuiComponent


class GuiSession(GuiComponent):
    """GuiSession — objeto SAP (prefijo de tipo 'ses')."""

    @property
    def acc_enhanced_tab_chain(self) -> bool:
        return self._com.AccEnhancedTabChain
    @acc_enhanced_tab_chain.setter
    def acc_enhanced_tab_chain(self, value: bool) -> None:
        self._com.AccEnhancedTabChain = value

    @property
    def acc_symbol_replacement(self) -> bool:
        return self._com.AccSymbolReplacement
    @acc_symbol_replacement.setter
    def acc_symbol_replacement(self, value: bool) -> None:
        self._com.AccSymbolReplacement = value

    @property
    def active_window(self) -> Any:
        return self._com.ActiveWindow

    @property
    def busy(self) -> bool:
        return self._com.Busy
    @busy.setter
    def busy(self, value: bool) -> None:
        self._com.Busy = value

    @property
    def error_list(self) -> Any:
        return self._com.ErrorList
    @error_list.setter
    def error_list(self, value: Any) -> None:
        self._com.ErrorList = value

    @property
    def info(self) -> Any:
        return self._com.Info

    @property
    def is_active(self) -> bool:
        return self._com.IsActive
    @is_active.setter
    def is_active(self, value: bool) -> None:
        self._com.IsActive = value

    @property
    def is_list_box_active(self) -> bool:
        return self._com.IsListBoxActive

    @property
    def list_box_curr_entry(self) -> int:
        return self._com.ListBoxCurrEntry

    @property
    def list_box_curr_entry_height(self) -> int:
        return self._com.ListBoxCurrEntryHeight

    @property
    def list_box_curr_entry_left(self) -> int:
        return self._com.ListBoxCurrEntryLeft

    @property
    def list_box_curr_entry_top(self) -> int:
        return self._com.ListBoxCurrEntryTop

    @property
    def list_box_curr_entry_width(self) -> int:
        return self._com.ListBoxCurrEntryWidth

    @property
    def list_box_height(self) -> int:
        return self._com.ListBoxHeight

    @property
    def list_box_left(self) -> int:
        return self._com.ListBoxLeft

    @property
    def list_box_top(self) -> int:
        return self._com.ListBoxTop

    @property
    def list_box_width(self) -> int:
        return self._com.ListBoxWidth

    @property
    def passport_pre_system_id(self) -> str:
        return self._com.PassportPreSystemId
    @passport_pre_system_id.setter
    def passport_pre_system_id(self, value: str) -> None:
        self._com.PassportPreSystemId = value

    @property
    def passport_system_id(self) -> str:
        return self._com.PassportSystemId
    @passport_system_id.setter
    def passport_system_id(self, value: str) -> None:
        self._com.PassportSystemId = value

    @property
    def passport_transaction_id(self) -> str:
        return self._com.PassportTransactionId
    @passport_transaction_id.setter
    def passport_transaction_id(self, value: str) -> None:
        self._com.PassportTransactionId = value

    @property
    def progress_percent(self) -> Any:
        return self._com.ProgressPercent

    @property
    def progress_text(self) -> str:
        return self._com.ProgressText

    @property
    def record(self) -> bool:
        return self._com.Record
    @record.setter
    def record(self, value: bool) -> None:
        self._com.Record = value

    @property
    def record_file(self) -> str:
        return self._com.RecordFile
    @record_file.setter
    def record_file(self, value: str) -> None:
        self._com.RecordFile = value

    @property
    def save_as_unicode(self) -> bool:
        return self._com.SaveAsUnicode
    @save_as_unicode.setter
    def save_as_unicode(self, value: bool) -> None:
        self._com.SaveAsUnicode = value

    @property
    def show_dropdown_keys(self) -> bool:
        return self._com.ShowDropdownKeys
    @show_dropdown_keys.setter
    def show_dropdown_keys(self, value: bool) -> None:
        self._com.ShowDropdownKeys = value

    @property
    def suppress_backend_popups(self) -> bool:
        return self._com.SuppressBackendPopups
    @suppress_backend_popups.setter
    def suppress_backend_popups(self, value: bool) -> None:
        self._com.SuppressBackendPopups = value

    @property
    def test_tool_mode(self) -> int:
        return self._com.TestToolMode
    @test_tool_mode.setter
    def test_tool_mode(self, value: int) -> None:
        self._com.TestToolMode = value

    def as_std_number_format(self, number: str) -> str:
        return self._com.AsStdNumberFormat(number)

    def clear_error_list(self) -> None:
        self._com.ClearErrorList()

    def create_session(self) -> None:
        self._com.CreateSession()

    def enable_jaws_events(self) -> None:
        self._com.EnableJawsEvents()

    def end_transaction(self) -> None:
        self._com.EndTransaction()

    def find_by_position(self, x: int, y: int, raise_: Any) -> Any:
        return self._com.FindByPosition(x, y, raise_)

    def get_icon_resource_name(self, text: str) -> str:
        return self._com.GetIconResourceName(text)

    def get_object_tree(self, id: str, props: Any) -> str:
        return self._com.GetObjectTree(id, props)

    def get_v_key_description(self, v_key: int) -> str:
        return self._com.GetVKeyDescription(v_key)

    def lock_session_ui(self) -> None:
        self._com.LockSessionUI()

    def send_command(self, command: str) -> None:
        self._com.SendCommand(command)

    def send_command_async(self, command: str) -> None:
        self._com.SendCommandAsync(command)

    def start_transaction(self, transaction: str) -> None:
        self._com.StartTransaction(transaction)

    def unlock_session_ui(self) -> None:
        self._com.UnlockSessionUI()

    def optional(self) -> None:
        self._com.Optional()

    def sample(self) -> None:
        self._com.Sample()

    def re_dim(self) -> None:
        self._com.ReDim()

    def end(self) -> None:
        self._com.End()

    def with_(self) -> None:
        self._com.With()

    def by_val(self) -> None:
        self._com.ByVal()
