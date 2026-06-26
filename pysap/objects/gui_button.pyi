# -*- coding: utf-8 -*-
# GENERADO automáticamente por pysap.codegen desde el PDF de la API.
# NO EDITAR A MANO: los cambios se perderán al regenerar.

from typing import Any
from pysap.objects.base import GuiComponent


class GuiButton(GuiComponent):
    @property
    def emphasized(self) -> bool: ...
    @property
    def left_label(self) -> Any: ...
    @left_label.setter
    def left_label(self, value: Any) -> None: ...
    @property
    def right_label(self) -> Any: ...
    @right_label.setter
    def right_label(self, value: Any) -> None: ...
    def press(self) -> None: ...
