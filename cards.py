from itertools import combinations

def smallcombo(nsmall, pool=None, start_after=None, **kwargs):
	# print(nsmall)
	if pool is None:
		pool = list(range(1,11)) * 2
		pool.sort()
	go = start_after is None
	bank = set([])
	for comb in combinations(pool, nsmall):
		if comb not in bank:
			bank.add(comb)
			if go:
				yield comb
			elif comb == start_after:
				go = True

# def largecombo(nlarge, xlarge=None, special=False, **kwargs):


def cards(nlarge=None, xlarge=None, special=False, **kwargs):
	larges = [25, 50, 75, 100] if not special else [12, 37, 62, 87]
	for nlarge in range(4,-1,-1) if nlarge is None else [nlarge]:
		kwargs['nsmall'] = 6 - nlarge
		if type(xlarge) is tuple:
			xlarge = [xlarge]
		for large in combinations(larges, nlarge) if xlarge is None else xlarge:
			for small in smallcombo(**kwargs):
				# nums = list(large) + list(small)
				nums = list(small) + list(large)
				yield nums
				# print('\t'.join([ str(num) for num in nums ]))

from datetime import timedelta

k = timedelta(0,27)
# print(k)

# print(len(list(cards(4)))*k)

# print(len(list(cards(3)))*k)0

# print(len(list(cards(2, xlarge=(25, 50))))*k)
# print(len(list(cards(2, xlarge=(25, 75))))*k)
# print(len(list(cards(2, xlarge=(25,100))))*k)
# print(len(list(cards(2, xlarge=(50, 75))))*k)
# print(len(list(cards(2, xlarge=(50,100))))*k)
# print(len(list(cards(2, xlarge=(75,100))))*k)

# print(len(list(cards(1, xlarge=(25,)))))
# print(len(list(cards(1, xlarge=(50,))))*k)
# print(len(list(cards(1, xlarge=(75,))))*k)
# print(len(list(cards(1, xlarge=(100,))))*k)

count = {}

# print(len(list(cards(0)))/3)

# print(1296*k)


# print(len(list(cards(0))))
# for nums in cards(0):
# 	key = '{0}-{1}'.format(*nums)
# 	count.setdefault(key, 0)
# 	count[key] += 1
# 	# print(nums)

# print(count)
# print(len(list(cards())))

# for x in cards():
# 	print(x)
# 	pass
