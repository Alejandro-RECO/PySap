"""Limpieza del texto crudo extraído del PDF (ADR-0004).

El extractor de PDF deja ruido: guiones suaves al partir palabras, glifos del
área de uso privado Unicode y espacios/saltos irregulares. Esta función los
normaliza para que los regex del parser sean fiables.
"""

from __future__ import annotations

import re

# Guion suave (soft hyphen) que el PDF inserta al cortar palabras.
_SOFT_HYPHEN = "­"

# Artefacto del PDF: una mayúscula se separa de su cola minúscula dentro de una
# palabra ("GuiT extField", "T ext"). Patrón: minúscula+MAYÚSCULA espacio minúscula.
_RE_SPLIT_CAP = re.compile(r"([a-z])([A-Z]) ([a-z])")


def despace(text: str) -> str:
    """Reúne mayúsculas partidas dentro de palabras (``GuiT extField`` -> ``GuiTextField``).

    No toca artículos sueltos (``A tree``), porque exige una minúscula antes de la
    mayúscula partida.
    """
    return _RE_SPLIT_CAP.sub(r"\1\2\3", text)


def _es_glifo_privado(ch: str) -> bool:
    """True si el carácter está en un Área de Uso Privado Unicode (glifos basura)."""
    cp = ord(ch)
    return (
        0xE000 <= cp <= 0xF8FF  # PUA básica
        or 0xF0000 <= cp <= 0xFFFFD  # PUA-A
        or 0x100000 <= cp <= 0x10FFFD  # PUA-B
    )


def normalize(text: str) -> str:
    """Devuelve el texto sin guiones suaves ni glifos privados y con espacios simples."""
    sin_guion = text.replace(_SOFT_HYPHEN, "")
    sin_glifos = "".join(ch for ch in sin_guion if not _es_glifo_privado(ch))
    # Colapsa cualquier secuencia de espacios en blanco (incluye saltos) a un espacio.
    return re.sub(r"\s+", " ", sin_glifos).strip()
