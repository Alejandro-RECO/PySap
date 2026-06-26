# ADR-0005 — Page Objects y validación de tipo en find_as

- **Estado:** Aceptada
- **Fecha:** 2026-06-26
- **Decidido con:** soporte_rpa@netapplications.com.co (vía Claude Code)

## Contexto

Fase 4 (ADR-0001): "Mapping + Process". Ya existe `PathRegistry` (nombre lógico
→ path) y los wrappers tipados (Fase 3). Faltan dos piezas:

1. **Page Object**: un patrón que agrupe los controles de una pantalla bajo
   nombres lógicos, para que las automatizaciones no esparzan paths SAP. Hoy el
   `PathRegistry` resuelve nombres, pero no hay nada que lo una a una `Session`
   ni que devuelva wrappers tipados por nombre lógico.
2. **Validación de tipo en `find_as`**: hoy `find_as(path, kind)` envuelve el
   objeto COM en `kind` sin comprobar que el control sea realmente de ese tipo.
   Si el path apunta a otro control, el error aparece tarde y confuso.

## Decisiones

| # | Tema | Decisión | Alternativas descartadas |
|---|------|----------|--------------------------|
| 1 | Validación | `find_as(path, kind, *, validate=False)`. Si `validate=True`, compara `com.Type` con el tipo SAP esperado y lanza `ComponentTypeError` si no coincide. **Opt-in** para no romper el comportamiento actual. | Validar siempre (rompe casos genéricos); no validar nunca |
| 2 | Tipo esperado | Atributo de clase opcional `sap_type`; si falta, se usa `kind.__name__` (los wrappers se llaman igual que su tipo SAP: `GuiButton`→`"GuiButton"`). | Mapa externo path→tipo; introspección del PDF en runtime |
| 3 | Page Object | `mapping/page_object.py`: clase base `PageObject(session, registry)` con `find(nombre)` y `find_as(nombre, kind, *, validate=True)` que resuelven el nombre lógico vía el registry. | Page object sin registry (paths a mano); función suelta |
| 4 | Campos declarativos | Descriptor `Field(nombre_logico, kind=None)` para declarar controles como atributos de clase con autocompletado. | Solo métodos; metaclases |
| 5 | Error | Nuevo `ComponentTypeError(PySapError)` con path, tipo esperado y hallado. | Reusar `ComponentNotFoundError` (confunde causas) |

## Diseño

- `pysap/runtime/session.py`: `find_as(path, kind, *, validate=False)`. El tipo
  esperado = `getattr(kind, "sap_type", kind.__name__)`; si `kind` es el genérico
  `GuiComponent`, no valida. Lanza `ComponentTypeError` ante discrepancia.
- `pysap/runtime/errors.py`: `ComponentTypeError`.
- `pysap/mapping/page_object.py`:
  - `PageObject`: guarda `session` y `registry`; `find`/`find_as` traducen nombre
    lógico → path (vía `registry.path`) y delegan en la `Session`.
  - `Field(nombre, kind=None)`: descriptor; en acceso resuelve contra la
    instancia (`find` o `find_as`). Da page objects declarativos::

        class LoginPage(PageObject):
            mandante = Field("mandante", GuiTextField)
            usuario = Field("usuario", GuiTextField)

- `pysap/mapping/__init__.py`: exporta `PathRegistry`, `PageObject`, `Field`.

## Consecuencias

- (+) Las pantallas se modelan una vez; los flujos usan nombres, no paths.
- (+) `find_as(validate=True)` detecta paths mal mapeados al instante, con un
  error claro (`ComponentTypeError`).
- (+) Page objects declarativos con autocompletado real (wrappers de Fase 3).
- (−) `validate` se apoya en que el nombre de clase coincida con el tipo SAP;
  los casos especiales requieren declarar `sap_type` en el wrapper.
- (−) El descriptor `Field` resuelve en cada acceso (sin caché): tras acciones que
  invalidan referencias COM, esto es lo correcto, pero no cachea repeticiones.
