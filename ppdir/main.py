from typing import Any

from .display import _display
from .merge import get_info

INCLUDE_DUNDERS = False
INCLUDE_DOCS = True
INCLUDE_SIGNATURES = False


def defaults(
    *,
    include_dunders: bool | None = None,
    include_docs: bool | None = None,
    include_signatures: bool | None = None,
) -> None:
    global INCLUDE_DUNDERS, INCLUDE_DOCS, INCLUDE_SIGNATURES  # noqa: PLW0603
    INCLUDE_DUNDERS = include_dunders if include_dunders is not None else INCLUDE_DUNDERS
    INCLUDE_DOCS = include_docs if include_docs is not None else INCLUDE_DOCS
    INCLUDE_SIGNATURES = include_signatures if include_signatures is not None else INCLUDE_SIGNATURES


def ppdir(
    inp_cls: Any,
    *,
    include_dunders: bool | None = None,
    include_docs: bool | None = None,
    include_signatures: bool | None = None,
) -> None:
    include_dunders = include_dunders if include_dunders is not None else INCLUDE_DUNDERS
    include_docs = include_docs if include_docs is not None else INCLUDE_DOCS
    include_signatures = include_signatures if include_signatures is not None else INCLUDE_SIGNATURES
    if not isinstance(inp_cls, type):
        inp_cls = inp_cls.__class__
    class_summaries = get_info(inp_cls)
    _display(
        class_summaries,
        include_dunders=include_dunders,
        include_docs=include_docs,
        include_signatures=include_signatures,
    )
