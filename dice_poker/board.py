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
        self.winner = None
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
        sections.append((tracking, (start, len(strip) - 1)))
        return sections

    @staticmethod
    def get_row(row: int) -> List[Spot]:
        row_spots = []
        for col in range(Board.BOARD_SIZE):
            row_spots.append(Spot(row, col))
        return row_spots

    @staticmethod
    def get_column(col: int) -> List[Spot]:
        col_spots = []
        for row in range(Board.BOARD_SIZE):
            col_spots.append(Spot(row, col))
        return col_spots

    @staticmethod
    def get_diagonal(start: Spot, end: Spot) -> List[Spot]:
        spots = []

        num_col = end.col - start.col 
        num_row = end.row - start.row

        direction = 1 if num_col > 0 else -1
        num_spots = (abs(num_col) if abs(num_col) < num_row else num_row) + 1
        for i in range(num_spots):
            spots.append(Spot(start.row + i, start.col + (i*direction)))
        return spots

    @staticmethod
    def pull_sequences_from_sections(sections: List, spots: List[Spot]) -> List[Sequence]:
        sequences = set()
        for sect in sections:
            if type(sect[0]) is Color and sect[1][1] - sect[1][0] + 1 >= 5:
                sequences.add(Sequence(sect[0], spots[sect[1][0]], spots[sect[1][1]]))
        return sequences

    @staticmethod
    def get_all_diagonals_endpoints() -> List[Tuple[Spot]]:
        endpoints = []
        for i in range(5):
            endpoints.append((Spot(0,i), Spot(8-i, 8)))
            endpoints.append((Spot(0, 8-i), Spot(8-i,0)))
            if i !=4:
                endpoints.append((Spot(i+1,0), Spot(8, 7-i)))
                endpoints.append((Spot(7-i,8), Spot(8, i+1)))
        return endpoints

    def find_sequence_in_strip(self, strip: List[Spot]) -> Set[Sequence]:
        sections = self.find_contigious_regions(strip)
        sequences = Board.pull_sequences_from_sections(sections, strip)
        return sequences

    def find_horizontal_sequences(self) -> Set[Sequence]:
        sequences = set()
        for row in range(Board.BOARD_SIZE):
            row = Board.get_row(row)
            sequences |= self.find_sequence_in_strip(row)
        return sequences

    def find_vertical_sequences(self) -> Set[Sequence]:
        sequences = set()
        for col in range(Board.BOARD_SIZE):
            col = Board.get_column(col)
            sequences |= self.find_sequence_in_strip(col)
        return sequences

    def find_diagonal_sequences(self) -> Set[Sequence]:
        sequences = set()
        for start, end in Board.get_all_diagonals_endpoints():
            diag = Board.get_diagonal(start, end)
            sequences |= self.find_sequence_in_strip(diag)
        return sequences

    def find_sequences(self) -> Set[Sequence]:
        horizontal = self.find_horizontal_sequences()
        vertical = self.find_vertical_sequences()
        diagonal = self.find_diagonal_sequences()
        return diagonal | vertical | horizontal 

    def who_won(self) -> Color:
        return self.winner

    def is_won(self) -> bool:
        sequences = self.find_sequences()
        seq_map = {Color.RED: 0, Color.BLUE:0}
        for seq in sequences:
            seq_map[seq.color] += 1
            if seq_map[seq.color] == 2:
                self.winner = seq.color
                return True
            if seq.end.row - seq.start.row == 8:
                self.winner = seq.color
                return True
            if seq.end.col - seq.start.col == 8:
                self.winner = seq.color
                return True
        return False

    def __str__(self) -> str:
        rep = {Color.BLUE: "B", Color.RED: "R", None: "0"}
        return "\n".join([" ".join([rep[el] for el in i]) for i in self.chip_placements])
