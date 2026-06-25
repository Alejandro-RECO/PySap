"""Entrypoint: abre SAP y hace login con la config del entorno.

Uso (con un `.env` o variables SAP_* exportadas)::

    python scripts/open_sap.py
    python scripts/open_sap.py --env .env

Carga :class:`SapConfig` desde el entorno, arranca SAP si hace falta, abre la
conexión y hace login (ver ADR-0003). Deja la sesión abierta para operar a mano
o como base de un proceso. No imprime credenciales.
"""

from __future__ import annotations

import argparse
import os
import sys

# Permite ejecutar el script directo (python scripts/open_sap.py) sin instalar
# el paquete: añade la raíz del proyecto al path.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pysap import SapConfig, start_session  # noqa: E402  (tras ajustar sys.path)
from pysap.runtime.errors import (
    MissingConfigError,
    PySapError,
    SapLaunchError,
    SapMessageError,
)


def main(argv: list[str] | None = None) -> int:
    """Punto de entrada. Devuelve un código de salida para el shell."""
    parser = argparse.ArgumentParser(description="Abre SAP y hace login (PySap).")
    parser.add_argument(
        "--env",
        dest="dotenv_path",
        default=".env",
        help="Ruta al archivo .env con las variables SAP_* (por defecto: .env).",
    )
    args = parser.parse_args(argv)

    # El .env es opcional: si no existe, se usan solo las variables de entorno.
    dotenv_path = args.dotenv_path if os.path.exists(args.dotenv_path) else None

    try:
        config = SapConfig.from_env(dotenv_path=dotenv_path)
    except MissingConfigError as exc:
        print(f"[config] {exc}", file=sys.stderr)
        print("Crea un .env (ver .env.example) o exporta las variables.", file=sys.stderr)
        return 2

    try:
        session = start_session(config)
    except SapLaunchError as exc:
        print(f"[arranque] {exc}", file=sys.stderr)
        return 3
    except SapMessageError as exc:
        print(f"[login] SAP rechazó el login: {exc}", file=sys.stderr)
        return 4
    except PySapError as exc:
        print(f"[pysap] {exc}", file=sys.stderr)
        return 1

    info = session.info
    estado = session.status()
    print(f"Sesión lista. Usuario={info.User} Mandante={info.Client}")
    if estado.text:
        print(f"Barra de estado [{estado.type}]: {estado.text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
