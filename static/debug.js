const root = ReactDOM.createRoot(document.getElementById("root"));

let socket = {
  callback: null,
  on: function (event, callback) {
    console.log(`socket.on("${event}", callback)`);
    this.callback = callback;
  },

  emit: function (...args) {
    this.callback({
      dice: Array.from({ length: 5 }, () => Math.floor(Math.random() * 6) + 1)
    });
  },
};

root.render(
  <div className="flex flex-col items-center">
    <Board />
    <Cup disable={false} socket={socket} />
  </div>
);
