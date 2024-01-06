import re


def resub(pattern, repl, string, **kwargs):
	return re.sub(pattern, lambda match: repl.format(*match.groups(), **match.groupdict()), string, **kwargs)

def refine(op, changed):
	initial = op
	op = resub(r'(\w)\+\((\w)\+(\w)\)', "{}+{}+{}", op)
	op = resub(r'(\w)\+\((\w)\-(\w)\)', "{}+{}-{}", op)
	op = resub(r'(\w)\*\((\w)\*(\w)\)', "{}*{}*{}", op)
	op = resub(r'(\w)\*\((\w)\/(\w)\)', "{}*{}/{}", op)
	op = resub(r'^\((.*?)\)$', "{}", op)
	if initial != op:
		print(initial,'->',op)
		changed[''] += 1
	return op

ops = set([])

with open('result/231225_1535_A140606.txt', 'r') as ifile, open('refined3.txt', 'w') as ofile:
	changed = {'':0}
	for line in ifile:
		if line[-1] == '\n':
			line = line[:-1]
		op = refine(line, changed)
		if op not in ops:
			ofile.write(op)
			ofile.write('\n')
		ops.add(op)

print(changed[''])