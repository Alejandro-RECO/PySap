"""Wrappers tipados de objetos Gui*.

``base`` y ``GuiTextField`` están escritos a mano como referencia; el resto se
generan con ``pysap.codegen`` a partir del PDF oficial (ver ADR-0004). Los
archivos generados llevan cabecera "GENERADO — NO EDITAR".
"""

from pysap.objects.base import GuiComponent
from pysap.objects.gui_application import GuiApplication
from pysap.objects.gui_button import GuiButton
from pysap.objects.gui_c_text_field import GuiCTextField
from pysap.objects.gui_check_box import GuiCheckBox
from pysap.objects.gui_combo_box import GuiComboBox
from pysap.objects.gui_connection import GuiConnection
from pysap.objects.gui_grid_view import GuiGridView
from pysap.objects.gui_main_window import GuiMainWindow
from pysap.objects.gui_password_field import GuiPasswordField
from pysap.objects.gui_radio_button import GuiRadioButton
from pysap.objects.gui_session import GuiSession
from pysap.objects.gui_statusbar import GuiStatusbar
from pysap.objects.gui_textfield import GuiTextField
from pysap.objects.gui_tree import GuiTree

__all__ = [
    "GuiComponent",
    "GuiApplication",
    "GuiButton",
    "GuiCTextField",
    "GuiCheckBox",
    "GuiComboBox",
    "GuiConnection",
    "GuiGridView",
    "GuiMainWindow",
    "GuiPasswordField",
    "GuiRadioButton",
    "GuiSession",
    "GuiStatusbar",
    "GuiTextField",
    "GuiTree",
]
