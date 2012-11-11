#!/usr/bin/python
# -*- coding:utf-8 -*-

from PySFML import sf

_IMG = ['nain1', 'nain2'] # doivent être des .png dans img/
IMG = {nom: sf.Image() for nom in _IMG}
for img in IMG:	IMG[img].LoadFromFile("./img/{0}.png".format(img)) # loadfromfiles

class PersoClient(object):
	def __init__(self, msg):
		self.x = msg['x']
		self.y = msg['y']
		self.id = msg['id']
		self.race = msg['r']
		self.nom = msg['n']
		self.spr = sf.Sprite(IMG['nain1'])

	def sprite(self):
		self.spr.SetPosition(self.x, self.y)
		return self.spr

	def modify(self, msg):
		#print "(@) I am updating myself, I'm", self.id, msg
		self.x = msg['x']
		self.y = msg['y']

