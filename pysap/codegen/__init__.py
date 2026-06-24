"""Codegen: parser del PDF de la API SAP + emisor de wrappers tipados.

Implementación en Fase 3 (ver docs/decisions/ADR-0001-stack.md, sección Fases).
El parser leerá el texto extraído del PDF oficial y generará, por cada objeto
``Gui*``, una clase tipada en ``pysap/objects/`` más su stub ``.pyi``.
"""
