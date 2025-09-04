from dataclasses import dataclass
from typing import Any

from ppdir import class_source_file

from .attr_doc_string import AttrInfo, MethodInfo, get_attr_docstrings, get_method_docstrings
from .display import _display
from .get_class_defines import get_class_defines


@dataclass
class ClassSummary:
    class_type: type
    source_info: class_source_file.SourceLines
    attr_info: list[AttrInfo]
    method_info: list[MethodInfo]


def get_info(inp_cls: Any) -> list[ClassSummary]:
    class_defines = get_class_defines(inp_cls)

    ret = []
    for mro_cls in inp_cls.mro():
        source_info = class_source_file.get_source_info(mro_cls)

        defines = class_defines[mro_cls.__name__]
        attr_info = get_attr_docstrings(mro_cls)
        method_info = get_method_docstrings(mro_cls)
        filtered_attr_info = [v for v in attr_info if v.name in defines]
        filtered_method_info = [v for v in method_info if v.name in defines]

        ret.append(
            ClassSummary(
                class_type=mro_cls,
                source_info=source_info,
                attr_info=filtered_attr_info,
                method_info=filtered_method_info,
            ),
        )
    return ret


def ppdir(
    inp_cls: Any,
    *,
    include_dunders: bool = False,
    include_docs: bool = True,
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
