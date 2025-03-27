from pydantic import BaseModel

from ppdir import ppdir


class BaseLayer(BaseModel):
    x: int
    y: float
    z: int

    def func(self) -> None:
        """Example test.

        Details are here
        """
        print("asd")


class NextLayer(BaseLayer):
    a: str

    def test(self) -> int:
        """Example text."""
        return 1


ppdir(NextLayer(x=1, y=2, z=3, a="b"))
