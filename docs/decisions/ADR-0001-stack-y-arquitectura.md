# ADR-0001 — Stack y arquitectura base de PySap

- **Estado:** Aceptada
- **Fecha:** 2026-06-24
- **Decidido con:** soporte_rpa@netapplications.com.co (vía Claude Code)

## Contexto

Se necesita un marco Python para automatizar SAP a través de la **SAP GUI
Scripting API**, que sea ágil, estable, controlable, medible y testeable, con
mapeo dinámico de objetos por `id`/`path` y autocompletado de métodos en el editor.

## Decisiones

| # | Tema | Decisión | Alternativas descartadas |
|---|------|----------|--------------------------|
| 1 | Conexión a SAP | **pywin32 / COM** (`win32com.client`, ROT `GetObject("SAPGUI")`) | VBScript por subprocess; sin SAP |
| 2 | Autocompletado | **Wrappers tipados + `.pyi` generados desde el PDF** | stubs sobre COM crudo; COM dinámico sin tipado |
| 3 | Testing | **pytest + capa mock de SAP**; integración marcada `@pytest.mark.sap` | pytest contra SAP real siempre; unittest |
| 4 | Trazabilidad | **ADRs en `docs/decisions/` + `docs/CHANGELOG.md`** | DECISIONS.md único; issues/PRs |
| 5 | Alcance v1 | **Core objects** (~14) con generador extensible | todos los objetos; mínimo absoluto |
| 6 | Tooling | **pip + venv + requirements.txt** | uv; Poetry |
| 7 | Nombre | **PySap** (paquete `pysap`) | — |
| 8 | Commits | **`Tipo: Descripción`** (máx. 20 palabras) | Conventional Commits completo |

## Modelo de objetos SAP (referencia)

```
GetObject("SAPGUI").GetScriptingEngine
  -> application (GuiApplication)
       -> connection (GuiConnection)   application.Children(n)
            -> session (GuiSession)     connection.Children(n)
                 -> findById(path)      -> componente Gui*
```

## Arquitectura

- `runtime/` — conexión COM, `Session` (envuelve `findById`), errores propios.
- `objects/` — `GuiComponent` base + wrappers tipados (generados en Fase 3).
- `mapping/` — `PathRegistry` (nombre lógico -> path) y Page Objects.
- `process/` — `Step` (acción + verificación) y `Process` (secuencia medible).
- `telemetry/` — `StepMetric` / `ProcessReport`.
- `codegen/` — parser del PDF + emisor de wrappers + `.pyi`.

## Fases

1. **Scaffold** — repo, venv, requirements, ADR-0001, skills, mock SAP, slice vertical. *(actual)*
2. **Runtime core** — connector + Session + base + errores (con tests mock). *(incluido en Fase 1)*
3. **Codegen** — parser PDF + emisor -> core 14 wrappers + `.pyi`.
4. **Mapping + Process** — registry, Page Object, telemetría avanzada.
5. **Demo end-to-end** — proceso real (login + transacción) con tests.

## Consecuencias

- (+) Autocompletado real y código testeable sin SAP.
- (+) Paths concentrados en el registry → robustez ante cambios de UI.
- (−) Dependencia de Windows + SAP GUI para integración real.
- (−) El codegen depende del formato del PDF oficial (versión 7.70 PL08).
