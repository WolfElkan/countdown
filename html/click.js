// const ALLOW_FRACTIONS = true
const ALLOW_FRACTIONS = false

const ASSUME_EQUAL = true
// const ASSUME_EQUAL = false
// determines the behavior of clicking the wrong operator
// true: start a new line
// false: change to correct operator

function $$(selector) {
	return $(selector)[0]
}

function type(obj) {
	if (!obj) {
		return obj
	}
	return obj.__proto__.constructor
}

function make(tag) {
	return $(document.createElement(tag))
}

function Fraction(numer, denom=1) {
	if (type(numer) == Fraction) {
		this.numer = numer.numer
		this.denom = numer.denom
	} else {
		this.numer = numer
		this.denom = denom
	}
	this.become = (frac) => {
		this.numer = frac.numer
		this.denom = frac.denom
	}
	this.whole = () => {
		return Math.floor(this.numer / this.denom)
	}
	this.numod = () => {
		return this.numer % this.denom
	}
	this.triple = () => {
		this.clean()
		return [
			this.whole(),
			this.numod(),
			this.denom
		]
	}
	this.toString = () => {
		let triple = this.triple()
		if (triple[1] == 0) {
			return triple[0].toString()
		} else {
			return `${triple[0]}_${triple[1]}/${triple[2]}`
		}
	}
	this.clean = () => {
		let common = gcd(this.numer, this.denom)
		this.numer /= common
		this.denom /= common
		return this
	}
	this.get = () => {
		if (this.whole() == 0) {
			return this.numer / this.denom
		} else {
			return this
		}
	}
	this.number_div = () => {
		if (this.numod() == 0) {
			var element = make('div')
				element.text(this.whole)
				element.addClass('num')
		} else {
			var element = make('div')
				var whole = make('div')
					whole.text(this.whole())
					whole.addClass('whole')
					whole.addClass('w'+this.whole())
				element.append(whole)
				var fraction = make('table')
					var numer_tr = make('tr')
						var numer = make('td')
							numer.text(this.numod())
							numer.addClass('numer')
						numer_tr.append(numer)
					fraction.append(numer_tr)
					var denom_tr = make('tr')
						var denom = make('td')
							denom.text(this.denom)
							denom.addClass('denom')
						denom_tr.append(denom)
					fraction.append(denom_tr)
					fraction.addClass('fraction')
				element.append(fraction)
				element.addClass('frac')
		}
		element.addClass('log')
		return element
	}
}
Fraction.from_triple = (array) => {
	let whole = array[0]
	let numod = array[1]
	let denom = array[2]
	let numer = whole * denom + numod
	return new Fraction(numer, denom)
}
Fraction.add = (a, b) => {
	if (type(a) == Number && type(b) == Number) {
		return a + b
	} else {
		let A = new Fraction(a)
		let B = new Fraction(b)
		let na = A.numer * B.denom
		let nb = B.numer * A.denom
		let den = A.denom * B.denom
		return new Fraction(na+nb,den).clean()
	}
}
Fraction.sub = (a, b) => {
	if (type(a) == Number && type(b) == Number) {
		return a - b
	} else {
		let A = new Fraction(a)
		let B = new Fraction(b)
		let na = A.numer * B.denom
		let nb = B.numer * A.denom
		let den = A.denom * B.denom
		return new Fraction(na-nb,den).clean()
	}
}
Fraction.mul = (a, b) => {
	if (type(a) == Number && type(b) == Number) {
		return a * b
	} else {
		let A = new Fraction(a)
		let B = new Fraction(b)
		let num = A.numer * B.numer
		let den = A.denom * B.denom
		return new Fraction(num,den).clean()
	}
}
Fraction.div = (a, b) => {
	if (type(a) == Number && type(b) == Number && a % b == 0) {
		return a / b
	} else {
		let A = new Fraction(a)
		let B = new Fraction(b)
		let num = A.numer * B.denom
		let den = A.denom * B.numer
		return new Fraction(num,den).clean()
	}
}



