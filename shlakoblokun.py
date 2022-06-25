#!/usr/bin/env python3
"""
Blend words from a vocabulary.

Each word is checked for overlapping characters against every other word.
It is considered a match when at least 2 chars are overlapping.
Example: "revenge" and "vengeance" have 5 overlapping chars,
so "revengeance" will be generated from this pair.
Each word must have at least 1 non-overlapping char at the start/end.

Uses Russian YARN database, by default.
"""

import argparse
import string
import sys
from tqdm import tqdm

def main() -> int:

	print(' ┌\\\\────────────\\\\\\\\────────────\\\\┐')
	print('>│ Shlakoblokun: the word blender │°>')
	print(' └//────────────////────────────//┘')

	# Parse command line arguments
	# TODO: argumentize min non-overlapping chars, min/max word len...
	argparser = argparse.ArgumentParser()
	argparser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default='ru/yarn.txt')
	argparser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default='output.txt')
	argparser.add_argument('-r', '--random', action='store_true',
	                       help='generate random blends, instead of going sequentially through the vocabulary')
	argparser.add_argument('-n', '--number', type=int,
	                       help='limit the number of generated word blends')
	argparser.add_argument('-d', '--depth', type=int, default=2,
	                       help='minimum depth (number of overlapping characters) of blending (default: %(default)s)')
	argparser.add_argument('-u', '--uppercase', action='store_true',
	                       help='uppercase overlapping characters in the output')
	argparser.add_argument('-c', '--capwords', action='store_true',
	                       help='also include Capitalized words (usually proper names)')
	argparser.add_argument('-m', '--multiwords', action='store_true',
	                       help='also include multiword (space separated) phrases')

	args = argparser.parse_args()

	# Read input file into a list
	print('Loading vocabulary...', end=' ')
	wlist = []
	with args.infile as file:
		for w in file:
			# Strip whitespace characters from both ends.
			# This is required, as reading a textfile auto-appends '\n'.
			w = w.strip(string.whitespace)
			# Skip comment lines, words with non-printables, words with <2 chars,
			# capitalized words and multiword strings (last ones are opinionated)
			if (w[0] != '#') and (len(w) > 2) and w.isprintable() \
			and w.islower() and (' ' not in w):
				wlist.append(w)

	# Search for overlapping characters at the beginning & end of all words.
	# Dictionary is used to save the number of overlapping chars (as values)
	# and to auto-deduplicate saved words (as keys).
	print(len(wlist), 'words loaded,', len(wlist)**2, 'pairs to check.')
	print('Starting search for overlapping substrings in the words')
	print('(this may take a few hours, depending of vocabulary size)...')
	wdict = dict()
	with args.outfile as file:
		# Show progress bars and ETAs
		# TODO: print number of generated blends
		# (as a progress bar, if limit was set in the options)
		for w1 in tqdm(wlist, smoothing=0.01, dynamic_ncols=True,
		desc='Total words processed'):
			for w2 in tqdm(wlist, leave=False, dynamic_ncols=True,
			desc='Current word vs. whole vocabulary'):
				if w1 != w2:
					# There must be non-overlapping characters in both words
					for i in range(1, len(w1)-1):
						if w2.startswith(w1[i:], 0, len(w2)-1):
							# Match! Take non-overlapping i characters from w1,
							# add UPPERCASED overlapping chars,
							# then add remaining chars from w2
							w3 = ''.join((w1[:i], w1[i:].upper(), w2[len(w1[i:]):]))
							if (w3 not in wlist) and (w3 not in wdict):
								wdict[w3] = len(w1)-i
								# Write blend word into a plain text file
								# together with overlap depth (\n is auto-appended)
								print(wdict[w3], w3, file=file)
							# After a match, proceed to next pair
							break
	print('Done.')
	return 0

if __name__ == '__main__':
	sys.exit(main())
