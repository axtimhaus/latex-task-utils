from pathlib import Path

from rich import print

from latex_task_utils.symbols import Symbol, read_toml


def test_read_toml():
    result = read_toml(Path(__file__).parent / "symbols.toml")
    print(result)
    assert result == [
        Symbol(name="Sym1", code="ABC", doc=None),
        Symbol(name="Sym2", code=r"\dot{\Sym1}", doc=None),
        Symbol(name="Sym3", code="def", doc=None),
        Symbol(name="Sym4", code=r"\dot{#1}", doc=None),
        Symbol(name="Sym5", code="def", doc="This is the docstring of the symbol."),
        Symbol(name="Sym6", code=r"\dot{#1}", doc="This is the docstring of the symbol."),
        Symbol(name="Sym1", code="ABCD", category=["Group1"], doc=None),
        Symbol(name="Sym1", code="ABCDE", category=["Group1", "Sub"], doc="This is the docstring of the symbol."),
    ]
