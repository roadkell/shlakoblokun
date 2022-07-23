#!/usr/bin/env python3
"""
Filter wordlist, keeping only words in Cyrillic

Note, this includes many Cyrillic alphabets, see:
https://en.wikipedia.org/wiki/Cyrillic_alphabets
https://en.wikipedia.org/wiki/List_of_Cyrillic_letters
https://en.wikipedia.org/wiki/Cyrillic_script_in_Unicode
"""

import argparse
import string
import sys
import unicodedata


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
			if (len(w) > 1):
				is_allowed = True
				for ch in w:
					if not (('CYRILLIC' in unicodedata.name(ch))
					        or (ch in string.punctuation)):
						is_allowed = False
						break
				if is_allowed:
					wset.add(w)

	# Write wordset into a plain text file, auto-adding newlines
	with args.outfile as f:
		for w in wset:
			print(w, file=f)

	return 0


if __name__ == '__main__':
	sys.exit(main())
