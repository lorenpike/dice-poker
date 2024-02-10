from itertools import cycle, chain
from collections import namedtuple
from random import choice

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

''' Codes
{
    's': 'straight',
    'f': 'full house',
    'p': 'two pair',
    'd': 'pair',
    't': 'triple',
    'l': 'lucky seven',
    'e': 'lucky eleven',
    ' ': 'free space',
    'y': 'yahtzee',
}
'''

board = np.array([
    ['s', 'p', 'p', 'p', 'd', 'p', 'p', 'p', 's'],
    ['d', 'f', 'p', 'p', 'p', 'p', 'p', 'f', 'd'],
    ['p', 't', 'f', 'p', 'p', 'p', 'f', 't', 'p'],
    ['t', 't', 'p', 'f', 'p', 'f', 'p', 't', 't'],
    ['l', 'p', 'e', 'p', ' ', 'p', 'e', 'p', 'l'],
    ['t', 't', 'p', 'f', 'p', 'f', 'p', 't', 't'],
    ['p', 't', 'f', 'p', 'p', 'p', 'f', 't', 'p'],
    ['d', 'f', 'p', 'p', 'p', 'p', 'p', 'f', 'd'],
    ['s', 'p', 'p', 'p', 'd', 'p', 'p', 'p', 's'],
], dtype='U8')

values = np.array([
    [[0, 0], [6, 6], [5, 6], [4, 6], [2, 0], [3, 6], [2, 6], [1, 6], [0, 0]],
    [[6, 0], [0, 0], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5], [0, 0], [4, 0]],
    [[4, 4], [2, 0], [0, 0], [3, 4], [1, 1], [2, 4], [0, 0], [6, 0], [1, 4]],
    [[4, 0], [1, 0], [3, 3], [0, 0], [2, 3], [0, 0], [1, 3], [3, 0], [5, 0]],
    [[0, 0], [1, 2], [0, 0], [2, 2], [0, 0], [2, 2], [0, 0], [1, 2], [0, 0]],
    [[5, 0], [3, 0], [1, 3], [0, 0], [2, 3], [0, 0], [3, 3], [1, 0], [4, 0]],
    [[1, 4], [6, 0], [0, 0], [2, 4], [1, 1], [3, 4], [0, 0], [2, 0], [4, 4]],
    [[5, 0], [0, 0], [5, 5], [4, 5], [3, 5], [2, 5], [1, 5], [0, 0], [3, 0]],
    [[0, 0], [1, 6], [2, 6], [3, 6], [1, 0], [4, 6], [5, 6], [6, 6], [0, 0]],
], dtype='b')


def roll(prev: np.ndarray = None):
    '''Roll the dice'''
    num_dice = 5
    if prev is None:
        prev = np.zeros((num_dice,))
    return np.where(prev == 0, np.random.randint(1, 6, (num_dice,)), prev)


def match(roll: np.ndarray):
    """Returns a list of matchs on a roll"""
    matches = []
    unique, counts = np.unique(roll, return_counts=True)

    # Yahtzee stop condition
    if len(unique) == 1:
        return [('y', np.array([0, 0], dtype='b'))]

    pairs = unique[counts >= 2]

    # Add all pairs
    matches.extend(('d', np.array([v, 0], dtype='b')) for v in pairs)

    # Add all double pairs with different numbers
    if len(pairs) > 1:
        matches.append(('p', np.sort(pairs).astype('b')))

    threes = unique[counts >= 3]
    if len(threes):
        matches.append(('t', np.array([threes[0], 0], dtype='b')))

    # Add all double pairs with the same number
    fours = unique[counts >= 4]
    if len(fours):
        matches.append(('p', np.array([fours[0], fours[0]], dtype='b')))

    # Add all full houses
    if (len(counts) == 2 and (np.sort(counts) == np.array([2, 3])).all()):
        matches.append(('f', np.array([0, 0], dtype='b')))

    # Add lucky 7
    if roll.sum() == 7:
        matches.append(('l', np.array([0, 0], dtype='b')))

    # Add lucky eleven
    if roll.sum() == 11:
        matches.append(('e', np.array([0, 0], dtype='b')))

    # Add straight
    if (
        len(unique) == 5
        and not all(np.isin(roll, v).any() for v in [1, 6])
    ):
        matches.append(('s', np.array([0, 0], dtype='b')))

    return matches


