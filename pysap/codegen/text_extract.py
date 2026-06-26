"""Extracción de texto del PDF de la API (ADR-0004).

Módulo fino aislado: es lo único que depende de ``pypdf``. El resto del codegen
trabaja sobre el texto que devuelve esta función, por lo que es testeable sin el
PDF. ``pypdf`` es dependencia de desarrollo (regenerar), no de runtime.
"""

from __future__ import annotations


def extract_pdf_text(pdf_path: str) -> str:
    """Devuelve todo el texto del PDF concatenado por páginas.

    Raises:
        ImportError: si ``pypdf`` no está instalado (``pip install pypdf``).
    """
    try:
        import pypdf
    except ImportError as exc:  # pragma: no cover - entorno sin pypdf
        raise ImportError(
            "pypdf no está instalado; necesario para regenerar los wrappers. "
            "Instálalo con 'pip install -r requirements-dev.txt'."
        ) from exc

    reader = pypdf.PdfReader(pdf_path)
    return "\n".join((page.extract_text() or "") for page in reader.pages)
