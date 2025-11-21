import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Self

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pytask
from matplotlib.figure import Figure

__all__ = [
    "Figure",
    "use_preamble",
    "set_default_figsize_mm",
    "mm_to_inch",
    "DEFAULT_FIGSIZE_MM",
    "DEFAULT_CONFIG",
    "use_default_config",
    "set_default_figsize_mm",
]


def use_preamble(path: Path):
    """Use the LaTeX preamble file located at `path` when generating plots with the PGF backend and LaTeX text."""
    preamble = path.read_text()
    matplotlib.rcParams.update({"pgf.preamble": preamble, "text.latex.preamble": preamble})


def mm_to_inch(v):
    """Convert mm to inch (vectorized)."""
    return np.asarray(v) / 25.4


DEFAULT_FIGSIZE_MM = [160, 120]
"""Default figure size in mm suitable for A4 paper."""
DEFAULT_CONFIG = {
    "pgf.texsystem": "lualatex",
    "pgf.rcfonts": False,
    "figure.constrained_layout.use": True,
    "figure.dpi": 600,
    "figure.figsize": mm_to_inch(DEFAULT_FIGSIZE_MM),
    "lines.linewidth": 1,
    "patch.linewidth": 1,
    "contour.linewidth": 1,
    "savefig.transparent": True,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "font.size": 8,
    "grid.linewidth": 0.5,
}
"""Default config of matplotlib for generating LaTeX compatible plots."""


def use_default_config(overrides: dict[str, Any] = dict()):
    """Apply the default config with optional overrides. Sets the backend to `pgf`."""
    matplotlib.use("pgf")
    matplotlib.rcParams.update(DEFAULT_CONFIG | overrides)


def set_default_figsize_mm(width_mm, height_mm):
    """Sets the default figsize in mm."""
    matplotlib.rcParams.update({"figure.figsize": mm_to_inch([width_mm, height_mm])})


DEFAULT_FORMATS = {"pdf", "png"}
"""Set of default formats to save figures in when using `FigureNode`."""


def save_figure(figure: Figure, path: Path, additional_formats: set[str] = DEFAULT_FORMATS):
    """Save a figure to a main file and some additional formats."""
    for p in (path.with_suffix(f".{s}") for s in set([path.suffix[1:], *additional_formats]) if s):
        print(p)
        figure.savefig(p)


try:
    import pytask

    @dataclass
    class FigureNode:
        """A `pytask` Node for saving `matplotlib` Figures to multiple formats. Give the main format as the path with the respective extensions and additional formats via the `additional_formats` field."""

        path: Path
        """The main file path."""
        name: str = ""
        """The name of the node."""
        additional_formats: set[str] = field(default_factory=lambda: set(DEFAULT_FORMATS))
        """Additional formats for saving figures, defaults to `DEFAULT_FORMATS`."""

        @property
        def signature(self) -> str:
            raw_key = str(pytask.hash_value(self.path))
            return hashlib.sha256(raw_key.encode()).hexdigest()

        @classmethod
        def from_path(cls, path: Path) -> Self:
            return cls(name=path.as_posix(), path=path)

        def state(self) -> str | None:
            return pytask.get_state_of_path(self.path)

        def load(self, is_product: bool = False) -> Path:
            return self.path

        def save(self, value: Figure) -> None:
            if isinstance(value, Figure):
                save_figure(value, self.path, self.additional_formats)
                plt.close(value)
            else:
                raise TypeError(f"'FigureNode' can only save 'plt.Figure', not {type(value)}")

    __all__ += ["FigureNode"]

except ImportError:
    pass