def valid_placements(matches: list) -> np.ndarray:
    if len(matches) == 0:
        return np.zeros(board.shape, dtype='b')

    if len(matches) == 1 and matches[0][0] == 'y':
        return (board != ' ').astype('b')

    return np.stack([
        (k == board) & (values == v.reshape(1, 1, -1)).all(axis=-1)
        for k, v in matches
    ]).any(axis=0).astype('b')


def get_indices(array: np.ndarray):
    assert array.dtype == np.bool_
    indices = np.stack(np.meshgrid(*(range(v) for v in array.shape)), axis=-1)
    return indices[array]


GameState = namedtuple("GameState", "dice options board")
PlayerMove = namedtuple("PlayerMove", "type value")

PLACE = 'place'
REROLL = 'reroll'


class Game:
    players = [*'xo']

    def __init__(self):
        self._state = np.full(board.shape, fill_value='-', dtype='U8')
        self._turn = cycle(self.players)

    def __str__(self):
        return (
            str(self._state)
            .replace('\'', '')
            .replace('[', ' ')
            .replace(']', '')
        )

    @property
    def still_open(self):
        available = '-' == self._state
        available[4, 4] = False
        return available

    @property
    def winner(self):
        scores = {p: self.num_sequences(p) for p in self.players}
        for p, v in scores.items():
            if v >= 2:
                return p
        return 'Tie'

    def turn(self):
        '''Definition of a turn'''
        player = next(self._turn)
        current_roll = None

        # Roll the dice
        for _ in range(3):
            current_roll = roll(prev=current_roll)
            matches = match(current_roll)
            valid_spots = valid_placements(matches)
            options = get_indices(valid_spots.astype('?') & self.still_open)
            move = yield GameState(current_roll, options, self._state.copy())
            if move.type == PLACE:
                x, y = move.value
                self._state[y, x] = player
                yield None
            elif move.type == REROLL:
                pickup = move.value
                current_roll = np.where(pickup, 0, current_roll)
            else:
                raise ValueError()

    def windows(self, player: str):
        state = self._state.copy()
        state[4, 4] = player

        directions = chain(
            sliding_window_view(state, (9, 1)).reshape(-1, 9),
            sliding_window_view(state, (1, 9)).reshape(-1, 9),
            (np.diag(state, k) for k in range(-4, 5)),
            (np.diag(np.rot90(state), k) for k in range(-4, 5)),
        )
        for window in directions:
            yield (window == player).astype('b')

    def num_sequences(self, player: str):
        num = 0
        for window in self.windows(player):
            convolved = np.convolve(window, np.ones(5, dtype='b'), 'valid')
            if (convolved == 5).all() and len(window) == 9:
                num += 2
            elif (convolved == 5).any():
                num += 1
        return num

    def end(self):
        return (
            any(self.num_sequences(p) >= 2 for p in self.players)
            or self.still_open.sum() == 0
        )

    def run(self):
        while True:
            play = self.turn()
            yield (lambda msg=None: play.send(msg))
            play.close()

            if self.end():
                break


def simple_bot(action: callable):
    state = action()
    for _ in range(2):
        if len(state.options) == 0:
            action(PlayerMove(REROLL, np.ones((5,))))
        else:
            action(PlayerMove(PLACE, choice(state.options)))
            break


if __name__ == "__main__":
    game = Game()
    print("Start")
    print(game, end="\n\n")

    try:
        for turn in game.run():
            simple_bot(turn)
    except KeyboardInterrupt:
        pass

    print("End")
    print(game, end="\n\n")
    print(f"{game.winner = }")
