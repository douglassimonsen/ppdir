from pydantic import BaseModel

import ppdir  # noqa: F401


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


NextLayer(x=1, y=2, z=3, a="b").ppdir()
