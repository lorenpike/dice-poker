// UI Elements

function URLLink() {
  const urlInputRef = React.useRef(null);
  const [copied, setCopied] = React.useState(false);

  const handleCopy = () => {
    if (urlInputRef.current) {
      urlInputRef.current.select();
      document.execCommand('copy');
      setCopied(true);
    }
  };

  let divStyle = `flex flex-row w-96 bg-gray-200 rounded-md shadow-xl ring-2 ${copied ? "ring-slate-600": "ring-slate-400"}`
  let btnStyle = `${copied ? "bg-slate-600": "bg-slate-400"} hover:bg-slate-600 text-white font-bold rounded-md p-2`;

  return (
    <div className={divStyle}>
      <input type="text" className="w-full ml-4" ref={urlInputRef} defaultValue= {window.location.href} disabled />
    <button className={btnStyle} onClick={handleCopy} disable={copied}>
    {copied ? "Copied!" :"Copy"}
      </button>
    </div>
  );
}

function WaitingRoom({ roomID }) {
  return (
    <div className=" bg-gray-100 flex flex-col justify-center items-center min-h-screen">
      <h1 className="m-4 text-3xl">Waiting for another player... </h1>
      <URLLink />
    </div>
  );
}
function Dice({ value, masked, onClick, disabled }) {
  const style = `bg-gray-${masked ? 400 : 0} rounded-lg ${disabled ? '': 'hover:bg-gray-400'} m-2 focus:outline-none focus:shadow-outline flex items-center justify-center w-12 h-12`;
  const imgSrc = value === '-' ? '/static/square.png' : `/static/dice-${value}.png`;
  return (
    <button onClick={onClick} disabled={disabled} className={style}>
      <img src={imgSrc} alt={`dice-${value}`}/>
    </button>
  );
}

function Cup({ disable,  socket }) {
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

  const rollBtnStyle = "bg-gray-900 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline h-12"
  const disableDice = numRolls == 0 || numRolls == 3 || disable;
  const hideRollButton = numRolls == 3 || disable;
  
  socket.on("board_event", (state) => setDice(state.dice));
  socket.on("end_turn_event", () => {
    setNumRolls(0);
    setDice(Array(5).fill("-"));
    setMask(Array(5).fill(false));
  });

  return (
    <form className="flex items-center mt-8">
      <Dice value={dice[0]} masked={mask[0]} onClick={onMask(0)} disabled={disableDice} />
      <Dice value={dice[1]} masked={mask[1]} onClick={onMask(1)} disabled={disableDice} />
      <Dice value={dice[2]} masked={mask[2]} onClick={onMask(2)} disabled={disableDice} />
      <Dice value={dice[3]} masked={mask[3]} onClick={onMask(3)} disabled={disableDice} />
      <Dice value={dice[4]} masked={mask[4]} onClick={onMask(4)} disabled={disableDice} />
      {!hideRollButton && <button onClick={onRoll} className={rollBtnStyle}>Roll!</button>}
    </form>
  );
}

function TwoPairTile({pair, style, onClick}) {
  let [first, second] = pair;

  return (
    <div className={style} onClick={onClick}>
      <div key={0} className="aspect-square">
          <img src={`/static/dice-${first}.png`} className="object-cover w-full h-full" />
      </div>
      <div key={1} className="aspect-square">
          <img src={`/static/dice-${first}.png`} className="object-cover w-full h-full" />
      </div>
      <div key={2} className="aspect-square">
          <img src={`/static/dice-${second}.png`} className="object-cover w-full h-full" />
      </div>
      <div key={3} className="aspect-square">
          <img src={`/static/dice-${second}.png`} className="object-cover w-full h-full" />
      </div>
    </div>

  );
}

function PairTile({value, style, onClick}) {
  return (
    <div className={style} onClick={onClick}>
      <div key={0} className="aspect-square">
          <img src={`/static/dice-${value}.png`} className="object-cover w-full" />
      </div>
      <div key={1} className="aspect-square">
          <img src={`/static/dice-${value}.png`} className="object-cover w-full" />
      </div>
    </div>

  );
}

function TripleTile({value, style, onClick}) {
  return (
    <div className={style} onClick={onClick}>
      <div key={0} className="aspect-square">
          <img src={`/static/dice-${value}.png`} className="object-cover w-full" />
      </div>
      <div key={2} className="aspect-square">
          <img src={`/static/dice-${value}.png`} className="object-cover w-full" />
      </div>
      <div key={3} className="aspect-square">
          <img src={`/static/dice-${value}.png`} className="object-cover w-full" />
      </div>
    </div>

  );
}

