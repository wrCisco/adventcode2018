#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
from copy import copy
from typing import Tuple, Mapping, Optional, Sequence



class Cave:


    def __init__(self, depth: int, target: Tuple[int, int]) -> None:
        self.depth = depth
        self.target = target
        self.mouth = (0, 0)
        
        self.map = [ ['.'] * (target[0] + max(target)) for n in range(target[1] + max(target)) ]
        self.map[0][0] = 'M'
        self.map[target[1]][target[0]] = 'T'
        
        self.region_types = {
            0: '.',  # rocky
            1: '=',  # wet
            2: '|'   # narrow
        }
        
        self.erosion_levels = self.find_erosion_levels()


    def find_erosion_levels(self) -> Mapping[Tuple[int, int], int]:
        erosion_levels = {}
        for y, row in enumerate(self.map):
            for x, region in enumerate(row):
                if (x, y) in ((0, 0), self.target):
                    geologic_index = 0
                elif y == 0:
                    geologic_index = x * 16807
                elif x == 0:
                    geologic_index = y * 48271
                else:
                    geologic_index = erosion_levels[(x-1, y)] * erosion_levels[(x, y-1)]
                erosion_levels[(x, y)] = (geologic_index + self.depth) % 20183
                # draw region on map
                self.map[y][x] = self.region_types[erosion_levels[(x, y)] % 3]
        return erosion_levels


    def risk_evaluation(self) -> int:
        risk = 0
        for row in self.map[:self.target[1]+1]:
            risk += row[:self.target[0]+1].count('=')
            risk += row[:self.target[0]+1].count('|') * 2
        return risk


    def print_map(self, dimensions: Optional[Tuple[int, int]] = None) -> None:
        if dimensions:
            x, y = dimensions
        else:
            x, y = len(self.map[0]), len(self.map)
        for row in self.map[:y+1]:
            print("".join(row[:x+1]))


class TestCave(Cave):

    def __init__(self, target: Tuple[int, int], map_: Sequence[Sequence[str]]) -> None:
        self.target = target
        self.mouth = (0, 0)
        self.map = map_ 
        


