from enum import Enum
from typing import List, NamedTuple, Tuple

from .dice_patterns import * 


class FreeSpace:
    pass

class Color(Enum):
    RED = 0
    BLUE = 1

class Spot(NamedTuple):
    row: int
    col: int

class Sequence(NamedTuple):
    color: Color
    start: Spot
    end: Spot

class Board:
    BOARD_SIZE = 9
    FREE_SPACE = Spot(4,4)

    BOARD = [
        [Straight(), Double(6,6), Double(5,6), Double(4,6), Pair(2), Double(3,6), Double(2,6), Double(1,6), Straight()],
        [Pair(6), FullHouse(), Double(1,5), Double(2,5), Double(3,5),Double(4,5), Double(5,5), FullHouse(), Pair(4)],
        [Double(4,4), Triple(2), FullHouse(), Double(3,4), Double(1,1), Double(2,4), FullHouse(), Triple(6), Double(1,4)],
        [Triple(4), Triple(1), Double(3,3), FullHouse(), Double(2,3), FullHouse(), Double(1,3), Triple(3), Triple(5)],
        [Lucky7(), Double(1,2), Lucky11(), Double(2,2), FreeSpace(), Double(2,2), Lucky11(), Double(1,2), Lucky7()],
        [Triple(5), Triple(3), Double(1,3), FullHouse(), Double(2,3), FullHouse(), Double(3,3), Triple(1), Triple(4)],
        [Double(1,4), Triple(6), FullHouse(), Double(2,4), Double(1,1), Double(3,4), FullHouse(), Triple(2), Double(4,4)],
        [Pair(5), FullHouse(), Double(5,5), Double(4,5), Double(3,5), Double(2,5), Double(1,5), FullHouse(), Pair(3)],
        [Straight(), Double(1,6), Double(2,6), Double(3,6), Pair(1), Double(4,6), Double(5,6), Double(6,6), Straight()]
    ]

    def __init__(self) -> None:
        self.create_new_board()

    def create_new_board(self):
        self.chip_placements = [[None for _ in range(Board.BOARD_SIZE)] for _ in range(Board.BOARD_SIZE)]

    def place_blue_chip(self, row: int, col: int):
        self.place_chip(Color.BLUE, row, col)

    def place_red_chip(self, row: int, col: int):
        self.place_chip(Color.RED, row, col)

    @staticmethod
    def is_on_board(row: int, col: int):
        if row > 8 or row < 0 or col > 8 or col < 0:
            raise ValueError("Placement is out of range")

    def check_valid_placement(self, row: int, col: int):
        Board.is_on_board(row, col)
        if row == 4 and col ==4:
            raise ValueError("Cannot place chip on Free Space")
        if self.chip_placements[row][col] is not None:
            raise ValueError("Spot is already claimed")
        
    def place_chip(self, color: Color, row: int, col: int):
        self.check_valid_placement(row, col)
        self.chip_placements[row][col] = color

    def get_spot(self, spot: Spot):
        Board.is_on_board(spot.row, spot.col)
        return self.chip_placements[spot.row][spot.col]

    def find_contigious_regions(self, strip: List[Spot]):
        sections = []
        first_spot = strip[0]
        tracking = self.get_spot(first_spot)
        start = 0
        for i, spot in enumerate(strip):
            if self.get_spot(spot) != tracking and spot != Board.FREE_SPACE:
                sections.append((tracking, (start, i-1)))
                start = i
                tracking = self.get_spot(spot)
                if strip[i-1] == Board.FREE_SPACE:
                    start -= 1
        sections.append((tracking, (start, Board.BOARD_SIZE - 1)))
        return sections

    def find_horizontal_sequence_in_row(self, row: int):
        row_spots = []
        for col in range(Board.BOARD_SIZE):
            row_spots.append(Spot(row, col))
        sections = self.find_contigious_regions(row_spots)
        sequences = []
        for sect in sections:
            if sect[0] in {Color.BLUE, Color.RED} and sect[1][1] - sect[1][0] + 1 >= 5:
                sequences.append(sect)
        return sequences

    def find_horizontal_sequences(self):
        sequences = set()
        for col in range(Board.BOARD_SIZE):
            seqs = self.find_horizontal_sequence_in_row(col)
            for s in seqs:
                sequences.add(Sequence(s[0], Spot(col, s[1][0]), Spot(col, s[1][1])))
        return sequences


    def __str__(self) -> str:
        return "\n".join([" ".join(i) for i in self.chip_placements])

def find_longest_sequence(nums: List[int]):
    nums.sort()
    longest_seq = seq = []
    for i, el in enumerate(nums):
        seq.append(el)
        if len(nums) == i + 1 or el + 1 != nums[i+1]:
            if len(seq) >= len(longest_seq):
                longest_seq = seq
            seq = []
    return longest_seq
