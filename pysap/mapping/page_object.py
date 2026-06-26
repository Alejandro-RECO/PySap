"""Page Object: agrupa los controles de una pantalla por nombre lógico (ADR-0005).

Une una :class:`~pysap.runtime.session.Session` con un :class:`PathRegistry`, de
modo que las automatizaciones usen nombres lógicos ("boton_guardar") en vez de
paths SAP. Soporta acceso por método (:meth:`PageObject.find`) y declarativo
(descriptor :class:`Field`).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, TypeVar

from pysap.objects.base import GuiComponent

if TYPE_CHECKING:
    from pysap.mapping.registry import PathRegistry
    from pysap.runtime.session import Session

T = TypeVar("T", bound=GuiComponent)


class PageObject:
    """Modela una pantalla SAP: resuelve nombres lógicos contra el registry."""

    def __init__(self, session: Session, registry: PathRegistry) -> None:
        self.session = session
        self.registry = registry

    def find(self, name: str) -> GuiComponent:
        """Devuelve el componente registrado bajo ``name`` (sin tipar)."""
        return self.session.find(self.registry.path(name))

    def find_as(self, name: str, kind: type[T], *, validate: bool = True) -> T:
        """Devuelve el componente ``name`` como ``kind``.

        Valida el tipo por defecto (``validate=True``): un path mal mapeado se
        detecta al instante con :class:`~pysap.runtime.errors.ComponentTypeError`.
        """
        return self.session.find_as(self.registry.path(name), kind, validate=validate)


class Field(Generic[T]):
    """Descriptor de un control de pantalla declarado como atributo de clase.

    Resuelve contra la instancia del :class:`PageObject` en cada acceso (sin
    caché: tras acciones que invalidan referencias COM, esto es lo correcto)::

        class LoginPage(PageObject):
            mandante = Field("mandante", GuiTextField)
    """

    def __init__(self, name: str, kind: type[T] | None = None) -> None:
        self.name = name
        self.kind = kind

    def __set_name__(self, owner: type, attr: str) -> None:
        self._attr = attr

    def __get__(self, instance: PageObject | None, owner: type | None = None) -> Any:
        if instance is None:  # acceso desde la clase, no la instancia
            return self
        if self.kind is None:
            return instance.find(self.name)
        return instance.find_as(self.name, self.kind)
