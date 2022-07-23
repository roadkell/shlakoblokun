#!/usr/bin/env python3
"""
Memory-efficient parser for [ru]Wiktionary XML dumps

XML dump as input, plaintext file as output.
Dumps can be downloaded here:
https://dumps.wikimedia.org/backup-index.html
https://dumps.wikimedia.org/ruwiktionary/latest/
https://meta.wikimedia.org/wiki/Mirroring_Wikimedia_project_XML_dumps#Current_Mirrors
"""

import argparse
import sys

from lxml import etree


def fast_iter(context, func, *args, **kwargs):
	"""
	http://lxml.de/parsing.html#modifying-the-tree
	Based on Liza Daly's fast_iter
	http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
	See also http://effbot.org/zone/element-iterparse.htm
	https://stackoverflow.com/questions/12160418/why-is-lxml-etree-iterparse-eating-up-all-my-memory
	"""
	for event, elem in context:
		titles = func(elem, *args, **kwargs)
		# It's safe to call clear() here because no descendants will be accessed
		elem.clear()
		# Also eliminate now-empty references from the root node to elem
		for ancestor in elem.xpath('ancestor-or-self::*'):
			while ancestor.getprevious() is not None:
				del ancestor.getparent()[0]
	del context
	return titles


def process_elem(elem, ns, titles):
	if elem.getparent().tag == (ns+'page'):
		is_ns0 = False
		is_ru = False
		for sib in etree.SiblingsIterator(elem, tag=('{*}ns')):
			if sib.text == '0':
				is_ns0 = True
				# print(sib.text)
				break
		for sib in etree.SiblingsIterator(elem, tag=('{*}revision')):
			for sibchild in etree.ElementChildIterator(sib, tag='{*}text'):
				if type(sibchild.text) == str \
				   and '= {{-ru-}} =' in sibchild.text:
					is_ru = True
					# print('= {{-ru-}} =')
					break
		if elem.tag == (ns+'title') \
		   and elem.text \
		   and is_ns0 \
		   and is_ru:
			titles.add(elem.text)
			# print(elem.text)
	return titles


def main() -> int:

	argparser = argparse.ArgumentParser()
	argparser.add_argument('infile', type=argparse.FileType('rb'),
	                       default=(None if sys.stdin.isatty() else sys.stdin))
	argparser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
	                       default=sys.stdout)
	args = argparser.parse_args()

	titles = set()
	ns = '{http://www.mediawiki.org/xml/export-0.10/}'

	with args.infile as f:
		try:
			print('Loading XML document and creating XML tree object...')
			context = etree.iterparse(f, events=('end',), tag=ns+'title')
			print('Done.')
			print('Parsing XML tree...')
			fast_iter(context, process_elem, ns, titles)

		except etree.ParseError:
			print('Unexpected end of XML document. Aborting...')

	print('Done.')
	print('Exporting wordlist into a plaintext file...')

	with args.outfile as f:
		for w in titles:
			print(w, file=f)

	print('Done.')

	return 0


if __name__ == '__main__':
	sys.exit(main())