class Climber:

    ADEQUATE_EQUIPS = {
        '.': ('torch', 'climbing gear'),
        '=': ('climbing gear', 'nothing'),
        '|': ('torch', 'nothing')
    }

    def __init__(self, cave: Cave) -> None:
        self.cave = cave
        self.equipment = ('torch', 'climbing gear', 'nothing')
        self.minutes = 0
        self.start = Leg(cave.mouth, self.minutes, 'torch', 0)
        self.paths = [ [self.start] ]
        self.reached_regions = { self.start }

        self.UPPER_LIMIT_X = len(self.cave.map)
        self.UPPER_LIMIT_Y = len(self.cave.map[0])

        self.distance_safe_limit = max(10, self.distance_to_target(self.start.coords) // 5)


    def find_shortest_path(self) -> int:
        minutes = 0
        while not minutes:
            min_distance = min(self.distance_to_target(path[-1].coords) for path in self.paths)
            # if self.minutes and not self.minutes % 100:
            #     print(f"Min distance at minute {self.minutes}: {min_distance} (there are {len(self.paths)} paths). Reached regions: {len(self.reached_regions)}.")
            #     # if not self.minutes % 1000:
            #     #     input()
            minutes = self.step(min_distance)
        return minutes

    def distance_to_target(self, coords: Tuple[int, int]) -> int:
        return abs(self.cave.target[0] - coords[0]) + abs(self.cave.target[1] - coords[1])

    def can_move(self, region_type: str, equipment: str) -> bool:
        return equipment in Climber.ADEQUATE_EQUIPS[region_type]

    def adjacent_regions(self, center: Tuple[int, int]):
        x, y = center
        adjacents = { (x, y - 1), (x - 1, y), (x, y + 1), (x + 1, y) }  # NWSE
        return [ (x, y) for (x, y) in adjacents if 0 <= x < self.UPPER_LIMIT_X and 0 <= y < self.UPPER_LIMIT_Y ]

    def step(self, min_distance_to_target: int) -> Optional[int]:
        self.minutes += 1  # every step == one minute
        dead_paths = []
        new_paths = []

        for path in self.paths:
            leg = path[-1]

            if leg.state > 0:  # if leg is switching equipment
                leg.state -= 1
                if leg.state == 0:  # if equipment has been switched
                    new_leg = Leg(leg.coords, self.minutes, leg.new_equip, 0)
                    if new_leg.coords == self.cave.target and new_leg.equipment == 'torch':  # arrived
                        return self.minutes
                    if new_leg in self.reached_regions:
                        #print("Already reached")
                        dead_paths.append(path)
                        continue
                    self.reached_regions.add(new_leg)
                    path.append(new_leg)
                    leg = new_leg
                else:
                    #print(f"Don't move from {leg.coords}\nNo new path (switching equipment from {leg.equipment} to {leg.new_equip})")
                    continue

            # heuristic optimization: if leg is too far from the destination compared to the nearest one,
            # or if there are not adjacent regions that aren't already visited, declare a dead_path
            distance_to_target = self.distance_to_target(leg.coords)
            adjacents = self.adjacent_regions(leg.coords)
            if (distance_to_target > self.distance_safe_limit and distance_to_target > (min_distance_to_target * 1.5)) \
                    or not set(Leg(adj, leg.minutes, leg.equipment) for adj in adjacents) - self.reached_regions:
                 dead_paths.append(path)
                 #print(f"Dead path {leg.coords} with {leg.equipment} (distance: {distance_to_target} - while min distance: {min_distance_to_target}).")
                 continue

            forks = False
            new_equips = []
            new_path_model = path.copy()
            for x, y in adjacents:
                if self.can_move(self.cave.map[y][x], leg.equipment):
                    #print(f"Can move from {leg.coords} [{self.cave.map[leg.y][leg.x]}] to ({x}, {y}) [{self.cave.map[y][x]}] with {leg.equipment}")
                    new_leg = Leg((x, y), self.minutes, leg.equipment, 0)
                    if new_leg.coords == self.cave.target:
                        if new_leg.equipment == 'torch':
                            return self.minutes
                        else:
                            new_leg.state = 7
                            new_leg.new_equip = 'torch'
                    if new_leg in self.reached_regions:
                        #print("Already reached")
                        continue
                    self.reached_regions.add(new_leg)
                    if not forks:
                        #print("No new path")
                        path.append(new_leg)
                        forks = True
                    else:
                        #print("New path")
                        new_path = new_path_model.copy()
                        new_path.append(new_leg)
                        new_paths.append(new_path)
                else:
                    #print(f"Cannot move from {leg.coords} [{self.cave.map[leg.y][leg.x]}] to ({x}, {y}) [{self.cave.map[y][x]}] with {leg.equipment}")
                    for equip in self.equipment:
                        if equip in Climber.ADEQUATE_EQUIPS[self.cave.map[leg.y][leg.x]] \
                                and equip in Climber.ADEQUATE_EQUIPS[self.cave.map[y][x]]:
                            new_equip = equip
                    if new_equip in new_equips:
                        #print("No new path (already switching equipment)")
                        continue
                    new_equips.append(new_equip)
                    if not forks:
                        #print("No new path (switching equipment)")
                        leg.state = 7
                        leg.new_equip = new_equip
                        forks = True
                    else:
                        #print("New path (switching equipment)")
                        new_path = new_path_model.copy()
                        new_path[-1] = copy(leg)
                        new_leg = new_path[-1]
                        new_leg.state = 7
                        new_leg.new_equip = new_equip
                        new_paths.append(new_path)
        for path in dead_paths:
            self.paths.remove(path)
        for path in new_paths:
            self.paths.append(path)


class Leg:
    """
    Stop over a region.
    """

    def __init__(self, coords: Tuple[int, int], minutes: int, equipment: str, state: int = 0) -> None:
        """
        @params
        coords: coordinates of the leg
        minutes: time of arrival at the leg
        equipment: equipment when arriving
        state: if state == 0 -> free to move over,
               if state > 0 -> minutes to wait before switching equipment
        """
        self.coords = coords
        self.minutes = minutes
        self.equipment = equipment
        self.state = state
        self.next_equip: str  # valorized only when state > 0

    @property
    def coords(self) -> Tuple[int, int]:
        return self.__x, self.__y

    @coords.setter
    def coords(self, value: Tuple[int, int]) -> None:
        self.__x, self.__y = value

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, value: int) -> None:
        self.__x = value

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, value: int) -> None:
        self.__y = value

    def __eq__(self, other: 'Leg') -> bool:
        return self.coords == other.coords and self.equipment == other.equipment

    def __hash__(self) -> int:
        # self.coords and self.equipment never get to change
        return hash((self.coords, self.equipment))

    
if __name__ == '__main__':
    cave = Cave(depth=9171, target=(7, 721))
    # cave.print_map((60, 721))
    risk = cave.risk_evaluation()
    print("Evaluated risk:", risk)

    # with open(
    #         os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_input_day22.txt'),
    #         encoding='utf-8'
    #     ) as fh:
    #     lines = [line for line in fh.read().splitlines() if line]
    # test_cave = TestCave((10, 10), lines)
    # climber = Climber(test_cave)

    print("Finding shortest path...")
    climber = Climber(cave)
    minutes = climber.find_shortest_path()
    print("Fewest minutes to reach the target:", minutes)