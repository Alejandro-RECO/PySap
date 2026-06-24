"""Feedback de SAP: clasificación de la barra de estado."""

from __future__ import annotations

from dataclasses import dataclass

# Tipos de mensaje SAP en la barra de estado.
ERROR_TYPES = frozenset({"E", "A"})  # Error, Abort
WARNING_TYPES = frozenset({"W"})
SUCCESS_TYPES = frozenset({"S"})
INFO_TYPES = frozenset({"I"})


@dataclass(frozen=True)
class Status:
    """Estado leído de la barra de estado (``sbar``)."""

    type: str  # S / W / E / A / I / "" (vacío)
    text: str

    @property
    def is_error(self) -> bool:
        return self.type in ERROR_TYPES

    @property
    def is_warning(self) -> bool:
        return self.type in WARNING_TYPES

    @property
    def is_success(self) -> bool:
        return self.type in SUCCESS_TYPES
