#!/usr/bin/env python3
"""
Generate hilarious (or not) word blends from a vocabulary.

Each word is checked for overlapping characters against every other word.
It is considered a match when at least some chars are overlapping.
Example: "revenge" and "vengeance" have 5 overlapping chars,
so "reVENGEance" will be generated from this pair.
Both words must have some non-overlapping chars at the start/end.

Uses Russian YARN database, by default.
"""
# TODO: add README.md for ru/yarn.txt
# TODO: make a clean way of exiting infinite mode
# TODO: load all vocabularies from a directory for a given language

# ============================================================================ #

import argparse
import random
import string
import sys

from tqdm import tqdm

# ============================================================================ #


def main() -> int:
	print(' ┌\\\\────────────\\\\\\\\────────────\\\\┐')
	print('>│ Shlakoblokun: the word blender │°>')
	print(' └//────────────////────────────//┘')

	args = parse_args()

	print('Loading vocabulary...', end=' ')

	wlist = read_infile(args.infile, args.capwords, args.multiwords)

	print('Done.')
	print(len(wlist), 'words loaded,', len(wlist)**2, 'pairs to check.')
	print('Starting search for overlapping substrings in word pairs...')

	numblends = write_outfile(args.outfile, wlist, args.random, args.number, args.depth, args.uppercase)

	# TODO: add timer
	print('Done.')
	print(numblends, 'word blends generated.')

	return 0

# ============================================================================ #


def parse_args() -> argparse.Namespace:
	"""
	Parse command line arguments
	"""
	# TODO: argumentize min non-overlapping chars, min/max word len...
	parser = argparse.ArgumentParser()
	parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
	                    default='ru/yarn.txt',
	                    help='vocabulary file (plain text)')
	parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
	                    default='output.txt',
	                    help='output file (plain text)')
	parser.add_argument('-r', '--random', action='store_true',
	                    help='generate random blends, instead of going \
	                    sequentially through the vocabulary')
	parser.add_argument('-n', '--number', type=int, default=0,
	                    help='number of word blends to generate')
	parser.add_argument('-d', '--depth', type=int, default=2,
	                    help='minimum depth of blending (default: %(default)s)')
	parser.add_argument('-u', '--uppercase', action='store_true',
	                    help='uppercase overLAPping characters in the output')
	parser.add_argument('-c', '--capwords', action='store_true',
	                    help='also include Capitalized words (usually proper names)')
	parser.add_argument('-m', '--multiwords', action='store_true',
	                    help='also include multiword (space separated) phrases')
	args = parser.parse_args()
	return args

# ============================================================================ #


def read_infile(infile,
                incl_capwords: bool,
                incl_multiwords: bool) -> list:
	"""
	Read vocabulary file into a list
	"""
	wlist = []
	with infile:
		for w in infile:
			# Strip whitespace characters from both ends.
			# This is always required, as reading a textfile auto-appends '\n'.
			w = w.strip(string.whitespace)
			# Skip #comment lines, words with non-printables, words with <3 chars,
			# capitalized words (arg-dependent) and multiword strings (arg-dependent)
			if (w[0] != '#') \
			   and (len(w) > 2) \
			   and w.isprintable() \
			   and (incl_capwords or w.islower()) \
			   and (incl_multiwords or (' ' not in w)):
				wlist.append(w)
	return wlist

# ============================================================================ #


def write_outfile(outfile,
                  wlist: list,
                  randomblends: bool,
                  maxblends: int,
                  mindepth: int,
                  uppercase: bool) -> int:
	"""
	Search for overlapping characters at the start & end of all words,
	blend matching pairs, and write results into a text file.
	Dictionary is used to save the number of overlapping chars (as values)
	and to auto-deduplicate saved words (as keys).
	"""
	with outfile:

		# Show progress bars and ETAs
		if maxblends:
			blend_pbar = tqdm(total=maxblends,
			                  smoothing=0.01,
			                  dynamic_ncols=True,
			                  unit='w',
			                  desc='Word blends generated')
		else:
			blend_pbar = tqdm(smoothing=0.01,
			                  dynamic_ncols=True,
			                  unit='w',
			                  desc='Word blends generated')
		w1_pbar = tqdm(wlist,
		               smoothing=0.01,
		               dynamic_ncols=True,
		               unit='w',
		               desc='First words processed')

		wdict = dict()
		blend_ctr = 0
		w1_ctr = 0

		while w1_ctr < len(wlist) and (maxblends <= 0 or blend_ctr < maxblends):

			if randomblends:
				w1 = random.choice(wlist)
			else:
				w1 = wlist[w1_ctr]

			for w2 in tqdm(wlist,
			               leave=False,
			               dynamic_ncols=True,
			               unit='w',
			               desc='Current word vs. whole vocabulary'):
				(wblend, depth) = check_n_blend(w1, w2, mindepth, uppercase)
				if (depth > 0) \
				   and (wblend.lower() not in wlist) \
				   and (wblend not in wdict):
					wdict[wblend] = depth
					if not randomblends:
						# Dynamically write blended word into plain text file
						# together with overlap depth (\n is auto-appended)
						print(depth, wblend, file=outfile)
						blend_ctr += 1
						blend_pbar.update()

			if randomblends and len(wdict):
				# Randomly choose one of generated blends (if present)
				wblend = random.choice(list(wdict))
				depth = wdict[wblend]
				# Write blended word into a plain text file
				# together with overlap depth (\n is auto-appended)
				print(depth, wblend, file=outfile)
				wdict.clear()
				blend_ctr += 1
				blend_pbar.update()

			w1_ctr += 1
			w1_pbar.update()

		w1_pbar.close()
		blend_pbar.close()

	return blend_ctr

# ============================================================================ #


def check_n_blend(w1: str,
                  w2: str,
                  mindepth: int,
                  uppercase: bool) -> tuple[str, int]:
	"""
	Check a pair of words for overlapping characters.
	There must also be some non-overlapping characters in both words.
	If match is found, blend them.
	"""
	wblend = ''
	depth = 0
	if w1 != w2:
		for i in range(1, len(w1) - (mindepth-1)):
			if w2.startswith(w1[i:], 0, len(w2) - 1):
				# Match! Now blend w1 & w2:
				# take i non-overlapping chars from w1,
				# add overlapping chars(optionally UPPERCASE them),
				# then add remaining chars from w2.
				depth = len(w1[i:])
				if uppercase:
					wblend = ''.join((w1[:i], w1[i:].upper(), w2[depth:]))
				else:
					wblend = ''.join((w1, w2[depth:]))
				# After a match is found, exit for loop (this pair is done)
				break
	return (wblend, depth)

# ============================================================================ #


if __name__ == '__main__':
	sys.exit(main())
