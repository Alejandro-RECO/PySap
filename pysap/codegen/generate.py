"""Driver del codegen: PDF -> wrappers ``.py`` + stubs ``.pyi`` (ADR-0004).

Encadena extraer -> parsear -> emitir -> escribir, para los objetos núcleo v1.
Ejecutable::

    python -m pysap.codegen.generate
    python -m pysap.codegen.generate --pdf docs/sap_gui_scripting_api.pdf
"""

from __future__ import annotations

import argparse
import os

from pysap.codegen.emitter import emit_module, emit_stub
from pysap.codegen.pdf_parser import ObjectSpec, parse_all
from pysap.codegen.text_extract import extract_pdf_text

# Objetos núcleo v1 (ADR-0001 / skill sap-codegen).
CORE_OBJECTS = [
    "GuiApplication",
    "GuiConnection",
    "GuiSession",
    "GuiMainWindow",
    "GuiButton",
    # GuiTextField: su sección en el PDF está degenerada (sin cabecera propia);
    # se mantiene el wrapper escrito a mano en objects/gui_textfield.py.
    "GuiCTextField",
    "GuiPasswordField",
    "GuiComboBox",
    "GuiCheckBox",
    "GuiRadioButton",
    "GuiGridView",
    "GuiTree",
    "GuiStatusbar",
]

_DEFAULT_PDF = os.path.join("docs", "sap_gui_scripting_api.pdf")
_DEFAULT_OUT = os.path.join("pysap", "objects")


def _module_filename(obj_name: str) -> str:
    """``GuiButton`` -> ``gui_button``."""
    from pysap.codegen.emitter import snake_case

    return snake_case(obj_name)


def write_specs(specs: list[ObjectSpec], out_dir: str) -> list[str]:
    """Emite y escribe ``.py`` + ``.pyi`` de cada spec. Devuelve rutas escritas."""
    escritos: list[str] = []
    for spec in specs:
        base = _module_filename(spec.name)
        py_path = os.path.join(out_dir, f"{base}.py")
        pyi_path = os.path.join(out_dir, f"{base}.pyi")
        with open(py_path, "w", encoding="utf-8") as fh:
            fh.write(emit_module(spec))
        with open(pyi_path, "w", encoding="utf-8") as fh:
            fh.write(emit_stub(spec))
        escritos += [py_path, pyi_path]
    return escritos


def generate(
    pdf_path: str = _DEFAULT_PDF,
    out_dir: str = _DEFAULT_OUT,
    objetos: list[str] | None = None,
) -> list[ObjectSpec]:
    """Genera los wrappers desde el PDF y los escribe en ``out_dir``."""
    texto = extract_pdf_text(pdf_path)
    specs = parse_all(texto, objetos or CORE_OBJECTS)
    write_specs(specs, out_dir)
    return specs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Genera wrappers Gui* desde el PDF.")
    parser.add_argument("--pdf", default=_DEFAULT_PDF, help="Ruta al PDF de la API.")
    parser.add_argument("--out", default=_DEFAULT_OUT, help="Carpeta de salida.")
    args = parser.parse_args(argv)

    specs = generate(args.pdf, args.out)
    print(f"Generados {len(specs)} wrappers en {args.out}:")
    for s in specs:
        print(f"  - {s.name}: {len(s.properties)} props, {len(s.methods)} métodos")
    faltantes = set(CORE_OBJECTS) - {s.name for s in specs}
    if faltantes:
        print(f"  (!) No encontrados en el PDF: {', '.join(sorted(faltantes))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
