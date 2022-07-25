#!/usr/bin/env python3
"""
Clean up Wiktionary plaintext dump and output result into plaintext file
"""

import argparse
import string
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
			# Ignore empty strings, words with unprintables,
			# words with colons and slashes (i.e. Wiktionary service pages)
			w = w.strip()
			if w \
			   and not w.isspace() \
			   and w.isprintable() \
			   and ('/' not in w) \
			   and (':' not in w):
				is_allowed = True
				has_letters = False
				for ch in w:
					# At least one letter must be present
					if ch.isalpha():
						has_letters = True
					# Only letters and punctuation are allowed
					if not (ch.isalpha() or (ch in string.punctuation)):
						is_allowed = False
						break
				if is_allowed and has_letters:
					wset.add(w)

	# Write wordset into a plain text file, auto-adding newlines
	with args.outfile as f:
		for w in wset:
			print(w, file=f)

	return 0


if __name__ == '__main__':
	sys.exit(main())
