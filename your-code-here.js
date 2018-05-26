/*

Welcome to the Minesweeper challenge!
TODO: Add description

 */

// Name to be displayed on dashboard
const username = "Anonymous";
// Choose game difficulty: beginner, intermediate, expert
const level = "beginner";
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
	var coordinates = generateRandomCoordinatesAtField(newField);

	// At the end you must to do a move
	return {action: "open", coordinates};
}
