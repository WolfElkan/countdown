from itertools import permutations, combinations
from random import randint
from datetime import datetime, timedelta
# from countdown import Operation
from cards import cards
from os import get_terminal_size as gts
import re

bankfile = 'countdown.txt'
# bankfile = 'results/231225_1509_A140606.txt'

ways = 974860

TOTAL_LEVELS = 6

PRINTED = set([])

def eval_op(match):
	print(match)
	exit()

def cecil_eval(string):
	print(string)
	if 'X' in string:
		return 'X'
	string = re.sub(r'\((\d+)([+*/-])(\d+)\)', eval_op, string)
	print(string)
	exit()
	return string


def replace_eval(string):
	string = string.replace('[','(')
	string = string.replace(']',')')
	string = string.replace('+<','-')
	string = string.replace('>','')
	return eval(string)


def latex(string):
	string = string.replace('[','\\frac{')
	string = string.replace('/','}{')
	string = string.replace(']','}')
	string = string.replace('*','\\times')
	string = string.replace('+<','-')
	string = string.replace('>','')
	string = string.replace('(','\\left(')
	string = string.replace(')','\\right)')
	return string


def plug(vals, line, eval_function=eval):
	test = str(line)
	for x in range(TOTAL_LEVELS):
		test = test.replace(chr(97+x),'{'+str(x)+'}')
	test = test.format(*vals)
	# if eval(test) == 952:
	# 	print(line)
	# return (latex(test), eval_function(test))
	return (test, eval_function(test))

def solve(target, n1, n2, n3, n4, n5, n6, tol=0, eval_function=eval):
	nums = [n1, n2, n3, n4, n5, n6]
	with open(bankfile) as file:
		n_operands = 0
		for line in file:
			if line[-1] == '\n':
				line = line[:-1]
			if line.isdigit():
				n_operands = int(line)
				# print(n_operands)
				# continue
			else:
				for vals in combinations(nums, n_operands):
					try:
						test, result = plug(vals, line, eval_function)
						if type(result) is float and result.is_integer():
							result = int(result)
						if abs(result - target) <= tol:
							if test not in PRINTED:
								print(f'{test} = {result}')
								PRINTED.add(test)
					except ZeroDivisionError:
						pass

# solve(952, 3,6,25,50,75,100, eval_function=eval)


def possible(nums):
	with open('countdown.txt') as file:
		n_operands = 0
		for line in file:
			if line[-1] == '\n':
				line = line[:-1]
			if line.isdigit():
				n_operands = int(line)
			else:
				for vals in combinations(nums, n_operands):
					test = str(line)
					for x in range(TOTAL_LEVELS):
						test = test.replace(chr(97+x),'{'+str(x)+'}')
					test = test.format(*vals)
					try:
						yield eval(test)
					except ZeroDivisionError:
						yield None

recording = True

# def possible(nums):
# 	for x in range(ways):
# 		yield randint(100,1000)

# recording = False

# smalls = sum([ [x, x] for x in range(1,11) ], [])
# print(smalls)
# exit()

# def smallcombo(nsmall, pool=None, start_after=None):
# 	if pool is None:
# 		pool = smalls
# 	go = start_after is None
# 	bank = set([])
# 	for comb in combinations(pool, nsmall):
# 		if comb not in bank:
# 			bank.add(comb)
# 			if go:
# 				yield comb
# 			elif comb == start_after:
# 				go = True

# same = 0
# diff = 0
# k = 0
# # for x in combinations(smalls,2):
# for x in smallcombo(2):
# 	if x[0] == x[1]:
# 		same += 1
# 		k += 2/(20*19)
# 	else:
# 		diff += 1
# 		k += (2/20) * (2/19) * 2
# print('same',same)
# print('diff',diff)
# print(k)
# exit()

# for x in range(26):
# 	print(chr(97+x), end='')
# 	print('\b')

# prog_bar(0,5, False)
# for x in range(41):
# 	prog_bar(x,5)
# print()
# exit()

