# Guía de funcionamiento de PySap

> Cómo funciona el proyecto de extremo a extremo: qué hace cada módulo, qué
> función/método vive en cada archivo y cómo conviven entre sí. Documento de
> referencia para entender el código sin tener que leerlo todo.

Para el *por qué* de cada decisión, ver los ADR en `docs/decisions/`. Para la
bitácora cronológica, ver `docs/CHANGELOG.md`. Este documento describe el *cómo*.

---

## 1. Idea en una frase

PySap automatiza **SAP GUI** desde Python hablando con él por **COM**
(`pywin32`). Sobre la API cruda de COM monta cuatro capas que lo hacen tipado,
estable, medible y testeable:

```
   [ tú / scripts/open_sap.py ]
              │
   bootstrap.start_session()        ← orquesta todo el arranque
              │
   ┌──────────┼───────────────────────────────┐
   │          │                                │
 launcher  connector                        Session
 (abrir    (open_connection /              (login + find +
  SAP)      connect)                         feedback)
              │                                │
              └──────────► objeto COM GuiSession ◄──┘
                                  │
            Process → Step → Session.find()/find_as()
                                  │
                         objects/ (GuiButton, …)
```

---

## 2. El modelo de objetos SAP (lo que envolvemos)

Todo en SAP GUI Scripting cuelga de una jerarquía COM. PySap la envuelve pero no
la cambia:

```
GetObject("SAPGUI").GetScriptingEngine
  → application (GuiApplication)        raíz COM
       → connection (GuiConnection)     application.Children(n)
            → session (GuiSession)      connection.Children(n)
                 → findById(path)       → componente Gui* (botón, campo, …)
```

`path` es el `id` de un control, p.ej. `wnd[0]/tbar[0]/btn[0]`. Cada capa de
PySap opera en un nivel de esta jerarquía.

---

## 3. Mapa de paquetes

| Paquete | Responsabilidad | Archivos clave |
|---------|-----------------|----------------|
| `pysap/runtime/` | Conexión COM, sesión, arranque, errores, feedback | `connector.py`, `session.py`, `launcher.py`, `bootstrap.py`, `feedback.py`, `errors.py` |
| `pysap/objects/` | Wrappers tipados de componentes `Gui*` (`base.py` a mano; el resto generados) | `base.py`, `gui_button.py`, `gui_textfield.py`, `gui_c_text_field.py`, `gui_combo_box.py`, … (15 en total) |
| `pysap/process/` | Unidades de ejecución medibles y reintentables | `step.py`, `process.py` |
| `pysap/telemetry/` | Estructuras de medición | `metrics.py` |
| `pysap/mapping/` | Nombres lógicos → paths SAP + Page Objects | `registry.py`, `page_object.py` |
| `pysap/config.py` | Config/credenciales desde el entorno | `config.py` |
| `pysap/codegen/` | Genera wrappers `Gui*` desde el PDF de la API (ADR-0004) | `pdf_parser.py`, `emitter.py`, `typemap.py`, `normalize.py`, `generate.py` |
| `scripts/` | Entrypoint ejecutable | `open_sap.py` |
| `tests/` | Unit (mock) + integración + capa mock | `tests/mocks/fake_sap.py` |

`pysap/__init__.py` reexporta la **API pública**: `connect`, `open_connection`,
`start_session`, `launch_sap`, `SapConfig`, `Session` y todas las excepciones.
Importas desde `pysap` directamente.

---

## 4. Runtime — el núcleo

### 4.1 `connector.py` — entrar al COM

Tres funciones, de cruda a lista:

- **`_get_scripting_engine()`** *(privada)* — el único punto que toca
  `win32com.client`. Hace `GetObject("SAPGUI").GetScriptingEngine` y devuelve el
  `GuiApplication`. Si falta `pywin32` o SAP no corre, lanza
  `SapNotRunningError`. Está aislada **a propósito**: es la costura que se
  mockea en tests (se inyecta un `FakeApplication` en su lugar).

- **`connect(connection_index, session_index, *, application=None)`** — se
  **engancha a una sesión SAP ya abierta**. Recorre
  `application.Children(i).Children(j)`, valida que existan y devuelve un
  `Session`. Si `application=None`, lo saca de `_get_scripting_engine()`.

