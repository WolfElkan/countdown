import random
from itertools import combinations

def ways(n):
	if n == 1:
		yield lambda a: a
	if n == 2:
		yield lambda a, b: "("+a+"+"+b+")"
		yield lambda a, b: "("+a+"-"+b+")"
		yield lambda a, b: "("+b+"-"+a+")"
		yield lambda a, b: "("+a+"*"+b+")"
		yield lambda a, b: "("+a+"/"+b+")"
		yield lambda a, b: "("+b+"/"+a+")"
	if n == 3:
		yield lambda a, b, c: "("+a+"+"+b+"+"+c+")"
		yield lambda a, b, c: "("+b+"+"+c+"-"+a+")"
		yield lambda a, b, c: "("+a+"-"+b+"+"+c+")"
		yield lambda a, b, c: "("+a+"+"+b+"-"+c+")"
		yield lambda a, b, c: "("+a+"-"+b+"-"+c+")"
		yield lambda a, b, c: "("+b+"-"+a+"-"+c+")"
		yield lambda a, b, c: "("+c+"-"+a+"-"+b+")"
		yield lambda a, b, c: "(("+b+"+"+c+")*"+a+")"
		yield lambda a, b, c: "(("+a+"+"+c+")*"+b+")"
		yield lambda a, b, c: "(("+a+"+"+b+")*"+c+")"
		yield lambda a, b, c: "(("+b+"-"+c+")*"+a+")"
		yield lambda a, b, c: "(("+c+"-"+b+")*"+a+")"
		yield lambda a, b, c: "(("+a+"-"+c+")*"+b+")"
		yield lambda a, b, c: "(("+c+"-"+a+")*"+b+")"
		yield lambda a, b, c: "(("+a+"-"+b+")*"+c+")"
		yield lambda a, b, c: "(("+b+"-"+a+")*"+c+")"
		yield lambda a, b, c: "(("+b+"+"+c+")/"+a+")"
		yield lambda a, b, c: "(("+a+"+"+c+")/"+b+")"
		yield lambda a, b, c: "(("+a+"+"+b+")/"+c+")"
		yield lambda a, b, c: "(("+b+"-"+c+")/"+a+")"
		yield lambda a, b, c: "(("+c+"-"+b+")/"+a+")"
		yield lambda a, b, c: "(("+a+"-"+c+")/"+b+")"
		yield lambda a, b, c: "(("+c+"-"+a+")/"+b+")"
		yield lambda a, b, c: "(("+a+"-"+b+")/"+c+")"
		yield lambda a, b, c: "(("+b+"-"+a+")/"+c+")"
		yield lambda a, b, c: "("+a+"/("+b+"+"+c+"))"
		yield lambda a, b, c: "("+b+"/("+a+"+"+c+"))"
		yield lambda a, b, c: "("+c+"/("+a+"+"+b+"))"
		yield lambda a, b, c: "("+a+"/("+b+"-"+c+"))"
		yield lambda a, b, c: "("+a+"/("+c+"-"+b+"))"
		yield lambda a, b, c: "("+b+"/("+a+"-"+c+"))"
		yield lambda a, b, c: "("+b+"/("+c+"-"+a+"))"
		yield lambda a, b, c: "("+c+"/("+a+"-"+b+"))"
		yield lambda a, b, c: "("+c+"/("+b+"-"+a+"))"
		yield lambda a, b, c: "("+a+"*"+b+"*"+c+")"
		yield lambda a, b, c: "("+b+"*"+c+"/"+a+")"
		yield lambda a, b, c: "("+a+"/"+b+"*"+c+")"
		yield lambda a, b, c: "("+a+"*"+b+"/"+c+")"
		yield lambda a, b, c: "("+a+"/("+b+"*"+c+"))"
		yield lambda a, b, c: "("+b+"/("+a+"*"+c+"))"
		yield lambda a, b, c: "("+c+"/("+a+"*"+b+"))"
		yield lambda a, b, c: "(("+b+"*"+c+")+"+a+")"
		yield lambda a, b, c: "(("+a+"*"+c+")+"+b+")"
		yield lambda a, b, c: "(("+a+"*"+b+")+"+c+")"
		yield lambda a, b, c: "(("+b+"/"+c+")+"+a+")"
		yield lambda a, b, c: "(("+c+"/"+b+")+"+a+")"
		yield lambda a, b, c: "(("+a+"/"+c+")+"+b+")"
		yield lambda a, b, c: "(("+c+"/"+a+")+"+b+")"
		yield lambda a, b, c: "(("+a+"/"+b+")+"+c+")"
		yield lambda a, b, c: "(("+b+"/"+a+")+"+c+")"
		yield lambda a, b, c: "(("+b+"*"+c+")-"+a+")"
		yield lambda a, b, c: "(("+a+"*"+c+")-"+b+")"
		yield lambda a, b, c: "(("+a+"*"+b+")-"+c+")"
		yield lambda a, b, c: "(("+b+"/"+c+")-"+a+")"
		yield lambda a, b, c: "(("+c+"/"+b+")-"+a+")"
		yield lambda a, b, c: "(("+a+"/"+c+")-"+b+")"
		yield lambda a, b, c: "(("+c+"/"+a+")-"+b+")"
		yield lambda a, b, c: "(("+a+"/"+b+")-"+c+")"
		yield lambda a, b, c: "(("+b+"/"+a+")-"+c+")"
		yield lambda a, b, c: "("+a+"-("+b+"*"+c+"))"
		yield lambda a, b, c: "("+b+"-("+a+"*"+c+"))"
		yield lambda a, b, c: "("+c+"-("+a+"*"+b+"))"
		yield lambda a, b, c: "("+a+"-("+b+"/"+c+"))"
		yield lambda a, b, c: "("+a+"-("+c+"/"+b+"))"
		yield lambda a, b, c: "("+b+"-("+a+"/"+c+"))"
		yield lambda a, b, c: "("+b+"-("+c+"/"+a+"))"
		yield lambda a, b, c: "("+c+"-("+a+"/"+b+"))"
		yield lambda a, b, c: "("+c+"-("+b+"/"+a+"))"

for c in ways(3):
	print(c('a','b','c'))

phi = (5**0.5-1)/2
# a, b, c, d, e, f = [ phi+x for x in range(6) ]
a, b, c, d, e, f = [ random.randint(1,100000) for x in range(6) ]

def combos(nums):
	n = len(nums)
	if n <= 3:
		for way in ways(n):
			yield way(*nums)
	else:
		for pivot in range(1,n):
			for X in combinations(nums, pivot):
				Y = list(set(nums) - set(X))
				# print(X, Y)
				for x in combos(X):
					for y in combos(Y):
						for way in ways(2):
							yield way(x, y)

vals = []
count = 0
for x in combos(list('abcd')):
	val = eval(x)
	if val not in vals:
		vals.append(val)
		count += 1
		print(x, eval(x))

print(count)