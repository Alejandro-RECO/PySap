# ADR-0002 — Estabilidad, conexión y feedback de SAP

- **Estado:** Aceptada
- **Fecha:** 2026-06-24
- **Decidido con:** soporte_rpa@netapplications.com.co (vía Claude Code)

## Contexto

Revisión de la Fase 1 detectó puntos de fuga para el objetivo "estable":
SAP responde de forma asíncrona, lanza ventanas modales (`wnd[1]`) y reporta
resultados por la barra de estado (`sbar`). El runtime solo se enganchaba a una
sesión existente. PySap es un **paquete/demostración** del funcionamiento, no un
proceso de negocio concreto.

## Decisiones

| # | Tema | Decisión |
|---|------|----------|
| 1 | Estabilidad | **Wait + retry por Step**: espera a una condición (pantalla lista) con timeout, y reintenta la acción N veces con retardo. `sleep`/`clock` inyectables para tests. |
| 2 | Conexión | **Soportar ambos**: engancharse a una sesión abierta (`connect`) y abrir conexión + login por código (`open_connection`, `Session.login`). |
| 3 | Feedback | **Helper completo**: lectura de la barra de estado (tipos S/W/E/A/I), detección de errores y manejo de popups (`has_popup`, `confirm_popup`, `cancel_popup`). |
| 4 | Alcance | La demo end-to-end es **genérica** (ilustra el paquete), no un proceso real. |

## Diseño

- `process/step.py`: `Step` gana `retries`, `retry_delay`, `wait_for`,
  `wait_timeout`, `wait_poll`. `run(session, *, sleep, clock)` con dependencias
  inyectables (tests sin esperas reales).
- `runtime/connector.py`: `open_connection(descripcion, *, application)`.
- `runtime/session.py`: `login(...)`, `status()`, `raise_on_error()`,
  `has_popup()`, `confirm_popup()`, `cancel_popup()`, `send_vkey()`.
- `runtime/feedback.py`: dataclass `Status` (type, text) + clasificación.
- `runtime/errors.py`: `SapMessageError`, `WaitTimeoutError`.
- Mock `fake_sap.py`: soporta `MessageType` en statusbar y ventanas `wnd[1]`.

## Consecuencias

- (+) "reintentable" y "estable" pasan a ser ciertos (antes solo declarado).
- (+) Tests deterministas: sin `sleep` real ni reloj de pared.
- (−) Más superficie de API que mantener y documentar.
- (−) `login` por código maneja credenciales: responsabilidad del usuario no
  versionarlas (se pasan como argumentos, nunca hardcodeadas).
