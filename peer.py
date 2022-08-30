#!/usr/bin/python3
######
# peer.py
#
# A class for managing peers and peer paths
#
# (c)2022 Patrick Timmons
######

class PeerPath:

	def __init__(self, intf='', state='unknown'):
		self.intf = intf
		self.state = state
		self.eventlog = []

class Peer:

	def __init__(self, name):
		self.name = name
		self.peer_paths = {}

	@property
	def pathcount(self):
		return len(self.peer_paths.keys())
