from pathlib import Path

import pytest
from rich import print

from latex_task_utils.symbols import read_toml


@pytest.mark.parametrize(
    ("file", "expected"),
    [
        (
            "symbols.toml",
            dict(
                Sym1=dict(code="abc", doc="A symbol."),
                Sym2=dict(code=r"\dot{#1}", doc=None),
                Sym3=dict(code=r"\frac{#1}{#2}", doc="Another symbol."),
            ),
        ),
        (
            "category.toml",
            dict(
                doc="The Root",
                symbols=dict(
                    Sym1=dict(code="abc", doc="A symbol."),
                    Sym2=dict(code=r"\dot{#1}", doc=None),
                ),
                categories=dict(
                    Cat1=dict(
                        doc="SubCat",
                        categories={},
                        symbols=dict(
                            Sym3=dict(code=r"\frac{#1}{#2}", doc="Another symbol."),
                        ),
                    )
                ),
            ),
        ),
    ],
)
def test_read_toml(file, expected):
    result = read_toml(Path(__file__).parent / file)
    print(result)
    assert result.model_dump() == expected
