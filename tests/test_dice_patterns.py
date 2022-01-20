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

def test_hash_roll():
    assert Pattern.hash_roll([1,1,1,1,1]) == {1:5}
    assert Pattern.hash_roll([1,2,1,4,1]) == {1:3, 4:1, 2:1}
    assert Pattern.hash_roll([1,1,4,4,4]) == {4:3, 1:2}

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
    
def test_is_pair():
    assert Pair(2).check([1,1,2,2,3])
    assert not Pair(3).check([1,2,3,4,5,])
    assert Pair(1).check([1,1,2,2,3])
    assert Pair(1).check([1,1,1,1,1])
    assert not Pair(6).check([4,3,4,2,3])

def test_is_triple():
    assert Triple(3).check([1,3,1,3,3])
    assert not Triple(2).check([1,2,3,3,3])
    assert not Triple(2).check([1,4,3,4,3])
    assert Triple(4).check([4,4,4,4,5])

def test_is_double():
    assert Double(2,2).check([2,2,2,2,1])
    assert not Double(2,2).check([2,2,2,1,1])
    assert Double(1,2).check([1,2,1,2,3])
    assert not Double(4,5).check([4,4,5,6,1])


@pytest.mark.parametrize("cls, name", [
    (Straight(), "Straight"),
    (FullHouse(), "FullHouse"),
    (Lucky11(), "Lucky11"),
    (Lucky7(), "Lucky7"),
    (Pair(3), "Pair"),
    (Triple(1), "Triple"),
    (Double(1,2), "Double"),
    (Yahtzee(), "Yahtzee")
])
def test_repr_for_classes(cls, name):
    assert repr(cls) == name

@pytest.mark.parametrize("cls, args, name", [
    (Triple, [3], "Triple(3)"),
    (Pair, [6], "Pair(6)"),
    (Double, [1,2], "Double(1,2)"),
    (Double, [2,1], "Double(1,2)")
])
def test_str_for_classes_with_die(cls, args, name):
    assert str(cls(*args)) == name

def test_roll_checker():
    assert RollChecker.check([1,2,3,4,5]) == {"Straight"}
    assert RollChecker.check([1,2,1,3,4]) == {"Lucky11", "Pair(1)"}
    assert RollChecker.check([1,1,1,1,3]) == {"Double(1,1)", "Pair(1)", "Triple(1)", "Lucky7"}
    assert RollChecker.check([6,6,6,6,6]) == {"Yahtzee", "Double(6,6)", "Pair(6)", "Triple(6)"}
    assert RollChecker.check([3,3,4,4,4]) == {"Pair(3)", "Pair(4)", "Triple(4)", "Double(3,4)", "FullHouse"}
