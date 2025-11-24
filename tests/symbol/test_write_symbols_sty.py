from rich import print

from latex_task_utils.symbols import Category, Symbol, write_symbols_sty

SYMBOLS = {
    "symbols": {
        "Sym1": Symbol(code="ABC", doc=None),
        "Sym2": Symbol(code=r"\dot{\Sym1}", doc=None),
        "Sym3": Symbol(code="def", doc="after"),
        "Sym4": Symbol(code=r"\dot{#1}", doc=None),
    },
    "categories": {
        "Group1": {
            "symbols": {
                "Sym1": Symbol(code="ABCD", doc="com2"),
            },
            "categories": {
                "Sub": {
                    "symbols": {
                        "Sym1": Symbol(code="ABCDE", doc=None),
                    }
                }
            },
        },
    },
}

EXPECTED = r"""
\gdef\Sym1{ABC}
\gdef\Sym2{\dot{\Sym1}}
\gdef\Sym3{def} % after
\gdef\Sym4#1{\dot{#1}}
\gdef\Group1Sym1{ABCD} % com2
\gdef\Group1SubSym1{ABCDE}
""".strip()


def test_write_symbols_sty(tmp_path):
    file = tmp_path / "symbols.sty"
    write_symbols_sty(file, Category.model_validate(SYMBOLS))
    result = file.read_text().strip()
    print(result)
    assert result == EXPECTED