class Operation {
	constructor(symbol, html) {
		this.symbol = symbol
		this.html = `&${html};`
	}
	element() {
		var el = make('div')
		el.addClass('log')
		el.addClass('op')
		el.html(this.html)
		return el
	}
	op_clickable () {
		return true
	}
	num_clickable(number) {
		let hypothetical = this.operate(CALC.buffer.concat([number]))
		// console.log(hypothetical)
		return hypothetical != undefined
	}
	click() {
		if (CALC.buffer.length > 0 && this.op_clickable()) {
			$('#current').append(this.element())
		} else {
			console.log(CALC)
		}
	}
	operate(numbers) {
		return numbers[0]
	}
	latex(numbers) {
		return numbers.join(this.symbol)
	}
}

// Instances

	ADD = new Operation('+', 'plus')
	ADD.operate = (numbers) => {
		if (ALLOW_FRACTIONS) {
			var result = new Fraction(0)
			for (var i = 0; i < numbers.length; i++) {
				result = Fraction.add(result, numbers[i])
			}
			return result
		} else {
			var result = numbers[0]
			for (var i = 1; i < numbers.length; i++) {
				result += numbers[i]
			}
			return result		
		}
	}

	SUB = new Operation('-', 'minus')
	SUB.operate = (numbers) => {
		if (ALLOW_FRACTIONS) {
			var result = new Fraction(numbers[0])
			for (var i = 1; i < numbers.length; i++) {
				result = Fraction.sub(result, numbers[i])
			}
			if (result.numer >= 0) {
				return result
			} else {
				return undefined
			}
		} else {
			result = numbers[0]
			for (var i = 1; i < numbers.length; i++) {
				result -= numbers[i]
			}
			if (result >= 0) {
				return result
			} else {
				return undefined
			}
		}
	}

	MUL = new Operation('*', 'times')
	MUL.operate = (numbers) => {
		if (ALLOW_FRACTIONS) {
			var result = new Fraction(1)
			for (var i = 0; i < numbers.length; i++) {
				result = Fraction.mul(result, numbers[i])
			}
			return result
		} else {
			var result = 1
			for (var i = 0; i < numbers.length; i++) {
				result *= numbers[i]
			}
			return result
		}
	}
	MUL.latex = (numbers) => {
		return numbers.join('\\times')
	}

	DIV = new Operation('/', 'divide')
	DIV.operate = (numbers) => {
		if (numbers.length != 2) {
			return undefined
		}
		if (numbers[0] % numbers[1] == 0) {
			return numbers[0] / numbers[1]
		} else if (ALLOW_FRACTIONS) {
			return Fraction.div(numbers[0], numbers[1])
		} else {
			return undefined
		}
	}
	DIV.latex = (numbers) => {
		return `\\frac{${numbers[0]}}{${numbers[1]}}`
	}
	DIV.op_clickable = () => {
		if (ALLOW_FRACTIONS) {
			return true
		}
		var available = $('.available')
		for (var i = 0; i < available.length; i++) {
			// console.log($(available[i]).text())
			if (CALC.buffer[0] % $(available[i]).text() == 0) {
				return true
			}
		}
		return false
	}
	DIV.num_clickable = (number) => {
		// console.log(number)
		return ALLOW_FRACTIONS || CALC.buffer[0] % number == 0
	}

function gcd(a, b) {
	var limit = 1000
	if (a == 0) {
		return b
	} else if (b == 0) {
		return a
	}
	while (a != b && limit > 0) {
		// console.log(a,b)
		limit--
		if (a > b) {
			if (a % b == 0) {
				return b
			} else {
				a %= b
			}
		} else {
			// b %= a
			let c = a
			a = b
			b = c
		}
	}
	return a
}

$(document).ready(() => {
	// arm()
	reset()
})

const CALC = {}
reset_calc()

function reset_calc() {
	// console.log('reset_calc')
	CALC.buffer = []
	CALC.op = new Operation()
	CALC.last = null
	$('#current').empty()
}

function reset() {
	console.log('reset:', format_duration(new Date() - CALC.start))
	$('.card').addClass('available')
	$('#previous').empty()
	reset_calc()
}

function pad(str, len=2, char='0') {
	str = String(str)
	while (str.length < len) {
		str = char + str
	}
	return str
}

function formatx(x) {
	return x.hour+x.hcolon+x.minute+x.mcolon+x.second+x.point+x.millis
}

