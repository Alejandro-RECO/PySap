# ADR-0003 — Arranque de SAP, configuración y login (entrypoint)

- **Estado:** Aceptada
- **Fecha:** 2026-06-25
- **Decidido con:** soporte_rpa@netapplications.com.co (vía Claude Code)

## Contexto

Las fases previas (ADR-0001/0002) entregan runtime, conexión, login por código,
Steps/Process y feedback, pero **sin un punto de entrada** que los integre. Falta
la Fase 5 (demo end-to-end): un archivo que **abra SAP** y **haga login**
reutilizando lo existente.

Dos fuerzas nuevas:

1. **"Abrir SAP"** debe cubrir el caso de SAP cerrado: hay que lanzar el binario
   `saplogon.exe` y esperar a que la Running Object Table (ROT) exponga el
   `GetScriptingEngine` antes de enganchar por COM.
2. **Credenciales**: ADR-0002 obliga a no versionarlas. Se necesita una fuente de
   configuración fuera del código.

ADR-0001 #1 descartó "VBScript por subprocess" como **mecanismo de scripting**;
esto es distinto: el scripting sigue siendo COM, el subprocess solo **arranca el
ejecutable** de SAP Logon.

## Decisiones

| # | Tema | Decisión | Alternativas descartadas |
|---|------|----------|--------------------------|
| 1 | Arranque | **Lanzar `saplogon.exe` vía `subprocess`** y sondear `GetScriptingEngine` con timeout hasta que la ROT responda. `opener`/`get_engine`/`sleep`/`clock` inyectables. | Asumir SAP siempre abierto; abrir vía COM puro (no existe sin proceso) |
| 2 | Config | **Variables de entorno** (`SAP_*`) con lector opcional de `.env` sin dependencia nueva. | `python-dotenv` (nuevo dep); archivo config versionable; args CLI con password |
| 3 | Integración | **`bootstrap.start_session`** orquesta arranque → `open_connection` → login como un `Process` de `Step`s, validando con feedback (`raise_on_error`). | Función monolítica sin Steps; sin telemetría |
| 4 | Entrypoint | **`scripts/open_sap.py`** ejecutable fino (`python -m`/directo) que carga config y llama a `start_session`. | Lógica dentro del script; `__main__` en el paquete |

## Diseño

- `pysap/config.py`: dataclass `SapConfig` (client, user, password, language,
  connection, logon_path) + `from_env()`. Lector `.env` mínimo propio (sin dep).
  `MissingConfigError` si falta una variable obligatoria.
- `pysap/runtime/launcher.py`: `launch_sap(logon_path, *, opener, get_engine,
  sleep, clock, timeout, poll)` → devuelve el `GuiApplication`. Si la ROT ya
  responde, no relanza; si no, `opener(logon_path)` y sondea hasta `timeout`.
- `pysap/runtime/bootstrap.py`: `start_session(config, *, application, launcher)`
  → app (lanza si hace falta) → `open_connection(config.connection)` →
  `Process("login")` con `Step` de login + verificación por barra de estado →
  devuelve `Session`.
- `pysap/runtime/errors.py`: `MissingConfigError`, `SapLaunchError`.
- `scripts/open_sap.py`: carga `SapConfig.from_env()`, llama `start_session`,
  imprime el `Status` resultante. Maneja errores con mensaje claro.
- Mock `fake_sap.py`: el `opener`/`get_engine` falsos permiten testear el
  arranque sin SAP ni proceso real.

## Consecuencias

- (+) Demo end-to-end real: un comando abre SAP y deja la sesión lista.
- (+) Arranque testeable sin SAP (todo inyectable); credenciales fuera del repo.
- (+) Reúne connect/open_connection, login, Steps/Process y feedback en un flujo.
- (−) `subprocess` + sondeo dependen del entorno Windows/SAP para integración real.
- (−) El `.env` no debe versionarse: responsabilidad operativa (`.gitignore`).
