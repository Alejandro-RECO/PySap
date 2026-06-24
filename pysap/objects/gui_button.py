"""GuiButton — botón de comando (push button)."""

from __future__ import annotations

from pysap.objects.base import GuiComponent


class GuiButton(GuiComponent):
    """Botón SAP. Ver 'GuiButton Object' en el PDF de la API."""

    def press(self) -> None:
        """Pulsa el botón."""
        self._com.Press()

    @property
    def left_label(self) -> str:
        return self._com.LeftLabel

    @property
    def right_label(self) -> str:
        return self._com.RightLabel