function format_duration(time) {

	if (isNaN(time)) {
		return ''
	}

	if (time < 0) {
		return '-' + format_duration(-time)
	}

	var x = {
		'hour':   '',
		'hcolon': '',
		'minute': '',
		'mcolon': '',
		'second': '',
		'point':  '',
		'millis': '',
	}

	x.millis = time % 1000
	time = Math.floor(time / 1000)
	if (time == 0) {return formatx(x) + ' ms'}

	x.millis = pad(x.millis, 3)
	x.point = '.'
	x.second = time % 60
	time = Math.floor(time / 60)
	if (time == 0) {return formatx(x)}

	x.second = pad(x.second)
	x.mcolon = ':'
	x.minute = time % 60
	time = Math.floor(time / 60)
	if (time == 0) {return formatx(x)}

	x.minute = pad(x.minute)
	x.hcolon = ':'
	x.hour = time
	time = Math.floor(time / 60)
	return formatx(x)
}

function arm() {
	elements = $('.card').not('.armed')
	elements.each((index, element) => {
		// console.log(element)
		$(element).click(card_click)
		$(element).addClass('armed')
	})
}

function card_click(event) {
	// console.log(CALC.op.symbol)
	if (CALC.last == 'num') {
		CALC.op.click()
	}
	var card = $(event.currentTarget)
	var num = card.hasClass('log') ? card : $(card.children()[0])
	var number = card.hasClass('frac') ? parse_fraction_div(num) : num.text()
	if (type(number) == Array) {
		number = Fraction.from_triple(number)
	}
	// number = ALLOW_FRACTIONS ? Fraction.from_triple(number) : Number(number)
	// console.log(number)
	if (card.hasClass('available') && CALC.op.num_clickable(number)) {
		// console.log(number)
		click_num(number)
		$(card).removeClass('available')
		$('#current').append(number_div(number))
	}
}

function parse_fraction_div(card) {
	let impfrac = card.children()
	let whole = impfrac[0]
	let frac = impfrac[1]
	frac = $(frac).children()
	let numer = frac[0]
	let denom = frac[1]
	return [
		Number($(whole).text()),
		Number($(numer).text()),
		Number($(denom).text()),
	]
}

function number_div(number) {
	if (ALLOW_FRACTIONS) {
		var fraction = new Fraction(number)
		return fraction.number_div()
	} else {
		var element = make('div')
			element.text(number)
			element.addClass('num')
			element.addClass('log')
		return element
	}
}

function parse_fraction(number) {
	var result = Number(number)
	if (result == result) {
		return result
	} else {
		var match
		if (match = /(\d+),(\d+),(\d+)/.exec(number)) {
			return [
				match[1],
				match[2],
				match[3],
			]
		}
	}
	console.log(number)
}

function click_num(number) {
	CALC.buffer.push(ALLOW_FRACTIONS ? number : Number(number))
	CALC.last = 'num'
	// console.log(number)
}

function equals() {
	// console.log('equals')
	var expression = CALC.buffer.join(' '+CALC.op.symbol+' ')
	var result = CALC.op.operate(CALC.buffer)
	console.log(expression+' = '+result.toString())

	var eq = make('div')
	eq.text('=')
	eq.addClass('log')
	eq.addClass('eq')
	$('#current').append(eq)

	var solved = $('.target').text() == result

	// var card = make('div')
	// 	var num = make('div')
	// 		num.text(result)
	// 	card.append(num)
	// 	card.addClass('log')
	// 	card.addClass('num')
	var card = number_div(result)
		card.addClass('result')
		card.addClass(solved ? 'solved' : 'available')
		card.click(card_click)
	$('#current').append(card)

	$('.recent').removeClass('recent')
	var equation = make('div')
	var terms = $('#current').children()
	for (var i = 0; i < terms.length; i++) {
		equation.append(terms[i])
	}
	equation.addClass('recent')

	reset_calc()
	$('#previous').append(equation)

	if (solved) {
		$('.target').addClass('solved')
		console.log('Solved in', format_duration(new Date() - CALC.start))
	}
}

function op_click(operation) {
	if (CALC.op.symbol && CALC.op.symbol != operation.symbol) {
		if (ASSUME_EQUAL) {
			equals()
			CALC.op = operation
		}
	} else {
		CALC.op = operation
	}
	if (CALC.buffer.length == 0) {
		$('.recent .result').click()
	}
	CALC.last = 'op'
	CALC.op.click()
}

