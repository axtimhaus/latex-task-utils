from latex_task_utils.symbols import Symbol
import pytest
from rich import print


@pytest.mark.parametrize(
    ("code", "replacement", "expected"),
    [
        ("abc", "", "abc"),
        ("a#1bc", "", "abc"),
        ("a#1bc", "*", "a*bc"),
        ("a#1b#2c", "", "abc"),
        ("a#1b#2c", "*", "a*b*c"),
        ("a#1b#2c", "*{}*", "a*1*b*2*c"),
    ],
)
def test_code_display_default(code, replacement, expected):
    s = Symbol(name="test", code=code)
    result = s.code_display(replacement)
    print(result)
    assert result == expected
