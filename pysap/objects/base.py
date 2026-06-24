"""GuiComponent: clase base de todos los wrappers de objetos SAP."""

from __future__ import annotations

from typing import Any


class GuiComponent:
    """Envoltura tipada de un objeto COM ``GuiComponent``.

    Propiedades comunes a todos los componentes SAP (id, type, name, text).
    Cualquier atributo no definido se delega al objeto COM subyacente, de modo
    que el wrapper sigue siendo útil aunque no cubra el 100% de la API.
    """

    def __init__(self, com_obj: Any) -> None:
        # Se asigna por __dict__ para no disparar __getattr__/__setattr__.
        object.__setattr__(self, "_com", com_obj)

    @property
    def com(self) -> Any:
        """Objeto COM crudo."""
        return self._com

    @property
    def id(self) -> str:
        return self._com.Id

    @property
    def type(self) -> str:
        """Nombre de tipo SAP (p.ej. ``GuiButton``)."""
        return self._com.Type

    @property
    def name(self) -> str:
        return self._com.Name

    @property
    def text(self) -> str:
        return self._com.Text

    @text.setter
    def text(self, value: str) -> None:
        self._com.Text = value

    # --- delegación al COM para todo lo no envuelto explícitamente ---

    def __getattr__(self, item: str) -> Any:
        # Solo se invoca si el atributo no existe en la clase/instancia.
        return getattr(object.__getattribute__(self, "_com"), item)

    def __repr__(self) -> str:
        try:
            return f"<{type(self).__name__} id={self.id!r} type={self.type!r}>"
        except Exception:  # pragma: no cover - COM sin Id/Type
            return f"<{type(self).__name__} (sin id)>"
