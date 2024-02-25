// Globals
const root = ReactDOM.createRoot(document.getElementById("root"));
const path = window.location.pathname;
const room = path.split("/").pop();

const socket = io();
let player_number = null;


// Socket Handling
socket.on("connect", () => {
  console.log(`connect ${socket.id} to room ${room}`);
  socket.emit("join_event", room);
});

socket.on("waiting_event", () => {
  player_number = 1;
  console.log("Currently waiting for another player");
});

socket.on("start_event", () => {
  if (player_number === null) {
    player_number = 2;
  }
  console.log("Game started");
  console.log(`You are player ${player_number}`);
  root.render(<Cup disable={player_number !== 1} socket={socket} />);
});

socket.on("board_event", (board) => {
  console.log(board);
});
