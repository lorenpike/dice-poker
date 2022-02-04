from dice_poker.color import Color
from .game import Game

def run():
    game = Game.start_new_game()
    while not game.is_finished():
        print("\n".join([" ".join([str(el) + "   " for el in row]) for row in game.board.BOARD]))
        print(str(game.board))
        print(game.turn)
        input("enter to roll: ")
        
        game.roll()
        print(repr(game._dice))
        user_input = "m"
        while user_input == "m":
            user_input = input("m to mask, p to place: ")
            if user_input == "m":
                mask = []
                for i in range(5):
                    mask.append(int(input(f"keep(1) or roll(0) {i} die: ")))

                game.roll(mask)
                print(repr(game._dice))

        row = int(input("enter row: "))
        col = int(input("enter col: "))
        game.place_chip(row, col)
        game.turn  = Color.BLUE if game.turn == Color.RED else Color.RED
        game.rolls = 0

    print(game.who_won())


if __name__ == "__main__":
    run()