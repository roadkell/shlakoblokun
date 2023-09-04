#!/usr/bin/env python3
"""
Generate hilarious (or not) portmanteaus from a vocabulary
https://github.com/roadkell/shlakoblokun

Each word is checked for overlapping characters against every other word.
It is considered a match when at least some chars are overlapping.
Example: "revenge" and "vengeance" have 5 overlapping chars,
so "reVENGEance" will be generated from this pair.

Arbitrary decision:
	When a blend is generated, we take overlapping chars from the second word.
	This might influence how the resulting blend is displayed, when
	there are uppercased/compound chars like ß (we use str.casefold()
	for all comparisons, so matching substrings might actually look different).

Naming conventions:
	...s    - suffix for plurals (sequence types)
	...ss   - suffix for 'sequence of sequence' (2-dimensional seq.)
	w       - word (ws - words)
	w...    - prefix for 'word'
	cfw     - casefolded word
	cf...   - prefix for 'casefolded'
	ch      - character (chs - characters)
	f       - file (fs - files)
	p       - path (ps - paths)

It might be slightly confusing with multidimensional stuff, for example:
	wlist   - list of 'word's (i.e. a sequence itself, could also be named 'ws');
	wlists  - sequence of 'wlist's (i.e. a sequence of list of word,
	          a 2-dimensional sequence, could also be named 'wss');
	          and since word is a 'str' (a sequence itself), its chars may be
	          addressed as 'chsss' (3-dimensional seq.),
	          but we don't go that deep, thankfully. =)

Arg names and README address words as w1 & w2, but codewise
they are zero-indexed (w[0], w[1]).

TODO: separate logic from presentation
TODO: implement caching
TODO: add -1or2, -1xor2 options for vocabularies
TODO: maybe replace argparse with click
"""

# ============================================================================ #

import argparse
import fileinput
import os
import random
import sys
# from collections import namedtuple
from io import TextIOWrapper
# from typing import Union

from tqdm import tqdm

# ============================================================================ #


def main() -> int:

	args = parse_args()

	if args.outfile != sys.stdout:
		print()
		print('         \\\\\\\\\\\\\\\\')
		print('   ┌────────────────┐__')
		print(' \\\\│ SHLAKOBL⎛⎞⎟⎠   │ °_\\')
		print(' //│         ⎝⎠⎟⎞UN │___/')
		print('   └────────────────┘')
		print('  Portmanteau Generator')
		print()
		# print('Loading vocabulary...', end=' ')

	# cachepath = Path('.cache')
	# CacheEntry = namedtuple('CacheEntry', ['w1', 'w2', 'blend', 'start', 'depth'])
	# cachelist = read_cache(cachepath)
	# cachelist = []

	wsets = read_infiles(args.infile, args.w1, args.w2)

	wlists = (filter_words(wsets[0],
	                       args.randomize,
	                       args.minlength,
	                       args.capitalized,
	                       args.phrases),
	          filter_words(wsets[1],
	                       args.randomize,
	                       args.minlength,
	                       args.capitalized,
	                       args.phrases))

	exwords = files2words(args.exclude_overlaps)
	cfexwords = set()
	for w in exwords:
		cfexwords.add(w.casefold())

	if args.outfile != sys.stdout:
		print(len(wlists[0]) + len(wlists[1]), 'words loaded,',
		      len(wlists[0]) * len(wlists[1]), 'pairs to check')
		print('Starting search for overlapping substrings in word pairs')
		print('Press Ctrl-C to quit anytime')
		print()

	numblends = write_outfile(args.outfile,
	                          cfexwords,
	                          wlists,
	                          # cachelist,
	                          args.number,
	                          args.depth,
	                          args.minfree,
	                          args.uppercase)

	# write_cache(cachepath, cachelist)

	return 0

# ============================================================================ #


