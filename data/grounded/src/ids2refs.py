import sys
import os

refs = {}
for line in sys.stdin:
	line = line.rstrip()
	els = line.split("\t")
	hashstr = els[0]
	response = els[6]
	refs[hashstr] = response

with open(sys.argv[1]) as f:
	for line in f:
		line = line.rstrip()
		els = line.split("\t")
		sys.stdout.write(els[0])
		for i in range(1,len(els)):
			p = els[i].split('|')
			score = p[0]
			hashstr = p[1]
			if hashstr in refs.keys():
				sys.stdout.write("\t" + score + "|" + refs[hashstr])
			else:
				print("WARNING: missing ref, automatic eval scores may differ: [%s]" % hashstr, file=sys.stderr)
		sys.stdout.write("\n")
