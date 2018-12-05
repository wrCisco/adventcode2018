#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os


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


if __name__ == '__main__':
    with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_day5.txt'),
            'rb'
        ) as fh:
        polymer = fh.read()

    reduced_polymer = reacting_polymer(polymer)

    print("Polymer's length:", len(reduced_polymer))

    ascii_uppercase = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    min_length = len(polymer)
    for c in ascii_uppercase:
        improved_polymer = polymer.replace(bytes((c,)), b'')
        improved_polymer = improved_polymer.replace(bytes((c+0x20,)), b'')
        reduced_impr_poly = reacting_polymer(improved_polymer)
        if min_length > len(reduced_impr_poly):
            min_length = len(reduced_impr_poly)

    print("Shortest length:", min_length)
