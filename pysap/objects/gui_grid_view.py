# -*- coding: utf-8 -*-
# GENERADO automáticamente por pysap.codegen desde el PDF de la API.
# NO EDITAR A MANO: los cambios se perderán al regenerar.

"""GuiGridView — wrapper generado."""

from __future__ import annotations

from typing import Any
from pysap.objects.base import GuiComponent


class GuiGridView(GuiComponent):
    """GuiGridView — objeto SAP (prefijo de tipo '')."""

    @property
    def column_count(self) -> int:
        return self._com.ColumnCount

    @property
    def column_order(self) -> Any:
        return self._com.ColumnOrder
    @column_order.setter
    def column_order(self, value: Any) -> None:
        self._com.ColumnOrder = value

    @property
    def current_cell_column(self) -> str:
        return self._com.CurrentCellColumn
    @current_cell_column.setter
    def current_cell_column(self, value: str) -> None:
        self._com.CurrentCellColumn = value

    @property
    def current_cell_row(self) -> int:
        return self._com.CurrentCellRow
    @current_cell_row.setter
    def current_cell_row(self, value: int) -> None:
        self._com.CurrentCellRow = value

    @property
    def first_visible_column(self) -> str:
        return self._com.FirstVisibleColumn
    @first_visible_column.setter
    def first_visible_column(self, value: str) -> None:
        self._com.FirstVisibleColumn = value

    @property
    def first_visible_row(self) -> int:
        return self._com.FirstVisibleRow
    @first_visible_row.setter
    def first_visible_row(self, value: int) -> None:
        self._com.FirstVisibleRow = value

    @property
    def frozen_column_count(self) -> int:
        return self._com.FrozenColumnCount

    @property
    def row_count(self) -> int:
        return self._com.RowCount

    @property
    def selected_cells(self) -> Any:
        return self._com.SelectedCells
    @selected_cells.setter
    def selected_cells(self, value: Any) -> None:
        self._com.SelectedCells = value

    @property
    def selected_columns(self) -> Any:
        return self._com.SelectedColumns
    @selected_columns.setter
    def selected_columns(self, value: Any) -> None:
        self._com.SelectedColumns = value

    @property
    def selected_rows(self) -> str:
        return self._com.SelectedRows
    @selected_rows.setter
    def selected_rows(self, value: str) -> None:
        self._com.SelectedRows = value

    @property
    def selection_mode(self) -> str:
        return self._com.SelectionMode

    @property
    def title(self) -> str:
        return self._com.Title

    @property
    def toolbar_button_count(self) -> int:
        return self._com.ToolbarButtonCount

    @property
    def visible_row_count(self) -> int:
        return self._com.VisibleRowCount

    def clear_selection(self) -> None:
        self._com.ClearSelection()

    def click(self, row: int, column: str) -> None:
        self._com.Click(row, column)

    def click_current_cell(self) -> None:
        self._com.ClickCurrentCell()

    def context_menu(self) -> None:
        self._com.ContextMenu()

    def current_cell_moved(self) -> None:
        self._com.CurrentCellMoved()

    def delete_rows(self, rows: str) -> None:
        self._com.DeleteRows(rows)

    def deselect_column(self, column: str) -> None:
        self._com.DeselectColumn(column)

    def double_click(self, row: int, column: str) -> None:
        self._com.DoubleClick(row, column)

    def double_click_current_cell(self) -> None:
        self._com.DoubleClickCurrentCell()

    def duplicate_rows(self, rows: str) -> None:
        self._com.DuplicateRows(rows)

    def get_cell_changeable(self, row: int, column: str) -> bool:
        return self._com.GetCellChangeable(row, column)

    def get_cell_check_box_checked(self, row: int, column: str) -> bool:
        return self._com.GetCellCheckBoxChecked(row, column)

    def get_cell_color(self, row: int, column: str) -> int:
        return self._com.GetCellColor(row, column)

    def get_cell_height(self, row: int, column: str) -> int:
        return self._com.GetCellHeight(row, column)

    def get_cell_hotspot_type(self, row: int, column: str) -> str:
        return self._com.GetCellHotspotType(row, column)

    def get_cell_icon(self, row: int, column: str) -> str:
        return self._com.GetCellIcon(row, column)

    def get_cell_left(self, row: int, column: str) -> int:
        return self._com.GetCellLeft(row, column)

    def get_cell_list_box_count(self, row: int, column: str) -> int:
        return self._com.GetCellListBoxCount(row, column)

    def get_cell_list_box_cur_index(self, row: int, column: str) -> str:
        return self._com.GetCellListBoxCurIndex(row, column)

    def get_cell_max_length(self, row: int, column: str) -> int:
        return self._com.GetCellMaxLength(row, column)

    def get_cell_state(self, row: int, column: str) -> str:
        return self._com.GetCellState(row, column)

    def get_cell_tooltip(self, row: int, column: str) -> str:
        return self._com.GetCellTooltip(row, column)

    def get_cell_top(self, row: int, column: str) -> int:
        return self._com.GetCellTop(row, column)

    def get_cell_type(self, row: int, column: str) -> str:
        return self._com.GetCellType(row, column)

    def get_cell_value(self, row: int, column: str) -> str:
        return self._com.GetCellValue(row, column)

    def get_cell_width(self, row: int, column: str) -> int:
        return self._com.GetCellWidth(row, column)

    def get_color_info(self, color: int) -> str:
        return self._com.GetColorInfo(color)

    def get_column_data_type(self, column: str) -> str:
        return self._com.GetColumnDataType(column)

    def get_column_operation_type(self, column: str) -> str:
        return self._com.GetColumnOperationType(column)

    def get_column_position(self, column: str) -> int:
        return self._com.GetColumnPosition(column)

    def get_column_sort_type(self, column: str) -> str:
        return self._com.GetColumnSortType(column)

    def get_column_titles(self, column: str) -> Any:
        return self._com.GetColumnTitles(column)

    def get_column_tooltip(self, column: str) -> str:
        return self._com.GetColumnTooltip(column)

    def get_column_total_type(self, column: str) -> str:
        return self._com.GetColumnTotalType(column)

    def get_displayed_column_title(self, column: str) -> str:
        return self._com.GetDisplayedColumnTitle(column)

    def get_row_total_level(self, row: int) -> int:
        return self._com.GetRowTotalLevel(row)

    def get_symbol_info(self, symbol: str) -> str:
        return self._com.GetSymbolInfo(symbol)

    def get_toolbar_button_checked(self, button_pos: int) -> bool:
        return self._com.GetToolbarButtonChecked(button_pos)

    def get_toolbar_button_enabled(self, button_pos: int) -> bool:
        return self._com.GetToolbarButtonEnabled(button_pos)

    def get_toolbar_button_icon(self, button_pos: int) -> str:
        return self._com.GetToolbarButtonIcon(button_pos)

    def get_toolbar_button_id(self, button_pos: int) -> str:
        return self._com.GetToolbarButtonId(button_pos)

    def get_toolbar_button_text(self, button_pos: int) -> str:
        return self._com.GetToolbarButtonText(button_pos)

    def get_toolbar_button_tooltip(self, button_pos: int) -> str:
        return self._com.GetToolbarButtonTooltip(button_pos)

    def get_toolbar_button_type(self, button_pos: int) -> str:
        return self._com.GetToolbarButtonType(button_pos)

    def get_toolbar_focus_button(self) -> int:
        return self._com.GetToolbarFocusButton()

    def has_cell_f4_help(self, row: int, column: str) -> bool:
        return self._com.HasCellF4Help(row, column)

    def history_cur_entry(self, row: int, column: str) -> str:
        return self._com.HistoryCurEntry(row, column)

    def history_cur_index(self, row: int, column: str) -> int:
        return self._com.HistoryCurIndex(row, column)

    def history_is_active(self, row: int, column: str) -> bool:
        return self._com.HistoryIsActive(row, column)

    def history_list(self, row: int, column: str) -> Any:
        return self._com.HistoryList(row, column)

    def insert_rows(self, rows: str) -> None:
        self._com.InsertRows(rows)

    def is_cell_hotspot(self, row: int, column: str) -> bool:
        return self._com.IsCellHotspot(row, column)

    def is_cell_symbol(self, row: int, column: str) -> bool:
        return self._com.IsCellSymbol(row, column)

    def is_cell_total_expander(self, row: int, column: str) -> bool:
        return self._com.IsCellTotalExpander(row, column)

    def is_column_filtered(self, column: str) -> bool:
        return self._com.IsColumnFiltered(column)

    def is_column_key(self, column: str) -> bool:
        return self._com.IsColumnKey(column)

    def is_total_row_expanded(self, row: int) -> bool:
        return self._com.IsTotalRowExpanded(row)

    def modify_cell(self, row: int, column: str, value: str) -> None:
        self._com.ModifyCell(row, column, value)

    def modify_check_box(self, row: int, column: str, checked: bool) -> None:
        self._com.ModifyCheckBox(row, column, checked)

    def move_rows(self, from_row: int, to_row: int, dest_row: int) -> None:
        self._com.MoveRows(from_row, to_row, dest_row)

    def press_button(self, row: int, column: str) -> None:
        self._com.PressButton(row, column)

    def press_button_current_cell(self) -> None:
        self._com.PressButtonCurrentCell()

    def press_column_header(self, column: str) -> None:
        self._com.PressColumnHeader(column)

    def press_enter(self) -> None:
        self._com.PressEnter()

    def press_f1(self) -> None:
        self._com.PressF1()

    def press_f4(self) -> None:
        self._com.PressF4()

    def press_toolbar_button(self, id: str) -> None:
        self._com.PressToolbarButton(id)

    def press_toolbar_context_button(self, id: str) -> None:
        self._com.PressToolbarContextButton(id)

    def press_total_row(self, row: int, column: str) -> None:
        self._com.PressTotalRow(row, column)

    def press_total_row_current_cell(self) -> None:
        self._com.PressTotalRowCurrentCell()

    def select_all(self) -> None:
        self._com.SelectAll()

    def select_column(self, column: str) -> None:
        self._com.SelectColumn(column)

    def selection_changed(self) -> None:
        self._com.SelectionChanged()

    def select_toolbar_menu_item(self, id: str) -> None:
        self._com.SelectToolbarMenuItem(id)

    def set_column_width(self, column: str, width: int) -> None:
        self._com.SetColumnWidth(column, width)

    def set_current_cell(self, row: int, column: str) -> None:
        self._com.SetCurrentCell(row, column)

    def trigger_modified(self) -> None:
        self._com.TriggerModified()

    def by_val(self) -> None:
        self._com.ByVal()
