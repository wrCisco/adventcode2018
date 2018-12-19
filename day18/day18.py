#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
from copy import deepcopy
from typing import List, Tuple, Mapping, Optional


class Ground:

    def __init__(self, input_: str) -> None:
        self.area = self._scan_ground(input_)
        self.snapshots = []

    def _scan_ground(self, input_: str) -> List[List[str]]:
        with open(input_, encoding='utf-8') as fh:
            return [list(line) for line in fh.read().split('\n') if line]

    def print_area(self, snapshot: Optional[List[List[str]]] = None) -> None:
        area = self.area if not snapshot else snapshot
        for line in area:
            print("".join(line))
        print("")

    def next_minute(self) -> None:
        self.last_snapshot = deepcopy(self.area)
        self.snapshots.append(self.last_snapshot)
        for y, line in enumerate(self.area):
            for x, acre in enumerate(line):
                adjacents = self.get_adjacent_acres((x, y))
                if acre == '.' and adjacents['|'] >= 3:
                    self.area[y][x] = '|'
                elif acre == '|' and adjacents['#'] >= 3:
                    self.area[y][x] = '#'
                elif acre == '#' and not (adjacents['#'] and adjacents['|']):
                    self.area[y][x] = '.'

    def get_adjacent_acres(
            self,
            center: Tuple[int, int],
            snapshot: Optional[List[List[str]]] = None
    ) -> Mapping[str, int]:
        area = self.last_snapshot if not snapshot else snapshot
        adjacents = set(((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)))
        if center[0] == 0:
            adjacents -= set(((-1, -1), (-1, 0), (-1, 1)))
        if center[1] == 0:
            adjacents -= set(((-1, -1), (0, -1), (1, -1)))
        if center[0] == len(self.area) - 1:
            adjacents -= set(((1, -1), (1, -0), (1, 1)))
        if center[1] == len(self.area) - 1:
            adjacents -= set(((-1, 1), (0, 1), (1, 1)))
        adjacent_acres = {
            '.': 0,  # open ground
            '|': 0,  # trees
            '#': 0   # lumberyard
        }
        cx, cy = center
        for adjacent in adjacents:
            adjx, adjy = adjacent
            adjacent_acres[area[cy+adjy][cx+adjx]] += 1
        return adjacent_acres

    def compute_value(self, snapshot: Optional[List[List[str]]] = None) -> int:
        area = self.area if not snapshot else snapshot
        trees = 0
        lumberyards = 0
        for line in area:
            trees += line.count('|')
            lumberyards += line.count('#')
        return trees * lumberyards


def find_period(ground: Ground) -> Optional[int]:
    for old_snapshot in ground.snapshots:
        if ground.last_snapshot == old_snapshot and ground.last_snapshot is not old_snapshot:
            # print(f"Found period. First snapshot: {ground.snapshots.index(old_snapshot)} - Last snapshot: {m}")
            # ground.print_area(old_snapshot)
            # ground.print_area(ground.last_snapshot)
            return m - (ground.snapshots.index(old_snapshot) + 1)


if __name__ == '__main__':
    ground = Ground(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_day18.txt'))
    for m in range(1, 1000000001):
        ground.next_minute()
        if m == 10:
            print(f"Value after ten minutes: {ground.compute_value()}")
        period = find_period(ground)
        if period:
            index = 1000000000 % period
            my_area = ground.snapshots[m - period + index]
            print(f"Value after one billion minutes: {ground.compute_value(my_area)}")
            break
