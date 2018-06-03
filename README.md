Minesweeper Online
==================

Minesweeper Online is a platform that allows you to write your own bot for Minesweeper on JavaScript or to organize a contest to compete in this fascinating experience together. Here is how it looks like:

TODO: img

All in the style of the good old game on Windows 2000, except you are not a player, your code is player!

## Wanna try?
We did everything so that you could start easily, quickly and without a complicated installation. To start coding your need to download **index.html** and **your-code-here.js** and place them in one folder. After that open index.html in your browser, your-code-here.js in your favorite editor and you are ready to go!

In the browser you can see the actual game process and watch the work of your program. Once you open the page - the code will start executing and you will see the actions of your program. We already implemented algorithm to randomly open cells(probably not the best tactics:))

In the script you'll see the **onUpdate()** function that will be called every time before your turn. As an only argument to onUpdate(), you get the game field: 
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
- __"1 .. 8"__ - count of mines around

To make a move you need to return an object, in which you must specify the type of move and coordinates of cell on which this move will be performed. 

You can also monitor the progress of other players in the public server dashboard: http://77.73.67.16:8154/

Have fun :)

## Setup your own server
In case you want to setup your own server to make a contest or for some reason you want to play on your own server, here is what you need to do this:

First of all: install Python 3.x if it's not installed yet.
```bash
# Clone repo
git clone https://github.com/rkoptev/minesweeper.git
cd minesweeper

# Install required modules
pip install -r requirements.txt

# Run server
python src/server.py
```

That's all. To make sure everything works fine - open dashboard in your browser:
```
localhost:8154
```

## Contribution
Special thanks to @kateboyko who developed that awesome old school looking frontend for Minesweeper Online.
