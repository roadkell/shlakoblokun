#!/usr/bin/env python3
"""
Generate hilarious (or not) portmanteaus from a vocabulary

Each word is checked for overlapping characters against every other word.
It is considered a match when at least some chars are overlapping.
Example: "revenge" and "vengeance" have 5 overlapping chars,
so "reVENGEance" will be generated from this pair.
Both words must have some non-overlapping chars at the start/end.
"""
# TODO: make a clean way of exiting infinite mode

# ============================================================================ #

import argparse
import os
import random
import sys
from collections import namedtuple
from pathlib import Path

from tqdm import tqdm

# ============================================================================ #


def main() -> int:
	print(' ┌────────────────┐')
	print(' │ SHLAKOBL⎛⎞⎟⎠   │')
	print(' │         ⎝⎠⎟⎞UN │')
	print(' └────────────────┘')
	print('Portmanteau Generator')
	print()

	print('Initializing...', end=' ')

	args = parse_args()

	# TODO: argumentize these
	wlen_min = 3

	# TODO: implement caching
	cachepath = Path('ru/.cache')
	CacheEntry = namedtuple('CacheEntry', ['w1', 'w2', 'blend', 'start', 'depth'])
	cachelist = read_cache(cachepath)

	print('Done.')
	print('Loading vocabulary...', end=' ')

	wlist = read_infiles(args.infiles)
	wlist = filter_list(wlist, wlen_min, args.capwords, args.multiwords)

	print('Done.')
	print(len(wlist), 'words loaded,', len(wlist)**2, 'pairs to check.')
	print('Starting search for overlapping substrings in word pairs...')

	numblends = write_outfile(args.outfile,
	                          wlist,
	                          cachelist,
	                          args.random,
	                          args.number,
	                          args.depth,
	                          args.uppercase)

	write_cache(cachepath, cachelist)

	# print('Done.')

	return 0

# ============================================================================ #


def parse_args() -> argparse.Namespace:
	"""
	Parse command line arguments
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('infiles', nargs='?', type=Path,
	                    default='ru',
	                    help='path to vocabulary file or directory')
	parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
	                    default=sys.stdout,
	                    help='path to output file')
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

	args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

	return args

# ============================================================================ #


def read_cache(cpath: Path) -> list[namedtuple]:
	"""
	Read cache file into a list of CacheEntries
	"""
	# TODO: use CSV
	clist = []
	with cpath.open() as f:
		for centry in f:
			clist.append(centry)

	return clist

# ============================================================================ #


def write_cache(cpath: Path, clist: list[namedtuple]):
	"""
	Write list of CacheEntries back into cache file
	"""
	# TODO: use CSV
	with cpath.open(mode='r+') as f:
		pass

	return 0

# ============================================================================ #


def read_infiles(inpath: Path) -> list:
	"""
	Get list of filenames for vocabulary file[s] and read their content
	"""
	pathset = set()
	inpath = inpath.resolve()
	if inpath.is_dir():
		for path in inpath.iterdir():
			# Ignore empty, hidden, and temp files
			if not path.is_dir() \
			   and not str(path).startswith('.') \
			   and not str(path).endswith('~') \
			   and (os.stat(path).st_size > 0):
				pathset.add(path)
	elif inpath.is_file() and (os.stat(inpath).st_size > 0):
		pathset.add(inpath)
	else:
		raise FileNotFoundError(str(inpath))

	# Using set to auto-dedupe word list
	wset = set()
	for path in pathset:
		wset |= set(read_infile(path))
	wlist = list(wset)

	return wlist

# ============================================================================ #


def read_infile(path) -> list:
	"""
	Read vocabulary file into a list
	"""
	wlist = []
	with path.open() as f:
		for w in f:
			# Strip whitespace characters from both ends. This is required,
			# as reading a textfile includes trailing newline characters.
			w = w.strip()
			# Skip empty strings, comment lines, words with non-printables
			if w \
			   and not w.isspace() \
			   and (w[0] != '#') \
			   and w.isprintable():
				wlist.append(w)

	return wlist

# ============================================================================ #


def filter_list(wlist: list,
                wlen_min: int,
                incl_capwords: bool,
                incl_multiwords: bool) -> list:
	"""
	Filter wordlist according to given arguments
	"""
	newlist = []
	for w in wlist:
		if (len(w) >= wlen_min) \
		   and (incl_capwords or w.islower()) \
		   and (incl_multiwords or (' ' not in w)):
			newlist.append(w)

	return newlist

# ============================================================================ #


def write_outfile(outfile,
                  wlist: list,
                  cachelist: namedtuple,
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
		if not randomblends:
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
				if wblend \
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
				if outfile == sys.stdout:
					tqdm.write(wblend)
				else:
					print(depth, wblend, file=outfile)
				wdict.clear()
				blend_ctr += 1
				blend_pbar.update()

			w1_ctr += 1
			if not randomblends:
				w1_pbar.update()

		if not randomblends:
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
