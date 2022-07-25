#!/usr/bin/env python3
"""
Remove inflections (word forms) from a ru-wordlist file or stdin,
output as a new textfile or stdout

Results can be unexpected, use with care.
"""
# TODO: better algo for capitalization preservation.

import argparse
import os
import pymorphy2
import sys

from pathlib import Path
from tqdm import tqdm


def main() -> int:

	# Parse command line arguments
	argparser = argparse.ArgumentParser()
	argparser.add_argument('infile', type=argparse.FileType('r'),
	                       default=(None if sys.stdin.isatty() else sys.stdin))
	argparser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
	                       default=sys.stdout)
	args = argparser.parse_args()

	fsize = Path(args.infile.name).stat().st_size
	morph = pymorphy2.MorphAnalyzer()
	wordset = set()
	offset = 0

	# Show fancy progress bar
	with tqdm(total=fsize,
	          smoothing=0.01,
	          dynamic_ncols=True,
	          unit='ch',
	          desc='Characters processed') as pbar:
		with args.infile as f:
			for w in f:
				w = w.strip()
				if w:
					if ' ' not in w:
						norm = morph.parse(w)[0].normal_form
						if w.istitle():
							norm = norm.title()
						elif w.isupper():
							norm = norm.upper()
						wordset.add(norm)
					else:
						wordset.add(w)
					offset += len(w.encode('utf-8')) + len(os.linesep)
					pbar.update(offset - pbar.n)

	# Write wordset into a plain text file, auto-adding newlines
	with args.outfile as f:
		for w in wordset:
			print(w, file=f)

	return 0


if __name__ == '__main__':
	sys.exit(main())
