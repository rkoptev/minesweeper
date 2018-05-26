// Setup
const level = "expert"; // beginner / intermediate / expert
const username = "vasiliy pupkin";
const TPS = 10; // ticks per second


function generateRandomCoordinatesAtField(field) {
	var maxY = field.length;
	var maxX = field[0].length;

	return [
		~~(Math.random() * maxX),
		~~(Math.random() * maxY)
	]
}

function onUpdate(newField) {
	var coordinates = generateRandomCoordinatesAtField(newField);

	// Think hard
	return {action: "open", coordinates};
}
