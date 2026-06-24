"""Wrapper tipado de GuiSession: acceso a componentes por id/path."""

from __future__ import annotations

from typing import Any, TypeVar

from pysap.objects.base import GuiComponent
from pysap.runtime.errors import ComponentNotFoundError, SapMessageError
from pysap.runtime.feedback import Status

T = TypeVar("T", bound=GuiComponent)


class Session:
    """Envuelve un objeto COM ``GuiSession``.

    Punto de entrada para localizar componentes mediante ``findById``.
    """

    def __init__(self, com_session: Any) -> None:
        self._com = com_session

    @property
    def com(self) -> Any:
        """Objeto COM crudo (escotilla de escape)."""
        return self._com

    def find(self, path: str) -> GuiComponent:
        """Localiza un componente por su ``id``/``path`` y lo envuelve.

        Lanza :class:`ComponentNotFoundError` si no existe.
        """
        # Raise=False -> devuelve None en vez de excepción COM.
        com_obj = self._com.findById(path, False)
        if com_obj is None:
            raise ComponentNotFoundError(path)
        return GuiComponent(com_obj)

    def find_as(self, path: str, kind: type[T]) -> T:
        """Como :meth:`find` pero devuelve el tipo de wrapper indicado.

        Da autocompletado fuerte en el editor::

            boton = session.find_as("wnd[0]/tbar[0]/btn[0]", GuiButton)
            boton.press()
        """
        com_obj = self._com.findById(path, False)
        if com_obj is None:
            raise ComponentNotFoundError(path)
        return kind(com_obj)

    def start_transaction(self, tcode: str) -> None:
        """Atajo: abre una transacción en la ventana 0."""
        self._com.findById("wnd[0]/tbar[0]/okcd").Text = f"/n{tcode}"
        self._com.findById("wnd[0]").sendVKey(0)

    def login(
        self,
        client: str,
        user: str,
        password: str,
        language: str = "",
    ) -> None:
        """Rellena la pantalla de login (SAP Logon) y confirma con Enter.

        Las credenciales se pasan como argumentos; nunca deben quedar
        hardcodeadas ni versionadas (ver ADR-0002).
        """
        self._com.findById("wnd[0]/usr/txtRSYST-MANDT").Text = client
        self._com.findById("wnd[0]/usr/txtRSYST-BNAME").Text = user
        self._com.findById("wnd[0]/usr/pwdRSYST-BCODE").Text = password
        if language:
            self._com.findById("wnd[0]/usr/txtRSYST-LANGU").Text = language
        self._com.findById("wnd[0]").sendVKey(0)

    # --- feedback: barra de estado y popups ---

    def status(self) -> Status:
        """Lee la barra de estado de la ventana 0. Vacío si no existe."""
        sbar = self._com.findById("wnd[0]/sbar", False)
        if sbar is None:
            return Status(type="", text="")
        return Status(type=sbar.MessageType or "", text=sbar.Text or "")

    def raise_on_error(self) -> None:
        """Lanza :class:`SapMessageError` si la barra de estado reporta error/aborto."""
        status = self.status()
        if status.is_error:
            raise SapMessageError(status.type, status.text)

    def has_popup(self, window_index: int = 1) -> bool:
        """True si existe una ventana modal (por defecto ``wnd[1]``)."""
        return self._com.findById(f"wnd[{window_index}]", False) is not None

    def send_vkey(self, key: int, window_index: int = 0) -> None:
        """Envía una tecla virtual a la ventana indicada (0=Enter, 12=F12...)."""
        self._com.findById(f"wnd[{window_index}]").sendVKey(key)

    def confirm_popup(self, window_index: int = 1) -> None:
        """Confirma el popup (Enter)."""
        self.send_vkey(0, window_index)

    def cancel_popup(self, window_index: int = 1) -> None:
        """Cancela el popup (F12)."""
        self.send_vkey(12, window_index)

    @property
    def info(self) -> Any:
        """``GuiSessionInfo`` (transacción, usuario, mandante, etc.)."""
        return self._com.Info