- **`open_connection(description, *, sync=True, application=None, sleep, clock, timeout, poll, …)`**
  — **abre una conexión nueva** por su nombre en SAP Logon
  (`app.OpenConnection`). El detalle fino: SAP puebla la sesión de forma
  **asíncrona**, así que en vez de leerla de golpe (lo que provoca el error COM
  614) **sondea** con `_resolve_session` cada `poll` segundos hasta `timeout`,
  lanzando `WaitTimeoutError` si nunca aparece.
  - **`_resolve_session(app, connection, session_index)`** — primero prueba la
    referencia devuelta por `OpenConnection`; si no expone la sesión, hace
    *fallback* recorriendo `app.Children` desde la más reciente (en algunas
    versiones la sesión nueva cuelga del `application`, no de la `connection`).
  - **`_session_from(connection, session_index)`** — helper que devuelve
    `connection.Children(session_index)` o `None`, tragando los errores COM de
    referencias aún no listas.

`sleep`/`clock` son inyectables → en tests el sondeo es instantáneo y
determinista.

### 4.2 `session.py` — `Session`, la fachada que más usarás

Envuelve un `GuiSession` COM y es **el punto de entrada para todo**. Grupos de
métodos:

**Localizar componentes**
- `find(path)` → envuelve el control en un `GuiComponent` genérico; lanza
  `ComponentNotFoundError` si no existe. Usa `findById(path, False)` para que
  COM devuelva `None` en vez de tirar excepción.
- `find_as(path, kind)` → igual, pero devuelve el **wrapper tipado** que indiques
  (`GuiButton`, `GuiTextField`, …). Esto da autocompletado fuerte en el editor.

**Localizar cuando el path es inestable** (ADR-0006). En SAP real el prefijo del
path cambia (índices de fila, subscreens, dynpros). Estos modos no dependen del
path completo y devuelven `GuiComponent` (lanzan `ComponentNotFoundError`, o
`None` con `raise_=False`):
- `find_by_id_suffix(suffix, kind=GuiComponent, *, root=None, validate=True)` →
  recorre `Children` en profundidad y devuelve el primer control cuyo `id`
  **termine** en `suffix`. Para paths con prefijo variable y final estable
  (`.../btnGUARDAR`). Integra la antigua `buscar_por_id_parcial`. Con `kind`
  devuelve el wrapper **tipado** y valida el tipo (como `find_as`):
  `session.find_by_id_suffix("ctxtGD-TAB", GuiTextField).text = "VBRP"`.
- `find_by_name(name, sap_type)` → COM `findByName`: primer control por **nombre +
  tipo**. Solo fiable en objetos de dynpro (la mayoría de controles no tiene
  `Name` útil).
- `find_all_by_name(name, sap_type)` → COM `findAllByName`: **todas** las
  coincidencias como lista (vacía si no hay).

**Acciones de alto nivel**
- `start_transaction(tcode)` → escribe `/n{tcode}` en el campo de comando y
  manda Enter.
- `login(client, user, password, language="")` → rellena los campos de la
  pantalla de login (`txtRSYST-MANDT`, `BNAME`, `pwdRSYST-BCODE`, `LANGU`) y
  confirma con Enter. **Las credenciales entran por argumento, nunca
  hardcodeadas** (ADR-0002).

**Feedback (barra de estado y popups)**
- `status()` → lee `wnd[0]/sbar` y devuelve un `Status` (ver `feedback.py`).
- `raise_on_error()` → si `status().is_error`, lanza `SapMessageError`.
- `has_popup(window_index=1)` → ¿hay ventana modal `wnd[1]`?
- `send_vkey(key, window_index=0)` → tecla virtual (0=Enter, 12=F12…).
- `confirm_popup()` / `cancel_popup()` → azúcar sobre `send_vkey` (Enter / F12).
- `info` *(property)* → `GuiSessionInfo` (usuario, mandante, transacción…).
- `com` *(property)* → escotilla de escape al objeto COM crudo.

### 4.3 `feedback.py` — clasificar lo que dice SAP

`Status` (dataclass `frozen`): `type` (S/W/E/A/I/"") + `text`. Propiedades
`is_error` (E/A), `is_warning` (W), `is_success` (S). Los conjuntos
`ERROR_TYPES`, etc., centralizan la clasificación. Lo consumen `Session.status()`
y `raise_on_error()`, y los `verify` de los Steps.

### 4.4 `launcher.py` — abrir SAP si está cerrado

`launch_sap(logon_path, *, opener, get_engine, sleep, clock, timeout, poll)`
garantiza que SAP esté disponible y devuelve el `GuiApplication`. Lógica en 3
pasos:

