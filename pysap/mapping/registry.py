"""PathRegistry: tabla de nombres lógicos -> paths SAP.

Permite que las automatizaciones usen nombres estables ("boton_guardar")
en vez de paths frágiles. Si SAP cambia un path, se ajusta en un solo sitio.
"""

from __future__ import annotations

from collections.abc import Mapping


class PathRegistry:
    """Mapa inmutable nombre_lógico -> path SAP."""

    def __init__(self, paths: Mapping[str, str] | None = None) -> None:
        self._paths: dict[str, str] = dict(paths or {})

    def register(self, name: str, path: str) -> None:
        """Asocia un nombre lógico a un path SAP."""
        self._paths[name] = path

    def path(self, name: str) -> str:
        """Devuelve el path asociado al nombre lógico."""
        try:
            return self._paths[name]
        except KeyError:
            raise KeyError(f"Nombre lógico no registrado: {name!r}") from None

    def __contains__(self, name: object) -> bool:
        return name in self._paths

    def __len__(self) -> int:
        return len(self._paths)
