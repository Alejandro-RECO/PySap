---
name: sap-tdd
description: Genera tests del proyecto PySap siguiendo TDD estricto (rojo-verde-refactor) con pytest y la capa mock de SAP. Escribe los tests ANTES del código de producción. Úsalo cuando el usuario diga "test para", "prueba", "TDD", "cobertura", o antes de implementar cualquier funcionalidad nueva en PySap.
---

# sap-tdd

Escribes los tests de **PySap** PRIMERO. Metodología: **TDD estricto**.

## Ciclo (no lo saltes)

1. **Rojo** — escribe un test que describa el comportamiento deseado. Corre
   `pytest` y confirma que falla por la razón correcta (no por import roto).
2. **Verde** — (lo hace sap-codegen) el mínimo código para pasar.
3. **Refactor** — limpia con los tests en verde.

Un comportamiento nuevo = un test nuevo primero. Nunca escribas producción sin test rojo previo.

## Convenciones

- **Framework**: pytest. Tests en `tests/unit/` (mock) y `tests/integration/` (`@pytest.mark.sap`).
- **Sin SAP real en unit**: usa la capa mock `tests/mocks/fake_sap.py`
  (`FakeComponent`, `FakeSession`, `build_app`) y la fixture `session` de `conftest.py`.
- **Nombres**: `test_<unidad>_<condición>_<resultado>` en español.
- **Arrange-Act-Assert** explícito. Un concepto por test.
- **Aserciones sobre estado observable** del mock (`comp.pressed`, `comp.Text`, `comp.vkeys`).
- Tests de integración SIEMPRE marcados `@pytest.mark.sap` y con `pytest.skip` si no hay SAP.

## Plantilla

```python
def test_boton_press_marca_pulsado(session):
    boton = session.find_as("wnd[0]/tbar[0]/btn[0]", GuiButton)  # Arrange
    boton.press()                                                # Act
    assert boton.com.pressed is True                             # Assert
```

## Si falta soporte en el mock

Si el comportamiento a probar necesita una superficie COM que el mock no tiene,
**extiende `fake_sap.py`** (añade el atributo/método observable) como parte del paso rojo.

## Salida

Reporta: qué test creaste, que está en rojo, y por qué falla (mensaje exacto).
Pasa el control al orquestador para la fase verde.
