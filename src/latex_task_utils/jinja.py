"""Module containing configuration for Jinja adapted to LaTeX needs."""

import jinja2
from typing import Any

__all__ = ["ENVIRONMENT_CONFIG", "get_env"]

ENVIRONMENT_CONFIG: dict[str, Any] = dict(
    block_start_string="<{",
    block_end_string="}>",
    variable_start_string="<<",
    variable_end_string=">>",
    comment_start_string="<%",
    comment_end_string="%>",
    line_statement_prefix=">>>",
    line_comment_prefix="%%%",
)
"""Default Jinja environment options adapted to LaTeX needs.
Sets variable markup to `<< ... >>`, block markup to `<{ ... }>` and comment markup to `<% ... %>`.
Also enable line statements with `>>> ...` and line comments with `%%% ...`.
For comments it is recommended to use the line comment syntax as LaTeX only knows line comments, so end of usual comment syntax would not be recognized by LaTeX lexers.
"""


def get_env(loader: jinja2.BaseLoader, **kwargs: Any) -> jinja2.Environment:
    """Create a Jinja environment with `ENVIRONMENT_CONFIG` as default config and the given loader. Additional `kwargs` are merged with the default config and forwarded to `jinja2.Environment()`. Result value is cached using `@lru_cache`."""
    return jinja2.Environment(loader=loader, **(ENVIRONMENT_CONFIG | kwargs))
