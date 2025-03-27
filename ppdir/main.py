import builtins
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from colorama import Fore, Style, init

init()


@dataclass
class Categories:
    methods: list[str] = field(default_factory=list)
    attributes: list[str] = field(default_factory=list)
    dunders: list[str] = field(default_factory=list)


class PpDirMixin:
    @staticmethod
    def _is_dunder(x: str) -> bool:
        return x.startswith("__") and x.endswith("__")

    @staticmethod
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

    @staticmethod
    def _display(data: dict[str, Categories], *, class_order: list[str], include_dunders: bool = False) -> None:
        for class_name in class_order:
            print(f"\n{Fore.BLUE}{class_name}{Style.RESET_ALL}")
            vals = data[class_name]
            if vals.attributes:
                print("    Attributes:")
                for val in vals.attributes:
                    print(f"        {Fore.GREEN}{val}{Style.RESET_ALL}")
            if vals.methods:
                print("    Methods:")
                for val in vals.methods:
                    print(f"        {Fore.YELLOW}{val}{Style.RESET_ALL}")
            if vals.dunders and include_dunders:
                print("    Dunders:")
                for val in vals.dunders:
                    print(f"        {Fore.RED}{val}{Style.RESET_ALL}")

    def ppdir(self, *, include_dunders: bool = False) -> None:
        mros = self.__class__.mro()
        mro_dict = {cls.__name__: self._expanded_dir(cls, mros) for cls in mros}
        ppdir_dict: dict[str, Categories] = {}
        for val in dir(self):
            if val in ("__signature__"):
                continue

            attr = getattr(self, val)

            if isinstance(attr, Callable):
                base_class_name = attr.__qualname__.split(".", 1)[0]
                categories = ppdir_dict.setdefault(base_class_name, Categories())
                if self._is_dunder(val):
                    categories.dunders.append(val)
                else:
                    categories.methods.append(val)
            else:
                for cls, cls_dir in mro_dict.items():
                    if val in cls_dir:
                        categories = ppdir_dict.setdefault(cls, Categories())
                        if self._is_dunder(val):
                            categories.dunders.append(val)
                        else:
                            categories.attributes.append(val)
                        break
                else:
                    msg = f"Unmatched val: {val}"
                    raise ValueError(msg)
        self._display(ppdir_dict, class_order=[cls.__name__ for cls in mros], include_dunders=include_dunders)


# On import, gets added to all classes


def my_build_class(func: Callable[[], Any], name: str, *bases: type, **kwargs: Any) -> Any:
    # any_non_class = any(not inspect.isclass(cls) for cls in bases)
    # if any_non_class:
    #     return _orig_build_class(func, name, *bases, **kwargs)

    # is_enum = any(issubclass(cls, Enum) for cls in bases)
    # if is_enum:
    #     return _orig_build_class(func, name, *bases, **kwargs)

    # has_protocol = any(issubclass(cls, Protocol) for cls in bases)
    # if has_protocol:
    #     return _orig_build_class(func, name, *bases, **kwargs)

    try:
        return _orig_build_class(func, name, *bases, PpDirMixin, **kwargs)
    except Exception:  # noqa: BLE001
        return _orig_build_class(func, name, *bases, **kwargs)


_orig_build_class = builtins.__build_class__
builtins.__build_class__ = my_build_class
