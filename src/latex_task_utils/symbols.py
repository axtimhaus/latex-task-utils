"""Module containing utilities for dealing with mathematical symbols."""

import re
from collections.abc import Generator, Iterable
from dataclasses import dataclass, field
from os import PathLike
from pathlib import Path
from typing import Any, Literal, TypeVar

import tomlkit

RE_ARGUMENT = re.compile(r"#(\d)")
DEFAULT_ARGUMENT_DISPLAY_REPLACEMENT = "\\bullet"
CATEGORY_ORDER: Literal["ltr", "rtl"] = "ltr"


@dataclass
class Symbol:
    """Dataclass representing a TeX Math Symbol with a macro `name`, a replacement `code` and an optional `comment`."""

    name: str
    code: str
    category: list[str] = field(default_factory=list)
    doc: str | None = None

    def code_display(self, replacement=DEFAULT_ARGUMENT_DISPLAY_REPLACEMENT) -> str:
        """Format the `code` for display in the TeX document. The argument sequences are replaced by `replacement`, where the first and only occurrence of `{}` in the replacement text is formatted with the respective parameter index (number after `#`)."""
        return RE_ARGUMENT.sub(lambda m: replacement.format(m.group(1)), self.code)

    def format_name_with_category(self) -> str:
        if CATEGORY_ORDER == "ltr":
            return "".join(append(self.category, self.name))
        if CATEGORY_ORDER == "rtl":
            return "".join(prepend(reversed(self.category), self.name))

    def create_macro(self) -> str:
        """Creates a plain TeX macro using `\\gdef` with the `name` and the `code`. The `code` is automatically scanned for arguments. `\\def` is used in favor of `\\newcommand` because it does not create an implicit group, so subscripts and superscripts work as expected."""
        arguments = RE_ARGUMENT.findall(self.code)
        return rf"\gdef\{self.format_name_with_category()}{''.join(f'#{arg}' for arg in arguments)}{{{self.code}}}{f' % {self.doc}' if self.doc else ''}"


_T = TypeVar("_T")


def append(iterable: Iterable[_T], element: _T) -> Iterable[_T]:
    yield from iterable
    yield element


def prepend(iterable: Iterable[_T], element: _T) -> Iterable[_T]:
    yield element
    yield from iterable


def parse_dict(d: dict[str, Any], category=[]) -> Generator[Symbol, None, None]:
    for k, v in d.items():
        match v:
            case str():
                yield Symbol(
                    name=k,
                    code=v,
                    category=category,
                )
            case dict() if "code" in v:
                yield Symbol(
                    name=k,
                    code=v["code"],
                    category=category,
                    doc=v.get("doc", None),
                )
            case dict():
                yield from parse_dict(v, category=category + [k])
            case _:
                raise ValueError(f"Unsupported value type: {type(v)}")


def _parse_toml(item) -> dict[str, Any]:
    def gen():
        for k, v in item.items():
            match v:
                case str() if k not in ["code", "comment"] and v.trivia.comment:  # type: ignore
                    yield k, dict(code=v.unwrap(), comment=v.trivia.comment.strip(" #"))  # type: ignore
                case str():
                    yield k, v.unwrap()  # type: ignore
                case dict():
                    yield k, _parse_toml(v)

    return dict(gen())


def read_toml(file: str | PathLike) -> list[Symbol]:
    """Read symbols from a TOML file where the keys are the symbol names, the string values are the code and optional comments at the end of the line. Tables are supported to create groups of commands. Any other values than strings will raise a `ValueError`."""

    file = Path(file)
    doc = tomlkit.loads(file.read_text())
    return list(parse_dict(_parse_toml(doc)))


def write_symbols_sty(file: Path, symbols: list[Symbol]):
    file.write_text("\n".join(s.create_macro() for s in symbols))
