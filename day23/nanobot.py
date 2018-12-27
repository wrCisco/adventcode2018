#!/usr/bin/env python3
# -*- coding: utf-8

from typing import Tuple


class Nanobot:

    def __init__(self, position: Tuple[int, int, int], signal_radius: int) -> None:
        self.__x, self.__y, self.__z = position
        self.signal_radius = signal_radius

    @property
    def coords(self) -> Tuple[int, int, int]:
        return self.__x, self.__y, self.__z

    @coords.setter
    def coords(self, values: Tuple[int, int, int]) -> None:
        raise AttributeError("Can't modify coordinates of the Nanobot.")
        #self.__x, self.__y, self.__z = values

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, value: int) -> None:
        raise AttributeError("Can't modify coordinates of the Nanobot.")
        #self.__x = value

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, value: int) -> None:
        raise AttributeError("Can't modify coordinates of the Nanobot.")
        #self.__y = value

    @property
    def z(self) -> int:
        return self.__z

    @z.setter
    def z(self, value: int) -> None:
        raise AttributeError("Can't modify coordinates of the Nanobot.")
        #self.__z = value

    def distance(self, x: int, y: int, z: int) -> int:
        return abs(self.x - x) + abs(self.y - y) + abs(self.z - z)

    def inrange(self, x: int, y: int, z: int) -> bool:
        return self.distance(x, y, z) <= self.signal_radius

    def intersection(self, other: 'Nanobot') -> int:
        return (self.signal_radius + other.signal_radius) - self.distance(*other.coords)

    def has_intersection(self, other: 'Nanobot') -> bool:
        return self.intersection(other) >= 0

    def __hash__(self):
        return hash((self.coords, self.signal_radius))

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z}), r = {self.signal_radius}"