def get_likely(nsmall, nums, **kwargs):
	repeat = 6 - len(set(nums))
	result = 2 ** (nsmall - repeat*2)
	return result

def pretty_delta5(delta):
	time_var = delta.total_seconds()
	# time_var *= 600
	if time_var < 60:
		return '{:14.2f}'.format(time_var)
	s = time_var % 60
	time_var = int(time_var)
	time_var //= 60
	m = time_var % 60
	if time_var < 60:
		return '{:8}:{:05.2f}'.format(m, s)
	time_var //= 60
	h = time_var
	return "{:5}:{:02}:{:05.2f}".format(h, m, s)

def pretty_delta1(delta):
	time_var = delta.total_seconds()
	# time_var *= 600
	if time_var < 60:
		return '{:10.2f}'.format(time_var)
	s = time_var % 60
	time_var = int(time_var)
	time_var //= 60
	m = time_var % 60
	if time_var < 60:
		return '{:4}:{:05.2f}'.format(m, s)
	time_var //= 60
	h = time_var
	return "{:1}:{:02}:{:05.2f}".format(h, m, s)

def prog_bar(prog, total_bar, backspace=True):
	prog = int(prog)
	rem = prog % 8
	black = prog // 8
	white = total_bar - black
	if rem > 0:
		white -= 1
	result = chr(0x2588) * black + (chr(0x2590 - rem) if rem else '' ) + (' ' * white)
	result = chr(0x2595) + result + chr(0x258f) + ' '
	return result


PREV = {'tick':(datetime.now().second + 1) % 60}

