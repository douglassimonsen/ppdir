from typing import Any

from .display import _display
from .merge import get_info


def defaults(
    *,
    include_dunders: bool | None = None,
    include_docs: bool | None = None,
    include_signatures: bool | None = None,
) -> None:
    ppdir.__kwdefaults__ = {
        "include_dunders": include_dunders,
        "include_docs": include_docs,
        "include_signatures": include_signatures,
    }


def ppdir(
    inp_cls: Any,
    *,
    include_dunders: bool = False,
    include_docs: bool = False,
    include_signatures: bool = False,
) -> None:
    if not isinstance(inp_cls, type):
        inp_cls = inp_cls.__class__
    class_summaries = get_info(inp_cls)
    _display(
        class_summaries,
        include_dunders=include_dunders,
        include_docs=include_docs,
        include_signatures=include_signatures,
    )
    try:
        _display(
            class_summaries,
            include_dunders=include_dunders,
            include_docs=include_docs,
            include_signatures=include_signatures,
        )
    except:  # noqa: E722
        print(dir(inp_cls))
