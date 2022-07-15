#!/usr/bin/env python3
"""
Dedupe a wordlist from a textfile or stdin, output as a new textfile or stdout.
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

	# Dedupe by importing worldlist into a set
	wordset = set()
	with args.infile as f:
		for word in f:
			wordset.add(word)
	with args.outfile as f:
		for word in wordset:
			f.write(word)

	return 0


if __name__ == '__main__':
	sys.exit(main())
