function choice(nlarge, delay=1) {
	if (nlarge == null) {
		nlarge = Math.random()
		nlarge *= 5
		nlarge = Math.floor(nlarge)
	}
	clear_cards()
	cards = get_six_numbers(nlarge)
	display_cards(cards, delay)
	if ($('.target').text() == '000') {
		setTimeout(() => {generate_target((target) => {
			// console.log(cards, target)
			console.log(`solve(${target},${cards.join(',')})`)
			arm()
		}, delay)}, 6000*delay)
	}
}

function clear_cards() {
	var card_divs = $('.card')
	// console.log(card_divs)
	card_divs.text('')
	for (var i = 0; i < card_divs.length; i++) {
		let n_class = card_divs[i].classList[1]
		if (n_class) {
			$(card_divs[i]).removeClass(n_class)
		}
	}
}

function get_six_numbers(nlarge) {
	// return [100,6,2,7,3,10]
	var numbers = []
	var nsmall = 6 - nlarge
	numbers = numbers.concat(get_numbers_from_set(LARGE, nlarge))
	numbers = numbers.concat(get_numbers_from_set(SMALL, nsmall))
	return numbers		
}

const LARGE = [25,50,75,100]
// const LARGE = [12,37,62,87]
const SMALL = [1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10]

function get_numbers_from_set(number_set, how_many) {
	result = []
	for (var i = 0; i < how_many; i++) {
		let rand = Math.random()
		rand *= number_set.length
		rand = Math.floor(rand)
		result = result.concat(number_set.splice(rand, 1))
	}
	return result
}

function generate_target(callback, delay=1) {
	if (delay > 0) {
		for (var i = 0; i < 19; i++) {
			setTimeout(() => {
				$('#target').text(get_target_number())
			}, i*50*delay);
		}
	}
	setTimeout(() => {
		var target = get_target_number()
		// var target = 567
		$('#target').text(target)
		CALC.start = new Date()
		if (callback) {
			callback(target)
		}
	}, 1000*delay)
	$('.target').removeClass('solved')
}

function get_target_number() {
	var target = Math.random()
	target *= 900
	target += 100
	target = Math.floor(target)
	return target
}

function display_cards(numbers, delay=1) {
	var cards = $('.card')
	for (var i = 0; i < numbers.length; i++) {
		display_card(cards, numbers, i, delay);
	}
}

function display_card(cards, numbers, i, delay=1) {
	setTimeout(() => {
		let card = $(cards[i])[0]
		$(card).empty()
		let num = make('div')
			num.text(numbers[i])
		$(card).append(num)
		// cards[i].innerText = numbers[i]
		// num.text(numbers[i])
		$(card).addClass('available')
		// cards[i].classList.add('n' + numbers[i])
		$(card).addClass('n' + numbers[i])
	}, (1000 * (5-i) + 500) * delay)
}

