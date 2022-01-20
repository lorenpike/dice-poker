from .dice_patterns import * 

class FreeSpace(Pattern):
    @staticmethod
    def check(roll: List[int]) -> bool:
        return True

class Board:
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
        pass

    