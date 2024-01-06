from itertools import combinations
from cards import cards

special = False

likely = dict([ (tuple(card), 0) for card in cards() ])
lookup = dict([ (tuple(card), None) for card in cards() ])
totals = dict([ (nlarge, 0) for nlarge in range(0,5) ])

smallpool = list(range(1,11)) * 2
smallpool.sort()
largepool = [25, 50, 75, 100] if not special else [12, 37, 62, 87]
for nlarge in range(0,5):
	nsmall = 6 - nlarge
	for large in combinations(largepool, nlarge):
		for small in combinations(smallpool, nsmall):
			nums = tuple(small + large)
			likely[nums] += 1
			lookup[nums] = nlarge
			totals[nlarge] += 1

# print(lookup)
# exit()
p = 0
for nums in likely:
	nlarge = lookup[nums]
	# print(nlarge)
	total = totals[nlarge]
	p += likely[nums] / total
	print("{2:3} {3:3} {4:3} {5:3} {6:3} {7:3} -> {0:3}/{1}".format(likely[nums], total, *nums))

# print(p)