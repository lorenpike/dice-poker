import socketio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

socket_io = socketio.AsyncServer(async_mode="asgi")
combined_asgi_app = socketio.ASGIApp(socket_io, app)

players = {}


@app.get("/")
async def index():
    with open("index.html") as f:
        return HTMLResponse(f.read())


@app.get("/game")
async def game():
    with open("game.html") as f:
        return HTMLResponse(f.read())


@app.get("/hello")
async def hello():
    return {"message": "Hello, World!"}


@socket_io.event
async def connect(socket_id, environ, auth):
    await socket_io.emit("hello", (1, 2, {"hello": "you"}), to=socket_id)


@socket_io.event
def disconnect(socket_id):
    print(f"disconnected {socket_id}")