1. ¿La ROT ya responde? (`get_engine()`) → engancha **sin relanzar**.
2. No responde → lanza el binario (`opener(logon_path)`, por defecto
   `subprocess.Popen`). Si no hay `logon_path`, lanza `SapLaunchError`.
3. Sondea `get_engine()` cada `poll` hasta `timeout`; si expira, `SapLaunchError`.

Todas las dependencias de SO (`opener`, `get_engine`, `sleep`, `clock`) son
inyectables → se testea el arranque **sin SAP ni proceso real**.

> Nota: ADR-0001 descartó VBScript como mecanismo de *scripting*; aquí el
> subprocess solo **arranca el ejecutable**. El scripting sigue siendo COM.

### 4.5 `bootstrap.py` — el pegamento

`start_session(config, *, application=None, launcher=launch_sap)` une todo en el
flujo de la demo end-to-end:

```python
app     = launcher(config.logon_path)          # 1. arranca SAP si hace falta
session = open_connection(config.connection,   # 2. abre conexión + sondea sesión
                          application=app)
Process("login").add(                          # 3. login como Step verificado
    Step("login",
         action=lambda s: s.login(config.client, config.user,
                                   config.password, config.language),
         verify=lambda s: not s.status().is_error)
).run(session)
return session                                 # 4. sesión lista para operar
```

El login no es una llamada suelta: es un `Step` dentro de un `Process`, así que
queda **medido** y **verificado** por la barra de estado como cualquier otra
acción.

### 4.6 `errors.py` — jerarquía de excepciones

Todas heredan de `PySapError`:

| Excepción | Cuándo |
|-----------|--------|
| `SapNotRunningError` | No hay SAP en la ROT (cerrado o scripting off) |
| `ComponentNotFoundError` | `find`/`find_as` con un path inexistente |
| `StepError` | Un `Process` falló en un step (envuelve la causa) |
| `WaitTimeoutError` | Expiró una espera (`open_connection`, `Step.wait_for`) |
| `SapMessageError` | La barra de estado reportó error/aborto (E/A) |
| `MissingConfigError` | Faltan variables `SAP_*` obligatorias |
| `SapLaunchError` | No se pudo arrancar/enganchar SAP |

---

## 5. Objects — wrappers tipados

### 5.1 `base.py` — `GuiComponent`

Base de **todos** los wrappers. Envuelve un componente COM y expone las
propiedades comunes: `id`, `type`, `name`, `text` (con setter). El truco clave:

- **`__getattr__`** delega al COM cualquier atributo no envuelto explícitamente.
  Significa que aunque el wrapper no cubra el 100% de la API, **sigue
  funcionando** (`componente.LoQueSea` cae al objeto COM).
- `_com` se asigna por `object.__setattr__` para no disparar la delegación.
- `com` *(property)* expone el COM crudo; `__repr__` muestra `id`/`type`.

### 5.2 Wrappers concretos (`gui_button.py`, `gui_textfield.py`, …)

Heredan de `GuiComponent` y añaden la API específica del control:

- **`GuiButton`**: `press()`, `left_label`, `right_label`.
- **`GuiTextField`**: `value` (get/set), `max_length`, `required`, `set_focus()`.

Hoy hay **15 wrappers** en `objects/` (`GuiButton`, `GuiTextField`,
`GuiCTextField`, `GuiComboBox`, `GuiCheckBox`, `GuiRadioButton`, `GuiGridView`,
`GuiTree`, `GuiStatusbar`, `GuiMainWindow`, `GuiPasswordField`, `GuiApplication`,
`GuiConnection`, `GuiSession`, y la base `GuiComponent`). Todos salvo `base.py`
los **genera `pysap.codegen`** desde el PDF oficial de la API (ADR-0004, Fase 3);
llevan la cabecera "GENERADO — NO EDITAR" y se regeneran, no se tocan a mano.
Aunque un wrapper no cubra una propiedad, la delegación COM de `GuiComponent`
(`__getattr__`) hace que siga siendo usable.

---

## 6. Process — ejecución medible y estable

### 6.1 `step.py` — `Step` (dataclass)

La **unidad atómica**. Campos:

- `name`, `action` (recibe `Session`, hace la interacción), `verify`
  (comprobación posterior opcional).
- **Reintentos**: `retries` (intentos extra), `retry_delay`.
- **Espera previa**: `wait_for` (condición antes de actuar), `wait_timeout`,
  `wait_poll`.

`run(session, *, sleep, clock)` ejecuta el ciclo:

