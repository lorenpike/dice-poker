const path = window.location.pathname;
const room = path.split("/").pop();

const root = document.getElementById("main");
const socket = io();
let player_number = null;

socket.on("connect", () => {
  console.log(`connect ${socket.id} to room ${room}`);
  socket.emit("join_event", room);
});

socket.on("waiting_event", () => {
    player_number = 1; 
    console.log("Currently waiting for another player");
});

socket.on("start_event", () => {
    if (player_number === null){
        player_number = 2;
    }
    console.log("Game started");
    console.log(`You are player ${player_number}`);

    if (player_number === 1){
        const btn = document.createElement("button");
        btn.innerHTML = "Roll";
        btn.onclick = () => socket.emit("roll_event");
        root.appendChild(btn);  
    }
});

socket.on("board_event", (board) => {
    console.log(board);
});


const player_move = (move) => {
    socket.emit("player_move_event", move)
};

