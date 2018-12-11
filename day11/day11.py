#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
from multiprocessing import Pool


def compute_largest(data):
    # TODO: reverse the order: instead of beginning from the smallest size,
    # begin from the biggest and memorize partial sums of rows and columns,
    # then proceed by subtraction
    # TODO: check if the maximum value for one size is already under
    # largest's value and skip that iteration
    y = data[0]
    #print("At y:", y)
    grid = data[1]
    largest = [(0,0,0),0]
    for x in range(len(grid)):
        region_power = 0
        for size in range(1, len(grid)-max(x, y)):
            for ry in range(y, y+size):
                rx = x + size-1
                region_power += grid[ry][rx]
            for rx in range(x, x+size-1):
                ry = y + size-1
                region_power += grid[ry][rx]
            if region_power > largest[1]:
                largest[0] = (x+1, y+1, size)
                largest[1] = region_power
    return largest


if __name__ == '__main__':
    serial_number = 7347

    grid = [ [0] * 300 for n in range(300) ]

    for y, line in enumerate(grid, 1):
        for x, cell in enumerate(line, 1):
            rack_id = x + 10
            power_level = int(str(((rack_id * y) + serial_number) * rack_id)[-3]) - 5
            grid[y-1][x-1] = power_level

    args_for_child_procs = ((y, grid_) for y in range(len(grid)) for grid_ in (grid,))
    with Pool(len(os.sched_getaffinity(0))) as p:
        result = p.map_async(compute_largest, args_for_child_procs)
        res_value = result.get()
        largest_power = max(res_value, key=lambda p: p[1])

    print(f"Region with largest power is "
          f"{largest_power[0][0]},{largest_power[0][1]},"
          f"{largest_power[0][2]}x{largest_power[0][2]}")