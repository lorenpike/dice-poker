from gettext import find
import pytest

from dice_poker.board import Board, Color, Sequence, Spot

def test_board_size():
    assert len(Board.BOARD) == 9
    for row in Board.BOARD:
        assert len(row) == 9

def test_no_chip_placements():
    board = Board()
    assert len(board.chip_placements) == 9
    for row in board.chip_placements:
        assert  len(row) == 9
        for el in row:
            assert el is None

def test_place_a_blue_chip():
    board = Board()
    board.place_blue_chip(row=0, col=0)
    assert board.chip_placements[0][0] == Color.BLUE

def test_place_a_red_chip():
    board = Board()
    board.place_red_chip(row=0, col=0)
    assert board.chip_placements[0][0] == Color.RED

def test_place_blue_then_red():
    board = Board()
    board.place_blue_chip(row=0, col=0)
    board.place_red_chip(row=0, col=1)
    assert board.chip_placements[0][0] == Color.BLUE
    assert board.chip_placements[0][1] == Color.RED

def test_raise_error_putting_chip_on_same_spot():
    board =  Board()
    board.place_blue_chip(row=0, col=0)
    with pytest.raises(ValueError):
        board.place_red_chip(row=0, col=0)

def test_cannot_place_chip_on_free_space():
    board = Board()
    with pytest.raises(ValueError):
        board.place_red_chip(row=4, col=4)

def test_get_spot():
    board = Board()
    board.place_blue_chip(0,0)
    spot_1 = Spot(0,0)
    spot_2 = Spot(0,1)
    assert board.get_spot(spot_1) == Color.BLUE
    assert board.get_spot(spot_2) is None

def test_raise_error_when_outside_board():
    board = Board()
    with pytest.raises(ValueError):
        board.place_blue_chip(row=9, col=1)
    with pytest.raises(ValueError):
        board.place_blue_chip(row=0, col=9)
    with pytest.raises(ValueError):
        board.place_blue_chip(row=-1, col=5)
    with pytest.raises(ValueError):
        board.place_blue_chip(row=0, col=-1)
        
def test_find_horizontal_sequences():
    board = Board()
    for i in range(5):
        board.place_blue_chip(row=0, col=i+1)
    expected = {Sequence(Color.BLUE, Spot(0,1), Spot(0,5))}
    assert board.find_horizontal_sequences() == expected

def test_find_two_horizontal_sequences():
    board = Board()
    for i in range(1,6):
        board.place_blue_chip(row=0, col=i)
        if i != 4:
            board.place_red_chip(row=4, col=i)
    expected = {
        Sequence(Color.BLUE, Spot(0,1), Spot(0,5)), 
        Sequence(Color.RED, Spot(4,1), Spot(4,5))
    }
    assert board.find_horizontal_sequences() == expected

def test_two_sequences_on_middle_row():
    board = Board()
    for i in range(4):
        board.place_blue_chip(row=4, col=i)
        board.place_red_chip(row=4, col=i+5)

    expected = {
        Sequence(Color.BLUE, Spot(4,0), Spot(4,4)),
        Sequence(Color.RED, Spot(4,4), Spot(4,8))
    }
    assert board.find_horizontal_sequences() == expected

def test_find_contiguious_sections_in_list_of_spots():
    board = Board()
    spots = []
    for i in range(9):
        spots.append(Spot(0, i))
    for i in range(3):
        board.place_blue_chip(0, i)
        board.place_red_chip(0, i+6)
    assert board.find_contigious_regions(spots) == [(Color.BLUE, (0,2)), (None, (3,5)), (Color.RED, (6,8))]

def test_find_vertical_sequences():
    board = Board()
    for i in range(5):
        board.place_blue_chip(row=i, col= 0)
        if i + 2 != 4: 
            board.place_red_chip(row=i+2, col=4)

    expected = {
        Sequence(Color.BLUE, Spot(0,0), Spot(4,0)),
        Sequence(Color.RED, Spot(2,4), Spot(6,4))
    }
    assert board.find_vertical_sequences() == expected

def test_get_main_diagonal():
    expected = []
    for i in range(9):
        expected.append(Spot(i,i))
    assert len(Board.get_diagonal(Spot(0,1), Spot(7,8))) == 8
    assert Board.get_diagonal(Spot(0,0), Spot(8,8)) == expected

def test_get_off_angle_diagonal():
    expected = []
    for i in range(8):
        expected.append(Spot(i+1, i))
    assert Board.get_diagonal(Spot(1,0), Spot(8,7)) == expected

def test_get_opposite_diagonal():
    expected = []
    for i in range(9):
        expected.append(Spot(i, 8-i))
    assert Board.get_diagonal(Spot(0,8), Spot(8,0)) == expected

def test_get_all_diagonals():
    board = Board()
    assert len(board.get_all_diagonals_endpoints()) == 18
    assert (Spot(4,0), Spot(8,4)) in board.get_all_diagonals_endpoints()
    assert (Spot(0,4), Spot(4,8)) in board.get_all_diagonals_endpoints()
    assert (Spot(4,8), Spot(8,4)) in board.get_all_diagonals_endpoints()
    assert (Spot(0,4), Spot(4,0)) in board.get_all_diagonals_endpoints()

def test_find_diagonal_sequences():
    board = Board()
    for i in range(5):
        board.place_blue_chip(i+1, i)
        board.place_red_chip(i+4, 8-i)
    expected = {
        Sequence(Color.BLUE, Spot(1,0), Spot(5,4)),
        Sequence(Color.RED, Spot(4,8), Spot(8,4))
    }
    assert board.find_diagonal_sequences() == expected

def test_two_sequences_main_diagonal():
    board = Board()
    for i in range(4):
        board.place_blue_chip(i,i)
        board.place_red_chip(i+5, i+5)
    expected = {
        Sequence(Color.BLUE, Spot(0,0), Spot(4,4)),
        Sequence(Color.RED, Spot(4,4), Spot(8,8))
    }
    assert board.find_diagonal_sequences() == expected

def test_find_sequences():
    board = Board()
    for i in range(5):
        board.place_blue_chip(i+1, i+2)
        board.place_red_chip(i, 0)
        board.place_blue_chip(8, 8-i)
    expected = {
        Sequence(Color.BLUE, Spot(1,2), Spot(5,6)),
        Sequence(Color.RED, Spot(0,0), Spot(4,0)),
        Sequence(Color.BLUE, Spot(8,4), Spot(8,8)),
    }
    assert board.find_sequences() == expected

def test_win():
    board = Board()
    assert board.is_won() == False
    assert board.who_won() is None
    for i in range(5):
        board.place_blue_chip(0,i)
        board.place_blue_chip(1,i)
    assert board.is_won() == True
    assert board.who_won() == Color.BLUE

def test_win_entire_row():
    board = Board()
    for i in range(9):
        board.place_blue_chip(0, i)
    assert board.is_won() == True
    assert board.who_won() == Color.BLUE

def test_win_entire_col():
    board = Board()
    for i in range(9):
        board.place_blue_chip(i, 0)
    assert board.is_won() == True
    assert board.who_won() == Color.BLUE

def test_win_entire_diagonal():
    board = Board()
    for i in range(4):
        board.place_red_chip(0+i, 8-i)
        board.place_red_chip(5+i, 3-i)
    assert board.is_won() == True
    assert board.who_won() == Color.RED

def test_is_empty():
    board = Board()
    assert board.is_empty() == True
    board.place_blue_chip(0,0)
    assert board.is_empty() == False