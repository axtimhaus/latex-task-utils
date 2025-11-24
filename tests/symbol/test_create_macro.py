import pytest
from rich import print

import latex_task_utils.symbols as symbols


@pytest.mark.parametrize(
    ("code", "args"),
    [
        ("abc", ""),
        ("a#1bc", "#1"),
        ("a#1bc", "#1"),
        ("a#1b#2c", "#1#2"),
        ("a#1b#2c", "#1#2"),
        ("a#1b#2c", "#1#2"),
    ],
)
def test_create_macro_top_level(code, args):
    s = symbols.Symbol(code=code)
    result = symbols.create_macro("test", s)
    print(result)
    assert result == rf"\gdef\test{args}{{{code}}}"


@pytest.mark.parametrize(
    ("order", "expected_name"),
    [
        (None, "topsubtest"),
        ("ltr", "topsubtest"),
        ("rtl", "testsubtop"),
    ],
)
def test_create_macro_groups(order, expected_name, monkeypatch):
    if order:
        monkeypatch.setattr(symbols, "CATEGORY_ORDER", order)
    s = symbols.Symbol(code="code")
    result = symbols.create_macro("test", s, ["top", "sub"])
    print(result)
    assert result == rf"\gdef\{expected_name}{{code}}"
