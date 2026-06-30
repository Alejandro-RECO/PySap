# ADR-0007 — Credenciales de SapConfig desde una clase Settings

- **Estado:** Aceptada
- **Fecha:** 2026-06-30
- **Decidido con:** soporte_rpa@netapplications.com.co (vía Claude Code)

## Contexto

`SapConfig` (`pysap/config.py`) hoy solo se construye con `from_env()`: lee las
variables `SAP_*` del entorno y, opcionalmente, de un `.env` (ADR-0003). Los
proyectos que **consumen** PySap suelen tener ya su propia capa de configuración
—una clase `Settings` de **pydantic `BaseSettings`**— con todas las variables
definidas y validadas. Obligarlos a exportar al entorno o a copiar valores a mano
para alimentar `SapConfig` duplica la fuente de verdad.

Se necesita una vía para construir `SapConfig` **directamente desde ese objeto de
settings**, sin acoplar PySap a pydantic ni a una convención de nombres concreta.

## Decisiones

| # | Tema | Decisión | Alternativas descartadas |
|---|------|----------|--------------------------|
| 1 | API | Nuevo classmethod `SapConfig.from_settings(settings, *, mapping=None)`, junto a `from_env`. Una responsabilidad por método, sin tocar la fuente existente. | Extender `from_env` para aceptar también un objeto (mezcla fuentes); función suelta fuera de la dataclass |
| 2 | Acoplamiento | **Duck typing**: se leen los valores con `getattr(settings, attr)`. Funciona con pydantic v1/v2 y con cualquier objeto. **No** se añade pydantic como dependencia (ADR-0001: solo `pywin32`). | Importar `pydantic`/`BaseSettings` y tipar el parámetro (acopla y suma dependencia) |
| 3 | Mapeo de nombres | `mapping` configurable `{campo_SapConfig: atributo_en_settings}`. Por defecto `_SETTINGS_MAP` con convención `sap_*` snake_case (la típica de `BaseSettings` que deriva de `SAP_*`). | Nombres fijos no configurables (rompe si el consumidor usa otros) |
| 4 | Validación / error | Reusar `MissingConfigError`, reportando el **nombre del atributo** ausente en `Settings`. Mismas obligatorias que `from_env`. | Nuevo tipo de error (misma causa: falta config) |
| 5 | Normalización | `str(valor)` sobre cada valor leído: pydantic puede entregar `SecretStr`, `int`, etc.; `SapConfig` trabaja con `str`. | Asumir que ya son `str` (rompe con tipos pydantic) |

## Diseño

- `pysap/config.py`:
  - `_SETTINGS_MAP = {"connection": "sap_connection", "client": "sap_client",
    "user": "sap_user", "password": "sap_password", "language": "sap_lang",
    "logon_path": "sap_logon_path"}`.
  - Listas de campos derivadas de los mapeos ya existentes (sin duplicar):
    `_CAMPOS_OBLIGATORIOS = tuple(_OBLIGATORIAS.values())`,
    `_CAMPOS_OPCIONALES = tuple(_OPCIONALES.values())`.
  - `from_settings(settings, *, mapping=None)`: lee por atributo según el mapeo,
    ignora ausentes/vacíos, valida obligatorias (`MissingConfigError`) y devuelve
    la dataclass. Los opcionales ausentes quedan `""` como en `from_env`.

## Consecuencias

- (+) El consumidor alimenta `SapConfig` desde su `Settings` con una sola llamada;
  una única fuente de verdad de la config.
- (+) PySap sigue sin depender de pydantic; `from_settings` es testeable con un
  objeto cualquiera (duck typing).
- (+) El mapeo configurable absorbe convenciones de nombres distintas sin tocar
  el código.
- (−) El default asume `sap_*`; con otros nombres hay que pasar `mapping`
  explícito (queda documentado).
- (−) La lectura por `getattr` no valida tipos: confía en que el consumidor (su
  `Settings`) ya validó; PySap solo normaliza a `str`.
