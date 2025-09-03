from dataclasses import dataclass
from typing import Any

from ppdir import attr_doc_string, class_source_file

from .display import _display
from .get_class_defines import get_class_defines


@dataclass
class ClassSummary:
    class_type: type
    source_info: class_source_file.SourceLines
    attr_info: dict[str, attr_doc_string.AttrInfo]


def get_info(inp_cls: Any):
    class_defines = get_class_defines(inp_cls)

    class_sources = {}
    class_attribute_docs = {}
    for mro_cls in inp_cls.mro():
        class_sources[mro_cls.__name__] = class_source_file.get_source_info(mro_cls)
        class_attribute_docs[mro_cls.__name__] = attr_doc_string.get_attr_doc_strings(
            mro_cls,
        ) | attr_doc_string.get_method_docstrings(mro_cls)

    ret = [
        ClassSummary(
            class_type=cls,
            source_info=class_sources[cls.__name__],
            attr_info=class_attribute_docs[cls.__name__],
        )
        for cls in inp_cls.mro()
    ]
    return class_defines, class_sources, class_attribute_docs


def ppdir(inp_cls: Any, *, include_dunders: bool = False, include_docs: bool = True) -> None:
    if not isinstance(inp_cls, type):
        inp_cls = inp_cls.__class__
    class_defines, class_sources, class_attribute_docs = get_info(inp_cls)
    _display(class_defines, class_sources, class_attribute_docs)