def parse_args() -> argparse.Namespace:
	"""
	Parse command line arguments. Print help when invoked without args

	Infile can be one or many files, one or many dirs, or sys.stdin (default).
	If no infile[s] | sys.stdin are specified, throw an error.
	"""
	parser = argparse.ArgumentParser(prog='python3 shlakoblokun.py')

	parser.add_argument('-i', '--infile',
	                    nargs='*',
	                    default=(None if sys.stdin.isatty() else sys.stdin),
	                    help='source vocabulary file[s] or dir (default: stdin)')
	parser.add_argument('-w1',
	                    nargs='*',
	                    help='vocabulary file[s]/dir to only source 1st words from')
	parser.add_argument('-w2',
	                    nargs='*',
	                    help='vocabulary file[s]/dir to only source 2nd words from')
	parser.add_argument('-e', '--exclude-overlaps',
	                    nargs='?',
	                    type=argparse.FileType('r'),
	                    help="vocabulary file with overlaps to ignore \
	                    (usually common suffixes) (default: %(default)s)")
	parser.add_argument('-o', '--outfile',
	                    nargs='?',
	                    type=argparse.FileType('w'),
	                    default=sys.stdout,
	                    help='output file (default: stdout)')
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
	                    help='minimum number of non-overlapping chars in each word \
	                    (default: %(default)s)')
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
	                    help='uppercase overlapping characters in the output \
	                    (ex., "reVENGEance")')
	parser.add_argument('-c', '--capitalized',
	                    action='store_true',
	                    help='also include capitalized words')
	parser.add_argument('-p', '--phrases',
	                    action='store_true',
	                    help='also include multi-word phrases')

	args = parser.parse_args(args=None if (sys.argv[1:] or not sys.stdin.isatty())
	                         else ['--help'])

	if not (args.infile or args.w1 and args.w2):
		parser.error('no source vocabularies specified')

	return args

# ============================================================================ #


# def read_cache(cpath: Path) -> list:
# 	"""
# 	Read cache file into a list of CacheEntries.
# 	"""
# 	# TODO: use CSV/TSV
# 	clist = []
# 	with cpath.open() as f:
# 		for centry in f:
# 			clist.append(centry)

# 	return clist

# ============================================================================ #


# def write_cache(cpath: Path, clist: list) -> int:
# 	"""
# 	Write list of CacheEntries back into cache file.
# 	"""
# 	# TODO: use CSV/TSV
# 	with cpath.open(mode='r+') as f:
# 		pass

# 	return 0

# ============================================================================ #


def read_infiles(infile, w1, w2) -> tuple[set[str], set[str]]:
	"""
	Read vocabulary file[s], return sets of words to blend

	Args:
		values of -i, -w1, -w2 options (some can be None)
	Returns:
		tuple: of 2 sets, for 1st and 2nd word to take words from
	"""

	files = (infile, w1, w2)
	wsets: tuple[set[str], set[str], set[str]] = (set(), set(), set())
	for (wset, file) in zip(wsets, files):
		wset |= files2words(file)

	return ((wsets[0] | wsets[1]),
	        (wsets[0] | wsets[2]))

# ============================================================================ #


def files2words(infiles: str | list[str] | TextIOWrapper | None) -> set[str]:
	"""
	Read lines from vocabulary file[s] or sys.stdin into a set

	Args:
		infiles:

		Since nargs='*' always produce a list (except when no arg is given),
		files from -i,-w1,-w2 options will always be either a list[str],
		or None, or (in case of sys.stdin) io.TextIOWrapper.
		File from -e option will produce a str, due to nargs='?'.

		If it is a directory, all files from it (excluding hidden and temporary)
		will be read non-recursively. Multiple dirs can be given too.

		If multiple files are given explicitly, they'll be read, regardless
		of hidden/temp status.

	Returns:
		set: of words from all given files.
	"""

	words = set()

	if infiles:

		if isinstance(infiles, TextIOWrapper):  # file object or sys.stdin

			with infiles as f:
				for w in f:
					words.add(line2word(w))

			return words

		else:

			outfiles: set[str] = set()

			if isinstance(infiles, list):
				for file in infiles:
					if file:
						if os.path.isdir(file):
							outfiles |= dir2files(file)
						else:
							outfiles.add(file)
			elif os.path.isdir(infiles):
				outfiles = dir2files(infiles)

			with fileinput.input(outfiles) as f:
				for w in f:
					words.add(line2word(w))

			return words

	else:

		return words

# ============================================================================ #


def dir2files(dir: str) -> set[str]:
	"""
	List all files in a directory, excluding hidden and temporary (POSIX-style)
	"""

	files = set()

	if dir:
		with os.scandir(dir) as it:
			for entry in it:
				if entry.is_file() \
				   and not entry.name.startswith('.') \
				   and not entry.name.endswith('~'):
					files.add(entry.path)

	return files

