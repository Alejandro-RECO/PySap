# ADR-0004 — Codegen: wrappers tipados desde el PDF de la API

- **Estado:** Aceptada
- **Fecha:** 2026-06-26
- **Decidido con:** soporte_rpa@netapplications.com.co (vía Claude Code)

## Contexto

ADR-0001 (#2, Fase 3) decidió generar wrappers tipados `Gui*` + `.pyi` desde el
PDF oficial (`docs/sap_gui_scripting_api.pdf`, 322 páginas) para tener
autocompletado real. Hasta ahora solo existían dos wrappers escritos a mano
(`GuiButton`, `GuiTextField`) como muestra. Falta el generador.

El texto extraído del PDF es **ruidoso**: columnas aplanadas, guiones suaves
(`­`), glifos privados, mayúsculas espaciadas (`T ype`, `T ext`) y listas de
miembros heredados mezcladas con declaraciones propias. Hay que decidir cómo
parsear esto de forma robusta y testeable.

Estructura observada por objeto en el texto:

```
GuiX Object
Description
<texto> ... GuiX extends the GuiY Object [page N]. The type prefix is <p>, ...
Methods
  All methods of the GuiZ Object [page N]:   ← heredados (bullets •)
  • SetFocus
  Press   This emulates ...                  ← propio
  Public Function GetLineText( _  ByVal Line As Long _ ) As String
Properties
  All properties of the GuiComponent Object: ← heredados (bullets •)
  • Id  • Name  • Type
  Emphasized (Read-only)
  Public Property Emphasized As Byte          ← propio
```

## Decisiones

| # | Tema | Decisión | Alternativas descartadas |
|---|------|----------|--------------------------|
| 1 | Extracción | **`pypdf`** extrae el texto en un módulo fino aislado (`text_extract.py`). El parser trabaja sobre **texto**, no sobre el PDF. | `pdfplumber`/`pymupdf` (dep más pesada); parsear el binario en el parser (intestable) |
| 2 | Parsing | **Regex sobre declaraciones explícitas** `Public Property/Function/Sub`. Solo se emiten **miembros propios**; los heredados (bullets `•`) los cubre la herencia/`__getattr__`. | Parsear los bullets (nombres corruptos `T ype`); IA/LLM en runtime |
| 3 | Tipos | **Mapa VB→Python** (`typemap.py`): `String→str`, `Long/Integer/Short→int`, `Byte/Boolean→bool`, `Double/Single→float`, `Gui*`/`Variant`/`Object`→`Any`. | Inferencia; todo `Any` |
| 4 | Nombres | COM PascalCase → API `snake_case` (`LeftLabel`→`left_label`, `Press`→`press`), igual que los wrappers a mano. | Mantener PascalCase |
| 5 | Herencia | Todos los wrappers generados heredan de **`GuiComponent`** (base con delegación COM). No se replica la jerarquía SAP completa en v1. | Cadena de herencia SAP completa (objetos fuera del core 14) |
| 6 | Salida | Por objeto: `pysap/objects/gui_x.py` + `gui_x.pyi`, con **cabecera "GENERADO — NO EDITAR"**. Regenerable. | Un solo módulo gigante; editar a mano |
| 7 | Núcleo v1 | Los **14 objetos** del ADR-0001/skill `sap-codegen`. | Los 80+ objetos del PDF |

## Diseño

- `pysap/codegen/text_extract.py`: `extract_pdf_text(path) -> str` (usa `pypdf`).
- `pysap/codegen/normalize.py`: `normalize(text)` quita guiones suaves, glifos
  privados y normaliza espacios. Función pura, testeable.
- `pysap/codegen/typemap.py`: `vb_to_python(vb_type) -> str`.
- `pysap/codegen/pdf_parser.py`: dataclasses `Param`, `MethodSpec`,
  `PropertySpec`, `ObjectSpec`; `parse_object(text, name)` y `parse_all(text)`.
- `pysap/codegen/emitter.py`: `emit_module(spec) -> str`, `emit_stub(spec) -> str`,
  `snake_case(name)`.
- `pysap/codegen/generate.py`: driver `generate(pdf_path, out_dir, objetos)` que
  encadena extraer → parsear → filtrar core → emitir → escribir. CLI ejecutable.
- `requirements-dev.txt`: añade `pypdf` (solo para regenerar; no es dep runtime).

## Consecuencias

- (+) Autocompletado y `.pyi` para los 14 objetos núcleo sin escribirlos a mano.
- (+) Regenerable: si SAP publica un PDF nuevo, se vuelve a correr.
- (+) Parser testeable con fragmentos de texto limpios (TDD sin el PDF real).
- (−) Solo miembros propios; los heredados funcionan por delegación COM pero sin
  tipado estático (limitación aceptada en v1, ampliable con la jerarquía).
- (−) El parser depende del formato del PDF (v7.70 PL08); cambios de layout
  pueden requerir ajustar los regex.
- (−) `pypdf` es dependencia de desarrollo (no de runtime): regenerar requiere
  instalarla.
