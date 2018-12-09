#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Player:

    def __init__(self, id_: int) -> None:
        self.id = id_
        self.score = 0


class Marble:

    def __init__(self, value: int, next_: 'Marble' = None, prev: 'Marble' = None):
        self.value = value
        self.next_marble = next_ if next_ else self
        self.prev_marble = prev if prev else self

    def insert(self, marble: 'Marble', offset: int = 0):
        m = self
        if offset >= 0:
            for n in range(offset):
                m = m.next_marble
        elif offset < 0:
            for n in range(-offset):
                m = m.prev_marble
        marble.next_marble = m.next_marble
        marble.prev_marble = m
        m.next_marble.prev_marble = marble
        m.next_marble = marble
    
    def remove(self, offset: int = 0):
        m = self
        if offset >= 0:
            for n in range(offset):
                m = m.next_marble
        elif offset < 0:
            for n in range(-offset):
                m = m.prev_marble
        m.prev_marble.next_marble = m.next_marble
        m.next_marble.prev_marble = m.prev_marble
        return m


class Game:

    def __init__(self, players: int, last_marble: int) -> None:
        self.last_marble = last_marble
        self.players = [Player(n) for n in range(players)]
        self.current_player = 0
        self.current_marble: Marble

    def play_game(self) -> Player:
        self.current_marble = Marble(0)
        for marble in range(1, self.last_marble+1):
            self.round(marble)
        return max(self.players, key=lambda p: p.score)

    def round(self, marble_value):
        if marble_value % 23:
            new_marble = Marble(marble_value)
            self.current_marble.insert(new_marble, 1)
            self.current_marble = new_marble
        else:
            other_marble = self.current_marble.remove(-7)
            self.players[self.current_player].score += marble_value + other_marble.value
            self.current_marble = other_marble.next_marble
        self.current_player += 1
        if self.current_player >= len(self.players):
            self.current_player = 0


if __name__ == '__main__':
    game = Game(players=416, last_marble=71975)
    winner = game.play_game()
    print("Score of the winning player:", winner.score)

    game = Game(players=416, last_marble=7197500)
    winner = game.play_game()
    print("Score of the winning player:", winner.score)
