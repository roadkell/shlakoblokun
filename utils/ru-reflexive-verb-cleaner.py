#!/usr/bin/env python3
"""
Filter Russian verb list, removing reflexive ('-ся') verbs
when a nonreflexive form is present
"""

import argparse
import sys


def main() -> int:

	# Parse command line arguments
	argparser = argparse.ArgumentParser()
	argparser.add_argument('infile', type=argparse.FileType('r'),
	                       default=(None if sys.stdin.isatty() else sys.stdin))
	argparser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
	                       default=sys.stdout)
	args = argparser.parse_args()

	# Dedupe by importing words into a set
	wset = set()
	with args.infile as f:
		for w in f:
			w = w.strip()
			wset.add(w)

	# If a non-reflexive verb is present, remove reflexive form
	newset = set()
	for w in wset:
		if w.endswith('ся'):
			if not w.removesuffix('ся') in wset:
				newset.add(w)
		else:
			newset.add(w)

	# Write wordset into a plain text file, auto-adding newlines
	with args.outfile as f:
		for w in newset:
			print(w, file=f)

	return 0


if __name__ == '__main__':
	sys.exit(main())
