# Demo paso a paso — probar PySap en SAP real

> Guía operativa para validar lo construido (Fases 1–5) contra una sesión SAP
> real. No es código de producción: son los pasos que **tú** ejecutas. Si algo
> falla, ve a la sección [9. Problemas](#9-problemas-y-como-reportarlos) y me
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

Esperado: `86 passed, 1 deselected`. Si falla aquí, **párate** y repórtalo
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

Abre una consola Python con la sesión ya lista. Crea un archivo temporal
`demo_a.py` en la raíz y pega esto, **ajustando la transacción**:

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

**Qué validas:** `start_session`, `start_transaction`, `status`, manejo de popups.

---

## 7. Demo B — wrapper tipado + verificación

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

**Qué validas:** `find_as` con `validate=True` (Fase 4), wrappers generados
(Fase 3), `send_vkey`, `raise_on_error`.

Si `validate=True` lanza `ComponentTypeError`, el path apunta a otro tipo de
control: revisa el path o quita `validate` para inspeccionar `comp.type`.

---

## 8. Demo C — Page Object + Process medido

El patrón recomendado para algo repetible. Crea `demo_c.py`:

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

**Qué validas:** todo junto — registry, Page Object, `Field`, `Process`/`Step`
con reintentos y verificación, telemetría (`ProcessReport`).

---

## 9. Problemas y cómo reportarlos

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

## 10. Checklist de validación del demo

- [ ] Paso 2: `pytest` verde sin SAP.
- [ ] Paso 4: `open_sap.py` deja la sesión lista (login automático).
- [ ] Paso 6: abre transacción y lee estado.
- [ ] Paso 7: escribe en un campo tipado y verifica sin error.
- [ ] Paso 8: Page Object + Process devuelven un `ProcessReport` con `ok=True`.

Cuando completes (o se rompa) cada casilla, me dices cuál y con el bloque del
paso 9 lo ajustamos. Este demo es exploratorio: esperamos encontrar paths que
recapturar y esperas (`wait_for`) que afinar — es justo lo que vamos a aprender.
