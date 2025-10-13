from latex_task_utils.symbols import Symbol
import pytest


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
def test_code_display_default(code, args):
    s = Symbol(name="test", code=code)
    result = s.create_macro()
    print(result)
    assert result == rf"\gdef\test{args}{{{code}}}"
