#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os


class Step(object):

    def __init__(self, name: str) -> None:
        self.name = name
        self.blocked_from = []
        self.blocking = []
        self.seconds_to_accomplish = 60 + ord(name) - 0x40


with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_day7.txt'),
        encoding='utf-8'
    ) as fh:
    lines = [line for line in fh.read().split('\n') if line]

steps = {}
for line in lines:
    blocking = line[5]
    blocked = line[-12]
    try:
        blocking_step = steps[blocking]
    except KeyError:
        blocking_step = Step(blocking)
        steps[blocking] = blocking_step
    try:
        blocked_step = steps[blocked]
    except KeyError:
        blocked_step = Step(blocked)
        steps[blocked] = blocked_step
    blocking_step.blocking.append(blocked_step)
    blocked_step.blocked_from.append(blocking_step)

tot_steps = len(steps)
unaccomplished_steps = [ step for step in steps.values() ]
accomplished_steps = []
working_steps = []
free_workers = 5
time = 0

# Solution to the first test:
#
# tot_steps = len(unaccomplished_steps)
# while len(accomplished_steps) < tot_steps:
#     next_step = None
#     for step in unaccomplished_steps:
#         candidate = True
#         for blocking in step.blocked_from:
#             if blocking in unaccomplished_steps:
#                 candidate = False
#         if candidate:
#             try:
#                 if ord(next_step.name) > ord(step.name):
#                     next_step = step
#             except AttributeError:
#                 next_step = step
#     accomplished_steps.append(next_step)
#     unaccomplished_steps.remove(next_step)

# print("Order of steps:", "".join(step.name for step in accomplished_steps))

while len(accomplished_steps) < tot_steps:
    next_steps = []
    for step in unaccomplished_steps:
        candidate = True
        for blocking in step.blocked_from:
            if blocking in unaccomplished_steps or blocking in working_steps:
                candidate = False
        if candidate:
            added = False
            for i, s in enumerate(next_steps):
                if ord(s.name) > ord(step.name):
                    next_steps = next_steps[:i] + [step] + next_steps[i:]
                    added = True
                    break
            if not added:
                next_steps.append(step)

    for step in next_steps:
        if free_workers:
            working_steps.append(step)
            unaccomplished_steps.remove(step)
            free_workers -= 1
    offset = 0
    for i in range(len(working_steps)):
        work = working_steps[i-offset]
        work.seconds_to_accomplish -= 1
        if not work.seconds_to_accomplish:
            accomplished_steps.append(work)
            working_steps.remove(work)
            free_workers += 1
            offset += 1
    time += 1

print("Time to accomplish all the steps for 5 workers:", time)