# ============================================================================ #


def line2word(w: str) -> str:
	"""
	Convert a line from a text file into a word

	1) remove inline comments;
	2) strip whitespace characters from both ends (this is required,
	  as reading lines from a textfile includes trailing newline chars);
	3) skip words with non-printable chars;

	No need to check w for existence on load, as it is always a string.
	After stripping newlines it may become empty.
	Empty string is considered printable by str.isprintable().
	"""

	w = w.partition('#')[0].strip()
	if w.isprintable():
		return w
	else:
		return ''

# ============================================================================ #


def filter_words(words: set[str],
                 do_randomize: bool,
                 minlength: int,
                 incl_capitalized: bool,
                 incl_phrases: bool
                 ) -> list[str]:
	"""
	Filter word set according to given arguments. Return a list of words
	"""

	outwords = []
	for w in words:
		if (len(w) >= minlength) \
		   and (incl_capitalized or w.islower()) \
		   and (incl_phrases or (' ' not in w)):
			outwords.append(w)

	if do_randomize:
		random.shuffle(outwords)
	else:
		outwords.sort()

	return outwords

# ============================================================================ #


def write_outfile(outfile,
                  cfexwords,
                  wlists: tuple[list[str], list[str]],
                  # cachelist,
                  maxblends: int,
                  mindepth: int,
                  minfree: int,
                  uppercase: bool
                  ) -> int:
	"""
	Search for blendable words, do the blending, write results to a file

	1) search for overlapping characters at the start & end of given words;
	2) blend matching pairs;
	3) dynamically write results into a text file;

	Dictionary is used to save the number of overlapping chars (as values)
	and to auto-deduplicate saved words (as keys).

	w.casefold() is used for all string comparisons, but then original words
	are actually blended for output.
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

		inwords = set(wlists[0] + wlists[1])
		blends = set()
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
					                                     cfexwords,
					                                     mindepth,
					                                     minfree)

					if depth:

						blend = blend_pair((words[0], words[1]),
						                   startpos,
						                   depth,
						                   uppercase)

						# An ugly way of checking if blend exists in inword set
						if (blend not in inwords) \
						   and (blend.lower() not in inwords) \
						   and (blend not in blends):
							blends.add(blend)
							# blends[blend] = depth
							# Dynamically write blended word into plaintext file
							# (print() auto-appends \n) or to sys.stdout
							# TODO: argumentize output string format
							# TODO: also save all data into cache
							# (and check blend existence against it)
							if outfile == sys.stdout:
								tqdm.write(blend, outfile)
							else:
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
               cfexwords: set,
               mindepth: int,
               minfree: int
               ) -> tuple[tuple[int, int],
                          tuple[int, int],
                          tuple[str, str]]:
	"""
	Check word pair for blendability

	Args:
		ws: a pair of words to check
		cfexwords: overlaps to ignore (from -e option)

	Returns:
		a tuple of:
		- tuple (startpos, depth)
		- tuple (cfstartpos, cfdepth)
		- tuple (w[0].casefold(), w[1].casefold())

	This algorithm uses casefold() string comparison, which, for some
	chars (like ß), changes word length (and, consequently, char indices).
	Even more, for some languages unicodedata.normalize('NFKD', str)
	might be needed. For now, we only address the first case,
	trying to calculate proper startpos & depth.
	https://stackoverflow.com/questions/319426/how-do-i-do-a-case-insensitive-string-comparison
	"""

	cfws = (ws[0].casefold(), ws[1].casefold())

	for i in range(minfree, len(cfws[0]) - (mindepth-1)):

		if cfws[1].startswith(cfws[0][i:], 0, len(cfws[1]) - minfree) \
		   and cfws[0][i:] not in cfexwords:
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
						startpos = i + 1    # may or may not be == cfstartpos
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
						depth = i + 1       # may or may not be == cfdepth
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
			        (cfstartpos, cfdepth),
			        cfws)

	return ((0, 0), (0, 0), ('', ''))

# ============================================================================ #


def blend_pair(ws: tuple[str, str],
               startpos: int,
               depth: int,
               uppercase: bool
               ) -> str:
	"""
	Blend a pair of words

	1) take 'startpos' non-overlapping chars from w[0];
	2) add 'depth' overlapping chars (optionally UPPERCASE them);
	3) add remaining chars from w[1];

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
