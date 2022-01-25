from dice_poker.game import Game
from dice_poker.color import Color

def test_start_new_game():
    game = Game.start_new_game()
    assert game.turn == Color.BLUE
    assert game.board.is_empty()