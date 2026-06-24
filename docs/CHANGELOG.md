# CHANGELOG

Bitácora cronológica del proyecto PySap. Formato libre por sesión; cada entrada
referencia los ADR y commits relevantes.

## 2026-06-24 — Fase 1: Scaffold + runtime core

- Estructura del proyecto creada (`pysap/`, `tests/`, `docs/`, `.claude/skills/`).
- Runtime COM funcional: `connect()`, `Session.find/find_as/start_transaction`.
- `GuiComponent` base + wrappers `GuiButton`, `GuiTextField`.
- `PathRegistry`, `Step`, `Process`, telemetría (`StepMetric`, `ProcessReport`).
- Capa mock SAP (`tests/mocks/fake_sap.py`) + tests unitarios verdes.
- 4 skills creadas: `sap-orchestrator`, `sap-codegen`, `sap-tdd`, `sap-commit`.
- ADR-0001 registrado.
- Git inicializado.

## 2026-06-24 — Revisión + estabilidad (ADR-0002)

- Revisión de coherencia; sin inconsistencias de código. Detectados puntos de fuga.
- `py.typed` + `package-data` → autocompletado al instalar el paquete (PEP 561).
- **Step**: espera (`wait_for`/`wait_timeout`/`wait_poll`) + reintentos
  (`retries`/`retry_delay`), con `sleep`/`clock` inyectables. Ya es "reintentable" de verdad.
- **Conexión**: `open_connection()` + `Session.login()` (attach + open).
- **Feedback**: `Session.status()`, `raise_on_error()`, `has_popup()`,
  `confirm_popup()`, `cancel_popup()`, `send_vkey()`; dataclass `Status`.
- Nuevos errores: `WaitTimeoutError`, `SapMessageError`.
- Mock ampliado (statusbar `MessageType`, popups `wnd[1]`, `OpenConnection`).
- Tests: 22 verde (+14). ADR-0002 registrado.

### Pendiente (fases siguientes)
- Fase 3: codegen PDF → 14 wrappers core + `.pyi`.
- Fase 4: `mapping/page_object.py`; validación de tipo opcional en `find_as`.
- Tooling: `pip install -r requirements-dev.txt` para correr `ruff`.
