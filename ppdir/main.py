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

    def to_string(self, *, include_docs: bool) -> str:
        if include_docs and self.summary():
            short_summary = self.summary()
            return f"{self.name}:   {short_summary}"
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
        vals = data[class_name]
        if vals.attributes:
            print("    Attributes:")
            for val in vals.attributes:
                print(f"        {Fore.GREEN}{val.to_string(include_docs=include_docs)}{Style.RESET_ALL}")
        if vals.methods:
            print("    Methods:")
            for val in vals.methods:
                print(f"        {Fore.YELLOW}{val.to_string(include_docs=include_docs)}{Style.RESET_ALL}")
        if vals.dunders and include_dunders:
            print("    Dunders:")
            for val in vals.dunders:
                print(f"        {Fore.RED}{val.to_string(include_docs=include_docs)}{Style.RESET_ALL}")


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
    return ret


def ppdir(inp_cls: Any, *, include_dunders: bool = False, include_docs: bool = True) -> None:
    mros = inp_cls.__class__.mro()
    mro_dict = {cls.__name__: _expanded_dir(cls, mros) for cls in mros}
    ppdir_dict: dict[str, Categories] = {}
    for val in dir(inp_cls):
        if val in ("__signature__"):
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
            for cls, cls_dir in mro_dict.items():
                if val in cls_dir:
                    categories = ppdir_dict.setdefault(cls, Categories())
                    if _is_dunder(val):
                        categories.dunders.append(meta)
                    else:
                        categories.attributes.append(meta)
                    break
            else:
                msg = f"Unmatched val: {val}"
                raise ValueError(msg)
    _display(
        ppdir_dict,
        class_order=[cls.__name__ for cls in mros],
        include_dunders=include_dunders,
        include_docs=include_docs,
    )
