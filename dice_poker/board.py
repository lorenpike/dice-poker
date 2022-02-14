from typing import List, NamedTuple, Tuple

from .dice_patterns import * 
from .color import Color


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
        self.winner = None
        self.create_new_board()

    def create_new_board(self) -> None:
        self.chip_placements = [[None for _ in range(Board.BOARD_SIZE)] for _ in range(Board.BOARD_SIZE)]

    def is_empty(self) -> bool:
        return all([all([el is None for el in row]) for row in self.chip_placements]) 

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

    def get_spots_from_roll(self, roll: List[int]) -> List[Spot]:
        spots = set()
        if not Yahtzee.check(roll):
            for i, row in enumerate(Board.BOARD):
                for j, pattern in enumerate(row):
                    spot = Spot(i,j)
                    if pattern.check(roll) and self.get_spot(spot) is None:
                        spots.add(spot)
        else:
            for i in range(Board.BOARD_SIZE):
                for j in range(Board.BOARD_SIZE):
                    if (i,j) != (4,4):
                        spots.add(Spot(i,j))
        return spots

    @classmethod
    def get_row(cls, row: int) -> List[Spot]:
        return [Spot(row, col) for col in range(cls.BOARD_SIZE)]

    @classmethod
    def get_column(cls, col: int) -> List[Spot]:
        return [Spot(row, col) for row in range(cls.BOARD_SIZE)]

    @staticmethod
    def get_all_diagonals_endpoints() -> List[Tuple[Spot]]:
        return ([(Spot(0,i), Spot(8-i, 8)) for i in range(4)] + 
                [(Spot(0, 8-i), Spot(8-i,0)) for i in range(4)] + 
                [(Spot(i+1,0), Spot(8, 7-i)) for i in range(4)] + 
                [(Spot(7-i,8), Spot(8, i+1)) for i in range(4)] +
                [(Spot(0,4), Spot(4,8)), (Spot(0,4), Spot(4,0))])

    @staticmethod
    def get_diagonal(start: Spot, end: Spot) -> List[Spot]:
        num_col, num_row = end.col - start.col, end.row - start.row
        direction = 1 if num_col > 0 else -1
        num_spots = (abs(num_col) if abs(num_col) < num_row else num_row) + 1
        return [Spot(start.row + i, start.col + (i*direction)) for i in range(num_spots)]

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
        sections.append((tracking, (start, len(strip) - 1)))
        return sections

    @staticmethod
    def pull_sequences_from_sections(sections: List, spots: List[Spot]) -> List[Sequence]:
        sequences = set()
        for sect in sections:
            if type(sect[0]) is Color and sect[1][1] - sect[1][0] + 1 >= 5:
                sequences.add(Sequence(sect[0], spots[sect[1][0]], spots[sect[1][1]]))
        return sequences

    def find_sequence_in_strip(self, strip: List[Spot]) -> Set[Sequence]:
        sections = self.find_contigious_regions(strip)
        sequences = Board.pull_sequences_from_sections(sections, strip)
        return sequences

    @classmethod
    def get_all_strips(cls) -> List[List[Spot]]:
        strips = [get(i) for i in range(cls.BOARD_SIZE) for get in [cls.get_column, cls.get_row]]
        for start, end in Board.get_all_diagonals_endpoints():
            strips.append(Board.get_diagonal(start, end))
        return strips

    def find_sequences(self) -> Set[Sequence]:
        strips = Board.get_all_strips() 
        sequences = set()
        for strip in strips:
            sequences |= self.find_sequence_in_strip(strip)
        return sequences

    def who_won(self) -> Color:
        sequences = self.find_sequences()
        for color in Color:
            if Board.is_there_a_win(sequences, color):
                return color

    def is_won(self) -> bool:
        sequences = self.find_sequences()
        return any(Board.is_there_a_win(sequences, color) for color in Color)

    def is_there_a_win(sequences: Set[Sequence], color: Color):
        return (Board.is_there_a_nine_across(sequences, color) 
                    or 
                Board.is_there_two_sequences(sequences, color))

    @staticmethod
    def is_there_a_nine_across(sequences: Set[Sequence], color: Color) -> bool:
        return any([
            9 in ((seq.end.row - seq.start.row + 1), (seq.end.col - seq.start.col + 1)) 
            and (color == seq.color) for seq in sequences])

    @staticmethod
    def is_there_two_sequences(sequences: Set[Sequence], color: Color) -> bool:
        return sum([color == seq.color for seq in sequences]) >= 2

    def __str__(self) -> str:
        rep = {Color.BLUE: "\033[94mB\033[0m", Color.RED: "\033[91mR\033[0m", None: " "}
        line_sep = "-"*37
        return line_sep+"\n"+("\n"+line_sep+"\n").join(["| " + " | ".join([rep[el] for el in i]) + " |" for i in self.chip_placements])+"\n"+line_sep
