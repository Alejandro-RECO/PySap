# PySap

Marco de trabajo en Python para automatizar SAP vía **SAP GUI Scripting API** (COM / pywin32).

Objetivo: automatizaciones **ágiles, estables, controlables, medibles y testeables**, con
mapeo dinámico de objetos SAP por `id`/`path` y autocompletado de métodos en el editor.

## Características

- **Runtime COM tipado**: engancha a SAP GUI corriendo y expone `session.find(path)`.
- **Búsqueda robusta**: cuando el path es inestable (filas, subscreens), localiza
  por sufijo de id (`find_by_id_suffix`) o por nombre (`find_by_name` / `find_all_by_name`).
- **Wrappers tipados** de objetos `Gui*` (generados desde el PDF oficial) → autocompletado real.
- **Mapping dinámico**: nombres lógicos → paths SAP (cambias un path en un solo sitio).
- **Steps / Process**: unidades atómicas medibles, reintentables y con telemetría.
- **TDD con mock**: corre tests sin SAP real; integración marcada aparte.
- **Trazabilidad**: decisiones en `docs/decisions/` (ADR) + `docs/CHANGELOG.md`.

## Requisitos

- Windows con SAP GUI instalado y **scripting habilitado** (cliente y servidor).
- Python 3.11+
- `pywin32`

## Instalación (dev)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
```

## Estructura

```
pysap/
  runtime/    conexión COM, sesión, errores
  objects/    wrappers tipados Gui* (+ .pyi)  [generados]
  mapping/    registry id/path, page objects
  process/    Step, Process
  telemetry/  métricas
  codegen/    parser PDF + emisor de wrappers
tests/        unit (mock) + integration (SAP real)
docs/         decisions (ADR), CHANGELOG, referencia objetos
.claude/skills/  orchestrator, codegen, tdd, commit
```

## Abrir SAP y hacer login

Configura las credenciales (nunca se versionan, ver ADR-0003): copia
`.env.example` a `.env` y rellénalo, o exporta las variables `SAP_*`.

```bash
python scripts/open_sap.py            # usa .env si existe
python scripts/open_sap.py --env ruta/al/.env
```

El script carga `SapConfig.from_env()`, arranca SAP si hace falta
(`saplogon.exe`), abre la conexión y hace login dejando la sesión lista.

Por código:

```python
from pysap import SapConfig, start_session

session = start_session(SapConfig.from_env())
session.start_transaction("VA01")
```

## Tests

```bash
pytest                 # unit con mock
pytest -m sap          # integración contra SAP real
```

## Convención de commits

`Tipo: Descripción` (máx. 20 palabras). Ver skill `sap-commit`.
