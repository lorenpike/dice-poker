from .board import Board
from .color import Color

class Game:
    def __init__(self) -> None:
        self._board = Board()
        self._turn = Color.BLUE

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
