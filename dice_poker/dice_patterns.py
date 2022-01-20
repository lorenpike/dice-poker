from typing import Dict, List, Set, Union
from abc import ABCMeta
from abc import abstractmethod

class Pattern(metaclass=ABCMeta):
    @abstractmethod
    def check(roll: List[int]) -> bool:
        raise NotImplementedError

    @staticmethod
    def hash_roll(roll: List[int]) -> Dict[int, int]:
        roll_count = dict()
        for r in roll:
            if r not in roll_count:
                roll_count[r] = 0
            roll_count[r] += 1
        return roll_count

    def __repr__(self) -> str:
        return self.__class__.__name__
    
    def __str__(self) -> str:
        return self.__class__.__name__


class Double(Pattern):
    def __init__(self, *nums: int) -> None:
        self.double = nums

    def check(self, roll: List[int]) -> bool:
        if len(set(self.double)) == 1:
            try:
                num = self.double[0]
                return Pattern.hash_roll(roll)[num] >= 4
            except KeyError:
                return False
        else:
            return all(Pair(n).check(roll) for n in self.double)

    def __str__(self) -> str:
        a, b = self.double
        first, second = (a, b) if a < b else (b, a)
        return f"{self.__class__.__name__}({first},{second})"

class Pair(Pattern):
    def __init__(self, num: int) -> None:
        self.pair_of = num

    def check(self, roll: List[int]) -> bool:
        try:
            return Pattern.hash_roll(roll)[self.pair_of] >= 2
        except KeyError:
            return False

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pair_of})"

class Triple(Pattern):
    def __init__(self, num: int) -> None:
        self.triple_of = num

    def check(self, roll: List[int]) -> Union[int, bool]:
        try:
            return Pattern.hash_roll(roll)[self.triple_of] >= 3
        except KeyError:
            return False
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.triple_of})"

class FullHouse(Pattern):
    @staticmethod
    def check(roll: List[int]) -> bool:
        return len(set(roll)) == 2 and 2 in Pattern.hash_roll(roll).values()

class Yahtzee(Pattern):
    @staticmethod
    def check(roll: List[int]) -> bool:
        return len(set(roll)) == 1

class Straight(Pattern):
    @staticmethod
    def check(roll: List[int]) -> bool:
        return len(set(roll)) == 5 and (1 not in roll or 6 not in roll)

class Lucky11(Pattern):
    @staticmethod
    def check(roll: List[int]) -> bool:
        return sum(roll) == 11

class Lucky7(Pattern):
    @staticmethod
    def check(roll: List[int]) -> bool:
        return sum(roll) == 7


class RollChecker(Pattern):
    @staticmethod
    def check(roll: List[int]) -> Set[str]:
        patterns = [
            FullHouse(),
            Straight(),
            Lucky11(),
            Lucky7(),
            Yahtzee()
        ]

        for i in range(1,7):
            patterns.append(Pair(i))
            patterns.append(Triple(i))
            for j in range(i,7):
                patterns.append(Double(i,j))

        return set(str(pattern) for pattern in patterns if pattern.check(roll))

    @staticmethod
    def check_types(roll: List[int]) -> Set[str]:
        patterns = [
            FullHouse(),
            Straight(),
            Lucky11(),
            Lucky7(),
            Yahtzee()
        ]

        for i in range(1,7):
            patterns.append(Pair(i))
            patterns.append(Triple(i))
            for j in range(i,7):
                patterns.append(Double(i,j))

        return set(repr(pattern) for pattern in patterns if pattern.check(roll))

    
