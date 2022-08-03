#!/usr/bin/env python3
"""
Generate hilarious (or not) portmanteaus from a vocabulary.

Each word is checked for overlapping characters against every other word.
It is considered a match when at least some chars are overlapping.
Example: "revenge" and "vengeance" have 5 overlapping chars,
so "reVENGEance" will be generated from this pair.
Both words must have some non-overlapping chars at the start/end.

Arbitrary decision:
	When a blend is generated, we take overlapping chars from the second word.
	This might influence how the resulting blend is displayed, when
	there are uppercased/compound chars like ß (we use str.casefold()
	for all comparisons, so matching substrings might actually look different).

Naming conventions:
	...s    - suffix for plurals (sequence)
	...ss   - suffix for 'sequence of 'sequence''
	w       - word (ww, ws - words)
	w...    - prefix for word
	cfw     - casefolded word
	cf...   - prefix for casefolded
	ch      - character
	f       - file (ff, fs - files)
	p       - path (pp, ps - paths)

It might be slightly confusing with multidimensional stuff, for example:
	wlist   - list of word (i.e. a sequence itself, could also be 'ws' or 'ww');
	wlists  - sequence of wlist (i.e. a sequence of list of word,
	          2-dimensional sequence, could also be 'wss' or 'wws' or 'www');
	          and since word is a str (a sequence itself), its chars may be
	          addressed as 'chsss' (3-dimensional sequence);
	          but we don't go that deep, thankfully. =)
"""
# TODO: separate logic from presentation
# TODO: implement caching

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
	print()
	print('         \\\\\\\\\\\\\\\\')
	print('   ┌────────────────┐__')
	print(' \\\\│ SHLAKOBL⎛⎞⎟⎠   │ °_\\')
	print(' //│         ⎝⎠⎟⎞UN │___/')
	print('   └────────────────┘')
	print('  Portmanteau Generator')
	print()

	args = parse_args()

	cachepath = Path('ru/.cache')
	CacheEntry = namedtuple('CacheEntry', ['w1', 'w2', 'blend', 'start', 'depth'])
	# cachelist = read_cache(cachepath)
	cachelist = []

	# print('Loading vocabulary...', end=' ')

	wlists = [[], []]
	(wlists[0], wlists[1]) = read_infiles(args.infile, args.w1, args.w2)

	for (i, wlist) in enumerate(wlists):
		wlists[i] = filter_words(wlist,
		                         args.randomize,
		                         args.minlength,
		                         args.capitalized,
		                         args.phrases)

	# print('Done.')
	print(len(wlists[0]) + len(wlists[1]), 'words loaded,',
	      len(wlists[0]) * len(wlists[1]), 'pairs to check')
	print('Starting search for overlapping substrings in word pairs')
	print('Press Ctrl-C to quit anytime')
	print()
	numblends = write_outfile(args.outfile,
	                          wlists,
	                          # cachelist,
	                          args.number,
	                          args.depth,
	                          args.minfree,
	                          args.uppercase)

	# write_cache(cachepath, cachelist)

	# print('Done.')

	return 0

# ============================================================================ #


