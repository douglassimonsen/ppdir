import inspect
from dataclasses import dataclass


@dataclass
class SourceLines:
    path: str
    start: int
    end: int

    def to_string(self) -> str:
        return f"{self.path}, lines {self.start}-{self.end}"


def get_source_info(cls: type) -> SourceLines:
    """Get the source file where the class is defined.

    Args:
        cls: The class to inspect.

    Returns:
        The source file path as a string.

    """
    try:
        source_path = inspect.getsourcefile(cls)
    except TypeError:
        return SourceLines("<built-in>", 0, 0)

    assert source_path is not None
    source_lines = inspect.getsourcelines(cls)
    start_line, end_line = source_lines[1], source_lines[1] + len(source_lines[0]) - 1
    return SourceLines(source_path, start_line, end_line)
