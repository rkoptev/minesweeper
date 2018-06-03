var socket = io('http://77.73.67.16:8154/play');

var mapElement = document.querySelector("#map");
var windowElement = document.querySelector("#minesweeper-game");
var score = document.querySelector('#score-time-count');
var flagsLeft = document.querySelector('#score-bomb-count');
var time = document.querySelector('.time');

var ticks = 0;
var cellSize = 30; // px

function Row() {
	var newRow = document.createElement('div');
	newRow.classList.add('row');
	newRow.style = `height: ${cellSize}px;`;
	return newRow;
}

function Cell(type) {
	var newCell = document.createElement('button');
	newCell.classList.add('cell');
	newCell.style = `height: ${cellSize}px; width: ${cellSize}px`;

	switch (type) {
		case " ":
			newCell.classList.add('closed');
			break;
		case "F":
			newCell.classList.add('flagged');
			break;
		case "0":
			newCell.classList.add('cleared');
			break;
		case "1":
		case "2":
		case "3":
		case "4":
		case "5":
		case "6":
		case "7":
		case "8":
			newCell.classList.add('mines-around-' + type);
			newCell.classList.add('cleared');
			newCell.innerHTML = type;
			break;
		case ".":
			newCell.classList.add('mine');
			break;
		case "X":
			newCell.classList.add('mine');
			newCell.classList.add('flagged-false');
			break;
		case "*":
			newCell.classList.add('mine-exploded');
			break;
	}
	return newCell;
}

function addCellToRow(cellElem, rowElem) {
	rowElem.appendChild(cellElem);
}

function addRowToField(rowElem) {
	mapElement.appendChild(rowElem);
}

function clearMap() {
	mapElement.innerHTML = "";
}

function repaintMap(map) {
	if (!map)
		return;

	clearMap();

	var mapSizes = {
		width: Math.min(map[0].length * cellSize, window.innerWidth),
		height: Math.min(map.length * cellSize, window.innerHeight)
	};

	mapElement.style = `width: ${mapSizes.width}px; height: ${mapSizes.height}px;`;
	windowElement.style = `width: ${mapSizes.width + 26}px;`;

	map.forEach(row => {
		var newRow = new Row();
		row.forEach(cell => addCellToRow(new Cell(cell), newRow));
		addRowToField(newRow);
	})
}

function addLeadingZeros(number) {
	return number < 10 ? `00${number}` :
		number < 100 ? `0${number}` : number
}

function currentDate() {
	var date = new Date();
	return `${date.getHours()}:${date.getMinutes()}`
}

function Minesweeper(difficulty, name, callback) {
	socket.emit("play", {difficulty, name});

	socket.on("update", function ({field, flags_left}) {
		score.innerHTML = addLeadingZeros(ticks++);
		time.innerHTML = currentDate()
		flagsLeft.innerHTML = addLeadingZeros(flags_left);

		repaintMap(field);

		var {action, coordinates} = callback(field);
		setTimeout(() => {
			socket.emit(action, {coordinates})
		}, 1000 / TPS)
	});

    socket.on("message", function (msg) {
        console.log('hey! new message from server: ' + msg);
    })
}
