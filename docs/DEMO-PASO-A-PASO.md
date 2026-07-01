# Demo paso a paso — probar PySap en SAP real

> Guía operativa para validar lo construido (Fases 1–5) contra una sesión SAP
> real. No es código de producción: son los pasos que **tú** ejecutas. Si algo
> falla, ve a la sección [10. Problemas](#10-problemas-y-como-reportarlos) y me
> envías el bloque indicado.

**Objetivo del demo:** abrir SAP, hacer login automático y ejecutar un proceso
mínimo (abrir una transacción y leer la barra de estado), usando `Session`,
`Process`/`Step`, los wrappers tipados y un Page Object.

---

## 0. Antes de empezar (requisitos)

- [ ] Windows con **SAP GUI** instalado.
- [ ] **Scripting habilitado** en cliente y servidor (ver paso 1).
- [ ] **Python 3.12+** (`python --version`).
- [ ] Acceso a un mandante de **pruebas/QAS** (no producción para el primer demo).
- [ ] Credenciales SAP válidas (usuario, mandante, contraseña).

---

## 1. Habilitar el SAP GUI Scripting

PySap habla con SAP por COM; sin scripting, nada funciona.

**Cliente (tu PC):**
1. Abre SAP Logon.
2. Menú de opciones (icono arriba a la izquierda) → **Options**.
3. **Accessibility & Scripting → Scripting**.
4. Marca **Enable scripting**.
5. **Desmarca** "Notify when a script attaches to SAP GUI" y "Notify when a
   script opens a connection" (si no, salta un popup que frena la automatización).
6. Aplica y reinicia SAP Logon.

**Servidor (si lo controla Basis):** el parámetro `sapgui/user_scripting = TRUE`
debe estar activo en el sistema. Si el paso 7 falla con "scripting deshabilitado",
pídeselo a Basis.

> Verificación rápida: con SAP abierto y logueado a mano, el grabador de scripts
> (paso 5) debe poder grabar. Si no, el scripting no está activo.

---

## 2. Preparar el entorno Python

En una terminal, en la carpeta del proyecto (`PySap`):

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
```

Verifica que los tests pasan (sin SAP, con mock):

```bash
pytest -q
```

Esperado: `96 passed, 1 deselected`. Si falla aquí, **párate** y repórtalo
(problema de entorno, no de SAP).

---

## 3. Configurar credenciales (.env)

Las credenciales **no se versionan** (ADR-0003). Crea un archivo `.env` en la
raíz del proyecto, copiando de `.env.example`:

```
SAP_CONNECTION=NOMBRE EXACTO DE LA ENTRADA EN SAP LOGON
SAP_CLIENT=100
SAP_USER=tu_usuario
SAP_PASSWORD=tu_contraseña
SAP_LANG=ES
SAP_LOGON_PATH=C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe
```

Claves:
- **`SAP_CONNECTION`**: el texto **literal** que aparece en la lista de SAP Logon
  (p.ej. "QAS - Calidad"). Cópialo exacto, con espacios.
- **`SAP_LOGON_PATH`**: ruta real a `saplogon.exe`. Confírmala en tu PC; la de
  arriba es la típica pero puede variar.
- `SAP_LANG` opcional (ES/EN).

---

## 4. Primer arranque: login automático

Cierra SAP por completo (para probar el arranque desde cero). Luego:

```bash
python scripts/open_sap.py
```

Qué hace (ADR-0003): carga `.env` → lanza `saplogon.exe` si hace falta → abre la
conexión → hace login → deja la sesión lista.

**Salida esperada:**
```
Sesión lista. Usuario=TU_USUARIO Mandante=100
Barra de estado [S]: ...
```

Si llegas aquí, **el núcleo funciona**: arranque + conexión + login + feedback.

Códigos de error del script (si algo falla):
| Código | Significado | Mira el paso |
|--------|-------------|--------------|
| 2 | Falta config (`SAP_*`) | 3 |
| 3 | No arrancó/enganchó SAP | 1, 4 |
| 4 | SAP rechazó el login | 3 (credenciales/mandante) |
| 1 | Otro error PySap | 9 |

---

## 5. Capturar los paths de los controles

Para automatizar una pantalla necesitas los `id`/path de sus campos y botones.
SAP te los da:

1. Con SAP abierto, arriba a la derecha está el icono de **grabar script**
   (o `Alt+F12` → *Script Recording and Playback*).
2. Pulsa **grabar**.
3. Haz **a mano** la tarea que quieres automatizar (p.ej. abrir VA03, escribir un
   número, Enter).
4. Detén la grabación. SAP genera un `.vbs`.
5. Abre ese `.vbs`: cada línea `session.findById("wnd[0]/...")` te da el **path
   exacto** de cada control que tocaste.

Anota los paths que te interesan. Esos son la materia prima del demo.

> Truco: pasa el ratón sobre un campo y mira la barra de estado, o usa el
> recorder; el path siempre tiene forma `wnd[0]/usr/...`.

---

## 6. Demo A — proceso mínimo (interactivo)

**Objetivo:** el "hola mundo" de PySap. Abrir SAP, entrar a una transacción, leer
lo que SAP responde y reaccionar si aparece un popup. Es el esqueleto sobre el que
se construyen los demos B, C y D.

Crea un archivo temporal `demo_a.py` en la raíz y pega esto, **ajustando la
transacción**:

```python
from pysap import SapConfig, start_session

session = start_session(SapConfig.from_env(dotenv_path=".env"))

# 1. Abrir una transacción (cámbiala por una tuya de solo lectura, p.ej. SE16, VA03)
session.start_transaction("SE16")

# 2. Leer la barra de estado
estado = session.status()
print("Estado:", estado.type, "-", estado.text)

# 3. ¿Hay popup? Manéjalo
if session.has_popup():
    print("Popup detectado, confirmando...")
    session.confirm_popup()
```

Ejecuta:
```bash
python demo_a.py
```

### Qué hace cada método (y cómo funciona por dentro)

- **`SapConfig.from_env(dotenv_path=".env")`** — lee el archivo `.env` (paso 3) y
  construye un objeto `SapConfig` con conexión, mandante, usuario, contraseña e
  idioma. Es un simple contenedor de datos: no toca SAP todavía, solo empaqueta la
  configuración para pasársela al arranque.

- **`start_session(config)`** — la pieza que **converge** arranque + conexión +
  login en una sola llamada. Por dentro hace tres cosas en cadena:
  1. `launch_sap(logon_path)` — garantiza que SAP esté abierto (lo lanza si no lo
     está) y devuelve el objeto COM `GuiApplication`.
  2. `open_connection(connection)` — abre la entrada de SAP Logon indicada y
     obtiene la `Session`.
  3. Ejecuta un `Process("login")` con un único `Step` que rellena la pantalla de
     login y **verifica** que la barra de estado no marque error. Si el login
     falla, lanza excepción aquí mismo. Devuelve la `Session` ya logueada.

  Es decir: cuando esta línea termina sin error, tienes garantizado el núcleo
  (arranque + conexión + login) funcionando. Todo lo demás opera sobre esta
  `session`.

- **`session.start_transaction("SE16")`** — atajo para navegar. Por dentro escribe
  `/nSE16` en el campo de comandos (`wnd[0]/tbar[0]/okcd`) y envía Enter
  (`sendVKey(0)`). El prefijo `/n` le dice a SAP "cierra lo actual y ve a esta
  transacción". Cambia `SE16` por una transacción de **solo lectura** para el
  primer demo.

- **`session.status()`** — lee la barra de estado inferior (`wnd[0]/sbar`) y
  devuelve un objeto `Status` con dos campos: `type` (una letra: `S`=éxito,
  `W`=aviso, `E`=error, `A`=aborto, `I`=info, o vacío) y `text` (el mensaje). Es
  la forma en que "escuchas" lo que SAP responde tras cada acción. `Status` también
  ofrece las propiedades `is_error`, `is_warning`, `is_success` para no comparar
  letras a mano.

- **`session.has_popup()`** — devuelve `True` si SAP abrió una ventana modal
  (`wnd[1]`). Los popups bloquean la automatización: hay que detectarlos y
  cerrarlos antes de seguir.

- **`session.confirm_popup()`** — confirma el popup pulsando Enter sobre él
  (`sendVKey(0)` en `wnd[1]`). Su gemelo es `cancel_popup()`, que envía F12
  (cancelar).

### Cómo converge todo

El flujo es: **configuración → sesión lista → acción → escucha → reacción**.
`start_session` te entrega el terreno preparado; `start_transaction` actúa;
`status` te dice qué pasó; `has_popup`/`confirm_popup` manejan lo inesperado. Ese
mismo ciclo —actuar y luego leer el feedback— es el que los demos siguientes
formalizan con wrappers tipados (B), Page Objects y Process (C) y búsquedas
robustas (D).

**Qué validas:** `start_session`, `start_transaction`, `status`, manejo de popups.

---

## 7. Demo B — wrapper tipado + verificación

**Objetivo:** en lugar de manipular objetos COM crudos (donde todo es "texto" y
cualquier error se ve solo al ejecutar), trabajar con **wrappers tipados**: clases
Python que representan cada tipo de control SAP (`GuiTextField`, `GuiButton`, …) y
te dan autocompletado y validación. Además, aprender a **verificar** que la acción
salió bien en vez de asumirlo.

Sobre la misma sesión, prueba un control tipado. Usa un **path real** capturado
en el paso 5. Ejemplo con un campo de texto y un botón:

```python
from pysap import SapConfig, start_session
from pysap.objects import GuiTextField, GuiButton

session = start_session(SapConfig.from_env(dotenv_path=".env"))
session.start_transaction("SE16")

# Cambia estos paths por los TUYOS (paso 5)
campo = session.find_as("wnd[0]/usr/ctxtDATABROWSE-TABLENAME", GuiTextField, validate=True)
campo.value = "T000"            # escribe en el campo
print("Escrito:", campo.com.Text)

session.send_vkey(0)            # Enter
session.raise_on_error()       # si SAP marcó error, lanza excepción clara
print("OK, estado:", session.status().text)
```

### Qué hace cada método (y cómo funciona por dentro)

- **`session.find_as(path, GuiTextField, validate=True)`** — localiza el control en
  ese `path` y lo devuelve **ya envuelto** en la clase indicada. Por dentro:
  1. Llama a `findById(path)` en COM. Si no existe, lanza `ComponentNotFoundError`
     con el path (error claro, no un `None` silencioso).
  2. Con `validate=True`, compara el tipo SAP real del control
     (`com_obj.Type`) contra el esperado por la clase (`GuiTextField`). Si no
     coinciden, lanza `ComponentTypeError`. Esto atrapa el error clásico: un path
     que apunta a un control distinto del que creías (ADR-0005).
  3. Devuelve una instancia de `GuiTextField` que envuelve el objeto COM.

  Diferencia con `find`: `find` devuelve un `GuiComponent` genérico (sin tipar);
  `find_as` te da el wrapper específico con sus propiedades y métodos.

- **`campo.value = "T000"`** — `GuiTextField` expone la propiedad `value`; su
  *setter* escribe en `com.Text` por debajo. Es más legible que `campo.com.Text =
  "T000"` y deja claro que estás rellenando el campo. Todo wrapper hereda además
  `id`, `type`, `name`, `text` de la clase base `GuiComponent`.

- **`campo.com.Text`** — `.com` es la **escotilla de escape**: el objeto COM crudo
  que hay dentro del wrapper. Sirve para leer/usar propiedades que el wrapper no
  envuelve explícitamente. (De hecho, cualquier atributo no definido en el wrapper
  se delega automáticamente al COM, así que el wrapper nunca te limita).

- **`session.send_vkey(0)`** — envía una tecla virtual a la ventana. `0` = Enter,
  `12` = F12, etc. Aquí confirma la consulta escrita en el campo.

- **`session.raise_on_error()`** — lee la barra de estado y, si es error o aborto
  (`type` en `E`/`A`), lanza `SapMessageError` con el tipo y el texto. Es el
  "corta-circuitos": convierte un mensaje de error de SAP —que de otro modo pasaría
  desapercibido— en una excepción Python que **detiene** el flujo con un mensaje
  claro.

### Cómo converge todo

Demo A actuaba y leía el estado a mano; Demo B da el salto a **trabajo tipado y
verificado**: `find_as` garantiza que tocas el control correcto (o falla al
instante), el wrapper te da una API limpia (`campo.value`), y `raise_on_error`
convierte el feedback de SAP en control de flujo. Los wrappers (`GuiTextField`,
`GuiButton`, …) se generan automáticamente desde el PDF de la API de SAP
(ADR-0004), por eso hay uno por cada tipo de control. Este trío —localizar tipado,
actuar, verificar— es exactamente lo que Demo C empaqueta en pasos reutilizables.

**Qué validas:** `find_as` con `validate=True` (Fase 4), wrappers generados
(Fase 3), `send_vkey`, `raise_on_error`.

Si `validate=True` lanza `ComponentTypeError`, el path apunta a otro tipo de
control: revisa el path o quita `validate` para inspeccionar `comp.type`.

---

## 8. Demo C — Page Object + Process medido

**Objetivo:** el patrón recomendado para automatizaciones **repetibles y de
producción**. Junta cuatro ideas que hasta ahora vimos sueltas:

1. **Registry** — una tabla que traduce nombres lógicos ("tabla") a paths SAP, para
   no repartir paths frágiles por todo el código.
2. **Page Object** — una clase que modela una pantalla SAP y expone sus controles
   como atributos limpios.
3. **Process / Step** — una secuencia de pasos, cada uno con verificación,
   reintentos y espera.
4. **Telemetría** — un reporte con el resultado y la duración de cada paso.

Crea `demo_c.py`:

```python
from pysap import SapConfig, start_session
from pysap.mapping import PathRegistry, PageObject, Field
from pysap.objects import GuiTextField
from pysap.process.process import Process
from pysap.process.step import Step

# 1. Registry: nombres lógicos -> paths reales (ajústalos, paso 5)
reg = PathRegistry()
reg.register("tabla", "wnd[0]/usr/ctxtDATABROWSE-TABLENAME")

# 2. Page Object declarativo
class SE16(PageObject):
    tabla = Field("tabla", GuiTextField)

session = start_session(SapConfig.from_env(dotenv_path=".env"))
session.start_transaction("SE16")
page = SE16(session, reg)

# 3. Proceso medido con verificación
proc = Process("consulta_tabla").add(
    Step("escribir_tabla",
         action=lambda s: setattr(page.tabla, "value", "T000"),
         verify=lambda s: not s.status().is_error,
         retries=1)
).add(
    Step("ejecutar", action=lambda s: s.send_vkey(0),
         verify=lambda s: not s.status().is_error)
)

reporte = proc.run(session)
print("Proceso OK:", reporte.ok)
print("Duración total (s):", round(reporte.total_duration_s, 3))
for m in reporte.steps:
    print(f"  {m.name}: ok={m.ok} {round(m.duration_s,3)}s {m.error or ''}")
```

### Bloque 1 — el Registry (nombres lógicos → paths)

- **`PathRegistry()`** — crea un mapa vacío `nombre_lógico -> path SAP`.
- **`reg.register("tabla", "wnd[0]/usr/ctxtDATABROWSE-TABLENAME")`** — asocia el
  nombre estable `"tabla"` al path real. **Por qué importa:** los paths SAP son
  frágiles (cambian entre versiones o pantallas). Si el path cambia, lo corriges
  en **un solo sitio** —aquí— y todo el resto del código, que solo conoce el nombre
  `"tabla"`, sigue funcionando. Internamente `path("tabla")` devuelve el path o
  lanza `KeyError` claro si el nombre no está registrado.

### Bloque 2 — el Page Object (modela la pantalla)

- **`class SE16(PageObject)`** — representa la pantalla de la transacción SE16.
  `PageObject` guarda la `session` y el `registry` juntos.
- **`tabla = Field("tabla", GuiTextField)`** — `Field` es un **descriptor**: un
  atributo "inteligente". Cada vez que accedes a `page.tabla`, el descriptor
  resuelve el nombre `"tabla"` contra el registry para obtener el path, y luego
  llama a `find_as(path, GuiTextField, validate=True)`. Es decir, `page.tabla` te
  devuelve, en el momento, un `GuiTextField` tipado y validado apuntando al control
  real.

  **Detalle clave: no hay caché.** El descriptor vuelve a localizar el control en
  **cada** acceso. Esto es intencional: tras acciones que refrescan la pantalla, las
  referencias COM viejas se invalidan; re-localizar siempre evita el temido "COM
  object is no longer valid".

- **`page = SE16(session, reg)`** — instancia la pantalla uniendo la sesión activa
  y el registry. A partir de aquí, `page.tabla` es tu campo, sin ver un solo path.

### Bloque 3 — el Process medido

- **`Process("consulta_tabla")`** — crea un proceso con nombre (aparecerá en el
  reporte).
- **`.add(Step(...))`** — añade un paso. `add` devuelve el propio proceso, por eso
  se **encadena** `.add(...).add(...)`.
- **`Step(name, action, verify, retries)`** — cada `Step` es la unidad atómica:
  - **`action=lambda s: setattr(page.tabla, "value", "T000")`** — la interacción con
    SAP. Recibe la sesión `s`. Aquí escribe `"T000"` en el campo tipado (equivale a
    `page.tabla.value = "T000"`; se usa `setattr` porque un `lambda` no admite
    asignación directa).
  - **`verify=lambda s: not s.status().is_error`** — comprobación **posterior**: lee
    la barra de estado y exige que no sea error. Si `verify` devuelve `False`, el
    step se considera fallido.
  - **`retries=1`** — un reintento extra si la acción o la verificación fallan (con
    `retries=1` son 2 intentos en total). Útil para pantallas que a veces tardan.
    `Step` también admite `retry_delay` (espera entre reintentos) y `wait_for` +
    `wait_timeout` (esperar a que una condición se cumpla **antes** de actuar).
  - Orden interno de un `Step`: primero espera `wait_for` (si lo hay) → ejecuta
    `action` reintentando hasta `retries+1` veces → tras cada intento evalúa
    `verify`. Solo cuando todos los intentos fallan re-lanza la excepción.

- **`proc.run(session)`** — ejecuta los steps **en orden**, cronometrando cada uno
  con `time.perf_counter()`. Por defecto `stop_on_error=True`: si un step falla,
  registra la métrica y **detiene** el proceso lanzando `StepError`. Devuelve un
  `ProcessReport`.

### Bloque 4 — el reporte (telemetría)

- **`reporte.ok`** — `True` solo si **todos** los steps salieron bien.
- **`reporte.total_duration_s`** — suma de la duración de todos los steps.
- **`reporte.steps`** — lista de `StepMetric`, uno por paso, con `.name`, `.ok`,
  `.duration_s` y `.error` (el mensaje si falló, `None` si no). El bucle final los
  imprime uno por uno. (También existe `reporte.failed` con solo los que fallaron).

### Cómo converge todo

Este es el demo donde **todas las piezas encajan**:

```
Registry (nombres → paths)
   ↓  el Page Object lo consulta
Page Object (page.tabla → GuiTextField tipado, re-localizado en cada acceso)
   ↓  los Steps lo usan en sus acciones
Process → Step (action + verify + retries)  ← el motor que actúa y comprueba
   ↓  run() cronometra cada paso
ProcessReport (ok, duración, detalle por step)  ← evidencia de qué pasó
```

El valor frente a los demos anteriores: en A y B tú leías el estado a mano y un
fallo pasaba desapercibido. Aquí **cada paso se autoverifica**, **se reintenta solo**
si conviene, **se mide**, y al final tienes un `ProcessReport` que puedes registrar,
auditar o usar para decidir si el proceso siguió. Es el paso de "script que corre"
a "proceso observable y robusto".

**Qué validas:** todo junto — registry, Page Object, `Field`, `Process`/`Step`
con reintentos y verificación, telemetría (`ProcessReport`).

---

## 9. Demo D — búsqueda robusta cuando el path es inestable

A veces el path capturado en el paso 5 **deja de funcionar**: SAP cambió un
índice de fila, un subscreen o el dynpro, y `find`/`find_as` lanzan
`ComponentNotFoundError` aunque el control siga en pantalla. Para eso están los
modos de búsqueda que no dependen del path completo (ADR-0006).

**Objetivo:** aprender los métodos de búsqueda robusta para cuando el path
capturado deja de funcionar aunque el control siga en pantalla.

Crea `demo_d.py` y ajusta los valores a tu pantalla:

```python
from pysap import SapConfig, start_session

session = start_session(SapConfig.from_env(dotenv_path=".env"))
session.start_transaction("SE16")

# 1. Por SUFIJO de id: el prefijo (wnd[0]/usr/...) puede cambiar; el final no.
#    Pon el último tramo del id que viste en el .vbs (paso 5), p.ej. el del botón ejecutar.
boton = session.find_by_id_suffix("btn[8]")          # raise_=False -> None si no está
print("Por sufijo:", None if boton is None else (boton.type, boton.id))

# 2. Por NOMBRE + tipo (solo fiable en campos de dynpro, que sí tienen Name).
campo = session.find_by_name("DATABROWSE-TABLENAME", "GuiCTextField", raise_=False)
print("Por nombre:", None if campo is None else (campo.id, campo.name))

# 3. TODAS las coincidencias por nombre + tipo (lista, vacía si no hay).
botones = session.find_all_by_name("btn[0]", "GuiButton")
print("Coincidencias:", [b.id for b in botones])

# 4. Acotar la búsqueda a un contenedor (más rápido y preciso que toda la sesión).
area = session.find("wnd[0]/usr")
dentro = session.find_by_id_suffix("TABLENAME", root=area, raise_=False)
print("Dentro de usr:", None if dentro is None else dentro.id)
```

Ejecuta:
```bash
python demo_d.py
```

### Qué hace cada método (y cómo funciona por dentro)

- **`session.find_by_id_suffix("btn[8]")`** — busca un control cuyo `id`
  **termine** en ese sufijo. Por dentro recorre el árbol de controles en
  profundidad (recorrido recursivo de la colección `Children`) y devuelve la
  primera coincidencia. **Por qué es la más robusta:** el prefijo del path
  (`wnd[0]/usr/subA:...`) es lo que SAP cambia entre pantallas; el final del `id`
  suele ser estable. Buscando solo por el final, sobrevives a esos cambios.
  Acepta también `kind` para devolver un wrapper tipado (como `find_as`) y
  `validate=True` para comprobar el tipo.

- **`session.find_by_name("DATABROWSE-TABLENAME", "GuiCTextField", raise_=False)`**
  — busca por la propiedad `Name` del control **más** su tipo SAP. Equivale al COM
  `findByName`, que devuelve solo la **primera** coincidencia. **Limitación
  importante:** la mayoría de controles SAP no tienen un `Name` significativo; esto
  es fiable sobre todo en campos de dynpro (los `RSYST-...`, `DATABROWSE-...`). Si
  el control no tiene `Name`, usa el sufijo de id.

- **`session.find_all_by_name("btn[0]", "GuiButton")`** — como el anterior pero
  devuelve **todas** las coincidencias en una lista (vacía si no hay ninguna). Úsalo
  cuando esperas varios controles con el mismo nombre/tipo y quieres recorrerlos.

- **`root=area` en `find_by_id_suffix`** — acota la búsqueda a un contenedor en vez
  de recorrer toda la sesión. Primero `session.find("wnd[0]/usr")` obtiene el área
  de usuario (donde viven los campos de la pantalla); pasarlo como `root` hace la
  búsqueda **más rápida y precisa** (menos ramas que recorrer, sin falsos positivos
  de barras de herramientas u otras ventanas).

- **`raise_=False`** — el interruptor común a estos métodos: en vez de lanzar
  `ComponentNotFoundError` cuando no encuentra, devuelve `None` (o lista vacía en
  `find_all_by_name`). Ideal para **inspeccionar sin romper**: pruebas varios
  sufijos/nombres y ves cuál engancha, sin que el script muera en el primer fallo.
  Con `raise_=True` (por defecto en `find_by_id_suffix`/`find_by_name`) obtienes el
  error explícito para producción.

### Cómo converge todo

Demos A–C asumen paths estables (`find`/`find_as`), que es lo normal. Demo D es la
**red de seguridad** para cuando esa suposición se rompe. La regla práctica de
cuándo usar cada estrategia:

> - **`find` / `find_as`** — path estable (lo normal). Siguen siendo la opción por defecto.
> - **`find_by_id_suffix`** — el prefijo cambia pero el final del id es estable. La más robusta.
> - **`find_by_name`** — campos de dynpro con `Name` significativo (la mayoría de
>   controles **no** lo tiene; si devuelve `None`, usa el sufijo de id).

Estos métodos devuelven los mismos wrappers (`GuiComponent`, o tipados con `kind`)
que `find_as`, así que una vez localizado el control, todo lo aprendido en los
demos B y C (`.value`, `.press()`, usarlo dentro de un `Step`) aplica igual. La
búsqueda robusta no reemplaza al Process medido: lo **alimenta** cuando el path
falla.

**Qué validas:** `find_by_id_suffix` (con y sin `root`), `find_by_name`,
`find_all_by_name`, y el modo `raise_=False` (devuelve `None`/lista vacía en vez
de excepción) para inspeccionar sin romper.

> Truco: `scripts/buscar_id_parcial.py <sufijo>` hace la búsqueda por sufijo
> contra la sesión abierta sin escribir código.

---

## 10. Problemas y cómo reportarlos

Cuando algo falle, mándame **este bloque** para que lo diagnostique:

1. **Qué paso/demo** ejecutabas (4, 6, 7, 8…).
2. **Comando exacto** que corriste.
3. **Traceback completo** (copia todo el texto rojo de la consola).
4. **El path** involucrado (si aplica).
5. Captura de la pantalla SAP en el momento del fallo (si puedes).

### Síntomas comunes (mira primero aquí)

| Síntoma | Causa probable | Acción |
|---------|----------------|--------|
| `SapNotRunningError` | Scripting deshabilitado o SAP cerrado | Paso 1 |
| `SapLaunchError` (timeout) | `SAP_LOGON_PATH` mal o SAP tarda en abrir | Paso 3; sube el timeout |
| Salta popup "a script is opening a connection" | Notificaciones de scripting activas | Paso 1.5 (desmárcalas) |
| `MissingConfigError` | Falta una variable en `.env` | Paso 3 |
| `SapMessageError [E]` en login | Usuario/mandante/clave inválidos | Paso 3 |
| `ComponentNotFoundError` | Path incorrecto o pantalla distinta | Recaptura el path (paso 5) |
| `ComponentTypeError` | El path es de otro tipo de control | Revisa el path o el `kind` |
| Login OK pero el campo no se llena | Pantalla aún no lista (asíncrono) | Añade `wait_for` al Step |
| `WaitTimeoutError` | La condición no se cumplió a tiempo | Sube `wait_timeout`/revisa la condición |

### Datos útiles para depurar dentro de Python

```python
print(session.info.Transaction)   # transacción actual
print(session.info.User, session.info.Client)
comp = session.find("wnd[0]/usr/ALGUN_PATH")
print(comp.type, comp.id, comp.text)   # qué control es de verdad
```

---

## 11. Checklist de validación del demo

- [ ] Paso 2: `pytest` verde sin SAP.
- [ ] Paso 4: `open_sap.py` deja la sesión lista (login automático).
- [ ] Paso 6: abre transacción y lee estado.
- [ ] Paso 7: escribe en un campo tipado y verifica sin error.
- [ ] Paso 8: Page Object + Process devuelven un `ProcessReport` con `ok=True`.
- [ ] Paso 9: búsqueda por sufijo de id / nombre localiza un control sin path completo.

Cuando completes (o se rompa) cada casilla, me dices cuál y con el bloque del
paso 10 lo ajustamos. Este demo es exploratorio: esperamos encontrar paths que
recapturar y esperas (`wait_for`) que afinar — es justo lo que vamos a aprender.