def parse_args() -> argparse.Namespace:
	"""
	Parse command line arguments. Print help when invoked without args.
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
	parser.add_argument('-f', '--minfree',
	                    type=int,
	                    default=1,
	                    help='minimum number of non-overlapping chars in each word (default: %(default)s)')
	parser.add_argument('-l', '--minlength',
	                    type=int,
	                    default=3,
	                    help='minimum length of source words (default: %(default)s)')
	parser.add_argument('-L', '--maxlength',
	                    type=int,
	                    default=0,
	                    help='maximum length of source words (default: unlimited)')
	parser.add_argument('-u', '--uppercase',
	                    action='store_true',
	                    help='uppercase overlapping characters in the output ("reVENGEance")')
	parser.add_argument('-c', '--capitalized',
	                    action='store_true',
	                    help='also include Capitalized words (proper names / abbreviations)')
	parser.add_argument('-p', '--phrases',
	                    action='store_true',
	                    help='also include multi-word phrases')

	args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

	if not (args.infile or args.w1 or args.w2):
		parser.error('No source vocabularies specified')

	return args

# ============================================================================ #


def read_cache(cpath: Path) -> list:
	"""
	Read cache file into a list of CacheEntries.
	"""
	# TODO: use CSV
	clist = []
	with cpath.open() as f:
		for centry in f:
			clist.append(centry)

	return clist

# ============================================================================ #


def write_cache(cpath: Path, clist: list):
	"""
	Write list of CacheEntries back into cache file.
	"""
	# TODO: use CSV
	with cpath.open(mode='r+') as f:
		pass

	return 0

# ============================================================================ #


def read_infiles(*pathstrs) -> tuple[list, list]:
	"""
	Get list of filenames for vocabulary file[s] and read their content.
	"""
	pathsets = [set(), set(), set()]    # [common, w1, w2]
	for (pathset, pathstr) in zip(pathsets, pathstrs):
		if type(pathstr) == list:
			for path in pathstr:
				pathset |= pathstr2pathset(path)
		elif type(pathstr) == str:
			pathset = pathstr2pathset(pathstr)

	wsets = [set(), set(), set()]    # [common, w1, w2]
	for (wset, pathset) in zip(wsets, pathsets):
		for path in pathset:
			wset |= set(file2list(path))

	wlists = [[], []]
	wlists[0] = sorted(wsets[0] | wsets[1])
	wlists[1] = sorted(wsets[0] | wsets[2])

	return (wlists[0], wlists[1])

# ============================================================================ #


def pathstr2pathset(pathstr: str) -> set[Path]:
	"""
	Unwrap a given nonempty path string into a set of absolute file paths.
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
	Import words from a single vocabulary file into a list.
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
                 minlen: int,
                 incl_capitalized: bool,
                 incl_phrases: bool) -> list[str]:
	"""
	Filter word list according to given arguments.
	"""
	outwords = []
	for w in words:
		if (len(w) >= minlen) \
		   and (incl_capitalized or w.islower()) \
		   and (incl_phrases or (' ' not in w)):
			outwords.append(w)

	if do_randomize:
		random.shuffle(outwords)

	return outwords

# ============================================================================ #


def write_outfile(outfile,
                  wlists: list[list[str]],
                  # cachelist,
                  maxblends: int,
                  mindepth: int,
                  minfree: int,
                  uppercase: bool) -> int:
	"""
	Search for overlapping characters at the start & end of all words,
	blend matching pairs, and write results into a text file.

	Dictionary is used to save the number of overlapping chars (as values)
	and to auto-deduplicate saved words (as keys).
	Note: we use w.casefold() for all string comparisons, but then
	we blend original words for output.
	"""
	with outfile:

		# Show progress bars and ETAs
		if maxblends:
			blend_pbar = tqdm(total=maxblends,
			                  smoothing=0.01,
			                  dynamic_ncols=True,
			                  unit='w',
			                  desc='Word blends generated',
			                  colour='green')
		else:
			blend_pbar = tqdm(smoothing=0.01,
			                  dynamic_ncols=True,
			                  unit='w',
			                  desc='Word blends generated',
			                  colour='green')

		w_pbar = tqdm(wlists[0],
		              smoothing=0.01,
		              dynamic_ncols=True,
		              unit='w',
		              desc='First words processed',
		              colour='green')

		blends = dict()
		blend_ctr = 0
		w_ctr = 0
		words = ['', '']

		try:

			while w_ctr < len(wlists[0]) and (maxblends <= 0 or blend_ctr < maxblends):

				words[0] = wlists[0][w_ctr]

				for words[1] in tqdm(wlists[1],
				                     leave=False,
				                     dynamic_ncols=True,
				                     unit='w',
				                     desc='Current word vs. whole vocabulary',
				                     colour='green'):

					(startpos, depth), _, _ = check_pair((words[0], words[1]),
					                                     mindepth,
					                                     minfree)
					if depth:
						blend = blend_pair((words[0], words[1]),
						                   startpos,
						                   depth,
						                   uppercase)

						if (blend not in (wlists[0] + wlists[1])) \
						   and (blend.lower() not in (wlists[0] + wlists[1])) \
						   and (blend not in blends):
							blends[blend] = depth
							# Dynamically write blended word into plain text file
							# together with overlap depth (\n is auto-appended)
							# TODO: argumentize output string format
							# TODO: also save all data into cache
							print(blend, file=outfile)
							blend_ctr += 1
							blend_pbar.update()
							if blend_ctr >= maxblends:
								break

				w_ctr += 1
				w_pbar.update()

			w_pbar.close()
			blend_pbar.close()

		except KeyboardInterrupt:
			pass

	return blend_ctr

