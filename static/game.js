const socket = io();

socket.on("connect", () => {
  console.log(`connect ${socket.id}`);
});

socket.on("update_board", () => {
    console.log("update_board");
})

socket.on("your_turn", () => {
    console.log("turn");
    enableButtons();
})

socket.on("disconnect", () => {
  console.log(`disconnect ${socket.id}`);
});

const enableButtons = () => {
    console.log("Enabling buttons");
}

const playMove = () =>{
    socket.emit("play_move", "test");
};