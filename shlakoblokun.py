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

	print(len(wlist), 'words loaded,', len(wlist)**2, 'pairs to check.')
	print('Starting search for overlapping substrings in the words')
	print('(this may take seconds or hours, depending on vocabulary size)...')

	write_outfile(args.outfile, wlist, args.random, args.number, args.depth, args.uppercase)

	print('Done.')

	return 0

# ============================================================================ #


def parse_args() -> argparse.Namespace:
	"""
	Parse command line arguments
	"""
	# TODO: implement -d argument
	# TODO: argumentize min non-overlapping chars, min/max word len...
	parser = argparse.ArgumentParser()
	parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default='ru/yarn.txt')
	parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default='output.txt')
	parser.add_argument('-r', '--random', action='store_true',
	                    help='generate random blends, instead of going sequentially through the vocabulary')
	parser.add_argument('-n', '--number', type=int, default=0,
	                    help='number of word blends to generate (default: unlimited)')
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
                  uppercase: bool):
	"""
	Search for overlapping characters at the beginning & end of all words,
	blend matching pairs, and write results into a text file (dynamically).
	Dictionary is used to save the number of overlapping chars (as values)
	and to auto-deduplicate saved words (as keys).
	"""
	wdict = dict()
	blend_ctr = 0
	with outfile:
		if randomblends:
			# TODO: print number of generated blends in real-time
			# (as a progress bar, if limit was set in the options)
			while (maxblends <= 0) or (blend_ctr < maxblends):
				w1 = random.choice(wlist)
				# TODO: search for matching w2, instead of randomly trying
				w2 = random.choice(wlist)
				(wblend, depth) = check_n_blend(w1, w2, mindepth, uppercase)
				if (depth > 0) and (wblend not in wlist) and (wblend not in wdict):
					# Write blended word into a plain text file
					# together with overlap depth (\n is auto-appended)
					# TODO: argumentize output string format
					wdict[wblend] = depth
					print(depth, wblend, file=outfile)
					blend_ctr += 1
		else:
			# Show progress bars and ETAs
			# TODO: print number of generated blends in real-time
			# (as a progress bar, if limit was set in the options)
			for w1 in tqdm(wlist, smoothing=0.01, dynamic_ncols=True,
			               desc='Total words processed'):
				if (maxblends <= 0) or (blend_ctr < maxblends):
					for w2 in tqdm(wlist, leave=False, dynamic_ncols=True,
					               desc='Current word vs. whole vocabulary'):
						if (maxblends <= 0) or (blend_ctr < maxblends):
							(wblend, depth) = check_n_blend(w1, w2, mindepth, uppercase)
							if (depth > 0) and (wblend not in wlist) and (wblend not in wdict):
								# Write blended word into a plain text file
								# together with overlap depth (\n is auto-appended)
								# TODO: argumentize output string format
								wdict[wblend] = depth
								print(depth, wblend, file=outfile)
								blend_ctr += 1
						else:
							break
				else:
					break
	tqdm.write('Blends generated: ' + str(blend_ctr))
	return outfile

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
	i = 0
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
