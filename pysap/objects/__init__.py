"""Wrappers tipados de objetos Gui*.

``base`` y unos pocos wrappers están escritos a mano como referencia; el resto
se generan con ``pysap.codegen`` a partir del PDF oficial.
"""

from pysap.objects.base import GuiComponent
from pysap.objects.gui_button import GuiButton
from pysap.objects.gui_textfield import GuiTextField

__all__ = ["GuiComponent", "GuiButton", "GuiTextField"]
