#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os


def draw_point(field, coords):
    distance_sum = 0
    min_distance = 1000
    more_min_distances = False
    other_min_distance = 1000
    for i, (x, y) in enumerate(coords):
        codepoint = chr(0x41 + i)
        if (px, py) == (x, y):
            nearest = codepoint
            min_distance = 0
        distance = abs(px - x) + abs(py - y)
        distance_sum += distance
        if distance < min_distance:
            min_distance = distance
            nearest = codepoint
        elif distance == min_distance:
            more_min_distances = True
            other_min_distance = distance
    if more_min_distances and other_min_distance == min_distance:
        nearest = ' '
    field[px][py] = nearest
    return nearest, distance_sum


def get_package_root():
    from . import __file__ as initpy_file_path
    return os.path.dirname(initpy_file_path)


with open(
        os.path.join(get_package_root(), 'input_day6.txt'),
        encoding='utf-8'
    ) as fh:
    lines = [line.split(', ') for line in fh.read().split('\n') if line]

coords = [(int(x), int(y)) for (x, y) in lines]
field = [ ['x'] * max((x for (x, y) in coords)) for n in range(max((y for (x, y) in coords)))]

areas = { chr(i): 0 for i in range(0x41, 0x41+len(coords)) }

to_exclude = []
near_to_all = 0
for px, row in enumerate(field):
    for py, col in enumerate(row):
        try:
            nearest_coord, sum_of_distances = draw_point(field, coords)
            if sum_of_distances < 10000:
                near_to_all += 1
            areas[nearest_coord] += 1
        except KeyError:
            pass
        if px in (0, len(field)-1) or py in (0, len(row)-1):
            to_exclude.append(nearest_coord)

max_area = 0
for area, locations in areas.items():
    if area in to_exclude:
        continue
    if locations > max_area:
        max_area = locations
        max_area_name = area

print("Max non infinite area is", max_area, "big.")

print("Number of locations within 10000 from all coords:", near_to_all)