# ============================================================================ #


def check_pair(ws: tuple[str, str],
               mindepth: int,
               minfree: int) -> tuple[tuple[int, int],
                                      tuple[str, str],
                                      tuple[int, int]]:
	"""
	Check word pair for blendability.

	Returns a tuple of:
		- tuple (startpos, depth)
		- tuple (w[0].casefold(), w[1].casefold())
		- tuple (cfstartpos, cfdepth)
	Note: this algorithm uses casefold() string comparison, which, for some
	chars (like ß), changes word length (and, consequently, char indices).
	Even more, for some languages unicodedata.normalize('NFKD', str)
	might be needed. For now, we only address the first case,
	trying to calculate proper startpos & depth.
	https://stackoverflow.com/questions/319426/how-do-i-do-a-case-insensitive-string-comparison
	"""
	cfws = []
	for w in ws:
		cfws.append(w.casefold())

	for i in range(minfree, len(cfws[0]) - (mindepth-1)):

		if cfws[1].startswith(cfws[0][i:], 0, len(cfws[1]) - minfree):
			# Match!
			cfstartpos = i
			cfdepth = len(cfws[0][i:])

			# Check if w.casefold differs from w, and calculate
			# proper startpos & depth for non-casefolded w
			# TODO: make a for loop for ws[0..1] instead
			if len(ws[0]) != len(cfws[0]):
				startpos = 0
				chlensum = 0
				for (i, ch) in enumerate(ws[0]):
					chlensum += len(ch.casefold())
					if chlensum >= cfstartpos:
						startpos = i + 1    # may or may not be = cfstartpos
						break
					# elif chlensum > cfstartpos:
						# a complex case when blend starts inside a compound
						# letter (e.g., Buße / busSE + SEmantic), we'll deal
						# with it later
			else:
				# Equality for w[0] means both startpos & depth are correct
				# (depth for original w[1] might differ, though)
				startpos = cfstartpos

			if len(ws[1]) != len(cfws[1]):
				depth = 0
				chlensum = 0
				for (i, ch) in enumerate(ws[1]):
					chlensum += len(ch.casefold())
					if chlensum >= cfdepth:
						depth = i + 1       # may or may not be = cfdepth
						break
					# elif chlensum > cfdepth:
						# a complex case when blend ends inside a compound
						# letter, we'll deal with it later
			else:
				# Equality for w[1] means depth is correct
				# (depth for original w[0] might differ, though)
				depth = cfdepth

			# After a match is found, exit for loop (this pair is done)
			return ((startpos, depth),
			        (cfws[0], cfws[1]),
			        (cfstartpos, cfdepth))

	return ((0, 0), ('', ''), (0, 0))

# ============================================================================ #


def blend_pair(ws: tuple[str, str],
               startpos: int,
               depth: int,
               uppercase: bool) -> str:
	"""
	Blend word pair.

	Take 'startpos' non-overlapping chars from w[0],
	add 'depth' overlapping chars (optionally UPPERCASE them),
	then add remaining chars from w[1].
	Arbitrary decision: take overlapping chars from w[1]. If there are
	differently uppercased/compound chars (like ß), result might look different.
	"""
	if uppercase:
		blend = ''.join((ws[0][:startpos], ws[1][:depth].upper(), ws[1][depth:]))
		# To use overlapping chars from ws[0] instead (maybe argumentize this):
		# blend = ''.join((ws[0][:startpos], ws[0][startpos:].upper(), ws[1][depth:]))
	else:
		blend = ''.join((ws[0][:startpos], ws[1]))

	return blend

# ============================================================================ #


if __name__ == '__main__':
	sys.exit(main())
