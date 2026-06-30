"""Demo: buscar un control por sufijo de id (path SAP inestable).

La lógica original de `buscar_por_id_parcial` ya está integrada en el paquete
como ``Session.find_by_id_suffix`` (búsqueda recursiva por sufijo de id), junto
con ``find_by_name`` / ``find_all_by_name`` para buscar por nombre.

Este script solo demuestra su uso contra una sesión SAP real.

Uso:
    python scripts/buscar_id_parcial.py btnGUARDAR
"""

from __future__ import annotations

import sys

from pysap import connect


def main(suffix: str) -> int:
    session = connect()
    comp = session.find_by_id_suffix(suffix, raise_=False)
    if comp is None:
        print(f"No se encontró ningún control cuyo id termine en {suffix!r}.")
        return 1
    print(f"Encontrado: id={comp.id!r} type={comp.type!r} name={comp.name!r}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python scripts/buscar_id_parcial.py <sufijo_id>")
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
