document.getElementById('new-game').addEventListener('click', () => {
    console.log("New game");
    window.location.href = "/game/new";
});

document.getElementById('join-game').addEventListener('submit', (e) => {
    console.log("Join game");
    e.preventDefault();
    const gameId = document.getElementById('game-id').value;
    if (!gameId) {
        alert("Please enter a game ID.");
        return;
    }
    window.location.href = `/game/${gameId}`;
});
