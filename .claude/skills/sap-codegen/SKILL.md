---
name: sap-codegen
description: Genera y escribe el código Python del proyecto PySap siguiendo POO limpia. Crea wrappers tipados de objetos SAP (Gui*), Steps, Process, mapeos y el generador de código desde el PDF. Úsalo cuando el usuario diga "implementa", "escribe la clase", "genera el wrapper", "crea el proceso", o tras sap-tdd para poner los tests en verde.
---

# sap-codegen

Escribes el código de **PySap**. Objetivo: POO limpia, tipada y mínima para pasar
los tests que sap-tdd ya escribió (rojo → verde → refactor).

## Estándares de código

- **Idioma**: docstrings y comentarios en español; nombres de identificadores en
  inglés cuando reflejen la API SAP (`GuiButton.press`), español en lógica de negocio.
- **Type hints obligatorios** en toda firma pública. `from __future__ import annotations`.
- **Una clase, una responsabilidad.** Wrappers heredan de `GuiComponent`.
- **No romper la escotilla COM**: `GuiComponent.__getattr__` delega al objeto COM;
  no la elimines.
- **Sin lógica en `__init__`** más allá de guardar dependencias.
- **Errores propios** (`pysap.runtime.errors`), nunca `Exception` desnuda al usuario.
- **ruff** limpio (line-length 100).

## Patrón de wrapper de objeto SAP

```python
from __future__ import annotations
from pysap.objects.base import GuiComponent

class GuiX(GuiComponent):
    """GuiX — <descripción>. Ver 'GuiX Object' en el PDF de la API."""

    def metodo(self) -> None:
        self._com.Metodo()

    @property
    def propiedad(self) -> str:
        return self._com.Propiedad
```

## Codegen desde el PDF (Fase 3)

- Fuente: texto extraído del PDF oficial (`sap_gui_scripting_api`).
- `pdf_parser.py`: por cada "GuiX Object" extrae propiedades + métodos + firmas.
- `emitter.py`: emite `pysap/objects/gui_x.py` + `gui_x.pyi`.
- Núcleo v1: GuiApplication, GuiConnection, GuiSession, GuiMainWindow, GuiButton,
  GuiTextField, GuiCTextField, GuiPasswordField, GuiComboBox, GuiCheckBox,
  GuiRadioButton, GuiGridView, GuiTree, GuiStatusbar.
- Regenerable; no editar a mano los archivos generados (marcarlos con cabecera).

## Reglas

- No escribas código sin que exista su test (lo confirma el orquestador).
- Tras escribir, corre `pytest` y reporta verde/rojo.
- Implementa lo mínimo; refactoriza solo con tests en verde.
