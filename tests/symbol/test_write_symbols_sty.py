from rich import print

from latex_task_utils.symbols import Symbol, write_symbols_sty

SYMBOLS = [
    Symbol(name="Sym1", code="ABC", comment=None),
    Symbol(name="Sym2", code=r"\dot{\Sym1}", comment=None),
    Symbol(name="Sym3", code="def", comment="after"),
    Symbol(name="Sym4", code=r"\dot{#1}", comment=None),
    Symbol(name="Sym1", code="ABCD", category=["Group1"], comment="com2"),
    Symbol(name="Sym1", code="ABCDE", category=["Group1", "Sub"], comment=None),
]

EXPECTED = r"""
\gdef\Sym1{ABC}
\gdef\Sym2{\dot{\Sym1}}
\gdef\Sym3{def} % after
\gdef\Sym4#1{\dot{#1}}
\gdef\Group1Sym1{ABCD} % com2
\gdef\Group1SubSym1{ABCDE}
""".strip()


def test_read_toml(tmp_path):
    file = tmp_path / "symbols.sty"
    write_symbols_sty(file, SYMBOLS)
    result = file.read_text().strip()
    print(result)
    assert result == EXPECTED
