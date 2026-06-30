# ADR-0006 — Búsqueda robusta de componentes (sufijo de id y nombre)

- **Estado:** Aceptada
- **Fecha:** 2026-06-30
- **Decidido con:** soporte_rpa@netapplications.com.co (vía Claude Code)

## Contexto

`Session.find`/`find_as` localizan un control por su `id`/`path` **exacto**
(`findById`). En SAP real, parte del path es **inestable**: índices de fila en
grids/tablas, subscreens con número variable (`subSUB:SAPLXXXX:0100`), dynpros
que cambian según el flujo. Cuando el prefijo cambia, `findById` rompe con
`ComponentNotFoundError` aunque el control "lógico" siga ahí.

La SAP GUI Scripting API (PDF oficial, `docs/sap_gui_scripting_api.pdf`) ya
ofrece alternativas que no dependen del path completo:

- `FindByName(Name, Type)` → primer descendiente por nombre + tipo.
- `FindAllByName(Name, Type)` → todas las coincidencias (`GuiComponentCollection`).
- `Children` (recorrido del árbol) para estrategias propias.

Existía además un script suelto (`scripts/buscar_id_parcial.py`) con una función
`buscar_por_id_parcial` que recorría `Children` y comparaba por **sufijo de id**.
Lógica útil, pero huérfana del paquete y con `except: pass` (tragaba todo error).

## Decisiones

| # | Tema | Decisión | Alternativas descartadas |
|---|------|----------|--------------------------|
| 1 | Dónde vive | Los nuevos modos de búsqueda van en `Session` (capa baja, escotilla flexible), junto a `find`/`find_as`. | Clase/servicio de búsqueda aparte (sobreingeniería para 3 métodos) |
| 2 | Sufijo de id | `find_by_id_suffix(suffix, *, root=None, raise_=True)`: recorre `Children` en profundidad, devuelve el primer control cuyo `id` termine en `suffix`. Integra y reemplaza a `buscar_por_id_parcial`. | Mantener el script suelto; usar regex sobre el id (innecesario) |
| 3 | Por nombre | `find_by_name(name, sap_type, *, raise_=True)` sobre COM `findByName`; `find_all_by_name(name, sap_type)` sobre `findAllByName` (lista de wrappers, vacía si no hay). | Solo `find_by_name` (sin la variante "todas") |
| 4 | Errores | Reusar `ComponentNotFoundError` con un `path` descriptivo (`*sufijo`, `name=… type=…`). `raise_=False` → `None`, alineado con el patrón de `find`. | Nuevo tipo de error (no aporta; la causa es la misma) |
| 5 | Tragar excepciones | El `except` amplio solo cubre lo inevitable: `findByName` lanza COM si no encuentra (no admite `raise=False`), y un control hoja puede no exponer `Children`. No se silencian otros errores. | `except: pass` global del script original |
| 6 | PageObject | **No** se duplican estos métodos en `PageObject`/`Field`. El Page Object modela path **estable** vía `PathRegistry`; mezclar "cómo buscar" ensucia esa semántica (YAGNI). | Exponer los 3 métodos también en `PageObject` |

## Diseño

- `pysap/runtime/session.py`:
  - `find_by_name(name, sap_type, *, raise_=True)` → `GuiComponent | None`.
  - `find_all_by_name(name, sap_type)` → `list[GuiComponent]`.
  - `find_by_id_suffix(suffix, *, root=None, raise_=True)` → `GuiComponent | None`.
    `root` acepta un wrapper `GuiComponent` o un COM crudo; por defecto, la raíz
    de la sesión. La recursión vive en el helper estático `_search_id_suffix`.
  - Todos devuelven wrappers `GuiComponent` y respetan el contrato de `find`
    (lanzan `ComponentNotFoundError`, o `None` con `raise_=False`).
- `scripts/buscar_id_parcial.py`: reescrito como **demo** que llama a
  `session.find_by_id_suffix(...)`; ya no contiene lógica propia.
- `tests/mocks/fake_sap.py`: el mock se amplía para soportar las nuevas rutas —
  `FakeComponent.Children`/`add_child` (árbol), `FakeChildren.__iter__`,
  `FakeSession.Children`/`findByName`/`findAllByName`.

## Consecuencias

- (+) Las automatizaciones sobreviven a cambios de prefijo de path: el sufijo de
  id o el nombre suelen ser estables aunque el `wnd[0]/usr/...` cambie.
- (+) La función huérfana queda integrada, testeada y con manejo de errores
  honesto (10 tests nuevos; 96 verde).
- (+) `Session` concentra toda la localización de controles; una sola superficie
  que aprender.
- (−) `find_by_name` solo es fiable en objetos de dynpro: la mayoría de controles
  no tiene un `Name` significativo (lo advierte el propio PDF). Para esos,
  `find_by_id_suffix` es la opción robusta.
- (−) `find_by_id_suffix` hace un recorrido en profundidad: en árboles muy
  grandes es más caro que un `findById` directo. Úsalo solo donde el path no sea
  fiable.
- **Pendiente (si aparece el caso):** si un path **mapeado** en el `PathRegistry`
  empieza a romperse a menudo, la evolución limpia no es duplicar métodos en
  `PageObject`, sino enseñar al registry **estrategias de resolución**
  (exacto / sufijo / nombre) en un único punto. Pospuesto por YAGNI.
