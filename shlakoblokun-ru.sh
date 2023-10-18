#!/usr/bin/env sh
#
# Shlakoblokun launch script with some options given as an example.
# https://github.com/roadkell/shlakoblokun
#
# Generate random blends, using vocabularies from shlakoblokun/data/ru/ folder,
# and save the result into output-ru.txt.
# You can run the script as is, or modify the options to your liking.

cd shlakoblokun/ || exit
python3 shlakoblokun.py \
	-i data/ru/n.txt \
	-b data/ru/adj.txt data/ru/adv.txt data/ru/v.txt \
	-e data/ru/overlaps.txt \
	-o ../output-ru.txt \
	-d 3 -r -u
