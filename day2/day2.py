#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os


def count_checksum(rows):
    twos = 0
    threes = 0
    for row in rows:
        letters = {}
        for c in row:
            try:
                letters[c] += 1
            except KeyError:
                letters[c] = 1
        for val in letters.values():
            if val == 2:
                twos += 1
                break
        for val in letters.values():
            if val == 3:
                threes += 1
                break
    return twos * threes


def compare_line(row, other):
    equals = ''
    different = 0
    for i, c in enumerate(row):
        if row[i] == other[i]:
            equals += row[i]
        else:
            different += 1
            if different > 1:
                return False
    return equals


def compare_lines(rows):
    for i, row in enumerate(rows):
        for other in rows[1:]:
            if row == other:
                continue
            eq = compare_line(row, other)
            if eq:
                return eq


with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_day2.txt'),
        encoding='utf-8'
    ) as fh:
    lines = [line for line in fh.read().split('\n') if line]

checksum = count_checksum(lines)
print("The checksum is", checksum)

common_letters = compare_lines(lines)
print("The common letters of the two boxes id are", common_letters)
