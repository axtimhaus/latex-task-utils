"""Module containing utilities for dealing with mathematical symbols."""

import re
from collections.abc import Iterable
from os import PathLike
from pathlib import Path
from typing import Any, Literal, Self, TypeVar

import pydantic
import tomlkit
from jinja2 import PackageLoader, Template

from latex_task_utils.jinja import get_env

RE_ARGUMENT = re.compile(r"#(\d)")
DEFAULT_ARGUMENT_DISPLAY_REPLACEMENT = "\\bullet"
CATEGORY_ORDER: Literal["ltr", "rtl"] = "ltr"


class Symbol(pydantic.BaseModel):
    code: str
    name: str | None = None
    doc: str | None = None

    def code_display(self, replacement=DEFAULT_ARGUMENT_DISPLAY_REPLACEMENT) -> str:
        """Format the `code` for display in the TeX document. The argument sequences are replaced by `replacement`, where the first and only occurrence of `{}` in the replacement text is formatted with the respective parameter index (number after `#`)."""
        return RE_ARGUMENT.sub(lambda m: replacement.format(m.group(1)), self.code)


def format_symbol_key(key: str, category: list[str] = []) -> str:
    """Format the name of the symbol including its category path."""
    if CATEGORY_ORDER == "ltr":
        return "".join(append(category, key))
    if CATEGORY_ORDER == "rtl":
        return "".join(prepend(reversed(category), key))


def create_macro(key: str, symbol: Symbol, category: list[str] = []) -> str:
    """Creates a plain TeX macro using `\\gdef` with the `name` and the `code`. The `code` is automatically scanned for arguments. `\\def` is used in favor of `\\newcommand` because it does not create an implicit group, so subscripts and superscripts work as expected."""
    arguments = RE_ARGUMENT.findall(symbol.code)
    comment = (
        f" % {f'{symbol.name}: {symbol.doc}' if symbol.name else symbol.doc}" if (symbol.name or symbol.doc) else ""
    )
    return (
        rf"\gdef\{format_symbol_key(key, category)}{''.join(f'#{arg}' for arg in arguments)}{{{symbol.code}}}{comment}"
    )


class Category(pydantic.BaseModel):
    name: str | None = None
    doc: str | None = None
    symbols: dict[str, Symbol] = pydantic.Field(default_factory=dict)
    categories: dict[str, Self] = pydantic.Field(default_factory=dict)


Symbols = pydantic.RootModel[dict[str, Symbol]]

_T = TypeVar("_T")


def append(iterable: Iterable[_T], element: _T) -> Iterable[_T]:
    yield from iterable
    yield element


def prepend(iterable: Iterable[_T], element: _T) -> Iterable[_T]:
    yield element
    yield from iterable


def normalize(d: dict[str, Any]) -> dict[str, Any]:
    result = dict()

    for k, v in d.items():
        match v:
            case str() if k in ["name", "doc", "code"]:  # leaf values
                result[k] = v
            case str():  # plain string symbol
                result[k] = dict(
                    code=v,
                )
            case dict():
                result[k] = normalize(v)
            case _:
                raise ValueError(f"Unable to parse: {k} = {repr(v)}")

    print(result)
    return result


def read_toml(file: str | PathLike) -> Symbols | Category:
    """Read symbols from a TOML file where the keys are the symbol names, the string values are the code and optional comments at the end of the line. Tables are supported to create groups of commands. Any other values than strings will raise a `ValueError`."""

    file = Path(file)
    doc = tomlkit.loads(file.read_text())
    normalized = normalize(doc)

    try:
        return Symbols.model_validate(normalized)
    except pydantic.ValidationError as e_symbols:
        try:
            return Category.model_validate(normalized)
        except pydantic.ValidationError as e_category:
            raise ExceptionGroup("Unable to parse data source: ", [e_symbols, e_category]) from None


def _code_for_symbols(symbols, category):
    return "\n".join(create_macro(n, s, category) for n, s in symbols.items())


def _code_for_categories(categories, category):
    return "\n".join(
        _code_for_symbols(c.symbols, [*category, n]) + "\n" + _code_for_categories(c.categories, [*category, n])
        for n, c in categories.items()
    )


def write_symbols_sty(file: Path, symbols: Symbols | Category):
    if isinstance(symbols, Category):
        file.write_text(_code_for_symbols(symbols.symbols, []) + "\n" + _code_for_categories(symbols.categories, []))
    else:
        file.write_text(_code_for_symbols(symbols, []))


_JINJA_ENV = get_env(PackageLoader("latex_task_utils", "symbols_templates"))


class SymbolsIndexTemplates:
    DESCRIPTION: Template = _JINJA_ENV.get_template("description.tex")


HEADING_BY_LEVEL = {
    -1: r"\chapter",
    0: r"\section",
    1: r"\subsection",
    2: r"\subsubsection",
    3: r"\paragraph",
    4: r"\subparagraph",
}


def get_heading_by_level(level: int):
    return HEADING_BY_LEVEL.get(level, r"\textbf")


def write_symbols_index(
    file: Path,
    symbols: Symbols | Category,
    template: Template = SymbolsIndexTemplates.DESCRIPTION,
    toplevel=0,
    heading: str | None = "List of Symbols",
    **kwargs,
):
    if isinstance(symbols, Category):
        rendered = template.render(
            category=symbols,
            heading=heading,
            toplevel=toplevel,
            get_heading_by_level=get_heading_by_level,
            **kwargs,
        )
    else:
        rendered = template.render(
            symbols=symbols,
            heading=heading,
            toplevel=toplevel,
            get_heading_by_level=get_heading_by_level,
            **kwargs,
        )
    file.write_text(rendered)
