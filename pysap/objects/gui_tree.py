# -*- coding: utf-8 -*-
# GENERADO automáticamente por pysap.codegen desde el PDF de la API.
# NO EDITAR A MANO: los cambios se perderán al regenerar.

"""GuiTree — wrapper generado."""

from __future__ import annotations

from typing import Any
from pysap.objects.base import GuiComponent


class GuiTree(GuiComponent):
    """GuiTree — objeto SAP (prefijo de tipo '')."""

    @property
    def column_order(self) -> Any:
        return self._com.ColumnOrder
    @column_order.setter
    def column_order(self, value: Any) -> None:
        self._com.ColumnOrder = value

    @property
    def hierarchy_header_width(self) -> int:
        return self._com.HierarchyHeaderWidth
    @hierarchy_header_width.setter
    def hierarchy_header_width(self, value: int) -> None:
        self._com.HierarchyHeaderWidth = value

    @property
    def selected_node(self) -> str:
        return self._com.SelectedNode
    @selected_node.setter
    def selected_node(self, value: str) -> None:
        self._com.SelectedNode = value

    @property
    def top_node(self) -> str:
        return self._com.TopNode
    @top_node.setter
    def top_node(self, value: str) -> None:
        self._com.TopNode = value

    def change_checkbox(self, node_key: str, item_name: str, checked: bool) -> None:
        self._com.ChangeCheckbox(node_key, item_name, checked)

    def click_link(self, node_key: str, item_name: str) -> None:
        self._com.ClickLink(node_key, item_name)

    def collapse_node(self, node_key: str) -> None:
        self._com.CollapseNode(node_key)

    def default_context_menu(self) -> None:
        self._com.DefaultContextMenu()

    def double_click_item(self, node_key: str, item_name: str) -> None:
        self._com.DoubleClickItem(node_key, item_name)

    def double_click_node(self, node_key: str) -> None:
        self._com.DoubleClickNode(node_key)

    def ensure_visible_horizontal_item(self, node_key: str, item_name: str) -> None:
        self._com.EnsureVisibleHorizontalItem(node_key, item_name)

    def expand_node(self, node_key: str) -> None:
        self._com.ExpandNode(node_key)

    def find_node_key_by_path(self, path: str) -> str:
        return self._com.FindNodeKeyByPath(path)

    def get_abap_image(self, key: str, name: str) -> str:
        return self._com.GetAbapImage(key, name)

    def get_all_node_keys(self) -> Any:
        return self._com.GetAllNodeKeys()

    def get_check_box_state(self, node_key: str, item_name: str) -> bool:
        return self._com.GetCheckBoxState(node_key, item_name)

    def get_column_col(self, col_name: str) -> Any:
        return self._com.GetColumnCol(col_name)

    def get_column_headers(self) -> Any:
        return self._com.GetColumnHeaders()

    def get_column_index_from_name(self, key: str) -> int:
        return self._com.GetColumnIndexFromName(key)

    def get_column_names(self) -> Any:
        return self._com.GetColumnNames()

    def get_column_title_from_name(self, key: str) -> str:
        return self._com.GetColumnTitleFromName(key)

    def get_column_titles(self) -> Any:
        return self._com.GetColumnTitles()

    def get_focused_node_key(self) -> str:
        return self._com.GetFocusedNodeKey()

    def get_hierarchy_level(self, key: str) -> int:
        return self._com.GetHierarchyLevel(key)

    def get_hierarchy_title(self) -> str:
        return self._com.GetHierarchyTitle()

    def get_is_disabled(self, node_key: str, item_name: str) -> bool:
        return self._com.GetIsDisabled(node_key, item_name)

    def get_is_editable(self, node_key: str, item_name: str) -> bool:
        return self._com.GetIsEditable(node_key, item_name)

    def get_is_high_lighted(self, node_key: str, item_name: str) -> bool:
        return self._com.GetIsHighLighted(node_key, item_name)

    def get_item_height(self, node_key: str, item_name: str) -> int:
        return self._com.GetItemHeight(node_key, item_name)

    def get_item_left(self, node_key: str, item_name: str) -> int:
        return self._com.GetItemLeft(node_key, item_name)

    def get_item_style(self, node_key: str, item_name: str) -> int:
        return self._com.GetItemStyle(node_key, item_name)

    def get_item_text(self, key: str, name: str) -> str:
        return self._com.GetItemText(key, name)

    def get_item_text_color(self, key: str, name: str) -> Any:
        return self._com.GetItemTextColor(key, name)

    def get_item_tool_tip(self, key: str, name: str) -> str:
        return self._com.GetItemToolTip(key, name)

    def get_item_top(self, node_key: str, item_name: str) -> int:
        return self._com.GetItemTop(node_key, item_name)

    def get_item_type(self, key: str, name: str) -> int:
        return self._com.GetItemType(key, name)

    def get_item_width(self, node_key: str, item_name: str) -> int:
        return self._com.GetItemWidth(node_key, item_name)

    def get_list_tree_node_item_count(self, node_key: str) -> int:
        return self._com.GetListTreeNodeItemCount(node_key)

    def get_next_node_key(self, node_key: str) -> str:
        return self._com.GetNextNodeKey(node_key)

    def get_node_abap_image(self, key: str) -> str:
        return self._com.GetNodeAbapImage(key)

    def get_node_children_count(self, key: str) -> int:
        return self._com.GetNodeChildrenCount(key)

    def get_node_children_count_by_path(self, path: str) -> int:
        return self._com.GetNodeChildrenCountByPath(path)

    def get_node_height(self, key: str) -> int:
        return self._com.GetNodeHeight(key)

    def get_node_index(self, key: str) -> int:
        return self._com.GetNodeIndex(key)

    def get_node_item_headers(self, node_key: str) -> Any:
        return self._com.GetNodeItemHeaders(node_key)

    def get_node_key_by_path(self, path: str) -> str:
        return self._com.GetNodeKeyByPath(path)

    def get_node_left(self, key: str) -> int:
        return self._com.GetNodeLeft(key)

    def get_node_path_by_key(self, key: str) -> str:
        return self._com.GetNodePathByKey(key)

    def get_nodes_col(self) -> Any:
        return self._com.GetNodesCol()

    def get_node_style(self, node_key: str) -> int:
        return self._com.GetNodeStyle(node_key)

    def get_node_text_by_key(self, path: str) -> str:
        return self._com.GetNodeTextByKey(path)

    def get_node_text_by_path(self, path: str) -> str:
        return self._com.GetNodeTextByPath(path)

    def get_node_text_color(self, key: str) -> Any:
        return self._com.GetNodeTextColor(key)

    def get_node_tool_tip(self, node_key: str) -> str:
        return self._com.GetNodeToolTip(node_key)

    def get_node_top(self, key: str) -> int:
        return self._com.GetNodeTop(key)

    def get_node_width(self, key: str) -> int:
        return self._com.GetNodeWidth(key)

    def get_parent(self, c_key: str) -> str:
        return self._com.GetParent(c_key)

    def get_previous_node_key(self, node_key: str) -> str:
        return self._com.GetPreviousNodeKey(node_key)

    def get_selected_nodes(self) -> Any:
        return self._com.GetSelectedNodes()

    def get_selection_mode(self) -> int:
        return self._com.GetSelectionMode()

    def get_style_description(self, n_style: int) -> str:
        return self._com.GetStyleDescription(n_style)

    def get_sub_nodes_col(self, node_key: str) -> Any:
        return self._com.GetSubNodesCol(node_key)

    def get_tree_type(self) -> int:
        return self._com.GetTreeType()

    def header_context_menu(self, header_name: str) -> None:
        self._com.HeaderContextMenu(header_name)

    def is_folder(self, node_key: str) -> bool:
        return self._com.IsFolder(node_key)

    def is_folder_expandable(self, node_key: str) -> bool:
        return self._com.IsFolderExpandable(node_key)

    def is_folder_expanded(self, node_key: str) -> bool:
        return self._com.IsFolderExpanded(node_key)

    def item_context_menu(self, node_key: str, item_name: str) -> None:
        self._com.ItemContextMenu(node_key, item_name)

    def node_context_menu(self, node_key: str) -> None:
        self._com.NodeContextMenu(node_key)

    def press_button(self, node_key: str, item_name: str) -> None:
        self._com.PressButton(node_key, item_name)

    def press_header(self, header_name: str) -> None:
        self._com.PressHeader(header_name)

    def press_key(self, key: str) -> None:
        self._com.PressKey(key)

    def select_column(self, column_name: str) -> None:
        self._com.SelectColumn(column_name)

    def selected_item_column(self) -> str:
        return self._com.SelectedItemColumn()

    def selected_item_node(self) -> str:
        return self._com.SelectedItemNode()

    def select_item(self, node_key: str, item_name: str) -> None:
        self._com.SelectItem(node_key, item_name)

    def select_node(self, node_key: str) -> None:
        self._com.SelectNode(node_key)

    def set_check_box_state(self, node_key: str, item_name: str, state: int) -> None:
        self._com.SetCheckBoxState(node_key, item_name, state)

    def set_column_width(self, column_name: str, width: int) -> None:
        self._com.SetColumnWidth(column_name, width)

    def unselect_all(self) -> None:
        self._com.UnselectAll()

    def unselect_column(self, column_name: str) -> None:
        self._com.UnselectColumn(column_name)

    def unselect_node(self, node_key: str) -> None:
        self._com.UnselectNode(node_key)

    def by_val(self) -> None:
        self._com.ByVal()

    def as_(self) -> None:
        self._com.As()

    def return_(self) -> None:
        self._com.Return()
