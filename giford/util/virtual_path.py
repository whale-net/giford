import math
from dataclasses import dataclass
from typing import Self


@dataclass
class Point:
    """
    Represents where a frame is positioned relative to the viewing frame

    Point(0,0) is the origin for the frame

    See below diagram for explanation on position):
      x→
    y -1, -1| 0, -1| 1, -1
    ↓ ------|------|------
      -1, 0 | 0, 0 | 1, 0
      ------|------|------
      -1, 1 | 0, 1 | 1, 1
    """

    x: float
    y: float

    @staticmethod
    def get_true_origin() -> "Point":
        return TRUE_ORIGIN_POINT


TRUE_ORIGIN_POINT: Point = Point(0, 0)


@dataclass
class Movement:
    """
    Represents a movement between 2 points

    Intended to be the
    """

    origin: Point
    target: Point

    @property
    def x_distance(self) -> float:
        return self.target.x - self.origin.x

    @property
    def y_distance(self) -> float:
        return self.target.y - self.origin.y

    def distance(self) -> float:
        return math.sqrt(self.x_distance**2 + self.y_distance**2)


class VirtualPath:
    """
    Virtual Paths allow frame actions to reproduce the same movements
    on different sized images by dynamically interpreting movements relative to the size of an image
    """

    def __init__(self, origin_point: Point | None = None):
        self.points: list[Point] = []

        if origin_point is not None:
            self.add_point(origin_point)

    def add_point(self, point: Point) -> Self:
        self.points.append(point)
        return self

    def add_point_from_coords(self, x: float, y: float) -> Self:
        self.add_point(Point(x, y))
        # allow function chaining
        return self

    def calculate_movements(self, is_from_true_origin: bool = True) -> list[Movement]:
        """
        calculate list of movements

        :param is_from_true_origin: produce movements relative to 0,0.
        setting False is probably not what you want, defaults to True
        :return: list of movements
        """
        if len(self.points) == 0:
            # no points, no movement. Unsure if this is best action here
            raise Exception("no points to produce movements")
        if len(self.points) == 1:
            # one point, no real movement
            return [Movement(origin=self.points[0], target=self.points[0])]

        # TODO return_to_origin: bool = False

        movements: list[Movement] = []
        for idx, point in enumerate(self.points):
            if is_from_true_origin:
                origin_point = Point.get_true_origin()
            elif idx == 0:
                origin_point = point
                continue

            m = Movement(origin_point, point)
            if not is_from_true_origin:
                origin_point = point
            movements.append(m)

        return movements
