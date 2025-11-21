from pathlib import Path
import latex_task_utils.matplotlib as m
import pytest
import matplotlib.pyplot as plt


@pytest.mark.parametrize("formats", [None, [], ["eps"]])
def test_save(tmp_path, formats):
    main_file = tmp_path / "fig.pdf"
    fig = plt.figure()
    if formats is not None:
        m.save_figure(fig, main_file, formats)
    else:
        m.save_figure(fig, main_file)
    plt.close(fig)

    assert main_file.exists()

    formats = formats if formats is not None else m.DEFAULT_FORMATS

    for f in formats:
        assert main_file.with_suffix(f".{f}").exists()


def test_save_main_without_suffix(tmp_path):
    main_file = tmp_path / "fig"
    fig = plt.figure()
    m.save_figure(fig, main_file)
    plt.close(fig)

    assert not main_file.exists()

    for f in m.DEFAULT_FORMATS:
        assert main_file.with_suffix(f".{f}").exists()
