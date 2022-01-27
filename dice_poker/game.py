from typing import List

from .board import Board, Spot
from .color import Color
from .dice import Dice

class Game:
    def __init__(self) -> None:
        self._board = Board()
        self._turn = Color.BLUE
        self.rolls = 0
        self._dice = Dice()

    @classmethod
    def start_new_game(cls):
        return cls()

    @property
    def board(self):
        return self._board

    @property
    def turn(self):
        return self._turn
    
    @turn.setter
    def turn(self, color: Color):
        self._turn = color

    @property
    def dice(self):
        return self._dice.dice
    
    def roll(self, mask: List[bool] = None):
        if self.rolls == 0:
            if mask is not None:
                raise ValueError("Cannot mask before the first roll")
            self.rolls += 1
            self._dice.new_roll() 
        elif 0 < self.rolls < 3:
            if mask is None:
                mask = [0,0,0,0,0]
            self.rolls += 1
            _ = self._dice.reroll(mask)
        else:
            raise ValueError("Only allowed three rolls")

    def get_possible_placements(self):
        return self.board.get_spots_from_roll(self.dice)

    def place_chip(self, row=int, col=int):
        if Spot(row, col) in self.get_possible_placements():
            self.board.place_chip(self.turn, row=row, col=col)
        else:
            raise ValueError("Placement does not match pattern on dice")
    
    def is_finished(self):
        return self.board.is_won()

    def who_won(self):
        return self.board.who_won()