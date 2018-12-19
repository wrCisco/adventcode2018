#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import re
from typing import Tuple, Sequence, List


class JoinOtherFlowException(Exception):
    pass


class Ground:

    def __init__(self, input_: str, water_spring: Tuple[int, int]) -> None:
        self.water_spring = water_spring
        self.vertical_slice = self._scan_ground(input_)

    def _scan_ground(self, input_:str) -> List[List[str]]:
        with open(input_, encoding='utf-8') as fh:
            lines = [line for line in fh.read().splitlines() if line]
        clay_coords = []
        for line in lines:
            coords = {}
            coords_str = line.split(', ')
            for coord in coords_str:
                name = coord[0]
                if '.' in coord:
                    min_, max_ = [int(i) for i in re.findall(r'\d+', coord)]
                else:
                    min_= int(coord[2:])
                    max_ = min_
                coords[name] = (min_, max_)
            clay_coords.append(coords)

        max_x = max(coords['x'][1]+2 for coords in clay_coords)
        # min_x = min(coords['x'][0] for coords in clay_coords)
        self.max_y = max(coords['y'][1]+1 for coords in clay_coords)
        self.min_y = min(coords['y'][0] for coords in clay_coords)

        vertical_slice = [ ['.'] * max_x for i in range(self.max_y) ]

        for coords in clay_coords:
            for x in range(coords['x'][0], coords['x'][1]+1):
                for y in range(coords['y'][0], coords['y'][1]+1):
                    vertical_slice[y][x] = '#'
        vertical_slice[self.water_spring[1]][self.water_spring[0]] = '+'
        return vertical_slice

    def __getitem__(self, value: int) -> List[str]:
        return self.vertical_slice[value]


class Water:

    def __init__(self, ground: Ground) -> None:
        self.ground = ground
        self.forks = []
        self.current = self.ground.water_spring

    @property
    def current(self) -> Tuple[int, int]:
        return self.__x, self.__y

    @current.setter
    def current(self, values: Tuple[int, int]) -> None:
        self.__x, self.__y = values
        if self.current in self.forks:
            self.forks.remove(self.current)

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, value: int) -> None:
        self.__x = value
        if self.current in self.forks:
            self.forks.remove(self.current)

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, value: int) -> None:
        self.__y = value
        if self.current in self.forks:
            self.forks.remove(self.current)

    def flow(self) -> None:
        try:
            while True:
                self.step()
        except (IndexError, JoinOtherFlowException):
            try:
                self.current = self.forks.pop()
            except IndexError:
                return
            else:
                self.flow()

    def step(self) -> None:
        can_flow_down = self.can_flow('down')
        if can_flow_down == 'yes':
            self.flow_down()
        elif can_flow_down == 'no':
            self.spread()
        else:
            raise JoinOtherFlowException

    def flow_down(self) -> None:
        self.ground[self.y+1][self.x] = '|'
        self.y += 1

    def flow_left(self) -> None:
        self.ground[self.y][self.x-1] = '|'
        self.x -= 1

    def flow_right(self) -> None:
        self.ground[self.y][self.x+1] = '|'
        self.x += 1

    def can_flow(self, direction: str) -> str:
        """
        Return values can be:
        'yes' -> movement towards dry sand ('.'),
        'no' -> movement towards clay or stable water ('#', '~'),
        'join' -> movement towards stream of water ('|')
        """
        ways = {
            'left': self.ground[self.y][self.x-1],
            'right': self.ground[self.y][self.x+1]
        }
        try:
            ways['down'] = self.ground[self.y+1][self.x]
        except IndexError:
            if direction == 'down':
                raise IndexError
            else:
                ways['down'] = ''
        # If water can go down, can only go down
        if ways['down'] == '.':
            return 'yes' if direction == 'down' else 'no'
        elif ways['down'] == '|':
            return 'join'
        else:
            if ways[direction] == '.':
                return 'yes'
            elif ways[direction] == '|':
                return 'join'
            else:
                return 'no'

    def spread(self) -> None:
        new_flows = []
        basin = []
        starting_point = self.current
        while self.can_flow('left') != 'no':
            self.flow_left()
        can_flow_down = self.can_flow('down')
        if can_flow_down == 'yes':
            new_flows.append(self.current)
        elif can_flow_down == 'no':
            basin.append(self.current)
        self.current = starting_point
        while self.can_flow('right') != 'no':
            self.flow_right()
        can_flow_down = self.can_flow('down')
        if can_flow_down == 'yes':
            new_flows.append(self.current)
        elif can_flow_down == 'no':
            basin.append(self.current)
        # if flow is blocked both right and left, stabilize water in the basin
        # and start a new spread one line upper, else follow the flow
        # at the new coordinates found (new_flows[0]) and optionally append
        # the coordinates of the second new flow to self.forks
        if len(basin) == 2:
            for x in range(basin[0][0], basin[1][0]+1):
                self.ground[self.y][x] = '~'
            self.current = (starting_point[0], starting_point[1]-1)
            self.ground[self.y][self.x] = '|'
            self.spread()
        else:
            self.current = new_flows[0]
            try:
                self.forks.append(new_flows[1])
            except IndexError:
                pass    


if __name__ == '__main__':
    ground = Ground(
        input_=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_day17.txt'),
        water_spring=(500, 0)
    )
    water = Water(ground)
    water.flow()

    wet_squares = 0
    stable_water = 0
    for y, row in enumerate(ground.vertical_slice):
        if ground.max_y > y >= ground.min_y:
            stable_water_in_row = row.count('~')
            stable_water += stable_water_in_row
            wet_squares += row.count('|') + stable_water_in_row
        print("".join(row[364:589]))

    print("Number of wet squares in the vertical slice:", wet_squares)
    print("Number of squares of stable water:", stable_water)
