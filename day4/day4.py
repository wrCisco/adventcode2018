#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
from datetime import datetime
import re


class Guard:
    def __init__(self, id_):
        self.id = id_
        self.minutes_sleeping = []


def find_favorite_minute(guard):
    mins_dict = {}
    for minute in guard.minutes_sleeping:
        try:
            mins_dict[minute] += 1
        except KeyError:
            mins_dict[minute] = 1

    favorite_minute = None
    max_times = 0
    for minute, times in mins_dict.items():
        if max_times < times:
            max_times = times
            favorite_minute = minute
    return favorite_minute, max_times


with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_day4.txt'),
        encoding='utf-8'
    ) as fh:
    lines = [line for line in fh.read().split('\n') if line]

lines.sort(key=lambda line: datetime.strptime(line[1:17], '%Y-%m-%d %H:%M'))

guards = {}

for line in lines:
    if 'begins shift' in line:
        id_ = re.search(r'#(\d+)', line).group(1)
        try:
            guards[id_]
        except KeyError:
            guards[id_] = Guard(int(id_))
    elif 'falls asleep' in line:
        start = int(re.search(r'\d+:(\d+)', line).group(1))
    elif 'wakes up' in line:
        end = int(re.search(r'\d+:(\d+)', line).group(1))
        guards[id_].minutes_sleeping.extend(range(start, end))

max_min_asleep = 0
for id_, guard in guards.items():
    if max_min_asleep < len(guard.minutes_sleeping):
        max_min_asleep = len(guard.minutes_sleeping)
        sleepy_guard = guard

print("The sleepy guard is", sleepy_guard.id)

favmin, times_asleep = find_favorite_minute(sleepy_guard)

print("His favorite minute for snap is", favmin)
print("So, the product of the two numbers is", sleepy_guard.id * favmin)

max_mins_dict = tuple()
for id_, guard in guards.items():
    favmin, times_asleep = find_favorite_minute(guard)
    if not max_mins_dict or max_mins_dict[2] < times_asleep:
        max_mins_dict = (guard, favmin, times_asleep)

print("The guard who spent the same minute most asleep is id", max_mins_dict[0].id)
print("The minute most spent asleep is", max_mins_dict[1], f"({max_mins_dict[2]} times)") 
print("And their product is", max_mins_dict[0].id * max_mins_dict[1])
