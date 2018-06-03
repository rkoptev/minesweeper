var serverUrl = 'http://77.73.67.16:8154';

var mapSample = document.querySelector('#sample');
var body = document.querySelector('#playground');
var time = document.querySelector('.time');
var loadPrevBtn = document.querySelector('[name=load-prev]');


var ticks = 0;
var cellSize = 30; // px

function Row () {
	var newRow = document.createElement('div');
	newRow.classList.add('row');
	newRow.style = `height: ${cellSize}px;`;
	return newRow;
}

function Cell (type) {
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

function addCellToRow (cellElem, rowElem) {
	rowElem.appendChild(cellElem);
}

function addRowToField (rowElem, mapElement) {
	mapElement.appendChild(rowElem);
}

function clearMap (windowElement) {
    var mapElement = windowElement.querySelector('.map');
	mapElement.innerHTML = "";
}

function repaintMap (map, windowElement) {
	if (!map)
		return;

	clearMap(windowElement);

	var mapSizes = {
		width: Math.min(map[0].length * cellSize),
		height: Math.min(map.length * cellSize)
	};
    var mapElement = windowElement.querySelector('.map');

	mapElement.style = `width: ${mapSizes.width}px; height: ${mapSizes.height}px;`;
	windowElement.style = `width: ${mapSizes.width + 26}px;`;

	map.forEach(row => {
		var newRow = new Row();
		row.forEach(cell => addCellToRow(new Cell(cell), newRow));
		addRowToField(newRow, mapElement);
	})
}

function addLeadingZeros (number) {
	return number < 10 ? `00${number}` :
		number < 100 ? `0${number}` : number
}

function currentDate () {
	var date = new Date();
	return `${date.getHours()}:${date.getMinutes()}`
}

function renderWindow (field, flags_left, ticks, mapElement) {
    var score = mapElement.querySelector('.score-time-count');
    var flagsLeft = mapElement.querySelector('.score-bomb-count');

    score.innerHTML = addLeadingZeros(ticks);
    flagsLeft.innerHTML = addLeadingZeros(flags_left);

    repaintMap(field, mapElement);
}

function Map (name) {
    var newMap = mapSample.cloneNode(true);

    newMap.style = 'display: block';
    newMap.id = name;

    var titlebar = newMap.querySelector('.titlebar')
    titlebar.innerHTML = `Minesweeper (${name})`

    body.appendChild(newMap);
    return newMap;
}

function Minesweeper (difficulty, name, callback) {
    var socket = io(serverUrl + '/play');

    socket.emit("play", {difficulty, name});

    var map = new Map('name');
    var prevField = [];
    var tmp = [];

    loadPrevBtn.addEventListener('click', function() {
        renderWindow(prevField, 0, --ticks, map);
    })

	socket.on("update", function ({field, flags_left}) {
        time.innerHTML = currentDate();
        prevField = tmp;
        tmp = field;
		renderWindow(field, flags_left, ticks++, map);

        try {
            var {action, coordinates} = callback(field);
            if(action && coordinates)
                setTimeout(() => {
                    socket.emit(action, {coordinates});
        		}, 1000 / TPS);
            else
                console.log('please provide correct action and coordinates');
        } catch (e) {
            console.log('You submitted wrong turn.');
            console.log(e);
        }
	});

    socket.on("end_game", function ({win}) {
        if(win)
            alert('you win! :)');

        var prevField = tmp;
    } )
    socket.on("message", function (msg) {
        console.error(msg);
    });
}

function clearPlayground () {
    body.innerHTML = ''
}

function Dashboard () {
    var socket = io(serverUrl + '/watch');

    socket.on("state", function ({fields}) {
        clearPlayground();

        time.innerHTML = currentDate();

        ticks++;
        fields.forEach(({field, flags_left, name}, i) => {
            var map = new Map(name + i);
            renderWindow(field, flags_left, ticks, map);
        });
    });
}
