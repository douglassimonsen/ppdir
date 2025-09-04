import textwrap
from typing import TYPE_CHECKING

from colorama import Fore, Style, init

init()

if TYPE_CHECKING:
    from .merge import ClassSummary
INDENT = " " * 2
MAX_ALIGNING_LENGTH = 60


def is_dunder(name: str) -> bool:
    return name.startswith("__") and name.endswith("__")


def _display(
    data: list["ClassSummary"],
    *,
    include_dunders: bool = False,
    include_docs: bool = True,
    include_signatures: bool = False,
) -> None:
    # We reverse the class order so the most specific class is on the bottom since that's likely what people care about
    ret = ""
    for class_summary in data[::-1]:
        source_info = class_summary.source_info.to_string()
        ret += f"\n{Fore.BLUE}{class_summary.class_type.__name__} ({source_info}){Style.RESET_ALL}\n"

        if class_summary.class_type.__doc__ and include_docs:
            docstr = textwrap.indent(class_summary.class_type.__doc__.splitlines()[0], INDENT)
            ret += f"{Fore.GREEN}{docstr}{Style.RESET_ALL}\n\n"

        if class_summary.attr_info:
            ret += f"{INDENT}Attributes:\n"

            vals = sorted(class_summary.attr_info, key=lambda v: v.name)
            colon_position: int = max(val.colon_position() for val in vals)
            colon_position = colon_position if colon_position <= MAX_ALIGNING_LENGTH else 0

            for val in vals:
                if not include_dunders and is_dunder(val.name):
                    continue

                val_str = val.to_string(colon_position=colon_position, include_docs=include_docs)
                ret += f"{INDENT * 2}{Fore.GREEN}{val_str}{Style.RESET_ALL}\n"
        if class_summary.method_info:
            ret += f"{INDENT}Methods:\n"
            vals = sorted(class_summary.method_info, key=lambda v: v.name)
            colon_position: int = max(val.colon_position(include_signatures=include_signatures) for val in vals)
            colon_position = colon_position if colon_position <= MAX_ALIGNING_LENGTH else 0

            for val in vals:
                if not include_dunders and is_dunder(val.name):
                    continue

                val_str = val.to_string(
                    colon_position=colon_position,
                    include_docs=include_docs,
                    include_signatures=include_signatures,
                )
                ret += f"{INDENT * 2}{Fore.GREEN}{val_str}{Style.RESET_ALL}\n"

    print(ret)
