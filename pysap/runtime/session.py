"""Wrapper tipado de GuiSession: acceso a componentes por id/path."""

from __future__ import annotations

from typing import Any, TypeVar

from pysap.objects.base import GuiComponent
from pysap.runtime.errors import (
    ComponentNotFoundError,
    ComponentTypeError,
    SapMessageError,
)
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

    def find_by_name(
        self, name: str, sap_type: str, *, raise_: bool = True
    ) -> GuiComponent | None:
        """Localiza el primer descendiente por ``Name`` + tipo SAP.

        Alternativa a :meth:`find` cuando el ``id`` no es estable (índices
        dinámicos) pero el nombre sí. Equivale a COM ``findByName(Name, Type)``,
        que devuelve solo la primera coincidencia (ver :meth:`find_all_by_name`
        para todas)::

            campo = session.find_by_name("RSYST-BNAME", "GuiTextField")

        Args:
            name: valor de la propiedad ``Name`` del control.
            sap_type: tipo SAP esperado (p.ej. ``"GuiButton"``).
            raise_: si ``True`` (por defecto) lanza :class:`ComponentNotFoundError`
                cuando no hay coincidencia; si ``False`` devuelve ``None``.
        """
        try:
            com_obj = self._com.findByName(name, sap_type)
        except Exception:
            # findByName lanza excepción COM si no encuentra (no admite raise=False).
            com_obj = None
        if com_obj is None:
            if raise_:
                raise ComponentNotFoundError(f"name={name!r} type={sap_type!r}")
            return None
        return GuiComponent(com_obj)

    def find_all_by_name(self, name: str, sap_type: str) -> list[GuiComponent]:
        """Devuelve todos los descendientes con ``Name`` + tipo dados.

        Equivale a COM ``findAllByName``. Lista vacía si no hay ninguno.
        """
        coll = self._com.findAllByName(name, sap_type)
        return [GuiComponent(coll(i)) for i in range(coll.Count)]

    def find_by_id_suffix(
        self,
        suffix: str,
        *,
        root: GuiComponent | Any = None,
        raise_: bool = True,
    ) -> GuiComponent | None:
        """Busca recursivamente un control cuyo ``id`` termine en ``suffix``.

        Útil cuando SAP cambia el prefijo del path (índices de fila, subscreens)
        pero el final del ``id`` es estable. Recorre el árbol ``Children`` y
        devuelve la primera coincidencia en orden de profundidad::

            boton = session.find_by_id_suffix("btnGUARDAR")

        Args:
            suffix: cadena con la que debe terminar el ``id``.
            root: contenedor desde el que buscar (wrapper o COM). Por defecto,
                la raíz de la sesión.
            raise_: si ``True`` (por defecto) lanza :class:`ComponentNotFoundError`
                cuando no hay coincidencia; si ``False`` devuelve ``None``.
        """
        if isinstance(root, GuiComponent):
            container = root.com
        else:
            container = root if root is not None else self._com
        com_obj = self._search_id_suffix(container, suffix)
        if com_obj is None:
            if raise_:
                raise ComponentNotFoundError(f"*{suffix}")
            return None
        return GuiComponent(com_obj)

    @staticmethod
    def _search_id_suffix(container: Any, suffix: str) -> Any:
        """Recorrido en profundidad de ``Children`` buscando un ``id`` por sufijo."""
        try:
            children = container.Children
        except Exception:
            # Un control hoja puede no exponer Children.
            return None
        for i in range(children.Count):
            child = children(i)
            if child.Id.endswith(suffix):
                return child
            found = Session._search_id_suffix(child, suffix)
            if found is not None:
                return found
        return None

    def find_as(self, path: str, kind: type[T], *, validate: bool = False) -> T:
        """Como :meth:`find` pero devuelve el tipo de wrapper indicado.

        Da autocompletado fuerte en el editor::

            boton = session.find_as("wnd[0]/tbar[0]/btn[0]", GuiButton)
            boton.press()

        Args:
            path: ``id``/path del control.
            kind: clase de wrapper a devolver.
            validate: si es ``True``, comprueba que el tipo SAP del control
                coincida con el esperado y lanza :class:`ComponentTypeError` si
                no. El esperado es ``kind.sap_type`` o, si falta, ``kind.__name__``.
                El genérico :class:`GuiComponent` nunca se valida (ver ADR-0005).
        """
        com_obj = self._com.findById(path, False)
        if com_obj is None:
            raise ComponentNotFoundError(path)
        if validate and kind is not GuiComponent:
            expected = getattr(kind, "sap_type", kind.__name__)
            found = com_obj.Type
            if found != expected:
                raise ComponentTypeError(path, expected, found)
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
