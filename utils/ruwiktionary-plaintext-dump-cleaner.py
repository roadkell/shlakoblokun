#!/usr/bin/env python3
"""
Clean up ru-Wiktionary plaintext dump, output as a new textfile or stdout.
"""

import argparse
import string
import sys
import unicodedata


def main() -> int:

	# Parse command line arguments
	argparser = argparse.ArgumentParser()
	argparser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
	                       default='../ru/.unprocessed/wiktionary.txt')
	argparser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
	                       default='../ru/wiktionary.txt')
	args = argparser.parse_args()

	# Dedupe by importing words into a set
	wset = set()
	with args.infile as f:
		for w in f:
			# Ignore empty strings, single chars, words with unprintables,
			# words with colons (Wiktionary service pages)
			w = w.strip(string.whitespace)
			if (len(w) > 1) \
			   and not w.isspace() \
			   and w.isprintable() \
			   and (':' not in w):
				is_cyrillic = True
				for ch in w:
					# Only cyrillic letters and punctuation are allowed
					if not (ch.isalpha()
					        and ('CYRILLIC' in unicodedata.name(ch))
					        or (ch in string.punctuation)):
						is_cyrillic = False
						break
				if is_cyrillic:
					wset.add(w)

	# Write word list into a plain text file, auto-adding newlines
	with args.outfile as f:
		for w in wset:
			print(w, file=f)

	return 0


if __name__ == '__main__':
	sys.exit(main())