1. Si hay `wait_for`, espera la condición (`_await_condition`, sondeo hasta
   `wait_timeout` o `WaitTimeoutError`).
2. Ejecuta `action` hasta `retries+1` veces; tras cada acción comprueba `verify`
   (si devuelve `False` → falla y reintenta).
3. Si agota intentos, re-lanza la última excepción.

`sleep`/`clock` inyectables → tests sin esperas reales. Esto es lo que hace que
"reintentable" y "estable" sean ciertos, no solo declarados (ADR-0002).

### 6.2 `process.py` — `Process`

Orquesta una lista ordenada de `Step`. Métodos:

- `add(step)` → encadenable (devuelve `self`).
- `run(session, *, stop_on_error=True)` → ejecuta cada step **midiendo su
  duración**, registra un `StepMetric` por step (ok/fallo/duración/error) y
  devuelve un `ProcessReport`. Por defecto detiene al primer fallo, envolviéndolo
  en `StepError`. Loguea por `logging` (`pysap.process`).

### 6.3 Cómo conviven Step ↔ Process ↔ Session ↔ telemetry

```
Process.run(session)
   └─ por cada Step:
        cronómetro start
        Step.run(session)         # wait_for → action(session) → verify(session)
        StepMetric(ok, duration)  # se acumula en ProcessReport
   devuelve ProcessReport
```

El `action`/`verify` del Step recibe la `Session`, con lo que dentro puede usar
`session.find_as(...)`, `session.status()`, etc. Así el feedback de SAP alimenta
la verificación del step.

---

## 7. Telemetry — `metrics.py`

- **`StepMetric`**: `name`, `ok`, `duration_s`, `error`.
- **`ProcessReport`**: `process_name` + lista de `StepMetric`. Propiedades
  derivadas: `ok` (todos verde), `total_duration_s`, `failed` (los caídos).
  `add(metric)` lo va llenando desde `Process.run`.

Es la salida medible del proyecto: cada ejecución de proceso produce un reporte
inspeccionable.

---

## 8. Mapping — `registry.py` + `page_object.py`

### 8.1 `PathRegistry` — nombres lógicos → paths

`PathRegistry` es un mapa **nombre lógico → path SAP**. En vez de esparcir
`wnd[0]/tbar[0]/btn[0]` por todo el código, registras `boton_guardar` → ese path
en un solo sitio. Si SAP cambia la UI, ajustas un único registro.

Métodos: `register(name, path)`, `path(name)` (lanza `KeyError` claro si falta),
`__contains__`, `__len__`.

### 8.2 `PageObject` y `Field` — modelar una pantalla (ADR-0005)

Encima del registry, un **Page Object** representa una pantalla SAP y expone sus
controles como atributos limpios. Une una `Session` con un `PathRegistry`:

- **`PageObject(session, registry)`** — guarda ambos. Métodos:
  - `find(name)` → resuelve `name` contra el registry y devuelve el control sin
    tipar (`session.find(path)`).
  - `find_as(name, kind, *, validate=True)` → igual pero devuelve el wrapper
    tipado y **valida el tipo por defecto** (un path mal mapeado se detecta al
    instante con `ComponentTypeError`).

- **`Field(name, kind=None)`** — descriptor para declarar un control como atributo
  de clase:

  ```python
  class LoginPage(PageObject):
      mandante = Field("mandante", GuiTextField)
  ```

  Cada acceso a `page.mandante` **re-resuelve** el control (llama a `find`/`find_as`
  por debajo). **No cachea a propósito**: tras acciones que refrescan la pantalla
  las referencias COM viejas se invalidan, así que re-localizar siempre es lo
  correcto. Con `kind=None` devuelve genérico; con `kind` devuelve tipado y
  validado.

Así una automatización usa `page.mandante.value = "100"` sin ver un solo path.
Es el patrón que arma el Demo C (ver `docs/DEMO-PASO-A-PASO.md`).

---

## 9. Config — `config.py`

`SapConfig` (dataclass `frozen`): `connection`, `client`, `user`, `password`
(obligatorias) + `language`, `logon_path` (opcionales).

- **`from_env(env=None, *, dotenv_path=None)`** construye la config:
  1. Si hay `dotenv_path`, lee el `.env` con `_read_dotenv` (parser propio
     `KEY=VALUE`, ignora comentarios/comillas — sin dependencia nueva).
  2. El **entorno real pisa al `.env`** (`valores.update(base)`).
  3. Valida obligatorias; si falta alguna → `MissingConfigError(faltantes)`.

