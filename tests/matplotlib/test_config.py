from pathlib import Path

import numpy as np
from matplotlib import get_backend, rcdefaults, rcParams

import latex_task_utils.matplotlib as m


def test_preamble(tmp_path: Path):
    file = tmp_path / "preamble.tex"
    file.write_text("FOO")
    m.use_preamble(file)
    assert rcParams["pgf.preamble"] == "FOO"
    assert rcParams["text.latex.preamble"] == "FOO"
    rcdefaults()


def test_default_config():
    m.use_default_config()
    assert get_backend() == "pgf"
    assert rcParams["figure.dpi"] > 100
    rcdefaults()


def test_default_figsize():
    m.set_default_figsize_mm(25.4, 25.4)
    assert np.isclose(rcParams["figure.figsize"], [1, 1]).all()
    rcdefaults()
