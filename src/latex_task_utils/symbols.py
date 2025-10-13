"""Module containing utilities for dealing with mathematical symbols."""

import re
from os import PathLike
from pathlib import Path
from dataclasses import dataclass

RE_ARGUMENT = re.compile(r"#(\d)")
DEFAULT_ARGUMENT_DISPLAY_REPLACEMENT = "\\bullet"


@dataclass
class Symbol:
    """Dataclass representing a TeX Math Symbol with a macro `name`, a replacement `code` and an optional `comment`."""

    name: str
    code: str
    comment: str | None = None

    def code_display(self, replacement=DEFAULT_ARGUMENT_DISPLAY_REPLACEMENT) -> str:
        """Format the `code` for display in the TeX document. The argument sequences are replaced by `replacement`, where the first and only occurrence of `{}` in the replacement text is formatted with the respective parameter index (number after `#`)."""
        return RE_ARGUMENT.sub(lambda m: replacement.format(m.group(1)), self.code)

    def create_macro(self) -> str:
        """Creates a plain TeX macro using `\\gdef` with the `name` and the `code`. The `code` is automatically scanned for arguments. `\\def` is used in favor of `\\newcommand` because it does not create an implicit group, so subscripts and superscripts work as expected."""
        if "#" in self.code:
            arguments = RE_ARGUMENT.findall(self.code)
            return rf"\gdef\{self.name}{''.join(f'#{arg}' for arg in arguments)}{{{self.code}}}"
        else:
            return rf"\gdef\{self.name}{{{self.code}}}"


def read_toml(file: str | PathLike) -> list[Symbol]:
    """Read symbols from a TOML file where the keys are the symbol names, the string values are the code and optional comments at the end of the line."""
    import tomlkit

    file = Path(file)
    data = tomlkit.loads(file.read_text())

    def get_comment(key: str) -> str | None:
        c = data.item(key).trivia.comment

        if not c:
            return None

        return c.strip(" #")

    return [Symbol(name=k, code=v, comment=get_comment(k)) for k, v in data.items()]
