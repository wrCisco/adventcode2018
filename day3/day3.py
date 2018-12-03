#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re
import os


class Square(object):

    def __init__(self, id_:int, x:int, y:int, width:int, height:int):
        self.id = id_
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def inches(self):
        return [(x, y) for x in range(self.x, self.x+self.width) 
                       for y in range(self.y, self.y+self.height)]


with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_day3.txt'),
        encoding='utf-8'
    ) as fh:
    lines = [line for line in fh.read().split('\n') if line]

squares = []
for line in lines:
    match = re.search(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line)
    id_, x, y, w, h = (match.group(1),
                       match.group(2),
                       match.group(3),
                       match.group(4),
                       match.group(5)
                      )
    sq = Square(int(id_), int(x), int(y), int(w), int(h))
    squares.append(sq)

fabric = [ [0] * 1000 for x in range(1000) ]

for sq in squares:
    for x, y in sq.inches():
        if not fabric[x][y]:
            fabric[x][y] = sq.id
        else:
            fabric[x][y] = 'X'

ids = {}
for row in fabric:
    for num in row:
        try:
            ids[num] += 1
        except KeyError:
            ids[num] = 1

print("Overlapping inches:", ids['X'])

for sq in squares:
    try:
        if ids[sq.id] == len(sq.inches()):
            print("Non overlapping square's id:", sq.id)
    except KeyError:
        pass
