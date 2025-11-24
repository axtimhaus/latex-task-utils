import pytest
from rich import print

from latex_task_utils.symbols import Category, Symbol, Symbols, write_symbols_index


@pytest.mark.parametrize(
    "input",
    [
        Symbols(
            dict(
                Sym1=Symbol(code="abc", doc="A symbol."),
                Sym2=Symbol(code=r"\dot{#1}"),
                Sym3=Symbol(code=r"\frac{#1}{#2}", doc="Another symbol.", name="Symbol 3"),
            )
        ),
        Category(
            name=None,
            doc="The Root",
            symbols=dict(
                Sym1=Symbol(code="abc", doc="A symbol."),
                Sym2=Symbol(code=r"\dot{#1}"),
            ),
            categories=dict(
                Cat1=Category(
                    name="Category 1",
                    doc="SubCat",
                    categories={},
                    symbols=dict(
                        Sym3=Symbol(code=r"\frac{#1}{#2}", doc="Another symbol.", name="Symbol 3"),
                    ),
                )
            ),
        ),
    ],
)
def test_write_symbols_index(tmp_path, input):
    file = tmp_path / "symbols.sty"
    print(file.as_uri())
    write_symbols_index(file, input)
    result = file.read_text().strip()
    print(result)
