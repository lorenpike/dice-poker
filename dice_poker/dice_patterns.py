from asyncio.proactor_events import _ProactorBaseWritePipeTransport
from typing import Dict, List, Union
from abc import ABCMeta
from abc import abstractmethod

class Pattern(metaclass=ABCMeta):
    @staticmethod
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


class Double(Pattern):
   @staticmethod
   def check(roll: List[int]) -> bool:
       return len(set(roll)) < 5

class Pair(Pattern):
    @staticmethod
    def check(roll: List[int]) -> bool:
        return len(set(roll)) <= 3

class Triple(Pattern):
    @staticmethod
    def check(roll: List[int]) -> Union[int, bool]:
       return any(i in Pattern.hash_roll(roll).values() for i in [3,4,5])

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
    def check(roll: List[int]) -> bool:
        patterns = [
            Double,
            Pair,
            Triple,
            FullHouse,
            Straight,
            Lucky11,
            Lucky7,
            Yahtzee
        ]

        return set(repr(pattern) for pattern in patterns if pattern.check(roll))
