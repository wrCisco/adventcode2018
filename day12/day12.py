#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from itertools import dropwhile


def check_change_state(states, pots, index, extremes, previous_global_state):
    actual_state = "".join(previous_global_state.get(index+offset, '.') for offset in range(-2, 3))
    for state, next_state in states:
        if actual_state == state:
            pots[index] = next_state
            if index < extremes[0]:
                extremes[0] = index
            elif index > extremes[1]:
                extremes[1] = index
            break

def next_generation(states, pots, extremes):
    global_state = pots.copy()
    for i in range(extremes[0]-2, extremes[1]+3):
        check_change_state(states, pots, i, extremes, global_state)
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
    states = [line.split(' => ') for line in lines[1:]]

    pots = {}
    for i, c in enumerate(initial_state):
        pots[i] = c

    extremes = [0, i]

    for generation in range(50000000000):
        stable = next_generation(states, pots, extremes)
        if generation == 19:
            total_sum_20th = sum(i for i, plant in pots.items() if plant == '#')
        if stable:
            total_sum = sum(i + 50000000000 - (generation+1) for i, plant in pots.items() if plant == '#')
            break
    print("Sum of numbers of pots containing plants after 20 generations:", total_sum_20th)
    print("Sum of numbers of pots containing plants after 50000000000 generations:", total_sum)