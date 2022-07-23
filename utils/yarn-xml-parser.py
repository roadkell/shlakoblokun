#!/usr/bin/env python3
"""
Parse Russian vocabulary from YARN project, presented in XML format,
and output result into plaintext file

YARN project homepage:
https://russianword.net/

XML dump can be downloaded here:
https://github.com/russianwordnet/yarn/releases/download/eol/yarn.xml

Vocabulary format explained:
https://nlpub.ru/YARN/Формат

Last and final dump: 2020-02-08
"""

import argparse
import sys
import xml.etree.ElementTree as ET


def main() -> int:

	# Parse command line arguments
	argparser = argparse.ArgumentParser()
	argparser.add_argument('infile', type=argparse.FileType('r'),
	                       default=(None if sys.stdin.isatty() else sys.stdin))
	argparser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
	                       default=sys.stdout)
	args = argparser.parse_args()

	# Parse XML structure
	with args.infile as f:
		tree = ET.parse(f)
	root = tree.getroot()
	ns = {'url': 'https://russianword.net'}
	wordlist = root.findall('./url:words/url:wordEntry/url:word', ns)

	# Write word list into a plain text file, auto-adding newlines
	with args.outfile as f:
		for word in wordlist:
			print(word.text, file=f)

	return 0


if __name__ == '__main__':
	sys.exit(main())
