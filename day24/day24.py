#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import re
from enum import Enum
from copy import deepcopy
from typing import Sequence, List, Tuple, Optional


class AttackTypes(Enum):
    SLASHING = 'slashing'
    RADIATION = 'radiation'
    COLD = 'cold'
    FIRE = 'fire'
    BLUDGEONING = 'bludgeoning'


class Attack:

    def __init__(self, type_: AttackTypes, damage: int) -> None:
        self.type = type_
        self.damage = damage


class Group:

    def __init__(
            self,
            units: int,
            hit_points: int,
            immunities: Sequence[AttackTypes],
            weaknesses: Sequence[AttackTypes],
            attack: Attack,
            initiative: int,
            army: Optional['Army'] = None
    ) -> None:
        self.units = units
        self.hit_points = hit_points
        self.immunities = immunities
        self.weaknesses = weaknesses
        self.attack = attack
        self.initiative = initiative
        self.army = army

    @property
    def effective_power(self) -> int:
        return self.units * self.attack.damage

    @effective_power.setter
    def effective_power(self, value: int):
        raise ValueError('effective_power attribute never can be set.')

    def damage_estimate(self, other: 'Group') -> int:
        if self.attack.type in other.immunities:
            return 0
        elif self.attack.type in other.weaknesses:
            return self.effective_power * 2
        else:
            return self.effective_power

    def launch_attack(self, other: 'Group') -> int:
        damage = self.damage_estimate(other)
        killed_units = min(damage // other.hit_points, other.units)
        other.units -= killed_units
        return killed_units

    def info_dump(self) -> None:
        print(
            f'Units: {self.units}\n'
            f'Hit points: {self.hit_points}\n'
            f'Immunities: {", ".join(i.value for i in self.immunities)}\n'
            f'Weaknesses: {", ".join(w.value for w in self.weaknesses)}\n'
            f'Attack: {self.attack.damage} of {self.attack.type.value} damage\n'
            f'Initiative: {self.initiative}\n'
            f'Army: {self.army.name}\n'
        )


class Army:

    def __init__(self, name: str, groups: Sequence[Group]) -> None:
        self.name = name
        self.groups = groups
        for group in self.groups:
            group.army = self


class Combat:

    def __init__(self, immune_system: Army, infection: Army) -> None:
        self.immune_system = immune_system
        self.infection = infection

    @property
    def groups(self) -> List[Group]:
        groups = self.immune_system.groups + self.infection.groups
        groups.sort(key=lambda group: (group.effective_power, group.initiative), reverse=True)
        return groups

    @groups.setter
    def groups(self) -> None:
        raise ValueError('groups attribute of Combat instance cannot be directly set.')

    def combat(self) -> Optional[Army]:
        while self.immune_system.groups and self.infection.groups:
            killed_units = self.fight()
            if not killed_units:
                return None
        if self.immune_system.groups:
            return self.immune_system
        else:
            return self.infection

    def fight(self) -> None:
        killed_units = self.attacking(self.target_selection())
        to_remove = [group for group in self.groups if group.units <= 0]
        for group in to_remove:
            group.army.groups.remove(group)
        return killed_units

    def target_selection(self) -> List[Tuple[Group, Group]]:
        fighting_groups = []
        targets = []
        for group in self.groups:
            possible_targets = []
            max_damage = 0
            if group.army.name == 'infection':
                enemies = self.immune_system.groups
            else:
                enemies = self.infection.groups
            for enemy in enemies:
                if enemy in targets:
                    continue
                estimated_damage = group.damage_estimate(enemy)
                if estimated_damage and estimated_damage == max_damage:
                    possible_targets.append(enemy)
                elif estimated_damage > max_damage:
                    max_damage = estimated_damage
                    possible_targets = [enemy]
            if possible_targets:
                possible_targets.sort(key=lambda group: (group.effective_power, group.initiative), reverse=True)
                target = possible_targets[0]
                fighting_groups.append((group, target))
                targets.append(target)
        return fighting_groups

    def attacking(self, fighting_groups: List[Tuple[Group, Group]]) -> int:
        fighting_groups.sort(key=lambda group: group[0].initiative, reverse=True)
        # print("\n\n\n\n\n\n\n\n\n!!!\nNew round\n!!!\n\n\n\n\n\n")
        killed_units = 0
        for attacker, defender in fighting_groups:
            if attacker.units <= 0:
                continue
            # print("Attacker:")
            # attacker.info_dump()
            # print("Defender (before):")
            # defender.info_dump()
            killed_units += attacker.launch_attack(defender)
            # print("Defender (after):")
            # defender.info_dump()
        return killed_units


def build_groups(description: str) -> Sequence[Group]:
    descriptions = [line for line in description.splitlines() if line]
    groups = []
    for descr in descriptions[1:]:
        units, hit_points, damage, initiative = [int(val) for val in re.findall(r'\d+', descr)]
        characteristics = ([], [])  # weaknesses, immunities
        characteristics_descr = ('weak to ', 'immune to ')
        for i, c in enumerate(characteristics_descr):
            index = descr.find(c)
            if index != -1:
                index += len(c)
                try:
                    characteristic_values = descr[index:descr[index:].index(';')+index].split(', ')
                    characteristics[i].extend([AttackTypes(val) for val in characteristic_values if val])
                except ValueError:
                    characteristic_values = descr[index:descr[index:].index(')')+index].split(', ')
                    characteristics[i].extend([AttackTypes(val) for val in characteristic_values if val])
        attack_type = AttackTypes(
            re.search(r'attack that does \d+ (\w+)', descr).group(1)
        )
        attack = Attack(attack_type, damage)
        group = Group(
            units,
            hit_points,
            characteristics[1],  # immunities
            characteristics[0],  # weaknesses
            attack,
            initiative
        )
        groups.append(group)
    return groups


if __name__ == '__main__':
    with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_day24.txt'),
            encoding='utf-8'
        ) as fh:
        imm_sys, inf = fh.read().split('\n\n')

    immune_system_groups = build_groups(imm_sys)
    infection_groups = build_groups(inf)

    immune_system = Army('immune_system', deepcopy(immune_system_groups))
    infection = Army('infection', deepcopy(infection_groups))

    # print('Immune system:\n')
    # for group in immune_system.groups:
    #     group.info_dump()
    # print('\nInfection:\n')
    # for group in infection.groups:
    #     group.info_dump()

    combat = Combat(immune_system, infection)
    winner = combat.combat()

    print(f'The winner is {winner.name}, with {sum(group.units for group in winner.groups)} units standing.')
    # for group in winner.groups:
    #     group.info_dump()

    boost = 1000
    upper_limit, lower_limit = 0, 0
    while not upper_limit - lower_limit == 1:
        prev_boost = boost
        immune_system = Army('immune_system', deepcopy(immune_system_groups))
        infection = Army('infection', deepcopy(infection_groups))
        for group in immune_system.groups:
            group.attack.damage += boost
        combat = Combat(immune_system, infection)
        winner = combat.combat()
        if not winner or winner.name == 'infection':
            lower_limit = boost
            if upper_limit:
                limits_sum = upper_limit + lower_limit
                boost = limits_sum // 2 + limits_sum % 2
            else:
                boost += 1000
        elif winner.name == 'immune_system':
            upper_limit = boost
            limits_sum = upper_limit + lower_limit
            boost = limits_sum // 2 + limits_sum % 2

    print("Minimum boost to give to immune system in order for him to win is", prev_boost)
    print(f'With boost of {prev_boost} {winner.name} wins with {sum(group.units for group in winner.groups)} units standing.')
