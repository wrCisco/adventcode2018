#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import re
from typing import Tuple


class Point:

    def __init__(self, coords: Tuple[int, int, int, int]) -> None:
        self.x, self.y, self.z, self.t = coords
        self.constellation = set()

    def same_constellation(self, other: 'Point') -> bool:
        return (abs(self.x - other.x) + abs(self.y - other.y)
                + abs(self.z - other.z) + abs(self.t - other.t) <= 3)


if __name__ == '__main__':
    with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_day25.txt'),
            encoding='utf-8'
        ) as fh:
        lines = [line for line in fh.read().splitlines() if line]

    points = []
    for line in lines:
        x, y, z, t = re.findall(r'-?\d+', line)
        points.append(Point((int(x), int(y), int(z), int(t))))

    constellations = []
    for i, point in enumerate(points):
        neighbours = []
        for j, other in enumerate(points):
            if other.same_constellation(point):
                neighbours.append(other)
        new_const = set()
        for neighbour in neighbours:
            if neighbour.constellation:
                new_const.update(neighbour.constellation)
                try:
                    constellations.remove(neighbour.constellation)
                except ValueError:
                    pass
            else:
                new_const.add(neighbour)
        if new_const:
            constellations.append(new_const)
            for p in new_const:
                p.constellation = new_const

    print(f"There are {len(constellations)} constellations of fixed spacetime points.")
