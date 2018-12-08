#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os


class Node:

    def __init__(self, children: int, metadata: int) -> None:
        self.num_children = children
        self.num_metadata = metadata
        self.children = []
        self.metadata = []

    def sum_metadata(self):
        if not self.children:
            return sum(self.metadata)
        sum_meta = 0
        for child in self.children:
            sum_meta += child.sum_metadata()
        return sum(self.metadata) + sum_meta

    def value(self):
        if not self.children:
            return sum(self.metadata)
        value = 0
        for i in self.metadata:
            if i:
                try:
                    value += self.children[i-1].value()
                except IndexError:
                    pass
        return value


def parse_node(sequence: list, root: Node = None, father: Node = None, index: int = 0):
    if index >= len(sequence) - 2:
        return root, index
    else:
        child = Node(sequence[index], sequence[index+1])
        if not root:
            root = child
        if not father:
            father = child
        else:
            father.children.append(child)
        index += 2
        for n in range(child.num_children):
            root, index = parse_node(sequence, root, child, index)
        for n in range(child.num_metadata):
            child.metadata.append(sequence[index])
            index += 1
        return root, index


if __name__ == '__main__':
    with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_day8.txt'),
            encoding='utf-8'
        ) as fh:
        numbers = [int(num) for num in fh.read().split() if num]

    root, _ = parse_node(numbers)
    print("Sum of metadata is", root.sum_metadata())
    print("Value of the root node is", root.value())