def ppb(
		nums,
		count,
		lost,
		perm_count,
		print_mod,
		total_cards,
		curr_start,
		init_start,
		total_bar,
		bar_inc,
		ticks,
		force=False,
		PREV=PREV,
		**kwargs
	):
	# if datetime.now().second == PREV['tick']:
	# 	PREV['tick'] = (datetime.now().second + 1) % 60
	if force or count % print_mod == 0:

		init_time = datetime.now() - init_start
		curr_time = datetime.now() - curr_start
		# 	current_set_so_far = datetime.now() - curr_start
		# 	time_per_card = current_set_so_far / (count+1)
		# 	time_per_card_set = time_per_card * total_cards
		# else:
		# remaining_card_sets = total_cards - perm_count
		# etr = time_per_card_set * remaining_card_sets
		# eta = curr_start + etr
		cards_completed = max(perm_count - 1 + (count / ways), 0.0001)
		time_per_card_set = init_time / cards_completed
		card_sets_remaining = total_cards - cards_completed
		etr = card_sets_remaining * time_per_card_set
		eta = datetime.now() + etr
		# eta = ' {:5.2f}'.format(etr.total_seconds())
		# eta = cards_completed

		pb = ''
		pb += "{:5}/{}: ".format(perm_count, total_cards)
		pb += "{:3} {:3} {:3} {:3} {:3} {:3}".format(*nums)
		pb += ' -> {:3} '.format(lost)
		pb += prog_bar(count // bar_inc, total_bar)
		pb += "{:3} ".format(kwargs['likely'])
		# now = datetime.now().isoformat().replace('T',' ')
		pb += datetime.now().isoformat()[11:16]#.replace('T',' ')
		# pb += "{:8.2f}".format(curr_time.total_seconds())
		pb += pretty_delta1(curr_time)
		pb += eta.strftime(' %Y-%m-%d %H:%M ')
		print(pb, end='\b'*len(pb))
		# print(pb)
	# PREV['tick'] = datetime.now().second
	# print(PREV['tick'])

def get_mods(**kwargs):
	total_bar = gts()[0] - 83
	ticks = total_bar * 8
	bar_inc = ways // ticks
	result = {
		'total_bar': total_bar,
		'ticks': ticks,
		'bar_inc': bar_inc,
	}
	with open('mods.txt', 'r') as modfile:
		for line in modfile:
			if line[-1] == '\n':
				line = line[:-1]
			key, val = tuple(line.split(':'))
			result[key] = eval(val)
	return result
	# {
	# 	'refresh_mod': 10,
	# 	'print_mod':    1,
	# }

# ppb([1,2,3,4,5,6], 333, 222)

# print('aaaaa', end='')
# print('\b\b\b\b', end='')
# print('ccccc')

# prev_tick = datetime.now()
# print(prev_tick.second)
# exit()

FILEPATH = '{filepath}/{now:%y%m%d_%H%M}_{ip}_{nlarge}L{nsmall}S_{fxlarge}.tsv'

def find_possible(nlarge=None, **kwargs):
	if not recording:
		print('NOT RECORDING')
	kwargs.setdefault('filepath','results')
	kwargs['nlarge'] = nlarge
	kwargs['nsmall'] = 6 - nlarge
	kwargs['now'] = datetime.now()
	if 'xlarge' in kwargs:
		kwargs['fxlarge'] = '-'.join([ str(l) for l in kwargs['xlarge'] ])
	else:
		kwargs['fxlarge'] = ''

	nsmall = 6 - nlarge
	print("{}L/{}S".format(nlarge, nsmall), end='')
	print(' ', datetime.now())

	kwargs['total_impossible'] = 0
	kwargs['total_impossible_likely'] = 0

	kwargs['total_cards'] = len(list(cards(**kwargs)))
	kwargs['total_cards_likely'] = 0
	kwargs.update(get_mods(**kwargs))

	with open(FILEPATH.format(ip='I', **kwargs), 'w') as i_file, open(FILEPATH.format(ip='P', **kwargs), 'w') as p_file:
		kwargs['init_start'] = datetime.now()
		kwargs['perm_count'] = 0
		# for large in combinations([25, 50, 75, 100], nlarge):
		# for large in [(25, 75)]:
		# 	for small in smallcombo(nsmall, start_after=(1,4,9,9)):
				# nums = list(large) + list(small)
		kwargs['perfect_count'] = 0
		kwargs['perfect_count_likely'] = 0
		for nums in cards(**kwargs):
			kwargs['nums'] = nums
			found = [ x < 100 for x in range(1000) ]
			kwargs['lost'] = 900
			skip = False
			kwargs['count'] = 0
			count = 0
			kwargs['curr_start'] = kwargs['init_start'] if kwargs['perm_count'] == 0 else datetime.now()
			kwargs['perm_count'] += 1
			kwargs['likely'] = get_likely(**kwargs)
			kwargs['total_cards_likely'] += kwargs['likely']
			print()
			if kwargs['perm_count'] % kwargs['refresh_mod'] == 0:
				prev_kwargs = dict(kwargs)
				mods = get_mods(**kwargs)
				kwargs.update(mods)
				for key, val in kwargs.items():
					if val != prev_kwargs[key]:
						print(key+':',val)
			for target in possible(nums):
				ppb(**kwargs)
				kwargs['count'] += 1
				if (type(target) is int or type(target) is float and round(target, 6).is_integer()) and 100 <= target < 1000:
					target = int(target)
					if not found[target]:
						# ppb(**kwargs)
						kwargs['lost'] -= 1
						found[target] = True
					if all(found):
						if recording:
							p_file.write('\t'.join([ str(num) for num in nums ]))
							p_file.write('\n')
						kwargs['perfect_count'] += 1
						kwargs['perfect_count_likely'] += kwargs['likely']
						skip = True
						ppb(force=True, **kwargs)
						break
			# print()
			# print(kwargs['count'])
			if skip:
				continue
			else:
				impossible = list(filter(lambda x: not found[x], range(1000)))
				# print(impossible)
				kwargs['total_impossible'] += len(impossible)
				kwargs['total_impossible_likely'] += len(impossible) * kwargs['likely']
				if recording:
					for imp in impossible:
						i_file.write('\t'.join([ str(num) for num in nums ]) + '\t' + str(imp))
						i_file.write('\n')
	# t = 'Total Impossible: {:'+str(20 + len(str(kwargs['total_cards'])))+'}'

	kwargs['total_puzzles'] = kwargs['total_cards'] * 900
	t = "{perfect_count:5}/{total_cards} perfect {total_impossible:23}/{total_puzzles} impossible {gap}{total_time}"
	total_time = datetime.now() - kwargs['init_start']
	print()
	print(t.format(
		total_time=pretty_delta5(total_time),
		gap = ' ' * (kwargs['total_bar'] - 4 - len(str(kwargs['total_puzzles']))),
		**kwargs
	))

	kwargs['perfect_count_pct'] = kwargs['perfect_count_likely'] / kwargs['total_cards_likely'] * 100
	kwargs['total_puzzles_likely'] = kwargs['total_cards_likely'] * 900
	kwargs['total_impossible_pct'] = kwargs['total_impossible_likely'] / kwargs['total_puzzles_likely'] * 100
	t = "{perfect_count_likely:5}/{total_cards_likely} = {perfect_count_pct:5.1f}% {gap1}"
	t += "{total_impossible_likely:21}/{total_puzzles_likely} = {total_impossible_pct:5.1f}% {gap2}{avg_time} avg"
	print(t.format(
		avg_time=pretty_delta5(total_time/kwargs['total_cards']),
		gap1 = ' ' * (len(str(kwargs['total_cards'])) - len(str(kwargs['total_cards_likely']))),
		gap2 = ' ' * (kwargs['total_bar'] - len(str(kwargs['total_impossible_likely'])) - len(str(kwargs['total_puzzles'])) - 2),
		**kwargs
	))

	if recording:
		with open('{filepath}finished.txt'.format(**kwargs), 'a') as f_file:
			for ip in 'IP':
				f_file.write(FILEPATH.format(ip=ip, **kwargs))
				f_file.write('\n')

# find_possible(2, xlarge=(50, 100))
# find_possible(1, xlarge=(100,))
# find_possible(2, xlarge=(75, 100), start_after=(8,9,9,10))
# find_possible(4, special=True)
# find_possible(0)

# solve(261, 7,7,10,6,6,8, eval_function=replace_eval)
# solve(869,50,100,6,8,5,7, eval_function=replace_eval)
# solve(722,6,1,8,10,1,7, eval_function=replace_eval, tol=1)
# solve(519, 3,8,10,8,75,100, eval_function=replace_eval)
# solve(961, 75,50,1,1,7,7, eval_function=replace_eval, tol=1)
# solve(338, 75, 10, 3, 1, 3, 6, eval_function=replace_eval)
# solve(778, 25, 100, 7, 4, 7, 2, eval_function=replace_eval)
# solve(741, 25, 100, 75, 4, 5, 9, eval_function=replace_eval)
# solve(887, 25, 50, 100, 75, 6, 2, eval_function=replace_eval)
# solve(567, 100,6,2,7,3,10, eval_function=replace_eval)
# solve(704, 50,100,75,25,1,3, eval_function=replace_eval)


# print(solve(796, 1, 25,5,7,1,7,3))

			# for target in range(100,1000):
			# 	print(nums, '->', target, end=' ')
			# 	if possible(target, *nums):
			# 		print('-')
			# 	else:
			# 		print('*** IMPOSSIBLE! ***')

				# for perm in permutations(nums, n_operands):
					# k = list(perm)
					# k += [0] * (4 - len(k))
					# a, b, c, d = k
					# 	# if eval(line) == target:
					# 		line = line.replace('a',str(a))
					# 		line = line.replace('b',str(b))
					# 		line = line.replace('c',str(c))
					# 		line = line.replace('d',str(d))
					# 		# line = line.replace('e',str(e))
					# 		# line = line.replace('f',str(f))
					# 		print(line)


# solve(117, 25, 75, 100, 3, 6, 8)
# solve(835, 50, 10, 9, 2, 3)

# solve(743,1,9,4,2,50,75)