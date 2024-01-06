import random, re
from itertools import permutations
from datetime import datetime, timedelta

START = datetime.now()

G = 5
TOTAL_LEVELS = 6
alphabet = 'abcdef'

def getrand():
	return random.random()

TEST_SETS = [ [ getrand() for t in range(TOTAL_LEVELS) ] for g in range(G) ]
# TEST_SETS = None

BLACK, RED, GREEN, BLUE, RESET = ('','','','','')

# BLACK = '\u001b[30m'
# RED   = '\u001b[31m'
# GREEN = '\u001b[32m'
# BLUE  = '\u001b[34m'
# RESET = "\u001b[0m"

def prog_bar(prog, color=''):
	rem = prog % 8
	return chr(0x2588) * (prog // 8) + (chr(0x2590 - rem) if rem else '' )


class Operation(object):
	"""docstring for Operation"""
	def __init__(self, number_lam, string_lam=None, n_operands=2, symbol='', subops=['nop','nop']):
		
		self.symbol = symbol

		self.number_lam = number_lam
		
		if string_lam is None:
			string_lam = lambda a, b: '(' + str(a) + self.symbol + str(b) + ')'
		self.string_lam = string_lam
		
		self.n_operands = n_operands
		
		if TEST_SETS:
			self.dyn_vals = [ self(*ts[:self.n_operands]) for ts in TEST_SETS ]
		
		self.isSorted = re.sub(r'\W','',str(self)) == alphabet[:self.n_operands]
		
		for s in range(len(subops)):
			if subops[s] == 'nop':
				subops[s] = Operation.nop()
		self.subops = subops

	def __call__(self, *args):
		typeset = set([ type(arg) for arg in args ])
		if typeset == {str}:
			return self.string_lam(*args)
		elif typeset in [{int}, {float}]:
			return self.calc_numbers(*args)
		elif typeset == {Operation}:
			return self.compose(*args)

	def calc_numbers(self, *args):
		if NotImplemented in args:
			return NotImplemented
		return self.number_lam(*args)

	def latex(self):
		if self.symbol == '':
			return self.__str__()
		elif self.symbol == '-':
			pass
		else:
			return self.symbol.join([ subop.latex() for subop in self.subops ])

	def compose(self, *args):
		n_operands = sum([ arg.n_operands for arg in args ])
		number_lam = lambda *nums: self.number_lam(args[0].number_lam(*(nums[:args[0].n_operands])), args[1].number_lam(*(nums[args[0].n_operands:])))
		string_lam = lambda *nums: self.string_lam(args[0].string_lam(*(nums[:args[0].n_operands])), args[1].string_lam(*(nums[args[0].n_operands:])))
		result = Operation(number_lam, string_lam, n_operands)
		result.subops = args
		return result

	def __str__(self):
		return self.string_lam(*list(alphabet[:self.n_operands]))

	def __repr__(self):
		return 'Operation.text("{}")'.format(self)

	def __format__(self, *args, **kwargs):
		return str(self).__format__(*args, **kwargs)

	def __eq__(self, other):
		if type(other) is not Operation:
			return False
		if self.n_operands != other.n_operands:
			return False
		if TEST_SETS:
			for g in range(len(TEST_SETS)):
				if abs(self.dyn_vals[g] - other.dyn_vals[g]) > 1e-8:
					return False
			return True
		else:
			for g in range(G):
				rands = [ getrand() for x in range(self.n_operands) ]
				if abs(self(*rands) - other(*rands)) > 1e-8:
					return False
			return True

	def __hash__(self):
		return hash(tuple([ NotImplemented if val == NotImplemented else round(val,8) for val in self.dyn_vals ]))

	def permute(self, *perm):
		assert len(perm) == self.n_operands
		number_lam = lambda *args: self.number_lam(*[ args[x] for x in perm ])
		string_lam = lambda *args: self.string_lam(*[ args[x] for x in perm ])	
		return Operation(number_lam, string_lam, self.n_operands)

	@staticmethod
	def text(txt):
		opsym = {
			'+':'add',
			'-':'sub',
			'*':'mul',
			'/':'div',
			'**':'exp',
			'add':'add',
			'sub':'sub',
			'mul':'mul',
			'div':'div',
			'exp':'exp',
		}
		txt = re.sub(r'\(\w([+*/-])\w\)',lambda match: opsym[match[1]], txt)
		txt = re.sub(r'\((?P<x>\w|add|sub|mul|div|exp)(?P<c>[+*/-])(?P<y>\w|add|sub|mul|div|exp)\)',lambda match: "{c}({x},{y})".format(opsym[match['c']], **match.groupdict()), txt)
		print(txt)

	@staticmethod
	def nop():
		return Operation(
			number_lam = lambda a: a, 
			string_lam = lambda a: a, 
			n_operands=1, 
			subops=[]
		)

class Add(Operation):
	"""Operation object for Addition"""
	def __init__(self, *subops):
		super(Add, self).__init__(
			number_lam = lambda a, b: a + b, 
			symbol = '+',
		)
	def __neg__(self):
		return Add()(-self.subops[0],-self.subops[1])


		
class Sub(Operation):
	"""Operation object for Subtraction"""
	def __init__(self, *subops):
		super(Sub, self).__init__(
			number_lam = lambda a, b: a - b, 
			symbol = '-',
		)
	def __neg__(self):
		return Sub()(self.subops[1],self.subops[0])
		
class Mul(Operation):
	"""Operation object for Multiplication"""
	def __init__(self, *subops):
		super(Mul, self).__init__(
			number_lam = lambda a, b: a * b, 
			symbol = '*',
		)
		
class Div(Operation):
	"""Operation object for Division"""
	def __init__(self, *subops):
		super(Div, self).__init__(
			number_lam = lambda a, b: a / b, 
			symbol = '/'
		)
		
Nop = Operation.nop


		
print(Add())
print(Sub())
print(Mul())
print(Div())

		

# print(Add(Sub(),Nop()))

# ops = [Add(), Sub(), Mul(), Div()]


# ops.append(exp)

# j = add(add,nop)
# k = add(nop,add)

# k = add(mul, mul)
# k = Operation.text("((a*b)+(c*d))")

# print(k(2,3,4,5))

# print(ops)
# exit()

# print(j)
# print(k.permute((1,0,2)))
# print(j==k)
# exit()

s_A140606 = [1, 4, 12, 204, 5196, 163596, 6119437]

class OperationBank(object):
	def __init__(self, file):
		self.file = file
		self.bank = [ set([]) for level in range(TOTAL_LEVELS+1) ]
		self.count = 0
		self.calls = 0
		self.since = 0
		self.large = 0
		self.prev = datetime.now()
	def __call__(self, op, base_op='', bypass=False):
		# self.bank.setdefault(op.n_operands, [])
		self.calls += 1
		self.since += 1
		added = False
		if bypass or op not in self.bank[op.n_operands]:
			added = True
			self.bank[op.n_operands].add(op)
			self.write(op)
			self.count += 1
			self.since = 0
		else:
			if self.since > self.large:
				self.large = self.since
		self.print(op, base_op, added)
	def print(self, op, base_op='', added=None):
		# color = ''
		# if added is not None:
		# 	color = GREEN if added else RED
		now = datetime.now()
		diff = now - self.prev

		# if op.n_operands < 6:
		pct = self.calls / s_A140606[op.n_operands]
		# else:
		# 	pct = self.count / 821389

		print("{nop} {calls:8} {pct:6.2f}% {spct:6.2f}% {since:8} {large:8} {base:30} -> {color}{op:30}{reset} {diff} {count:8} {bar}".format(
			nop   = op.n_operands,
			calls = self.calls,
			pct   = pct * 100,
			spct  = (pct**2) * 100,
			since = self.since,
			large = self.large,
			base  = base_op,
			op    = op.latex(),
			diff  = diff,
			count = self.count,
			color = BLUE if added else '',
			reset = RESET if added else '',
			bar   = prog_bar(int(diff / timedelta(0,0.000010)+0.5)),
		))
		self.prev = now
	def write(self, text):
		text = str(text)
		# text = text.replace('*','\\times')
		# text = text.replace('/','}{')
		# text = text.replace('[','\\frac{')
		# text = text.replace(']','}')
		text = text.replace(' ','')
		self.file.write(text)
		self.file.write('\n')
	def __getitem__(self, key):
		return self.bank[key]


					# class FileBank(OperationBank):
					# 	"""docstring for FileBank"""
					# 	def __init__(self, source_file, file):
					# 		super(FileBank, self).__init__(file)
					# 		self.source_file = source_file
					# 		for line in self.source_file:
					# 			if line[-1] == '\n':
					# 				line = line[:-1]
					# 			self(Operation.text(line), bypass=True)

					# with open('countdown5.txt','r') as source_file, open('countdown6.txt','w') as file:

					# 	bank = FileBank(source_file, file)

					# 	for op in ops:
					# 		bank(op)

					# 	for N in range(6,TOTAL_LEVELS+1):

					# 		if N > 1:
					# 			for p in range(1,N):
					# 				for x in bank[p]:
					# 					for y in bank[N-p]:
					# 						for c in ops:
					# 							op = c(x,y)
					# 							if op.isSorted:
					# 								for perm in permutations(range(N)):
					# 									bank(op.permute(*perm), op)

							
					# exit()


with open('A140606.txt', 'w'):
	pass

#       1       1       1
#       6       7      12
#      68      75     204
#    1170    1245    5196
#   27142   28387  163596
#  793002  821389 6119437

def go():

	filepath = 'results/{:%y%m%d_%H%M}_A140606.txt'.format(datetime.now())

	with open(filepath,'w') as file:

		bank = OperationBank(file)

		file.write('1\n')
		bank(nop)
		file.write('2\n')

		for op in ops:
			bank(op)

		for N in range(2,TOTAL_LEVELS+1):
			if N > 2:
				file.write(str(N))
				file.write('\n')
			if N > 1:
				for p in range(1,N):
					for x in bank[p]:
						for y in bank[N-p]:
							for c in ops:
								op = c(x,y)
								if op.isSorted:
									for perm in permutations(range(N)):
										bank(op.permute(*perm), op)

			print(datetime.now())

	with open('results/finished.txt', 'a') as file:
		file.write(filepath)
		file.write('\n')

	print(datetime.now() - START)

			# with open('A140606.txt', 'a') as A140606:
			# 	A140606.write(str(len(bank[N])))
			# 	A140606.write('\n')

# go()