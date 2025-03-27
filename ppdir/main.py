from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from colorama import Fore, Style, init

init()


@dataclass
class Attributes:
    name: str
    docstring: str

    def summary(self) -> str:
        # Adding a trailing space since splitlines returns an empty list from an empty string. Gets removed by the strip
        return (self.docstring + " ").splitlines()[0].strip()

    def to_string(self, *, max_len: int, include_docs: bool) -> str:
        if include_docs and self.summary():
            short_summary = self.summary()
            spacing = " " * (max_len - len(self.name) + 1)
            return f"{self.name}:{spacing}{short_summary}"
        return self.name


@dataclass
class Categories:
    methods: list[Attributes] = field(default_factory=list)
    attributes: list[Attributes] = field(default_factory=list)
    dunders: list[Attributes] = field(default_factory=list)


def _is_dunder(x: str) -> bool:
    return x.startswith("__") and x.endswith("__")


def _display(
    data: dict[str, Categories],
    *,
    class_order: list[str],
    include_dunders: bool = False,
    include_docs: bool = True,
) -> None:
    for class_name in class_order:
        print(f"\n{Fore.BLUE}{class_name}{Style.RESET_ALL}")
        vals = data.get(class_name, Categories())
        if vals.attributes:
            print("    Attributes:")
            max_len = max(len(val.name) for val in vals.attributes)
            for val in vals.attributes:
                val_str = val.to_string(include_docs=include_docs, max_len=max_len)
                print(
                    f"        {Fore.GREEN}{val_str}{Style.RESET_ALL}",
                )
        if vals.methods:
            print("    Methods:")
            max_len = max(len(val.name) for val in vals.methods)
            for val in vals.methods:
                val_str = val.to_string(include_docs=include_docs, max_len=max_len)
                print(
                    f"        {Fore.YELLOW}{val_str}{Style.RESET_ALL}",
                )
        if vals.dunders and include_dunders:
            print("    Dunders:")
            max_len = max(len(val.name) for val in vals.dunders)
            for val in vals.dunders:
                val_str = val.to_string(include_docs=include_docs, max_len=max_len)
                print(f"        {Fore.RED}{val_str}{Style.RESET_ALL}")


def _expanded_dir(main_cls: type, all_mros: list[type]) -> list[str]:
    prior_mros = all_mros[all_mros.index(main_cls) + 1 :]
    ret: list[str] = list(main_cls.__dict__.keys())
    if hasattr(main_cls, "__slots__"):
        ret.extend(main_cls.__slots__)
    if hasattr(main_cls, "__pydantic_fields__"):
        prior_mros_pydantic_fields = [
            key for prior_cls in prior_mros for key in getattr(prior_cls, "__pydantic_fields__", {})
        ]
        ret.extend(key for key in main_cls.__pydantic_fields__ if key not in prior_mros_pydantic_fields)
    ret.sort()
    return ret


def _find_base_class(meta: Attributes, mro_dict: dict[str, list[str]], ppdir_dict: dict[str, Categories]):
    for cls, cls_dir in mro_dict.items():
        if meta.name in cls_dir:
            categories = ppdir_dict.setdefault(cls, Categories())
            if _is_dunder(meta.name):
                categories.dunders.append(meta)
            else:
                categories.attributes.append(meta)
            break
    else:
        msg = f"Unmatched val: {meta.name}"
        raise ValueError(msg)


def ppdir(inp_cls: Any, *, include_dunders: bool = False, include_docs: bool = True) -> None:
    mros = inp_cls.__class__.mro()
    mro_dict = {cls.__name__: _expanded_dir(cls, mros) for cls in mros}
    ppdir_dict: dict[str, Categories] = {}

    class_attrs = dir(inp_cls)
    for val in class_attrs:
        if val == "__signature__":
            continue

        attr = getattr(inp_cls, val)
        meta = Attributes(name=val, docstring=attr.__doc__ or "")
        if isinstance(attr, Callable):
            base_class_name = attr.__qualname__.split(".", 1)[0]
            categories = ppdir_dict.setdefault(base_class_name, Categories())
            if _is_dunder(val):
                categories.dunders.append(meta)
            else:
                categories.methods.append(meta)
        else:
            _find_base_class(meta, mro_dict, ppdir_dict)

    _display(
        ppdir_dict,
        class_order=[cls.__name__ for cls in mros],
        include_dunders=include_dunders,
        include_docs=include_docs,
    )
