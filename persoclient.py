#!/usr/bin/python
# -*- coding:utf-8 -*-

from PySFML import sf

IMG = {
	'fifi': sf.Image(),
	'fifo': sf.Image(),
}

IMG['fifi'].LoadFromFile("./img/fifi.png")
IMG['fifo'].LoadFromFile("./img/fifi.png")

class PersoClient(object):
	def __init__(self, msg):
		self.x = msg['x']
		self.y = msg['y']
		self.id = msg['id']
		self.race = msg['r']
		self.nom = msg['n']
		self.spr = sf.Sprite(IMG['fifi'])

	def sprite(self):
		self.spr.SetPosition(self.x, self.y)
		return self.spr

	def modify(self, msg):
		print "(@) I am updating myself, I'm", self.id, msg
		self.x = msg['x']
		self.y = msg['y']

