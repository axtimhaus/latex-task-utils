import latex_task_utils.jinja
import jinja2
import pytest

TEMPLATES = {
    "block": r"<{ for v in var4 }><<v>><{ endfor }>",
    "comment": r"<% comment %>abc",
    "line comment": "%%% comment\nabc",
    "line statement": ">>> for v in var4\n    <<- v >>\n>>> endfor",
}

EXPECTED = {
    "block": "123",
    "comment": "abc",
    "line comment": "\nabc",
    "line statement": "1\n2\n3\n",
}


@pytest.fixture
def jinja_env():
    return latex_task_utils.jinja.get_env(loader=jinja2.DictLoader(TEMPLATES))


@pytest.mark.parametrize("template", TEMPLATES.keys())
def test_render(template: str, jinja_env: jinja2.Environment):
    result = jinja_env.get_template(template).render(
        var1=42, var2=21, var3="abc", var4=[1, 2, 3]
    )
    print(result)
    assert result == EXPECTED[template]
