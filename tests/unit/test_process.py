"""Tests de Step / Process / telemetría."""

from __future__ import annotations

import pytest

from pysap.objects import GuiButton, GuiTextField
from pysap.process import Process, Step
from pysap.runtime.errors import StepError


def test_process_ejecuta_steps_y_reporta_ok(session):
    proc = Process("demo")
    proc.add(Step("escribir", lambda s: setattr(s.find_as("wnd[0]/usr/txtF1", GuiTextField), "value", "X")))
    proc.add(Step("pulsar", lambda s: s.find_as("wnd[0]/tbar[0]/btn[0]", GuiButton).press()))

    report = proc.run(session)

    assert report.ok is True
    assert len(report.steps) == 2
    assert report.total_duration_s >= 0


def test_step_verify_fallida_marca_error(session):
    proc = Process("demo")
    proc.add(
        Step(
            "verifica_falla",
            action=lambda s: None,
            verify=lambda s: False,
        )
    )
    with pytest.raises(StepError):
        proc.run(session)


def test_process_sin_stop_on_error_continua(session):
    proc = Process("demo")
    proc.add(Step("falla", action=lambda s: (_ for _ in ()).throw(RuntimeError("boom"))))
    proc.add(Step("ok", action=lambda s: None))

    report = proc.run(session, stop_on_error=False)

    assert report.ok is False
    assert len(report.failed) == 1
    assert len(report.steps) == 2
