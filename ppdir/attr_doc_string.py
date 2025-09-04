import ast
import inspect
from dataclasses import dataclass


@dataclass
class AttrInfo:
    name: str
    type: str
    doc: str

    def to_string(self, colon_position: int, *, include_docs: bool) -> str:
        pre_colon = f"{self.name} ({self.type})".ljust(colon_position)

        if include_docs:
            doc_summary = self.doc.splitlines()[0] if self.doc else "--N/A--"
            return f"{pre_colon}: {doc_summary}"

        return pre_colon

    def colon_position(self) -> int:
        return len(self.name) + len(self.type) + 3


@dataclass
class MethodInfo:
    name: str
    type: str
    doc: str

    def to_string(self, colon_position: int, *, include_docs: bool, include_signatures: bool) -> str:
        pre_colon = self.name
        if include_signatures:
            pre_colon += f" ({self.type})"
        pre_colon = pre_colon.ljust(colon_position)[:-1]
        if include_docs:
            doc_summary = self.doc.splitlines()[0] if self.doc else "--N/A--"
            return f"{pre_colon}: {doc_summary}"

        return pre_colon

    def colon_position(self, *, include_signatures: bool) -> int:
        if include_signatures:
            return len(self.name) + len(self.type) + 3
        return len(self.name) + 3


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
    last_doc: str | None = None

    # This section can cause issues if an IDIOT creates docstrings for the first
    # class attribute, but not for the class itself.
    body = tree.body
    if not isinstance(body[0], ast.AnnAssign):
        body = body[1:]

    for expr in body:
        # When encouter an Expr, check if the expr a string
        if isinstance(expr, ast.Expr):
            # The value is a ast.Value node
            # therefore another access to value is needed
            assert isinstance(expr.value, ast.Constant)
            value = expr.value.value
            if isinstance(value, str):
                last_doc = value.strip()

        # if the last known doc string is not none
        # and this next node is an annotation, that's a docstring
        if isinstance(expr, ast.AnnAssign):
            # expr.target is a ast.Name
            name = ast.unparse(expr.target)
            type_name = ast.unparse(expr.annotation)
            attribute_docs.append(AttrInfo(name=name, type=type_name, doc=last_doc or ""))
            last_doc = None

    return attribute_docs


def get_method_docstrings(cls: type) -> list[MethodInfo]:
    methods = inspect.getmembers(cls, predicate=inspect.ismethod)
    ret = []
    for method in methods:
        signature = inspect.signature(method[1])  # This is just to ensure it doesn't error
        ret.append(
            MethodInfo(
                name=method[0],
                type=str(signature),
                doc=method[1].__doc__ or "",
            ),
        )
    return ret
