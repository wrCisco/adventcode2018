#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
from typing import Union


class Cart:

    track: list
    directions = '<^>v'
    groundbackslash = {
        '>': 'v',
        'v': '>',
        '^': '<',
        '<': '^'
    }
    groundslash = {
        '>': '^',
        '^': '>',
        '<': 'v',
        'v': '<'
    }

    def __init__(self, coordinates: tuple, direction: str) -> None:
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.dir = direction
        self.movements = {
            '>': self.move_right,
            '<': self.move_left,
            '^': self.move_up,
            'v': self.move_down
        }
        self.intersections = 0
        self.ground = '-' if self.dir in ('>', '<') else '|'

    def move(self) -> None:
        Cart.track[self.y][self.x] = self.ground
        self.movements[self.dir]()
        self.ground = Cart.track[self.y][self.x]
        if self.ground == '\\':
            self.dir = Cart.groundbackslash[self.dir]
        elif self.ground == '/':
            self.dir = Cart.groundslash[self.dir]
        elif self.ground == '+':
            if self.intersections == 0:
                self.turn('left')
            elif self.intersections == 2:
                self.turn('right')
            self.intersections = (self.intersections + 1) % 3

    def turn(self, way: str) -> None:
        d = 1 if way == 'right' else -1
        index = (Cart.directions.index(self.dir) + d) % 4
        self.dir = Cart.directions[index]

    def move_right(self) -> None:
        self.x += 1

    def move_left(self) -> None:
        self.x -= 1

    def move_down(self) -> None:
        self.y += 1

    def move_up(self) -> None:
        self.y -= 1

    def crash(self, other: 'Cart') -> bool:
        return (self.x, self.y) == (other.x, other.y)

    def remove_from_track(self) -> None:
        Cart.track[self.y][self.x] = self.ground


def tick(carts: list) -> Union[tuple, None]:
    carts.sort(key=lambda c: (c.y, c.x))
    first_crash = None
    removed = []
    for i in range(len(carts)):
        if i in removed:
            continue
        carts[i].move()
        for j in range(len(carts)):
            if j in removed:
                continue
            if carts[i] is not carts[j] and carts[i].crash(carts[j]):
                carts[i].remove_from_track()
                removed.extend([i, j])
                if not first_crash:
                    first_crash = carts[i].x, carts[i].y
    carts[:] = (carts[i] for i in range(len(carts)) if i not in removed)
    return first_crash


def main() -> None:
    with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_day13.txt'),
            encoding='utf-8'
        ) as fh:
        Cart.track = [list(line) for line in fh.read().split('\n') if line]

    carts = []
    for i, y in enumerate(Cart.track):
        for j, x in enumerate(y):
            if x in Cart.directions:
                carts.append(Cart((j, i), x))

    while True:
        first_crash = tick(carts)
        if first_crash:
            break
    print("Coordinates of first crash:", first_crash)

    while True:
        tick(carts)
        if len(carts) == 1:
            break
    print("Coordinates of last cart standing:", (carts[0].x, carts[0].y))


if __name__ == '__main__':
    main()
