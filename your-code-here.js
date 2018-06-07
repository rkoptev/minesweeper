// Welcome to the Minesweeper challenge!

// Uncomment following string if you are running on local server
//serverUrl = 'http://localhost:8154';

// Choose your name
const username = "Anonymous";
// Choose game difficulty: beginner, intermediate, expert
const level = "expert";
// How many moves per second you want to perform?
// (Hint: less values are good for step-to-step debugging, bigger values - for final testing)
// We recommend to start with 1 step per second
const TPS = 1;


function generateRandomCoordinatesAtField(field) {
    var maxY = field.length;
    var maxX = field[0].length;

    return [
        ~~(Math.random() * maxX),
        ~~(Math.random() * maxY)
    ]
}

// This is where your magic happens
function onUpdate(newField) {
    // In every game update you need to do a move
    // Possible moves: open, mark (place flag), unmark

	var coordinates = generateRandomCoordinatesAtField(newField);
	return {action: "open", coordinates};
}
