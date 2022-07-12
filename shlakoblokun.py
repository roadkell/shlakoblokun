#!/usr/bin/env python3
"""
Blend words from a vocabulary.

Each word is checked for overlapping characters against every other word.
It is considered a match when at least 2 chars are overlapping.
Example: "revenge" and "vengeance" have 5 overlapping chars,
so "reVENGEance" will be generated from this pair.
Each word must have at least 1 non-overlapping char at the start/end.

Uses Russian YARN database, by default.
"""
# ============================================================================ #

import argparse
import string
import sys
from tqdm import tqdm

# ============================================================================ #

def main():

	print(' ┌\\\\────────────\\\\\\\\────────────\\\\┐')
	print('>│ Shlakoblokun: the word blender │°>')
	print(' └//────────────////────────────//┘')

	args = parse_args()

	print('Loading vocabulary...', end=' ')

	wlist = read_infile(args.infile, args.capwords, args.multiwords)

	print(len(wlist), 'words loaded,', len(wlist)**2, 'pairs to check.')
	print('Starting search for overlapping substrings in the words')
	print('(this may take a few hours, depending on vocabulary size)...')

	write_outfile(args.outfile, wlist, args.uppercase)

	print('Done.')

	return 0

# ============================================================================ #

def parse_args() -> argparse.Namespace:
	"""
	Parse command line arguments
	"""
	# TODO: implement -r,-n,-d arguments
	# TODO: argumentize min non-overlapping chars, min/max word len...
	parser = argparse.ArgumentParser()
	parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default='ru/yarn.txt')
	parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default='output.txt')
	parser.add_argument('-r', '--random', action='store_true',
	                       help='generate random blends, instead of going sequentially through the vocabulary')
	parser.add_argument('-n', '--number', type=int, default=0,
	                       help='number of word blends to generate (default: run indefinitely)')
	parser.add_argument('-d', '--depth', type=int, default=2,
	                       help='minimum depth of blending (default: %(default)s)')
	parser.add_argument('-u', '--uppercase', action='store_true',
	                       help='uppercase overlapping characters in the output')
	parser.add_argument('-c', '--capwords', action='store_true',
	                       help='also include Capitalized words (usually proper names)')
	parser.add_argument('-m', '--multiwords', action='store_true',
	                       help='also include multiword (space separated) phrases')
	args = parser.parse_args()
	return args

# ============================================================================ #

def read_infile(infile, incl_capwords: bool, incl_multiwords: bool) -> list:
	"""
	Read vocabulary file into a list
	"""
	wlist = []
	with infile:
		for w in infile:
			# Strip whitespace characters from both ends.
			# This is always required, as reading a textfile auto-appends '\n'.
			w = w.strip(string.whitespace)
			# Skip comment lines, words with non-printables, words with <2 chars,
			# capitalized words (arg-dependent) and multiword strings (arg-dependent)
			if (w[0] != '#') and (len(w) > 2) and w.isprintable() \
			and (incl_capwords or w.islower()) \
			and (incl_multiwords or (' ' not in w)):
				wlist.append(w)
	return wlist

# ============================================================================ #

def write_outfile(outfile, wlist: list, uppercase: bool):
	"""
	Search for overlapping characters at the beginning & end of all words,
	blend matching pairs, and write results into a text file.
	Dictionary is used to save the number of overlapping chars (as values)
	and to auto-deduplicate saved words (as keys).
	"""
	wdict = dict()
	with outfile:
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
							# Match!
							w3 = blend_words(w1, w2, i, uppercase)
							if (w3 not in wlist) and (w3 not in wdict):
								# Write blended word into a plain text file
								# together with overlap depth (\n is auto-appended)
								# TODO: argumentize output string format
								wdict[w3] = len(w1) - i
								print(wdict[w3], w3, file=outfile)
							# After a match, proceed to next pair
							break
	return 0

# ============================================================================ #

def blend_words(w1: str, w2: str, i: int, uppercase: bool) -> str:
	"""
	Take non-overlapping i characters from w1,
	add overlapping chars (optionally UPPERCASE them),
	then add remaining chars from w2
	"""
	if uppercase:
		w3 = ''.join((w1[:i], w1[i:].upper(), w2[len(w1[i:]):]))
	else:
		w3 = ''.join((w1, w2[len(w1[i:]):]))
	return w3

# ============================================================================ #

if __name__ == '__main__':
	sys.exit(main())
