import math
from dataclasses import dataclass

@dataclass 
class Point():
    """
    Represents where a frame is positioned relative to the viewing frame

    Point(0,0) is the origin
      x→
    y -1, -1| 0, -1| 1, -1
    ↓ ------|------|------
      -1, 0 | 0, 0 | 1, 0
      ------|------|------
      -1, 1 | 0, 1 | 1, 1
    """
    x: float
    y: float

@dataclass
class Movement():
    """
    Represents a movement between 2 points

    Intended to be the 
    """
    origin: Point
    target: Point

    def distance(self) -> float:
        return math.sqrt((self.target.x - self.origin.x) ** 2 + (self.target.y - self.origin.y) ** 2)



class VirtualPath():
    """
    Virtual Paths allow frame actions to reproduce the same movements 
    on different sized images by dynamically interpreting movements relative to the size of an image
    """
    def __init__(self, origin_point: Point = Point(0,0)):
        self.points: list[Point] = []

        if origin_point is not None:
            self.add_point(origin_point)


    def add_point(self, point: Point):
        self.points.append(point)
        return self

    def add_point_from_coords(self, x: float, y: float):
        self.add_point(Point(x,y))
        # allow function chaining
        return self

    def calculate_movements(self) -> list[Movement]:
        if len(self.points) == 0:
            # no points, no movement. Unsure if this is best action here
            raise Exception("no points to produce movements")
        if len(self.points) == 1:
            # one point, no real movement
            return [Movement(origin=self.points[0], target=self.points[0])]
        
        # TODO return_to_origin: bool = False
        
        movements: list[Movement] = []
        for idx, point in enumerate(self.points):
            if idx == 0:
                origin_point = point
                continue

            m = Movement(origin_point, point)
            origin_point = point
            movements.append(m)

        return movements
