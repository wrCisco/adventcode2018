#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
from typing import Sequence, Tuple, List


class Building:

    def __init__(
            self,
            map_: Sequence[Sequence[str]],
            start: Tuple[int, int],
            regex: str
    ) -> None:
        self.map = map_
        self.starting_point = start
        self.regex = regex
        self.reg_index = 0  # index to parse regex
        self.paths = [[]]
        #self.paths_index = 0  # index to current path is always -1
        self.forks = []
        self.current_pos = self.starting_point

        self.movements = {
            'N': lambda current: (current[0], current[1]-2),
            'S': lambda current: (current[0], current[1]+2),
            'W': lambda current: (current[0]-2, current[1]),
            'E': lambda current: (current[0]+2, current[1])
        }

    def walk_paths(self) -> None:
        self.draw_adjacents('initial')
        while self.step():
            # print(self.paths[-1])
            # self.print_map()
            # input()
            pass
        self.print_map(True)

    def print_map(self, finished: bool = False) -> None:
        min_x, min_y = len(self.map[0]), len(self.map)
        max_x, max_y = 0, 0
        for y, row in enumerate(self.map):
            for x, square in enumerate(row):
                if self.map[y][x] != '.':
                    if x < min_x:
                        min_x = x
                    elif x > max_x:
                        max_x = x
                    if y < min_y:
                        min_y = y
                    elif y > max_y:
                        max_y = y
        for y, row in enumerate(self.map[min_y:max_y+1]):
            r = "".join(row[min_x:max_x+1])
            if finished:
                r = r.replace('?', '#')
            print(r)

    def adjacents(self, center: Tuple[int, int]) -> List[Tuple[int, int]]:
        return [
            (center[0], center[1]-1), (center[0], center[1]+1),      # N S
            (center[0]-1, center[1]), (center[0]+1, center[1]),      # W E 
            (center[0]-1, center[1]-1), (center[0]+1, center[1]-1),  # diagonals
            (center[0]-1, center[1]+1), (center[0]+1, center[1]+1),  # diagonals
        ]

    def square(self, coords: Tuple[int, int]) -> str:
        return self.map[coords[1]][coords[0]]

    def set_square(self, coords: Tuple[int, int], value: str) -> None:
        self.map[coords[1]][coords[0]] = value

    def draw_adjacents(self, last_move: str = '') -> None:
        adjacents = self.adjacents(self.current_pos)
        for adj in adjacents[4:]:
            self.set_square(adj, '#')
        if last_move == 'initial':
            for adj in adjacents[:4]:
                self.set_square(adj, '?')
                return
        elif last_move and last_move in 'NSWE':
            door = '-' if last_move in 'NS' else '|'
            index = 'NSWE'.index(last_move)
            if self.square(adjacents[index]) in '.?':
                self.set_square(adjacents[index], door)
        for adjacent in adjacents[:4]:
            if self.square(adjacent) == '.':
                self.set_square(adjacent, '?')

    def step(self) -> bool:
        self.reg_index += 1
        next_char = self.regex[self.reg_index]
        if next_char in 'NEWS':
            next_pos = self.movements[next_char](self.current_pos)
            self.paths[-1].append(next_pos)
            self.draw_adjacents(next_char)
            self.current_pos = next_pos
            self.draw_adjacents()
        elif next_char == '(':
            self.forks.append(self.paths[-1].copy())
        elif next_char == '|':
            if self.regex[self.reg_index+1] != ')':
                self.paths.append(self.forks[-1].copy())
                #self.paths_index = len(self.paths) - 1
                self.current_pos = self.paths[-1][-1]
            elif self.regex[self.reg_index+1] == ')':
                # self.current_pos here returns at the starting point of the optional detour,
                # so no need to reset it
                assert (len(self.paths[-1]) - len(self.forks[-1])) % 2 == 0
                farthest_room = (len(self.paths[-1]) - len(self.forks[-1])) // 2
                self.paths[-1][:] = self.paths[-1][:-farthest_room]
        elif next_char == ')':
            if self.regex[self.reg_index+1] in 'NEWS(':
                self.paths.append(self.forks[-1].copy())
                #self.paths_index = len(self.paths) - 1
                self.current_pos = self.paths[-1][-1]
            self.forks.pop()
        elif next_char == '$':
            return False
        return True


if __name__ == '__main__':
    with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_day20.txt'),
            encoding='utf-8'
        ) as fh:
        reg = fh.read().strip('\n')

    # that's probably enough (but not for tests)
    height = (reg.count('N') + reg.count('S')) // 2
    width = (reg.count('W') + reg.count('E')) // 2

    grid = [ ['.'] * width for n in range(height) ]
    starting_point = [width // 2, height // 2]
    grid[starting_point[1]][starting_point[0]] = 'X'
    building = Building(grid, starting_point, reg)
    building.walk_paths()
    longest_path = max(building.paths, key=lambda path: len(path))
    farthest_room = longest_path[-1]
    alternatives = []
    for path in building.paths:
        if farthest_room in path and path is not longest_path:
            alternatives.append((path, path.index(farthest_room)))
    print("The shortest path to the farthest room is", len(longest_path))
    print(f"There are {len(alternatives)} alternative routes for that room")

    rooms = set()
    least_doors = 1000
    for path in building.paths:
        rooms.update(path[least_doors-1:])
    print(f"Rooms over {least_doors} doors to pass in order to reach them are", len(rooms))
