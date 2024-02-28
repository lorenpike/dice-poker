// Globals
const root = ReactDOM.createRoot(document.getElementById("root"));
const path = window.location.pathname;
const room = path.split("/").pop();
const socket = io();

let player_number = null;
let active_player = false;

const render = () => {
  root.render(
    <div className="flex flex-col items-center h-dvh">
      <Cup disable={!active_player} socket={socket} />
      <Board disable={!active_player} socket={socket} />
    </div>);
}


// Socket Handling
socket.on("connect", () => {
  console.log(`connect ${socket.id} to room ${room}`);
  socket.emit("join_event", room);
});

socket.on("waiting_event", () => {
  player_number = 1;
  active_player = true;
  console.log("Currently waiting for another player");
  root.render(<WaitingRoom roomID={room}/>);
});

socket.on("start_event", () => {
  if (player_number === null) {
    player_number = 2;
  }
  console.log("Game started");
  console.log(`You are player ${player_number}`);
  render();
});

socket.on("end_turn_event", () => {
  console.log("Ending turn");
  active_player = !active_player;
  render();
});

socket.on("board_event", (board) => {
  console.log(board);
});
