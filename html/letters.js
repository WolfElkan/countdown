var vowel_freq = {
	'A':15,
	'E':21,
	'I':13,
	'O':13,
	'U': 5,
}
var consonant_freq = {
	'B': 2,  
	'C': 3,  
	'D': 6,  
	'F': 2,  
	'G': 3,  
	'H': 2,  
	'J': 1,  
	'K': 1,  
	'L': 5,  
	'M': 4,  
	'N': 8,  
	'P': 4,  
	'Q': 1,  
	'R': 9,  
	'S': 9,  
	'T': 9,  
	'V': 1,  
	'W': 1,  
	'X': 1,  
	'Y': 1,  
	'Z': 1,  
}

function get_numbers_from_set(number_set, how_many=1) {
	result = []
	for (var i = 0; i < how_many; i++) {
		let rand = Math.random()
		rand *= number_set.length
		rand = Math.floor(rand)
		result = result.concat(number_set.splice(rand, 1))
	}
	return result
}

