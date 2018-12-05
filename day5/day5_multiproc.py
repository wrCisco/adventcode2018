#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
from multiprocessing import Pool


def reacting_polymer(poly):
    n = 0
    while n < len(poly) - 2:
        if ((0x41 <= poly[n] <= 0x5A and poly[n] == poly[n+1] - 0x20)
                or (0x61 <= poly[n] <= 0x7A and poly[n] == poly[n+1] + 0x20)):
            poly = poly[:n]+poly[n+2:]
            n = max(n-1, 0)
        else:
            n += 1
    return poly


def improving_polymer(data):
    improved = data[1].replace(bytes((data[0],)), b'')
    improved = improved.replace(bytes((data[0]+0x20,)), b'')
    reduced_impr_poly = reacting_polymer(improved)
    return len(reduced_impr_poly)


if __name__ == '__main__':
    with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_day5.txt'),
            'rb'
        ) as fh:
        polymer = fh.read()

    reduced_polymer = reacting_polymer(polymer)

    print("Polymer's length:", len(reduced_polymer))

    ascii_uppercase = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    args_for_child_procs = ((c, formula) for c in ascii_uppercase for formula in (polymer,))

    min_length = len(polymer)
    with Pool(len(os.sched_getaffinity(0))) as p:
        result = p.map_async(improving_polymer, args_for_child_procs)
        res_value = result.get()
        min_length = min(res_value)

    print("Shortest length:", min_length)
