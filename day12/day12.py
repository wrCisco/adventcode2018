#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from itertools import dropwhile


def next_generation(states, pots, extremes):
    global_state = pots.copy()
    extremes[0] -= 2
    extremes[1] += 2
    for i in range(extremes[0], extremes[1]+1):
        state = "".join(global_state.get(i+offset, '.') for offset in range(-2, 3))
        pots[i] = states[state]
    for i in range(extremes[0], extremes[0]+len(pots)):
        if pots[i] == '.':
            del pots[i]
            extremes[0] += 1
        else:
            break
    for i in range(extremes[1], extremes[1]-len(pots), -1):
        if pots[i] == '.':
            del pots[i]
            extremes[1] -= 1
        else:
            break
    try:
        stable = True
        for i in range(extremes[0]-1, extremes[1]):
            if global_state[i] != pots[i+1]:
                stable = False
    except KeyError:
        return False
    return stable


if __name__ == '__main__':
    with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_day12.txt'),
            encoding='utf-8'
        ) as fh:
        lines = [line for line in fh.read().split('\n') if line]
    initial_state = lines[0][lines[0].index('#'):]
    states = {}
    for line in lines[1:]:
        rule = line.split(' => ')
        states[rule[0]] = rule[1]

    pots = {}
    for i, c in enumerate(initial_state):
        pots[i] = c

    extremes = [0, i]

    for generation in range(1, 50000000000):
        stable = next_generation(states, pots, extremes)
        #print(f"{generation}: ", "." * abs(extremes[0]), "".join(pots[i] for i in range(extremes[0], extremes[1]+1)), sep="")
        if generation == 20:
            total_sum_20th = sum(i for i, plant in pots.items() if plant == '#')
        if stable:
            total_sum = sum(i + 50000000000 - generation for i, plant in pots.items() if plant == '#')
            break
    print("Sum of numbers of pots containing plants after 20 generations:", total_sum_20th)
    print("Sum of numbers of pots containing plants after 50000000000 generations:", total_sum)
