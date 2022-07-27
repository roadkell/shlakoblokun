#!/usr/bin/env python3
"""
Filter Russian verb list, removing reflexive ('-ся') verbs
when a nonreflexive form is present
"""

import argparse
import sys


def main() -> int:

	# Parse command line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('infile',
	                    type=argparse.FileType('r'),
	                    default=(None if sys.stdin.isatty() else sys.stdin))
	parser.add_argument('outfile',
	                    nargs='?',
	                    type=argparse.FileType('w'),
	                    default=sys.stdout)
	args = parser.parse_args()

	# Dedupe by importing words into a set
	words = set()
	with args.infile as f:
		for w in f:
			w = w.strip()
			words.add(w)

	# If a non-reflexive verb is present, remove reflexive form
	cleanwords = set()
	for w in words:
		if w.endswith('ся'):
			if not w.removesuffix('ся') in words:
				cleanwords.add(w)
		else:
			cleanwords.add(w)

	# Write sorted wordset into a plain text file, auto-adding newlines
	with args.outfile as f:
		for w in sorted(cleanwords):
			print(w, file=f)

	return 0


if __name__ == '__main__':
	sys.exit(main())
