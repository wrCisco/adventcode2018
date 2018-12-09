#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Player:

    def __init__(self, id_: int) -> None:
        self.id = id_
        self.score = 0


class Game:

    def __init__(self, players: int, last_marble: int) -> None:
        self.circle = []
        self.last_marble = last_marble
        self.players = [Player(n) for n in range(players)]
        self.current_player = 0
        self.current_marble_index: int

    def play_game(self) -> Player:
        self.start_game()
        for marble in range(1, self.last_marble+1):
            self.round(marble)
        return max(self.players, key=lambda p: p.score)

    def start_game(self) -> None:
        self.circle.append(0)
        self.current_marble_index = 0

    def round(self, next_marble):
        if next_marble % 23:
            pos = self.current_marble_index + 2
            if pos > len(self.circle):
                pos = pos - len(self.circle)
            self.circle.insert(pos, next_marble)
            self.current_marble_index = pos
        else:
            other_marble_index = self.current_marble_index - 7
            if other_marble_index < 0:
                other_marble_index = len(self.circle) + other_marble_index
            self.players[self.current_player].score += (next_marble
                                                       + self.circle[other_marble_index])
            self.circle.pop(other_marble_index)
            self.current_marble_index = other_marble_index
        self.current_player += 1
        if self.current_player >= len(self.players):
            self.current_player = 0

    def print_circle(self):
        m = ''
        marbles = "   ".join(m for m in self.circle)
        print(f'[{self.current_player}] ')


if __name__ == '__main__':
    game = Game(players=416, last_marble=71975)
    winner = game.play_game()
    print("Score of the winning player:", winner.score)

