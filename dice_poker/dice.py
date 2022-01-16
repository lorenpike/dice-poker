import random
from typing import List

class Dice:
    @staticmethod
    def roll() -> List[int]:
        return list(random.randint(1,6) for _ in range(5))

    @staticmethod
    def reroll(mask: List[int], roll: List[int]) -> List[int]:
        return [random.randint(1,6) if not m else r for m,r in zip(mask, roll)]



def roll_til_yahtzee():
    count = 0
    dice = Dice()
    while True:
         roll = dice.roll()
         count += 1
         if len(list(set(roll))) == 1:
             print(roll)
             print(f"it took {count} rolls")
             break

