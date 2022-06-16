#!/usr/bin/python3
######
# flapper.py
#
# A tool for parsing through 128T logs (routingManager) to look for evidence of path flaps,
# and to create some human-readable/interpretable output.
#
# (c)2022 Patrick Timmons
######

import os
import re
import argparse
import sys

FLAP_REGEX = r'.*Peer path state change'

def main(argv):

	parser = argparse.ArgumentParser(description='128T peer path flap analyzer')
	parser.add_argument('--input', '-i', metavar='<filename>', type=str,
						help='routingManager to analyze')

	args = parser.parse_args()

	flap_count = 0
	flap_down = 0
	flap_up = 0
	with open(args.input) as fin:
		for line in fin:
			is_flap = re.search(FLAP_REGEX, line)
			if is_flap:
				flap_count += 1
				tokens = line.split()
				if flap_count % 100 == 0:
					print(tokens)


	print(f'Found {flap_count} flaps in the file.')


if __name__ == '__main__':
	main(sys.argv[1:])