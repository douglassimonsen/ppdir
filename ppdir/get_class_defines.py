def _expanded_dir(cls: type) -> list[str]:
    ret: list[str] = dir(cls)
    ret.extend(cls.__dict__.keys())
    if "__annotations__" in cls.__dict__:
        ret.extend(cls.__annotations__.keys())
    if "__pydantic_fields__" in cls.__dict__:
        # If a field exists, but isn't set by the instance, it doesn't appear in the dir() call
        ret.extend(cls.__pydantic_fields__.keys())
    return list(set(ret))


def get_class_defines(cls: type) -> dict[str, list[str]]:
    all_class_entities = _expanded_dir(cls)

    ret = {}
    for mro in cls.mro()[::-1]:
        ret[mro.__name__] = []
        for entity in _expanded_dir(mro):
            if entity in all_class_entities:
                ret[mro.__name__].append(entity)
                all_class_entities.remove(entity)
    return ret
