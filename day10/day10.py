#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import re


class Point:

    def __init__(self, pos: tuple, velocity: tuple) -> None:
        self.x = pos[0]
        self.y = pos[1]
        self.velocity = velocity

    def move(self) -> None:
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def isnear(self, other: 'Point') -> bool:
        if abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1:
            return True
        return False


def allnear(points: list) -> bool:
    arenear = [False] * len(points)
    for i, point in enumerate(points):
        for j, other in enumerate(points):
            if point is not other and point.isnear(other):
                arenear[i] = True
                arenear[j] = True
    return all(arenear)


def printpoints(points: list) -> None: 
    minx = min(points, key=lambda p: p.x).x
    miny = min(points, key=lambda p: p.y).y
    maxx = max(points, key=lambda p: p.x).x
    maxy = max(points, key=lambda p: p.y).y
    if (maxx-minx) * (maxy-miny) < 1000000:
        field = [ ['.'] * (maxx - minx + 1) for n in range(maxy - miny + 1) ]
        for point in points:
            field[point.y - miny][point.x - minx] = '#'
        for line in field:
            print(" ".join(p for p in line))


if __name__ == '__main__':
    with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_day10.txt'),
            encoding='utf-8'
        ) as fh:
        lines = [line for line in fh.read().split('\n') if line]

points = []
for line in lines:
    match = re.search(r'<([ -]\d+), ([ -]\d+)> velocity=<([ -]\d+), ([ -]\d+)>', line)
    position = (int(match.group(1)), int(match.group(2)))
    velocity = (int(match.group(3)), int(match.group(4)))
    points.append(Point(position, velocity))

counter = 0
while True:
    counter += 1
    for point in points:
        point.move()
    if counter > 10000:
        if allnear(points):
            print("Seconds:", counter)
            printpoints(points)
            out = input("Do you want to exit now? (y/n) ")
            if out == 'y':
                break
