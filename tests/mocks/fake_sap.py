"""Objetos SAP falsos para TDD sin SAP real.

Reproducen la superficie COM mínima usada por PySap:
- ``GetScriptingEngine`` -> app con ``Children``
- ``connection.Children`` -> sesiones
- ``session.findById(path, raise)`` -> componente o None
- componentes con Id/Type/Name/Text + métodos (Press, SetFocus, sendVKey...)
"""

from __future__ import annotations

from typing import Any


class FakeComponent:
    """Componente SAP falso. Registra interacciones para aserciones en tests."""

    def __init__(
        self,
        id: str,
        type: str = "GuiComponent",
        name: str = "",
        text: str = "",
        message_type: str = "",
    ) -> None:
        self.Id = id
        self.Type = type
        self.Name = name
        self.Text = text
        # Solo relevante en la barra de estado (S/W/E/A/I).
        self.MessageType = message_type
        # Hijos para emular el árbol de contenedores (Children).
        self._children: list[FakeComponent] = []
        # Banderas observables por los tests.
        self.pressed = False
        self.focused = False
        self.vkeys: list[int] = []

    def add_child(self, child: FakeComponent) -> FakeComponent:
        """Cuelga un componente como hijo directo (para árboles de prueba)."""
        self._children.append(child)
        return child

    @property
    def Children(self) -> FakeChildren:
        return FakeChildren(self._children)

    def Press(self) -> None:
        self.pressed = True

    def SetFocus(self) -> None:
        self.focused = True

    def sendVKey(self, key: int) -> None:
        self.vkeys.append(key)


class FakeChildren:
    """Emula la colección COM ``Children`` (1-based vía __call__)."""

    def __init__(self, items: list[Any]) -> None:
        self._items = items

    @property
    def Count(self) -> int:
        return len(self._items)

    def __call__(self, index: int) -> Any:
        return self._items[index]

    def __iter__(self) -> Any:
        return iter(self._items)


class FakeSession:
    """Sesión SAP falsa con un diccionario path -> FakeComponent."""

    def __init__(self, components: dict[str, FakeComponent] | None = None) -> None:
        self._components = components or {}
        self.Info = FakeSessionInfo()

    def add(self, component: FakeComponent) -> FakeComponent:
        self._components[component.Id] = component
        return component

    @property
    def Children(self) -> FakeChildren:
        """Raíz del árbol: expone los componentes registrados como hijos."""
        return FakeChildren(list(self._components.values()))

    def findById(self, path: str, raise_on_missing: Any = True) -> Any:
        comp = self._components.get(path)
        if comp is None and raise_on_missing:
            raise Exception(f"control could not be found by id {path}")
        return comp

    def findByName(self, name: str, type: str) -> Any:
        for comp in self._components.values():
            if comp.Name == name and comp.Type == type:
                return comp
        raise Exception(f"control could not be found by name {name}/{type}")

    def findAllByName(self, name: str, type: str) -> FakeChildren:
        hits = [c for c in self._components.values() if c.Name == name and c.Type == type]
        return FakeChildren(hits)


class FakeSessionInfo:
    def __init__(self) -> None:
        self.Transaction = ""
        self.User = "TESTUSER"
        self.Client = "100"


class FakeConnection:
    def __init__(self, sessions: list[FakeSession]) -> None:
        self.Children = FakeChildren(sessions)


class FakeApplication:
    """GuiApplication falso: raíz del modelo de objetos."""

    def __init__(self, connections: list[FakeConnection]) -> None:
        self._connections = connections
        self.Children = FakeChildren(connections)
        self.opened: list[str] = []

    def OpenConnection(self, description: str, sync: bool = True) -> FakeConnection:
        """Emula abrir una conexión nueva con una sesión en pantalla de login."""
        self.opened.append(description)
        session = FakeSession()
        session.add(FakeComponent("wnd[0]", type="GuiMainWindow"))
        session.add(FakeComponent("wnd[0]/usr/txtRSYST-MANDT", type="GuiTextField"))
        session.add(FakeComponent("wnd[0]/usr/txtRSYST-BNAME", type="GuiTextField"))
        session.add(FakeComponent("wnd[0]/usr/pwdRSYST-BCODE", type="GuiPasswordField"))
        session.add(FakeComponent("wnd[0]/usr/txtRSYST-LANGU", type="GuiTextField"))
        session.add(FakeComponent("wnd[0]/sbar", type="GuiStatusbar"))
        conn = FakeConnection([session])
        self._connections.append(conn)
        self.Children = FakeChildren(self._connections)
        return conn


def build_app(session: FakeSession) -> FakeApplication:
    """Atajo: app con una conexión y una sesión."""
    return FakeApplication([FakeConnection([session])])
