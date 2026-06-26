# Decisiones de arquitectura (ADR)

Cada decisión relevante se registra como un **Architecture Decision Record**
numerado: `ADR-NNNN-titulo.md`.

## Formato

- **Estado:** Propuesta | Aceptada | Reemplazada por ADR-XXXX
- **Fecha:** AAAA-MM-DD
- **Contexto** — qué problema/fuerzas motivan la decisión.
- **Decisión** — qué se decide.
- **Consecuencias** — efectos (+/−).

## Regla de trazabilidad

Toda decisión arquitectónica nueva crea un ADR **antes** de implementarla, y el
commit correspondiente la referencia (ej. `Doc: ADR-0002 ...`). El orquestador
(skill `sap-orchestrator`) hace cumplir esta regla.

## Índice

- [ADR-0001 — Stack y arquitectura base](ADR-0001-stack-y-arquitectura.md)
- [ADR-0002 — Estabilidad, conexión y feedback](ADR-0002-estabilidad-conexion-feedback.md)
- [ADR-0003 — Arranque de SAP, configuración y login](ADR-0003-arranque-y-login.md)
- [ADR-0004 — Codegen: wrappers tipados desde el PDF](ADR-0004-codegen-pdf-wrappers.md)
