// Globals
const root = ReactDOM.createRoot(document.getElementById("root"));
const path = window.location.pathname;
const room = path.split("/").pop();

const socket = io();
let player_number = null;

function Dice({ value, masked, onClick, disabled }) {
let background = masked ? '#777' : '#fff';
  return (
    <button onClick={onClick} disabled={disabled} style= {{"background": background}}>
      {value}
    </button>
  );
}

// UI Elements
function Cup({ disable }) {
  const [dice, setDice] = React.useState(Array(5).fill("-"));
  const [mask, setMask] = React.useState(Array(5).fill(false));
  const [numRolls, setNumRolls] = React.useState(0);

  const onRoll = (event) => {
    event.preventDefault();
    if (numRolls === 0) {
      socket.emit("roll_event");
    } else {
      socket.emit("player_move_event", {
        type: "reroll",
        value: mask.map((el) => !el),
      });
    }
    setNumRolls(numRolls + 1);
  };

  const onMask = (idx) => {
    return (event) => {
      event.preventDefault();
      let newMask = mask.slice();
      newMask[idx] = !newMask[idx];
      setMask(newMask);
    };
  };

  const disableDice = numRolls == 0 || numRolls == 3 || disable;
  const hideRollButton = numRolls == 3 || disable;

  socket.on("board_event", (state) => setDice(state.dice));

  return (
    <form>
      <Dice value={dice[0]} masked={mask[0]} onClick={onMask(0)} disabled={disableDice} />
      <Dice value={dice[1]} masked={mask[1]} onClick={onMask(1)} disabled={disableDice} />
      <Dice value={dice[2]} masked={mask[2]} onClick={onMask(2)} disabled={disableDice} />
      <Dice value={dice[3]} masked={mask[3]} onClick={onMask(3)} disabled={disableDice} />
      <Dice value={dice[4]} masked={mask[4]} onClick={onMask(4)} disabled={disableDice} />
      {!hideRollButton && <button onClick={onRoll}>Roll!</button>}
    </form>
  );
}

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
  root.render(<Cup disable={player_number !== 1} />);
});

socket.on("board_event", (board) => {
  console.log(board);
});
