#!/usr/bin/env python3
# -*- coding: utf-8 -*-


recipes = [3, 7]
cur_index1 = 0
cur_index2 = 1

obj = [7, 9, 3, 0, 6, 1]
while obj not in (recipes[-6:], recipes[-7:-1]):
    recipes.extend(int(x) for x in str(sum((recipes[cur_index1], recipes[cur_index2]))))
    cur_index1 = (cur_index1 + 1 + recipes[cur_index1]) % len(recipes)
    cur_index2 = (cur_index2 + 1 + recipes[cur_index2]) % len(recipes)
    # if len(recipes) in (793071, 793072):
    #     print("Scores of the ten recipes after the first 793061:", "".join(str(x) for x in recipes[793061:793071]))

if recipes[-6:] == obj:
    print(len(recipes)-6)
else:
    print(len(recipes)-7)
