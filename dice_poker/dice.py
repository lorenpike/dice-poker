import random
from typing import List

class Dice:
    
    @staticmethod
    def roll() -> List[int]:
        return list(random.randint(1,6) for _ in range(5))

    def new_roll(self) -> List[int]:
        self.dice = Dice.roll() 
        return self.dice

    def reroll(self, mask: List[int]) -> List[int]:
        self.dice = [random.randint(1,6) if not m else r for m,r in zip(mask, self.dice)]
        return self.dice

    def __str__(self) -> str:
        icons = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}
        return "".join(str([icons[d] for d in self.dice]).split("'"))

    def __repr__(self) -> str:
        return f"Dice({self.dice})"
