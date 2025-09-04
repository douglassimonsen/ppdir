from pydantic import BaseModel

from ppdir import defaults, ppdir

defaults(include_docs=True, include_signatures=False, include_dunders=True)


class BaseLayer(BaseModel):
    x: int
    y: float
    z: int

    def func(self) -> None:
        """Example test.

        Details are here
        """
        print("asd", self)

    def func2(self) -> None:
        """Example test2.

        Details are here
        """
        print("asd", self)


class NextLayer(BaseLayer):
    a: str
    """asdasd"""

    @staticmethod
    def static_test() -> int:
        """Example text."""
        return 1

    @classmethod
    def class_test(cls) -> int:
        """Example class method."""
        return 1

    def instance_test(self) -> None:
        """Asdasd."""
        return


x = NextLayer(x=1, y=2, z=3, a="b")
print(dir(x))
ppdir(x)
