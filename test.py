from collections.abc import Callable
from dataclasses import dataclass, field
from pprint import pprint

from pydantic import BaseModel


@dataclass
class Categories:
    methods: list[str] = field(default_factory=list)
    attributes: list[str] = field(default_factory=list)
    dunders: list[str] = field(default_factory=list)


class BaseLayer(BaseModel):
    x: int
    y: float
    z: int

    def func(self) -> None:
        print("asd")


class NextLayer(BaseLayer):
    a: str

    def test(self) -> int:
        return 1

    def ppdir(self) -> None:
        def is_dunder(x: str) -> bool:
            return x.startswith("__") and x.endswith("__")

        def expanded_dir(cls: type, all_mros: list[type]) -> list[str]:
            prior_mros = all_mros[all_mros.index(cls) + 1 :]
            ret: list[str] = list(cls.__dict__.keys())
            if hasattr(cls, "__slots__"):
                ret.extend(cls.__slots__)
            if hasattr(cls, "__pydantic_fields__"):
                prior_mros_pydantic_fields = [
                    key for prior_cls in prior_mros for key in getattr(prior_cls, "__pydantic_fields__", {})
                ]
                ret.extend(key for key in cls.__pydantic_fields__ if key not in prior_mros_pydantic_fields)
            return ret
            # if val in cls.__dict__ or val in getattr(cls, "__slots__", ()):

        mros = self.__class__.mro()
        mro_dict = {cls.__name__: expanded_dir(cls, mros) for cls in mros}
        ppdir_dict: dict[str, Categories] = {}
        for val in dir(self):
            if val in ("__signature__"):
                continue

            attr = getattr(self, val)

            if isinstance(attr, Callable):
                base_class_name = attr.__qualname__.split(".", 1)[0]
                categories = ppdir_dict.setdefault(base_class_name, Categories())
                if is_dunder(val):
                    categories.dunders.append(val)
                else:
                    categories.methods.append(val)
            else:
                for cls, cls_dir in mro_dict.items():
                    if val in cls_dir:
                        categories = ppdir_dict.setdefault(cls, Categories())
                        if is_dunder(val):
                            categories.dunders.append(val)
                        else:
                            categories.attributes.append(val)
                        break
                else:
                    msg = f"Unmatched val: {val}"
                    raise ValueError(msg)
        pprint(ppdir_dict)


NextLayer(x=1, y=2, z=3, a="b").ppdir()