Mapeos `_OBLIGATORIAS`/`_OPCIONALES` traducen `SAP_*` → atributos. Las
credenciales **nunca se versionan** (ADR-0003); el `.env` está en `.gitignore`.

---

## 10. Entrypoint — `scripts/open_sap.py`

Ejecutable fino. `main(argv)`:

1. Parsea `--env` (default `.env`); si el archivo no existe, usa solo el entorno.
2. `SapConfig.from_env(dotenv_path=...)` → si falta config, error claro y
   `return 2`.
3. `start_session(config)` → maneja `SapLaunchError` (3), `SapMessageError` (4),
   `PySapError` genérico (1).
4. Éxito: imprime usuario/mandante y la barra de estado. **No imprime
   credenciales.** `return 0`.

Códigos de salida distintos por tipo de fallo → usable en automatización/CI.
Ajusta `sys.path` para correr directo sin instalar el paquete.

---

## 11. Testing — mock que reemplaza a SAP

La clave de testear sin SAP: **inyectar un `FakeApplication`** donde el código
real sacaría el `GuiApplication` de la ROT. Como `connect`, `open_connection`,
`launch_sap` y `start_session` aceptan `application=`/`get_engine=`, los tests
pasan los falsos.

`tests/mocks/fake_sap.py` reproduce la superficie COM mínima:

| Fake | Emula | Detalle |
|------|-------|---------|
| `FakeComponent` | un control `Gui*` | `Id/Type/Name/Text/MessageType` + `Press`/`SetFocus`/`sendVKey`; `Children`/`add_child` (árbol para `find_by_id_suffix`); registra `pressed`/`focused`/`vkeys` para aserciones |
| `FakeChildren` | colección COM `Children` | `Count` + `__call__(index)` + `__iter__` |
| `FakeSession` | `GuiSession` | dict `path → FakeComponent`; `findById(path, raise)`, `findByName`/`findAllByName`, `Children` (raíz) |
| `FakeSessionInfo` | `GuiSessionInfo` | `User`, `Client`, `Transaction` |
| `FakeConnection` / `FakeApplication` | conexión / raíz | `OpenConnection` crea una sesión con la pantalla de login poblada |
| `build_app(session)` | atajo | app con 1 conexión y 1 sesión |

Tests unit cubren: `connection`, `session`, `step_wait_retry`, `process`,
`feedback`, `config`, `launcher`, `bootstrap`. Integración real en
`tests/integration/` marcada `@pytest.mark.sap` (solo con SAP de verdad).

---

## 12. Recorrido completo — del comando a la sesión lista

```
$ python scripts/open_sap.py
   │
   ▼
main()  ── SapConfig.from_env(".env")            config.py  (valida SAP_*)
   │
   ▼
start_session(config)                            bootstrap.py
   │
   ├─ launch_sap(logon_path)                     launcher.py
   │     ├─ get_engine() responde? → app
   │     └─ no → subprocess.Popen + sondeo
   │
   ├─ open_connection(connection, application=app)   connector.py
   │     └─ OpenConnection + sondeo asíncrono → Session
   │
   └─ Process("login").run(session)              process.py + step.py
         └─ Step "login":
              action  → session.login(...)       session.py
              verify  → not session.status().is_error   feedback.py
              métrica → StepMetric → ProcessReport      metrics.py
   │
   ▼
session lista  →  main() imprime usuario/mandante + barra de estado
```

A partir de ahí operas: `session.start_transaction("VA01")`,
`session.find_as("...", GuiButton).press()`, o montas tus propios
`Process`/`Step` para flujos medidos.

---

## 13. Estado y pendientes

Funcionando hoy (96 tests verde): runtime completo, conexión dual
(attach + open), arranque, login, feedback, Steps/Process, telemetría, config,
entrypoint, codegen (Fase 3), Page Objects + validación de tipo (Fase 4) y
búsqueda robusta de componentes por sufijo de id / nombre (ADR-0006).

Pendiente:
- **Codegen** — encadenar la jerarquía SAP completa para tipar también los
  miembros heredados (hoy funcionan por delegación COM, sin tipo estático).
- **Mapping** — si un path mapeado se vuelve inestable, dar estrategias de
  resolución (exacto/sufijo/nombre) al `PathRegistry` (ADR-0006, pospuesto).
- **Telemetría avanzada** — agregados/percentiles sobre `ProcessReport`.

Ver `docs/CHANGELOG.md` y `docs/decisions/` para el detalle y el *porqué*.
