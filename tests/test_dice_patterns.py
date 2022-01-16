import pytest

from dice_poker.dice_patterns import *

@pytest.mark.parametrize("subcls", [
    Double,
    Pair,
    Triple,
    FullHouse,
    Straight,
    Lucky11,
    Lucky7,
    Yahtzee

])
def test_patterns(subcls):
    assert issubclass(subcls, Pattern)

def test_is_straight():
    assert Straight.check([1,2,3,4,5])
    assert not Straight.check([3,4,2,3,6])
    assert Straight.check([2,3,5,6,4])
    assert not Straight.check([2,2,2,2,2])

def test_is_lucky7():
    assert Lucky7.check([1,1,1,2,2])
    assert Lucky7.check([1,1,1,1,3])
    assert not Lucky7.check([1,2,5,3,6])
    assert not Lucky7.check([1,1,1,1,1])

def test_is_luck11():
    assert Lucky11.check([1,1,1,3,5])
    assert Lucky11.check([2,2,2,2,3])
    assert not Lucky11.check([1,2,5,3,6])
    assert not Lucky11.check([1,1,1,1,1])

def test_is_yahtzee():
    assert Yahtzee.check([1,1,1,1,1])
    assert Yahtzee.check([4,4,4,4,4])
    assert not Yahtzee.check([2,3,1,4,2])
    assert not Yahtzee.check([3,3,3,3,2])
    
def test_check_roll():
    assert RollChecker.check([1,2,2,1,5]) == ("Pair(2)", "Lucky11", "Pair(1)", "Double(1,2)")
    assert RollChecker.check([1,2,3,4,5]) == ("Straight")
    assert RollChecker.check([1,1,1,1,1]) == ("Yahtzee", "Pair(1)", "Triple(1)", "Double(1,1)")