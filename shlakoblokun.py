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
# TODO: separate logic from presentation

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
	print('         \\\\\\\\\\\\\\\\')
	print('   ┌────────────────┐__')
	print(' \\\\│ SHLAKOBL⎛⎞⎟⎠   │ °_\\')
	print(' //│         ⎝⎠⎟⎞UN │___/')
	print('   └────────────────┘')
	print('  Portmanteau Generator')
	print()

	args = parse_args()

	# TODO: implement caching
	cachepath = Path('ru/.cache')
	CacheEntry = namedtuple('CacheEntry', ['w1', 'w2', 'blend', 'start', 'depth'])
	# cachelist = read_cache(cachepath)
	cachelist = []

	print('Loading vocabulary...', end=' ')

	words = [[], []]
	(words[0], words[1]) = read_infiles(args.infile, args.w1, args.w2)

	for (i, ws) in enumerate(words):
		words[i] = filter_words(ws,
		                        args.randomize,
		                        args.length,
		                        args.capwords,
		                        args.multiwords)

	print('Done.')
	print(len(words[0]) + len(words[1]), 'words loaded,',
	      len(words[0]) * len(words[1]), 'pairs to check.')
	print('Starting search for overlapping substrings in word pairs...')

	numblends = write_outfile(args.outfile,
	                          words,
	                          cachelist,
	                          args.number,
	                          args.depth,
	                          args.uppercase)

	# write_cache(cachepath, cachelist)

	# print('Done.')

	return 0

# ============================================================================ #


def parse_args() -> argparse.Namespace:
	"""
	Parse command line arguments
	"""
	parser = argparse.ArgumentParser()

	parser.add_argument('-i', '--infile',
	                    nargs='*',
	                    default=(None if sys.stdin.isatty() else sys.stdin),
	                    help='source vocabulary file[s] or dir[s]')
	parser.add_argument('-w1',
	                    nargs='*',
	                    help='vocabulary file[s]/dir[s] to only source 1st words from')
	parser.add_argument('-w2',
	                    nargs='*',
	                    help='vocabulary file[s]/dir[s] to only source 2nd words from')
	parser.add_argument('-o', '--outfile',
	                    nargs='?',
	                    type=argparse.FileType('w'),
	                    default=sys.stdout,
	                    help='output file')
	parser.add_argument('-r', '--randomize',
	                    action='store_true',
	                    help='shuffle vocabulary, instead of going alphabetically')
	parser.add_argument('-n', '--number',
	                    type=int,
	                    default=0,
	                    help='number of word blends to generate (default: unlimited)')
	parser.add_argument('-d', '--depth',
	                    type=int,
	                    default=2,
	                    help='minimum depth of blending (default: %(default)s)')
	parser.add_argument('-l', '--length',
	                    type=int,
	                    default=3,
	                    help='minimum length of source words (default: %(default)s)')
	parser.add_argument('-u', '--uppercase',
	                    action='store_true',
	                    help='uppercase overLAPping characters in the output')
	parser.add_argument('-c', '--capwords',
	                    action='store_true',
	                    help='also include Capitalized words (usually proper names)')
	parser.add_argument('-m', '--multiwords',
	                    action='store_true',
	                    help='also include multiword (space separated) phrases')

	args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

	if not (args.infile or args.w1 or args.w2):
		parser.error('No source vocabularies specified')

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


def read_infiles(*pathstrs) -> tuple[list, list]:
	"""
	Get list of filenames for vocabulary file[s] and read their content
	"""
	pathsets = [set(), set(), set()]    # common, w1, w2
	for (i, pp) in enumerate(pathstrs):
		if type(pp) == list:
			for p in pp:
				pathsets[i] |= pathstr2pathset(p)
		elif type(pp) == str:
			pathsets[i] = pathstr2pathset(pp)
		# else:
			# print(str(pp) + ' is not a valid path, skipping...')

	wordsets = [set(), set(), set()]
	for (i, ps) in enumerate(pathsets):
		for p in ps:
			wordsets[i] |= set(file2list(p))

	w1s = sorted(wordsets[0] | wordsets[1])
	w2s = sorted(wordsets[0] | wordsets[2])

	return (w1s, w2s)

# ============================================================================ #


def pathstr2pathset(pathstr: str) -> set[Path]:
	"""
	Unwrap a given nonempty path string into a set of absolute paths
	"""
	paths = set()
	if pathstr:
		path = Path(pathstr).resolve()
		if path.is_dir():
			for p in path.iterdir():
				# Ignore empty, hidden, and temp files
				if not p.is_dir() \
				   and not str(p).startswith('.') \
				   and not str(p).endswith('~') \
				   and (os.stat(p).st_size > 0):
					paths.add(p)
		elif path.is_file() and (os.stat(path).st_size > 0):
			# If a path to a file is given, always read it, even if temp/hidden
			paths.add(path)

	return paths

# ============================================================================ #


def file2list(path: Path) -> list[str]:
	"""
	Import words from a single vocabulary file into a list
	"""
	words = []
	with path.open() as f:
		for w in f:
			if w:
				# Strip whitespace characters from both ends. This is required,
				# as reading a textfile includes trailing newline characters.
				w = w.strip()
				# Skip empty strings, comment lines, words with non-printables
				if not w.isspace() \
				   and (w[0] != '#') \
				   and w.isprintable():
					words.append(w)

	return words

# ============================================================================ #


def filter_words(words: list,
                 do_randomize: bool,
                 wlen_min: int,
                 incl_capwords: bool,
                 incl_multiwords: bool) -> list[str]:
	"""
	Filter word list according to given arguments
	"""
	outwords = []
	for w in words:
		if (len(w) >= wlen_min) \
		   and (incl_capwords or w.islower()) \
		   and (incl_multiwords or (' ' not in w)):
			outwords.append(w)

	if do_randomize:
		random.shuffle(outwords)

	return outwords

# ============================================================================ #


def write_outfile(outfile,
                  words: list[list[str]],
                  cachelist: namedtuple,
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
		w1_pbar = tqdm(words[0],
		               smoothing=0.01,
		               dynamic_ncols=True,
		               unit='w',
		               desc='First words processed')

		wdict = dict()
		blend_ctr = 0
		w1_ctr = 0

		while w1_ctr < len(words[0]) and (maxblends <= 0 or blend_ctr < maxblends):

			w1 = words[0][w1_ctr]

			for w2 in tqdm(words[1],
			               leave=False,
			               dynamic_ncols=True,
			               unit='w',
			               desc='Current word vs. whole vocabulary'):
				(wblend, depth) = check_n_blend(w1, w2, mindepth, uppercase)
				if wblend \
				   and (wblend.lower() not in words[0]) \
				   and (wblend.lower() not in words[1]) \
				   and (wblend not in wdict):
					wdict[wblend] = depth
					# Dynamically write blended word into plain text file
					# together with overlap depth (\n is auto-appended)
					print(depth, wblend, file=outfile)
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
