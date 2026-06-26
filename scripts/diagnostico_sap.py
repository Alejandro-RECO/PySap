"""Diagnóstico de conexiones SAP: enumera lo que ve la SAP GUI Scripting API.

Uso: abre SAP a mano (la conexión que quieres, p.ej. "SALUD CALIDAD"), déjala
en la pantalla de login o ya logueada, y corre:

    python scripts/diagnostico_sap.py

Imprime las conexiones abiertas, su descripción EXACTA y sus sesiones. Con ese
nombre exacto se rellena SAP_CONNECTION en el .env.
"""

from __future__ import annotations

import sys


def main() -> int:
    try:
        import win32com.client
    except ImportError:
        print("pywin32 no está instalado. pip install pywin32", file=sys.stderr)
        return 1

    try:
        engine = win32com.client.GetObject("SAPGUI").GetScriptingEngine
    except Exception as exc:  # noqa: BLE001
        print(f"No se pudo enganchar a SAP GUI: {exc}", file=sys.stderr)
        print("¿SAP abierto? ¿Scripting habilitado (cliente y servidor)?", file=sys.stderr)
        return 2

    total = engine.Children.Count
    print(f"Conexiones abiertas: {total}")
    if total == 0:
        print("No hay ninguna conexión abierta. Abre 'SALUD CALIDAD' a mano primero.")
        return 0

    for i in range(total):
        conn = engine.Children(i)
        # Descripción y cadena de conexión (los nombres pueden variar por versión).
        desc = getattr(conn, "Description", "<sin Description>")
        cstr = getattr(conn, "ConnectionString", "")
        n_ses = conn.Children.Count
        print(f"\n[Conexión {i}]")
        print(f"  Description       : {desc!r}")
        print(f"  ConnectionString  : {cstr!r}")
        print(f"  Sesiones          : {n_ses}")
        for j in range(n_ses):
            ses = conn.Children(j)
            info = ses.Info
            print(
                f"    sesión {j}: usuario={getattr(info, 'User', '')!r} "
                f"mandante={getattr(info, 'Client', '')!r} "
                f"transacción={getattr(info, 'Transaction', '')!r}"
            )

    print("\n--> Copia el valor de 'Description' EXACTO a SAP_CONNECTION en el .env.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
