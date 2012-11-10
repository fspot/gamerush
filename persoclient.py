#!/usr/bin/python
# -*- coding:utf-8 -*-

from PySFML import sf

_IMG = ['nain1', 'nain2']

IMG = {
	'fifi': sf.Image(),
}

IMG['fifi'].LoadFromFile("./img/man1.bmp")

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

