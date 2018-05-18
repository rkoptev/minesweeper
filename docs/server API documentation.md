# Server API documentation
Internal API documentation for front-end and back-end communication (It's not an actual game API)

### Player
```javascript
var socket = io('http://77.73.67.16:8154/play');
```

#### socket.emit("play", { "difficulty": "beginner", "name": "Cool Hacker"})
Call this method to start new game. You can select different difficulty among beginner (9x9 & 10 mines), intermediate (16x16 & 40 mines) and expert (30x16 & 99 mines). There is also field for your name to easily find your game in dashboard

#### socket.emit("mark_cell", { "coordinates": [x,y] })
Call this method to place flag in cell. The flag marks a bomb. It's actually not necessary to win the game, but placing flags may make debug for you easier.

#### socket.emit("unmark_cell", { "coordinates": [x,y] })
Call this method to remove flag from cell. 

#### socket.emit("open_cell", { "coordinates": [x,y] })
Call this method to open cell.

#### socket.on("update", { "field": [...] })
This event fires every time when field update. It's needed for UI update and for updating game bot. Here is the example of field for beginner game:
```
[[" ", " ", " ", " ", " ", " ", " ", " ", " "]
[" ", " ", " ", " ", " ", " ", " ", " ", " "]
[" ", " ", " ", " ", " ", " ", " ", " ", " "]
["1", "2", "F", " ", " ", " ", " ", " ", " "]
["0", "1", "1", "1", "1", " ", " ", " ", " "]
["0", "0", "0", "0", "1", " ", " ", " ", " "]
["0", "0", "0", "0", "1", "2", "2", " ", " "]
["1", "1", "0", "0", "0", "0", "1", " ", " "]
[" ", "1", "0", "0", "0", "0", "1", " ", " "]]
```
The field itself is a 2D nested array with symbol representation of cells. Here you can see partly opened field with one flagged mine ("F"). Here is the list of possible objects on field:
- __" "__ - undiscovered cell
- __"F"__ - flagged
- __"0"__ - empty cell
- __"1 .. 8"__ - count of mines around,
- __"."__ - mine
- __"X"__ - false flagged mine
- __"*"__ - exploded mine

#### socket.on("end_game", { "win": true })
Called when game ends. If you want to start new game, call "play" again.

### Watcher
```javascript
var socket = io('http://77.73.67.16:8154/watch');
```
Watchers - are class of users that do not play the game, they only watch the games. Actually it's a public dashboard. They have only one update event.

#### socket.on("update", { "fields": [...] })
fields - is an array of fields that are in the same format as earlier.