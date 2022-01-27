import pytest
from dice_poker.board import Spot
from dice_poker.game import Game
from dice_poker.color import Color

def test_start_new_game():
    game = Game.start_new_game()
    assert game.turn == Color.BLUE
    assert game.board.is_empty()
    assert game.rolls == 0


def test_roll_once():
    game = Game.start_new_game()
    game.roll()
    assert game.rolls == 1
    assert game.dice is not None 
    assert len(game.dice) == 5

def test_roll_twice():
    game = Game.start_new_game()
    game.roll()
    x1, x2 = game.dice[0], game.dice[2]
    game.roll([1,0,1,0,0])
    assert game.rolls == 2
    assert x1 == game.dice[0]
    assert x2 == game.dice[2]

def test_value_error_masking_first_roll():
    game = Game.start_new_game()
    with pytest.raises(ValueError):
        game.roll([1,1,1,1,1])

def test_roll_four_times():
    game = Game.start_new_game()
    game.roll()
    game.roll()
    game.roll()
    assert game.rolls == 3
    with pytest.raises(ValueError):
        game.roll()

def test_get_available_spots():
    game = Game.start_new_game()
    game._dice.dice = [1,4,4,6,6]
    spots = game.get_possible_placements()
    assert spots == {Spot(0,3), Spot(8,5), Spot(1,0), Spot(1,8)}

def test_place_chip():
    game = Game.start_new_game()
    game._dice.dice = [1,4,4,6,6]
    game.place_chip(row=0, col=3)
    assert game.board.get_spot(Spot(0,3)) == Color.BLUE

def test_place_chip_raise_value_error():
    game = Game.start_new_game()
    game._dice.dice = [1,4,4,6,6]
    with pytest.raises(ValueError):
        game.place_chip(row=0, col=4)