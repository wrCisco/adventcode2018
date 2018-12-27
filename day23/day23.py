#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from typing import Tuple, Union

from nanobot import Nanobot


def to_origin(point, nanobots):
    max_in_range = len(nanobots)
    in_range = len(nanobots)
    pos = point
    diffs = (
        (-1, -1, -1),
        (-1,  0,  0),
        ( 0, -1,  0),
        ( 0,  0, -1),
        (-1, -1,  0),
        (-1,  0, -1),
        ( 0, -1, -1),
        (-1, -1,  1),
        (-1,  1, -1),
        ( 1, -1, -1)
    )
    for diff in diffs:
        while in_range >= max_in_range:
            prev_range = in_range
            prev_pos = pos
            pos = (pos[0] + diff[0], pos[1] + diff[1], pos[2] + diff[2])
            in_range = 0
            for bot in nanobots:
                if bot.inrange(*pos):
                    in_range += 1
        in_range = prev_range
        pos = prev_pos
        #print(f"Pos ({pos[0]}, {pos[1]}, {pos[2]}) is in range of {in_range}")
    return prev_pos


if __name__ == '__main__':
    with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_day23.txt'),
            encoding='utf-8'
        ) as fh:
        lines = [line for line in fh.read().splitlines() if line]

    nanobots = []
    for line in lines:
        x, y, z, r = re.findall(r'-?\d+', line)
        nanobots.append(Nanobot((int(x), int(y), int(z)), int(r)))
    strongest = max(nanobots, key=lambda n: n.signal_radius)

    nanobots_in_range = []
    for nanobot in nanobots:
        if strongest.inrange(*nanobot.coords):
            nanobots_in_range.append(nanobot)
    print(f"Nanobots in range of the signal of the strongest amongst them are {len(nanobots_in_range)}")

    intersections = { nanobot: set() for nanobot in nanobots }
    for nanobot, intersecting in intersections.items():
        for other in nanobots:
            if nanobot.has_intersection(other):  # including self
                intersecting.add(other)
    # print("Max intersections:", max(len(inters) for inters in intersections.values()))
    to_remove = []
    for nanobot, intersecting in intersections.items():
        if len(intersecting) < 974:  # number found "by eye", after printing how many intersecting spheres every sphere has
            to_remove.append(nanobot)
      
    for bot in to_remove:
        del intersections[bot]
        for intersecting in intersections.values():
            try:
                intersecting.remove(bot)
            except KeyError:
                pass
    print(f"{len(intersections)} remaining")

    # for nanobot, intersecting in intersections.items():
    #     print(f"Nanobot {nanobot} intersects {len(intersecting)} other nanobots")

    nanobots = list(intersections.keys())
    #from intersecting_nanobots import nanobots

    superintersection = []
    for i, nanobot in enumerate(nanobots):
        a = ((sum(nanobot.coords) - nanobot.signal_radius),
             (sum(nanobot.coords) + nanobot.signal_radius))
        b = ((nanobot.x + nanobot.y - nanobot.z - nanobot.signal_radius),
             (nanobot.x + nanobot.y - nanobot.z + nanobot.signal_radius))
        c = ((nanobot.x - nanobot.y + nanobot.z - nanobot.signal_radius),
             (nanobot.x - nanobot.y + nanobot.z + nanobot.signal_radius))
        d = ((nanobot.x - nanobot.y - nanobot.z - nanobot.signal_radius),
             (nanobot.x - nanobot.y - nanobot.z + nanobot.signal_radius))
        values = [a, b, c, d]
        if not superintersection:
            superintersection.extend(values)
        else:
            for j, vals in enumerate(superintersection):
                superintersection[j] = (max(vals[0], values[j][0]), min(vals[1], values[j][1]))

    point = (
        (superintersection[0][1] + superintersection[3][0]) // 2,
        (superintersection[0][1] - superintersection[2][0]) // 2,
        (superintersection[0][1] - superintersection[1][0]) // 2
    )

    # out_of_range = 0
    # for bot in nanobots:
    #     #print(bot, "margin:", bot.distance(*point) - bot.signal_radius)
    #     if not bot.inrange(*point):
    #         out_of_range += 1
    # if not out_of_range:
    #     print("All in range!")
    # else:
    #     print(f"{out_of_range} out of range!")
   
    solution = to_origin(point, nanobots)

    print(f"Manhattan distance between ({solution[0]}, {solution[1]}, {solution[2]}) and (0,0,0) is", sum(solution))
    