from dice_poker.dice import Dice

def test_roll_dice():
    roll = Dice.roll()
    assert len(roll) == 5
    assert type(roll[0]) == int

def test_masked_reroll():
    dices = [Dice() for _ in range(10)]
    rolls = [dice.new_roll() for dice in dices]
    rerolls = [dice.reroll([0,1,0,0,0]) for dice in dices]
    assert all(roll[1] == reroll[1] for roll, reroll in zip(rolls, rerolls))
    assert any(any(x != y for x,y in zip(r1, r2)) for r1, r2 in zip(rolls, rerolls))

def test_roll_twice():
    assert any(Dice.roll() != Dice.roll() for _ in range(10))
