// UI Elements

function Dice({ value, masked, onClick, disabled }) {
  const style = `bg-gray-${masked ? 400 : 0} rounded-lg hover:bg-gray-400 m-2 focus:outline-none focus:shadow-outline flex items-center justify-center w-12 h-12`;
  
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

  const disableDice = numRolls == 0 || numRolls == 3 || disable;
  const hideRollButton = numRolls == 3 || disable;
  
  React.useEffect(() => {
    console.log(mask); // Log the updated state
  }, [mask]);
  socket.on("board_event", (state) => setDice(state.dice));

  const rollBtnStyle = "bg-gray-900 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline m-2"

  return (
    <form className="flex">
      <Dice value={dice[0]} masked={mask[0]} onClick={onMask(0)} disabled={disableDice} />
      <Dice value={dice[1]} masked={mask[1]} onClick={onMask(1)} disabled={disableDice} />
      <Dice value={dice[2]} masked={mask[2]} onClick={onMask(2)} disabled={disableDice} />
      <Dice value={dice[3]} masked={mask[3]} onClick={onMask(3)} disabled={disableDice} />
      <Dice value={dice[4]} masked={mask[4]} onClick={onMask(4)} disabled={disableDice} />
      {!hideRollButton && <button onClick={onRoll} className={rollBtnStyle}>Roll!</button>}
    </form>
  );
}

function TwoPairTile({pair}) {
  let [first, second] = pair;

  return (
    <div className="grid grid-cols-2 gap-1 w-32 h-32 border-4 border-stone-900 p-2 rounded-xl bg-indigo-200">
      <div key={0} className="aspect-w-1 aspect-h-1">
          <img src={`/static/dice-${first}.png`} className="object-cover w-full h-full" />
      </div>
      <div key={1} className="aspect-w-1 aspect-h-1">
          <img src={`/static/dice-${first}.png`} className="object-cover w-full h-full" />
      </div>
      <div key={2} className="aspect-w-1 aspect-h-1">
          <img src={`/static/dice-${second}.png`} className="object-cover w-full h-full" />
      </div>
      <div key={3} className="aspect-w-1 aspect-h-1">
          <img src={`/static/dice-${second}.png`} className="object-cover w-full h-full" />
      </div>
    </div>

  );
}

function PairTile({value}) {
  return (
    <div className="grid grid-cols-2 gap-1 content-center w-32 h-32 border-4 border-stone-900 p-2 rounded-xl bg-indigo-200">
      <div key={0} className="aspect-w-1 aspect-h-1">
          <img src={`/static/dice-${value}.png`} className="object-cover w-full" />
      </div>
      <div key={1} className="aspect-w-1 aspect-h-1">
          <img src={`/static/dice-${value}.png`} className="object-cover w-full" />
      </div>
    </div>

  );
}

function TripleTile({value}) {
  return (
    <div className="grid grid-cols-2 gap-1 w-32 h-32 border-4 border-stone-900 p-2 rounded-xl bg-indigo-200">
      <div key={0} className="aspect-w-1 aspect-h-1">
          <img src={`/static/dice-${value}.png`} className="object-cover w-full" />
      </div>
      <div key={2} className="aspect-w-1 aspect-h-1">
          <img src={`/static/dice-${value}.png`} className="object-cover w-full" />
      </div>
      <div key={3} className="aspect-w-1 aspect-h-1">
          <img src={`/static/dice-${value}.png`} className="object-cover w-full" />
      </div>
    </div>

  );
}

function NamedTile({text}) {
  return (
    <div className="flex justify-center items-center w-32 h-32 border-4 border-stone-900 rounded-xl bg-indigo-200 font-bold text-xl">
      {text}
    </div>
  );
}

function Board() {
  const board = [
    [<NamedTile text="Straight" />, <TwoPairTile pair={[6, 6]} />, <TwoPairTile pair={[6, 5]} />, <TwoPairTile pair={[6, 4]} />, <PairTile value={2} />, <TwoPairTile pair={[6, 3]} />, <TwoPairTile pair={[6, 2]} />, <TwoPairTile pair={[6, 1]} />, <NamedTile text="Full House"/>],
    [<PairTile value={6} />, <NamedTile text="Full House"/>, <TwoPairTile pair={[5, 1]} />, <TwoPairTile pair={[5, 2]} />, <TwoPairTile pair={[5, 3]} />, <TwoPairTile pair={[5, 4]} />, <TwoPairTile pair={[5, 5]} />, <NamedTile text="Full House" />, <PairTile value={4} />],
    [<TwoPairTile pair={[4, 4]} />, <TripleTile value={2}/>, <NamedTile text="Full House"/>, <TwoPairTile pair={[4, 3]} />, <TwoPairTile pair={[1, 1]} />, <TwoPairTile pair={[4, 2]} />, <NamedTile text="Full House"/>, <TripleTile value={6} />, <TwoPairTile pair={[4, 1]} />],
    [<TripleTile value={4} />, <TripleTile value={1} />, <TwoPairTile pair={[3, 3]} />, <NamedTile text="Full House" />, <TwoPairTile pair={[3, 2]} />, <NamedTile text="Full House"/>, <TwoPairTile pair={[3, 1]} />, <TripleTile value={3} />, <TripleTile value={5} />],
    [<NamedTile text="Lucky 7"/>, <TwoPairTile pair={[2, 1]} />, <NamedTile text="Lucky 11"/>, <TwoPairTile pair={[2, 2]} />, <NamedTile text="Free Space"/>, <TwoPairTile pair={[2, 2]} />, <NamedTile text="Lucky 11"/>, <TwoPairTile pair={[2, 1]} />, <NamedTile text="Lucky 7"/>],
    [<TripleTile value={5} />, <TripleTile value={3} />, <TwoPairTile pair={[1, 3]} />, <NamedTile text="Full House"/>, <TwoPairTile pair={[2, 3]} />, <NamedTile text="Full House"/>, <TwoPairTile pair={[3, 3]} />, <TripleTile value={1} />, <TripleTile value={4} />],
    [<TwoPairTile pair={[1, 4]} />, <TripleTile value={6} />, <NamedTile text="Full House"/>, <TwoPairTile pair={[2, 4]} />, <TwoPairTile pair={[1, 1]} />, <TwoPairTile pair={[3, 4]} />, <NamedTile text="Full House"/>, <TripleTile value={2} />, <TwoPairTile pair={[4, 4]} />],
    [<PairTile value={5} />, <NamedTile text="Full House"/>, <TwoPairTile pair={[5, 5]} />, <TwoPairTile pair={[4, 5]} />, <TwoPairTile pair={[3, 5]} />, <TwoPairTile pair={[2, 5]} />, <TwoPairTile pair={[1, 5]} />, <NamedTile text="Full House"/>, <PairTile value={3} />],
    [<NamedTile text="Straight"/>, <TwoPairTile pair={[1, 6]} />, <TwoPairTile pair={[2, 6]} />, <TwoPairTile pair={[3, 6]} />, <PairTile value={1} />, <TwoPairTile pair={[4, 6]} />, <TwoPairTile pair={[5, 6]} />, <TwoPairTile pair={[6, 6]} />, <NamedTile text="Straight"/>],
  ];

  return (
    <table className="rounded-xl ring-8 ring-indigo-800 m-4">
      {board.map(row => (
        <tr>
        {row.map(el => (
          <td>{el}</td>
        ))}
        </tr>
      ))}
    </table>
  );
}

