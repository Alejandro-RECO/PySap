"""Wrapper tipado de GuiSession: acceso a componentes por id/path."""

from __future__ import annotations

from typing import Any, TypeVar

from pysap.objects.base import GuiComponent
from pysap.runtime.errors import ComponentNotFoundError

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

    @property
    def info(self) -> Any:
        """``GuiSessionInfo`` (transacción, usuario, mandante, etc.)."""
        return self._com.Info
