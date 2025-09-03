import ast
import inspect
from dataclasses import dataclass


@dataclass
class AttrInfo:
    type: str
    doc: str


def ast_find_classdef(tree: ast.Module) -> ast.ClassDef | None:
    for e in ast.walk(tree):
        if isinstance(e, ast.ClassDef):
            return e
    return None


def get_attr_doc_strings(cls: type) -> dict[str, str]:
    try:
        src = inspect.getsource(cls)
    except TypeError:
        # This can occur when you try to get the source of a built-in, like dict
        return {}

    tree = ast.parse(src)
    tree = ast_find_classdef(tree)
    assert tree is not None

    attribute_docs = {}
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
            attribute_docs[name] = {"type": type_name, "doc": last_doc or ""}
            last_doc = None

    return attribute_docs


def get_method_docstrings(cls: type) -> dict[str, str]:
    breakpoint()
