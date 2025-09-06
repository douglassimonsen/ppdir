import ast
import inspect
from dataclasses import dataclass
from typing import Literal


@dataclass
class AttrInfo:
    name: str
    type: str
    doc: str

    def _pre_colon_str(self) -> str:
        return f"{self.name} ({self.type})"

    def to_string(self, colon_position: int, *, include_docs: bool) -> str:
        colon = ":" if include_docs else ""
        pre_colon = f"{self._pre_colon_str()}{colon}".ljust(colon_position + 1)

        if include_docs:
            doc_summary = self.doc.strip().splitlines()[0] if self.doc else "--N/A--"
            return f"{pre_colon} {doc_summary}"
        return pre_colon

    def colon_position(self) -> int:
        return len(self._pre_colon_str())


@dataclass
class MethodInfo:
    name: str
    signature: str
    method_type: Literal["instance", "class", "static"]
    doc: str

    def _pre_colon_str(self, *, include_signatures: bool) -> str:
        pre_colon = self.name
        if include_signatures:
            pre_colon += f" ({self.signature})"
        return pre_colon

    def to_string(self, colon_position: int, *, include_docs: bool, include_signatures: bool) -> str:
        colon = ":" if include_docs else ""
        pre_colon = f"{self._pre_colon_str(include_signatures=include_signatures)}{colon}".ljust(colon_position + 1)

        if self.method_type == "class":
            pre_colon = f"\b\bᶜ {pre_colon}"
        elif self.method_type == "static":
            pre_colon = f"\b\bˢ {pre_colon}"

        if include_docs:
            doc_summary = self.doc.strip().splitlines()[0] if self.doc else "--N/A--"
            return f"{pre_colon} {doc_summary}"

        return pre_colon

    def colon_position(self, *, include_signatures: bool) -> int:
        return len(self._pre_colon_str(include_signatures=include_signatures))


def ast_find_classdef(tree: ast.Module) -> ast.ClassDef | None:
    for e in ast.walk(tree):
        if isinstance(e, ast.ClassDef):
            return e
    return None


def get_attr_docstrings(cls: type) -> list[AttrInfo]:
    try:
        src = inspect.getsource(cls)
    except TypeError:
        # This can occur when you try to get the source of a built-in, like dict
        return []

    tree = ast.parse(src)
    tree = ast_find_classdef(tree)
    assert tree is not None

    attribute_docs = []

    body = tree.body
    if not isinstance(body[0], ast.AnnAssign):
        body = body[1:]

    for expr in body:
        # When encouter an Expr, check if the expr a string
        if isinstance(expr, ast.Expr):
            if not attribute_docs:
                continue

            # The value is a ast.Value node
            # therefore another access to value is needed
            assert isinstance(expr.value, ast.Constant)
            doc_string = expr.value.value
            doc_string = doc_string if isinstance(doc_string, str) else None
            last_attr = attribute_docs[-1]
            if not last_attr.doc and doc_string is not None:
                last_attr.doc = doc_string

        # if the last known doc string is not none
        # and this next node is an annotation, that's a docstring
        if isinstance(expr, ast.AnnAssign):
            # expr.target is a ast.Name
            name = ast.unparse(expr.target)
            type_name = ast.unparse(expr.annotation)
            attribute_docs.append(
                AttrInfo(name=name, type=type_name, doc=""),
            )

    return attribute_docs


def get_method_docstrings(cls: type) -> list[MethodInfo]:
    methods = inspect.getmembers(cls, predicate=lambda x: inspect.ismethod(x) or inspect.isfunction(x))
    ret = []
    for method in methods:
        signature = inspect.signature(method[1])  # This is just to ensure it doesn't error

        method_with_possible_decorators = inspect.getattr_static(cls, method[0])

        method_type = "instance"
        if isinstance(method_with_possible_decorators, classmethod):
            method_type = "class"
        elif isinstance(method_with_possible_decorators, staticmethod):
            method_type = "static"

        ret.append(
            MethodInfo(
                name=method[0],
                signature=str(signature),
                method_type=method_type,
                doc=method[1].__doc__ or "",
            ),
        )
    return ret
