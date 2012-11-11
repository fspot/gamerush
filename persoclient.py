#!/usr/bin/python
# -*- coding:utf-8 -*-

from PySFML import sf
import time
from c import *

A_MEURT, A_CRIE, A_DECOLE, A_VOLE, A_TOMBE, A_MARCHE = range(6)

# doivent être des .png dans img/
_IMG = [
	'n/1', 'n/2', 'n/touched',  # normal
	'n/b/b', 'n/b/m',  # bouclier et marteau
]
_IMG += ['n/m/{}'.format(i) for i in range(1,11)]

IMG = {nom: sf.Image() for nom in _IMG}
for img in IMG:	IMG[img].LoadFromFile("./img/{0}.png".format(img)) # loadfromfiles

NAINSEQ = {
	A_MEURT : [
		{'d':0.2, 'i':IMG['n/m/1']},
		{'d':0.2, 'i':IMG['n/m/2']},
		{'d':0.2, 'i':IMG['n/m/3']},
		{'d':0.2, 'i':IMG['n/m/4']},
		{'d':0.2, 'i':IMG['n/m/5']},
		{'d':0.2, 'i':IMG['n/m/6']},
		{'d':0.2, 'i':IMG['n/m/7']},
		{'d':0.2, 'i':IMG['n/m/8']},
		{'d':0.2, 'i':IMG['n/m/9']},
		{'d':0.2, 'i':IMG['n/m/10']},
	],
	A_CRIE : [
		{'d':0.3, 'i':IMG['n/touched']},
	],
	A_MARCHE : [
		{'d':0.3, 'i':IMG['n/1']},
		{'d':0.3, 'i':IMG['n/2']},
	],
}

class PersoClient(object):
	def __init__(self, msg):
		self.x = msg['x']
		self.y = msg['y']
		self.id = msg['id']
		if 'pr' in msg:
			self.projo = True
		else:
			self.projo = False
		if 'r' in msg:
			self.race = msg['r']
		else:
			self.race = msg['pr']
		if 'n' in msg:
			self.nom = msg['n']
		else:
			self.nom = ''
		self.alpha = 0
		self.spr = sf.Sprite(IMG['n/1'])
		self.t = time.time()
		self.anim = A_MARCHE
		self.anim_pos = 0
		self.anim_max = 1

	def sprite(self):
		if self.race == NAIN:
			if time.time() - self.t > NAINSEQ[self.anim][self.anim_pos]['d']:
				if self.anim_pos + 1 < self.anim_max:
					self.anim_pos += 1
				else:
					self.anim_pos = 0
				self.t = time.time()
				self.spr = sf.Sprite(NAINSEQ[self.anim][self.anim_pos]['i'])
		self.spr.SetPosition(self.x, self.y)
		return self.spr

	def modify(self, msg):
		#print "(@) I am updating myself, I'm", self.id, msg
		if 'x' in msg: self.x = msg['x']
		if 'y' in msg: self.y = msg['y']
		if 'a' in msg: self.alpha = msg['a']
		if 'an' in msg: self.animate(msg['an'])

	def animate(self, anim):
		if self.race == NAIN:
			seq = NAINSEQ
		if anim < self.anim: # higher priority
			self.t = time.time()
			self.anim = anim
			self.anim_pos = 0
			self.anim_max = len(seq[anim])