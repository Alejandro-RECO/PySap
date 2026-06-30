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

## 2026-06-25 — Fase 5 (parcial): arranque + login (ADR-0003)

- **Config**: `pysap/config.py` `SapConfig` + `from_env()` con lector `.env`
  propio (sin dependencia nueva); el entorno pisa al `.env`. `.env.example` +
  `.gitignore` para `.env`. Credenciales fuera del repo.
- **Arranque**: `pysap/runtime/launcher.py` `launch_sap()` — engancha si la ROT
  responde; si no, lanza `saplogon.exe` y sondea con timeout. Todo inyectable.
- **Integración**: `pysap/runtime/bootstrap.py` `start_session()` — arranque →
  `open_connection` → login como `Process`/`Step`, verificado con feedback.
- **Entrypoint**: `scripts/open_sap.py` ejecutable (`python scripts/open_sap.py`).
- Nuevos errores: `MissingConfigError`, `SapLaunchError`. Mock: `sbar` en
  `OpenConnection`. Tests: 36 verde (+14). ADR-0003 registrado.

## 2026-06-26 — Fase 3: codegen PDF → wrappers (ADR-0004)

- **Codegen**: `pysap/codegen/` parsea el PDF oficial y emite wrappers tipados.
  - `text_extract.py` (`extract_pdf_text`, usa `pypdf`), `normalize.py`
    (`normalize`/`despace` limpian guiones suaves, glifos PUA y mayúsculas
    partidas tipo `GuiT extField`), `typemap.py` (VB→Python), `pdf_parser.py`
    (`parse_object`/`parse_all` → `ObjectSpec`/`Method`/`Property`/`Param`),
    `emitter.py` (`emit_module`/`emit_stub`/`snake_case`, sanea keywords y
    duplicados), `generate.py` (driver/CLI `python -m pysap.codegen.generate`).
  - Detección de secciones por **línea que termina en `GuiX Object`** (evita
    índice/refs cruzadas); solo se emiten **miembros propios** (los heredados van
    por delegación COM).
- **13 wrappers generados** (`.py` + `.pyi`) en `pysap/objects/`: GuiApplication,
  GuiConnection, GuiSession, GuiMainWindow, GuiButton, GuiCTextField,
  GuiPasswordField, GuiComboBox, GuiCheckBox, GuiRadioButton, GuiGridView,
  GuiTree, GuiStatusbar. `GuiTextField` se mantiene a mano (sección degenerada
  en el PDF). `objects/__init__.py` exporta los 14 + `GuiComponent`.
- Tooling: `pypdf` añadido a `requirements-dev.txt` (solo regenerar).
- Tests: 76 verde (+40), `ruff` limpio. ADR-0004 registrado.

## 2026-06-26 — Fase 4: Page Objects y validación de tipo (ADR-0005)

- **Validación**: `Session.find_as(path, kind, *, validate=False)`. Con
  `validate=True` compara `com.Type` con `kind.sap_type`/`kind.__name__` y lanza
  `ComponentTypeError` si no coincide. El genérico `GuiComponent` no se valida.
- **Page Object**: `pysap/mapping/page_object.py`:
  - `PageObject(session, registry)` con `find(nombre)` y
    `find_as(nombre, kind, *, validate=True)` que resuelven el nombre lógico vía
    `PathRegistry`.
  - `Field(nombre, kind=None)`: descriptor para page objects declarativos con
    autocompletado (usa los wrappers de Fase 3).
- Nuevo error `ComponentTypeError` (path, esperado, hallado); exportado en
  `pysap` y en `pysap.mapping` (`PageObject`, `Field`).
- Tests: 86 verde (+10), `ruff` limpio. ADR-0005 registrado.

## 2026-06-30 — Búsqueda robusta de componentes (ADR-0006)

- **Problema**: `find`/`find_as` exigen el path exacto; en SAP real el prefijo es
  inestable (índices de fila, subscreens, dynpros). Se añaden modos de búsqueda
  que no dependen del path completo.
- **`Session`** (nuevos métodos de localización):
  - `find_by_id_suffix(suffix, *, root=None, raise_=True)` — recorre `Children`
    en profundidad y devuelve el primer control cuyo `id` termine en `suffix`.
  - `find_by_name(name, sap_type, *, raise_=True)` — COM `findByName` (primer
    match por nombre + tipo).
  - `find_all_by_name(name, sap_type)` — COM `findAllByName` (lista de wrappers).
  - Todos devuelven `GuiComponent` y respetan el contrato de `find`
    (`ComponentNotFoundError`, o `None` con `raise_=False`).
- **Integración**: la antigua `buscar_por_id_parcial` (script suelto) queda
  absorbida por `find_by_id_suffix` con manejo de errores honesto (sin
  `except: pass`). `scripts/buscar_id_parcial.py` reescrito como demo que llama a
  la API del paquete.
- **Diseño**: los métodos viven en `Session`, **no** se duplican en `PageObject`
  (el Page Object modela path estable; ver ADR-0006). Si un path mapeado se
  rompe, la evolución será dar estrategias al `PathRegistry`, no inflar el Page
  Object.
- Mock ampliado (`Children` jerárquico, `__iter__`, `findByName`,
  `findAllByName`). Tests: 96 verde (+10), `ruff` limpio. ADR-0006 registrado.

## 2026-06-30 — find_by_id_suffix tipado (extensión ADR-0006)

- **`find_by_id_suffix(suffix, kind=GuiComponent, *, root=None, raise_=True,
  validate=True)`**: ahora acepta un `kind` (segundo posicional) y devuelve el
  wrapper tipado, igual que `find_as`. Antes solo devolvía `GuiComponent` y
  `find_by_id_suffix("x", Kind)` fallaba con `TypeError`.
- Con `kind` distinto del genérico valida el tipo SAP (`ComponentTypeError`);
  `validate=False` lo omite. Sin `kind`, comportamiento previo intacto.
- Tests: 100 verde (+4), `ruff` limpio. Documentado como extensión de ADR-0006.
  Rama `feature/find-suffix-tipado`.

### Pendiente (fases siguientes)
- Codegen: encadenar la jerarquía SAP completa para tipar también los miembros
  heredados (hoy funcionan por delegación, sin tipo estático).
- Telemetría avanzada (ADR-0001 Fase 4): agregados/percentiles sobre
  `ProcessReport`.
