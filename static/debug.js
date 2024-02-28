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

let board_socket = {
  on: function (e, callback) {
    console.log(`socket.on(${e}, callback)`);
  },
  emit: function (e, obj) {
    console.log(`socket.emit(${e}, ${JSON.stringify(obj)})`);
  }
};


root.render(
  <div className="flex flex-col items-center h-dvh">
    <Cup disable={false} socket={socket} />
    <Board socket={board_socket}/>
  </div>
);