function NamedTile({text, style, onClick}) {
  return (
    <div className={style} onClick={onClick}>
      {text}
    </div>
  );
}

function Tile({type, value, onClick, state, disabled}) {
  // state: is x, o, available, disabled
  let color;
  switch (state) {
    case "x":
      color = "bg-blue-400";
      break;
    case "o":
      color = "bg-red-400";
      break;
    case "available":
      color = "bg-indigo-400 hover:bg-indigo-600";
      break;
    default:
      color = "bg-indigo-200";
  }
  let style =`h-20 w-20 rounded-md ${color} font-bold text-l text-center m-0.5`;
  let codes = {
    "s": "Straight",
    "f": "Full House",
    "l": "Lucky 7",
    "e": "Lucky 11",
    " ": "Free Space",
  };
  
  if  (disabled || state !== "available") {
    onClick = (e) => {};
  }

  let alignment;
  switch (type) {
    case "d":
      alignment = "grid grid-cols-2 gap-1 content-center p-2";
      return <PairTile value={value} style={`${alignment} ${style}`} onClick={onClick} />;
    case "p":
      alignment = "grid grid-cols-2 gap-1 p-2";
      return <TwoPairTile pair={value} style={`${alignment} ${style}`} onClick={onClick} />;
    case "t":
      alignment = "grid grid-cols-2 gap-1 p-2";
      return <TripleTile value={value} style={`${alignment} ${style}`} onClick={onClick} />;
    case "n":
      alignment = "flex justify-center items-center p-2";
      return <NamedTile text={codes[value]} style={`${alignment} ${style}`} onClick={onClick} />;
  }
  
}

function Board({ disable, socket }) {

  const [placed, setPlaced] = React.useState(Array(9).fill(null).map(() => Array(9).fill('-')));
  const [available, setAvailable] = React.useState([]);

  const onClick = (x, y) => {
    return (event) => {
      event.preventDefault();
      console.log(x, y);
      socket.emit("player_move_event", {
        type: "place",
        value: [x, y],
      })
    };  
  };

  socket.on("board_event", (state) => {
    setPlaced(state.board);
    setAvailable(state.options);
  });

  socket.on("end_turn_event", () => {
    setAvailable([]);
  });


  const board = [
    ["n", "p", "p", "p", "d", "p", "p", "p", "n"],
    ["d", "n", "p", "p", "p", "p", "p", "n", "d"],
    ["p", "t", "n", "p", "p", "p", "n", "t", "p"],
    ["t", "t", "p", "n", "p", "n", "p", "t", "t"],
    ["n", "p", "n", "p", "n", "p", "n", "p", "n"],
    ["t", "t", "p", "n", "p", "n", "p", "t", "t"],
    ["p", "t", "n", "p", "p", "p", "n", "t", "p"],
    ["d", "n", "p", "p", "p", "p", "p", "n", "d"],
    ["n", "p", "p", "p", "d", "p", "p", "p", "n"]
  ];
  const values = [
    ["s", [6, 6], [6, 5], [6, 4], 2, [6, 3], [6, 2], [6, 1], "s"],
    [6, "f", [5, 1], [5, 2], [5, 3], [5, 4], [5, 5], "f", 4],
    [[4, 4], 2, "f", [4, 3], [1, 1], [4, 2], "f", 6, [4, 1]],
    [4, 1, [3, 3], "f", [3, 2], "f", [3, 1], 3, 5],
    ["l", [2, 1], "e", [2, 2], " ", [2, 2], "e", [2, 1], "l"],
    [5, 3, [1, 3], "f", [2, 3], "f", [3, 3], 1, 4],
    [[1, 4], 6, "f", [2, 4], [1, 1], [3, 4], "f", 2, [4, 4]],
    [5, "f", [5, 5], [4, 5], [3, 5], [2, 5], [1, 5], "f", 3],
    ["s", [1, 6], [2, 6], [3, 6], 1, [4, 6], [5, 6], [6, 6], "s"],
  ];

  const tile_state = placed.map((row, y) => row.map((el, x) => {
    if (el !== "-") {
      return el;
    } else {
      let coords = [x, y];
      let isAvailable = available.some(pair => pair.every((v, i) => v === coords[i]));
      return isAvailable ? "available" : "disabled";
    };
  }));

  return (
    <div className="flex justify-center items-center h-full w-full m-auto">
      <table className="h-min w-min">
        {board.map((row, y) => (
          <tr>
          {row.map((el, x) => (
            <td><Tile type={el} value={values[y][x]} onClick={onClick(x, y)} state={tile_state[y][x]} disabled={disable}/></td>
          ))}
          </tr>
        ))}
      </table>
    </div>
  );
}

