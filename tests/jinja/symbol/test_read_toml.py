from pathlib import Path
from latex_task_utils.symbols import Symbol, read_toml


def test_read_toml():
    result = read_toml(Path(__file__).parent / "symbols.toml")
    print(result)
    assert result == [
        Symbol(name="Sym1", code="ABC", comment=None),
        Symbol(name="Sym2", code=r"\dot{\Sym1}", comment=None),
        Symbol(name="Sym3", code="def", comment="after"),
        Symbol(name="Sym4", code=r"\dot{#1}", comment=None),
    ]
