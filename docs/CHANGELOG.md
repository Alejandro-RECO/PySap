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
