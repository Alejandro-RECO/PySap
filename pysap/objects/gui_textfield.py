"""GuiTextField — campo de texto editable."""

from __future__ import annotations

from pysap.objects.base import GuiComponent


class GuiTextField(GuiComponent):
    """Campo de texto SAP. Ver 'GuiTextField Object' en el PDF de la API."""

    @property
    def value(self) -> str:
        return self._com.Text

    @value.setter
    def value(self, v: str) -> None:
        self._com.Text = v

    @property
    def max_length(self) -> int:
        return self._com.MaxLength

    @property
    def required(self) -> bool:
        return bool(self._com.Required)

    def set_focus(self) -> None:
        self._com.SetFocus()
