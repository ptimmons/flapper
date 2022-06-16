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
	skipped = 0

	peer_flaps = {}
	intf_flaps = {}

	with open(args.input) as fin:
		for line in fin:
			is_flap = re.search(FLAP_REGEX, line)
			if is_flap:
				tokens = line.split()
				if len(tokens) < 30:
					skipped += 1
					continue
				peer_name = tokens[15]
				peer_intf = tokens[18]
				node_name = tokens[21]

				self_intf = tokens[24]
				self_vlan = tokens[27]

				peer_state = tokens[29]
				
				if peer_name in peer_flaps.keys():
					if peer_flaps[self_intf][peer_name][peer_intf]['state'] == peer_state:
						skipped += 1
						continue
					peer_flaps[self_intf][peer_name][peer_intf]['state'] == peer_state
					peer_flaps[self_intf][peer_name][peer_intf]['count'] += 1
				else:
					if peer_state == 'down':
						# only add them here if they're down (presume they're up to begin with)
						peer_flaps[self_intf] = {}
						peer_flaps[self_intf][peer_name] = {}
						peer_flaps[self_intf][peer_name][peer_intf] = {}
						peer_flaps[self_intf][peer_name][peer_intf]['state'] = peer_state
						peer_flaps[self_intf][peer_name][peer_intf]['count'] = 1
					else:
						skipped += 1
						continue
				if self_intf in intf_flaps.keys():
					intf_flaps[self_intf] += 1
				else:
					intf_flaps[self_intf] = 1
				if tokens[29] == 'up':
					flap_up += 1
				elif tokens[29] == 'down':
					flap_down += 1
				flap_count += 1


	print(f'Found {flap_count} flaps in the file.')
	print(f'  up: {flap_up}, down: {flap_down}')
	print(f'  skipped {skipped}')
	print(peer_flaps)
	print(intf_flaps)


if __name__ == '__main__':
	main(sys.argv[1:])