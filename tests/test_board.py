from dice_poker.board import Board

def test_board_size():
    assert len(Board.BOARD) == 9
    for row in Board.BOARD:
        assert len(row) == 9
