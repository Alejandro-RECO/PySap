---
name: sap-commit
description: Genera los commits del proyecto PySap con el formato estándar "Tipo: Descripción" (máximo 20 palabras). Úsalo cuando el usuario diga "commit", "haz un commit", "guarda los cambios", o tras cerrar una tarea con tests en verde.
---

# sap-commit

Generas commits de **PySap**. Formato fijo, definido por el equipo.

## Formato obligatorio

```
Tipo: Descripción
```

- **Una sola línea** de asunto. La descripción NO supera **20 palabras**.
- **Tipo** (en español, primera letra mayúscula):

| Tipo | Uso |
|------|-----|
| `Feat` | Nueva funcionalidad |
| `Fix` | Corrección de bug |
| `Test` | Añade o ajusta tests |
| `Refactor` | Cambio interno sin alterar comportamiento |
| `Doc` | Documentación / ADR / CHANGELOG |
| `Chore` | Tooling, config, dependencias |

- Descripción en **imperativo presente**: "agrega", "corrige", "genera".
- Si el commit cubre un ADR, refiérelo en la descripción: `Doc: ADR-0002 mapeo dinámico de paths`.

## Ejemplos válidos

```
Feat: agrega wrapper tipado GuiButton con método press
Test: cubre Session.find y find_as con sesión mock
Fix: corrige delegación COM en GuiComponent __getattr__
Doc: ADR-0001 registra stack y arquitectura base
```

## Reglas

- **Commit atómico**: un cambio lógico por commit. Si hay varios, divide.
- Antes de commitear: confirma `pytest` en verde y `ruff` limpio.
- No incluyas en el asunto detalles obvios del diff; el "qué" va en el asunto, el
  "por qué" (si no es evidente) en el cuerpo opcional, separado por línea en blanco.
- Verifica `git status`/`git diff` antes de redactar; describe lo que realmente cambió.

## Procedimiento

1. `git status` + `git diff --staged` para ver el cambio real.
2. Redacta `Tipo: Descripción` (≤20 palabras).
3. `git add` de los archivos del cambio lógico.
4. `git commit -m "Tipo: Descripción"`.
