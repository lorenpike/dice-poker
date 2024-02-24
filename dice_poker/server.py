import logging

import numpy as np
import socketio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from .game import Game, PlayerMove
from .utils import random_code

# Logging
fmt_str = "\u001b[38;5;241m%(levelname)s:\u001b[0m\t%(message)s"
logging.basicConfig(level=logging.DEBUG, format=fmt_str)
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

socket_io = socketio.AsyncServer(async_mode="asgi")
combined_asgi_app = socketio.ASGIApp(socket_io, app)


class Rooms(dict):
    @property
    def via_player(self):
        return {
            **{v.player_1: v for v in self.values()},
            **{v.player_2: v for v in self.values()},
        }


rooms = Rooms()


class Controller:
    def __init__(self, room_id: str):
        self.room_id = room_id
        self._game = Game()
        self._game_gen = None
        self.player_1 = None
        self.player_2 = None
        self.current_turn = None

    @property
    def game_loop(self):
        if self._game_gen is None:
            self._game_gen = self._game.run()
        return self._game_gen

    async def notify_game_state(self, dice, options, board):
        data = {
            "dice": dice.tolist(),
            "options": options.tolist(),
            "board": board.tolist(),
        }
        await socket_io.emit("board_event", data, room=self.room_id)

    async def add(self, player_id: str):
        await socket_io.enter_room(player_id, self.room_id)
        logger.debug(f"Socket {player_id!r} joined room {self.room_id!r}")

        if self.player_1 is None:
            self.player_1 = player_id
            logger.debug(f"{player_id} is player 1")
            await socket_io.emit("waiting_event", to=self.player_1)
        elif self.player_2 is None:
            self.player_2 = player_id
            logger.debug(f"{player_id} is player 2")
            await socket_io.emit("start_event", room=self.room_id)
        else:
            logger.debug(f"{player_id} is spectating")

    async def first_roll(self):
        self.current_turn = next(self.game_loop)
        state = self.current_turn()
        await self.notify_game_state(*state)

    async def player_move(self, data):
        move = PlayerMove(data["type"], data["value"])
        state = self.current_turn(move)
        await self.notify_game_state(*state)


@app.get("/")
async def index():
    with open("index.html") as f:
        return HTMLResponse(f.read())


@app.get("/game/new")
async def game():
    room = random_code()
    return RedirectResponse(f"/game/{room}")


@app.get("/game/{room}")
async def game(room: str):
    with open("game.html") as f:
        return HTMLResponse(f.read())


# Client-triggered Events
@socket_io.event
async def connect(socket_id, environ, auth):
    logger.debug(f"Connected {socket_id = } {auth = }")


@socket_io.event
async def join_event(socket_id, room_id):
    if room_id not in rooms:
        logger.debug(f"Room {room_id} does not exist. Creating it...")
        rooms[room_id] = Controller(room_id)
    controller = rooms[room_id]
    await controller.add(socket_id)


@socket_io.event
async def roll_event(socket_id):
    await rooms.via_player[socket_id].first_roll()


@socket_io.event
async def player_move_event(socket_id, data):
    await rooms.via_player[socket_id].player_move(data)


@socket_io.event
def disconnect(socket_id):
    logger.debug(f"Disconnected {socket_id}")
