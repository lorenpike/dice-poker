# Player One

1. New game -> Redirect to /game/xxxxxxx
2. Receives waiting page (copy link to other...)
3. (Once player two joins) Game loads and player one has a button to roll
4. Roll occurs
5. Player One has a choose to reroll or end turn
6. On an end of turn buttons disappear, a tile is updated

# Player Two

1. Click link from player one
2. Game loads, no buttons available 
3. Watches dice roll from player one
4. On the end of player Ones turn, control goes to him and his turn starts

***This repeats until an end of game***


# Events

* join event - from client
* waiting event - from server
* start event - from server
* board event - from server
* roll event - from client
* player move event - from client
* end_event - from server


# Commands

```bash
uvicorn dice_poker.server:combined_asgi_app --reload
```