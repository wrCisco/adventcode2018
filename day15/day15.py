#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
from typing import Sequence, Tuple, List, Optional, Union


class Game:

    def __init__(
            self,
            input_: str,
            no_elvish_losses: bool = False,
            elves_attack_power: int = 3
    ) -> None:
        self.cave = self._cave_from_input(input_)
        self.units = self._units_from_cave(elves_attack_power)
        self.no_elvish_losses = no_elvish_losses

    def _cave_from_input(self, input_: str) -> List[List[str]]:
        with open(input_, encoding='utf-8') as fh:
            return [list(line) for line in fh.read().split('\n') if line]


    def _units_from_cave(self, elves_attack_power: int) -> List['Unit']:
        units = []
        for y, line in enumerate(self.cave):
            for x, square in enumerate(line):
                if self.cave[y][x] == 'E':
                    units.append(Unit('Elf', (x, y), self.cave, elves_attack_power))
                elif self.cave[y][x] == 'G':
                    units.append(Unit('Goblin', (x, y), self.cave))
        return units

    def combat(self) -> int:
        rounds = 0
        while self.round():
            rounds += 1
            if not self.no_elvish_losses:
                self.print_cave()
                self.print_stats(rounds)
                input()
        self.print_cave()
        self.print_stats(rounds+1)
        return rounds

    def round(self) -> bool:
        self.units.sort(key=lambda u: (u.y, u.x))
        offset = 0
        remaining_units = self.units.copy()
        for unit in self.units:
            if unit.hit_points <= 0:
                continue
            target = unit.turn(remaining_units)
            # target can be a boolean value or the reference to an attacked unit.
            # False means that the moving unit didn't find any target to attack
            # and so the combat ends.
            # True means that the unit moved without attacking anyone.
            if not target:
                self.units = remaining_units
                return False
            try:
                if target.hit_points <= 0:
                    if self.no_elvish_losses and target.race == 'Elf':
                        return False
                    self.cave[target.y][target.x] = '.'
                    remaining_units.remove(target)
            except AttributeError:
                pass
        self.units = remaining_units
        return True

    def result(self) -> int:
        rounds = self.combat()
        hit_points = sum(max(0, unit.hit_points) for unit in self.units)
        print(rounds, hit_points)
        return rounds * hit_points

    def print_cave(self) -> None:
        for y, line in enumerate(self.cave):
            line_of_cave = "".join(line) + " "
            for x, square in enumerate(line):
                if square in ('G', 'E'):
                    coords = (x, y)
                    for unit in self.units:
                        if unit.coords == coords:
                            line_of_cave += f"{unit.race[0]}({unit.hit_points}) "
                            break
            print(line_of_cave)
        print("")

    def print_stats(self, rounds: int) -> None:
        print(f"Round: {rounds}")
        elves, goblins = 0, 0
        elves_hp, goblins_hp = 0, 0
        for unit in self.units:
            if unit.race == 'Elf':
                elves += 1
                elves_hp += unit.hit_points
            else:
                goblins += 1
                goblins_hp += unit.hit_points
        print(f"Elves: {elves} - Goblins: {goblins}")
        print(f"Elves HP: {elves_hp} - Goblins HP: {goblins_hp}")


class Unit:

    def __init__(
            self,
            race: str,
            coords: Tuple[int, int],
            cave: Sequence[Sequence],
            attack_power: int = 3
    ) -> None:
        self.cave = cave
        self.race = race
        self.x = coords[0]
        self.y = coords[1]
        self.hit_points = 200
        self.attack_power = attack_power
        self.target_letter = 'G' if self.race == 'Elf' else 'E'

    @property
    def coords(self) -> Tuple[int, int]:
        return self.__x, self.__y

    @coords.setter
    def coords(self, values: Tuple[int, int]):
        self.x = values[0]
        self.y = values[1]
    
    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, value: int):
        self.__x = value

    @property
    def y(self) -> int:
        return self.__y
    
    @y.setter
    def y(self, value: int):
        self.__y = value

    def squares_in_range(
            self,
            center: Optional[Tuple[int, int]] = None
    ) -> List[Tuple]:
        if center:
            x, y = center
        else:
            x, y = self.x, self.y
        return [
            (x, y-1),
            (x-1, y),
            (x+1, y),
            (x, y+1)
        ]

    def open_squares_in_range(
            self,
            center: Optional[Tuple[int, int]] = None
    ) -> List[Tuple]:
        return [sq for sq in self.squares_in_range(center) if self.cave[sq[1]][sq[0]] == '.']

    def attack(self, targets: 'Unit') -> Optional['Unit']:
        candidates = []
        for target in targets:
            if target.coords in self.squares_in_range():
                candidates.append(target)
        if candidates:
            candidates.sort(key=lambda target: (target.hit_points, target.y, target.x))
            candidates[0].hit_points -= self.attack_power
            return candidates[0]
        return

    def move(self, targets: 'Unit') -> None:
        targets_squares_in_range = []
        for target in targets:
            targets_squares_in_range.extend(target.open_squares_in_range())
        if not targets_squares_in_range:
            return
        paths = [[coord] for coord in self.open_squares_in_range()]
        if not paths:
            return
        reached_squares = set(self.open_squares_in_range())
        prev_reached_squares = reached_squares.copy()
        paths_to_targets = []
        for path in paths:
            if path[-1] in targets_squares_in_range:
                paths_to_targets.append(path)
        while not paths_to_targets:
            new_paths = []
            for i, path in enumerate(paths):
                continuations = self.open_squares_in_range(path[-1])
                forks = False
                for cont in continuations:
                    if cont in reached_squares:
                        continue
                    reached_squares.add(cont)
                    if not forks:
                        path.append(cont)
                        forks = True
                    else:
                        new_path = path.copy()[:-1]
                        new_path.append(cont)
                        new_paths.append((new_path, i))
            for offset, path in enumerate(new_paths, 1):
                paths.insert(path[1] + offset, path[0])
            for path in paths:
                if path[-1] in targets_squares_in_range:
                    paths_to_targets.append(path)
            if prev_reached_squares == reached_squares:
                return
            prev_reached_squares.update(reached_squares)
        step = None
        for sq in self.open_squares_in_range():
            for path in paths_to_targets:
                if path[0] == sq:
                    step = sq
                    break
            if step:
                break
        self.cave[self.y][self.x] = '.'
        self.coords = step
        self.cave[self.y][self.x] = self.race[0]


    def turn(self, units: Sequence['Unit']) -> Union[bool, 'Unit']:
        targets = [unit for unit in units if unit.race != self.race]
        if not targets:
            return False
        target = self.attack(targets)
        if target:
            #print(f"Unit at {self.coords} attacked unit at {target.coords}.")
            return target
        self.move(targets)
        target = self.attack(targets)
        if target:
            #print(f"Unit at {self.coords} attacked unit at {target.coords}.")
            return target
        return True


if __name__ == '__main__':
    game = Game(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'input_day15.txt'
            #'test_input_1.txt'
        )
    )
    elves = sum(1 for unit in game.units if unit.race == 'Elf')
    print("Outcome of battle:", game.result())

    elves_attack = 4
    elves_perfect = False
    while not elves_perfect:
        game = Game(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'input_day15.txt'
            ),
            True,
            elves_attack
        )
        outcome = game.result()
        if elves == len(game.units):
            elves_perfect = True
        else:
            elves_attack += 1
    print("Outcome of battle:", outcome, f"(elves's attack power: {elves_attack})")
