from typing import Any

from .display import _display
from .merge import get_info


def defaults(
    *,
    include_dunders: bool = False,
    include_docs: bool = True,
    include_private: bool = False,
    include_signatures: bool = False,
) -> None:
    ppdir.__kwdefaults__ = {
        "include_dunders": include_dunders,
        "include_docs": include_docs,
        "include_private": include_private,
        "include_signatures": include_signatures,
    }


def ppdir(
    inp_cls: Any,
    *,
    include_dunders: bool = False,
    include_docs: bool = True,
    include_private: bool = False,
    include_signatures: bool = False,
) -> None:
    if not isinstance(inp_cls, type):
        inp_cls = inp_cls.__class__
    class_summaries = get_info(inp_cls)
    try:
        _display(
            class_summaries,
            include_dunders=include_dunders,
            include_docs=include_docs,
            include_private=include_private,
            include_signatures=include_signatures,
        )
    except Exception as e:  # noqa: BLE001
        print(f"Error displaying info for {inp_cls}: {e}")
        print(dir(inp_cls))
