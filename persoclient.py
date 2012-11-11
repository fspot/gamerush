#!/usr/bin/python
# -*- coding:utf-8 -*-

from PySFML import sf
import time
from c import *

A_MEURT, A_CRIE, A_DECOLE, A_VOLE, A_TOMBE, A_MARCHE, A_TETE = range(7)
GAUCHE, DROITE = True, False
DJ = 0

# doivent être des .png dans img/
_IMG = [
	'n/1', 'n/2', 'n/touched',  # normal
	'n/b/b', 'n/b/m', 'e/b/1',  # bouclier et marteau
	'e/a/1', 'e/v/1', 'e/v/2', # elfe qui vole et atterrit
	'd/bibine', 'd/n', 'd/n2', 'd/pneu', # decor
]
_IMG += ['n/m/{}'.format(i) for i in range(1,11)]
_IMG += ['e/m/{}'.format(i) for i in range(1,9)]
_IMG += ['e/c/{}'.format(i) for i in range(1,10)]
_IMG += ['a/baf/b{}'.format(i) for i in range(1,5)]

STATICOFS = {
	'n/b/b': (13,18),
	'n/b/m': (0,0),
	'e/b/1': (0,0),
}

IMG = {nom: sf.Image() for nom in _IMG}
for img in IMG:	IMG[img].LoadFromFile("./img/{0}.png".format(img)) # loadfromfiles

NAINSEQ = {
	A_MEURT : [
		{'d':0.2, 'i':IMG['n/m/1'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['n/m/2'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['n/m/3'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['n/m/4'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['n/m/5'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['n/m/6'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['n/m/7'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['n/m/8'], 'o':(0,-5)},
		{'d':0.2, 'i':IMG['n/m/9'], 'o':(0,-15)},
		{'d':0.2, 'i':IMG['n/m/10'], 'o':(0,-25)},
	],
	A_CRIE : [
		{'d':0.3, 'i':IMG['n/touched'], 'o':(0,0)},
	],
	A_TOMBE : [
		{'d':0.3, 'i':IMG['n/touched'], 'o':(0,0)},
	],
	A_MARCHE : [
		{'d':0.2, 'i':IMG['n/1'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['n/2'], 'o':(0,0)},
	],
	A_TETE : [
		{'d':0.6, 'i':IMG['n/1'], 'o':(0,0)},
		{'d':0.6, 'i':IMG['n/2'], 'o':(0,0)},
	],
}

ELFESEQ = {
	A_MEURT : [
		{'d':0.2, 'i':IMG['e/m/1'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['e/m/2'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['e/m/3'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['e/m/4'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['e/m/5'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['e/m/6'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['e/m/7'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['e/m/8'], 'o':(0,-5)},
	],
	A_TOMBE : [
		{'d':0.3, 'i':IMG['e/a/1'], 'o':(0,0)},
	],
	A_MARCHE : [
		{'d':0.2, 'i':IMG['e/c/1'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['e/c/2'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['e/c/3'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['e/c/4'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['e/c/5'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['e/c/6'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['e/c/7'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['e/c/8'], 'o':(0,-5)},
		{'d':0.2, 'i':IMG['e/c/9'], 'o':(0,-5)},
	],
	A_DECOLE : [
		{'d':0.4, 'i':IMG['e/v/1'], 'o':(0,0)},
	],
	A_VOLE : [
		{'d':0.4, 'i':IMG['e/v/2'], 'o':(0,0)},
	],
}

STATICSEQ = {
	DJ : [
		{'d':0.1, 'i':IMG['a/baf/b1'], 'o':(0,0)},
		{'d':0.1, 'i':IMG['a/baf/b2'], 'o':(0,0)},
		{'d':0.15, 'i':IMG['a/baf/b3'], 'o':(0,0)},
		{'d':0.1, 'i':IMG['a/baf/b4'], 'o':(0,0)},
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
		if 'anim' in msg:
			self.anim = msg['anim']
		self.anim_pos = 0
		if self.race == NAIN:
			self.anim_max = 1
		elif self.race == ELFE:
			self.anim_max = 1
		else:
			self.anim_max = len(STATICSEQ[self.anim])
		self.anim_finie = False
		self.orientation = DROITE

	def sprite(self):
		if self.projo:

			return
		elif self.race == NAIN:
			seq = NAINSEQ
		elif self.race == ELFE:
			seq = ELFESEQ
		else:
			seq = STATICSEQ
		print '!!',self.anim, self.anim_pos
		anim = seq[self.anim][self.anim_pos]
		print '!!',anim
		print '!! >? ', time.time(), self.t, time.time()-self.t
		if time.time() - self.t > anim['d']:
			if self.anim_pos + 1 < self.anim_max:
				print '!!', 'INC'
				self.anim_pos += 1
			else:
				self.anim_pos = 0
				self.anim_finie = True
			self.t = time.time()
			self.spr = sf.Sprite(anim['i'])
			self.spr.FlipX(self.orientation)
		self.spr.SetPosition(self.x - anim['o'][0], self.y - anim['o'][1])
		if (self.orientation == GAUCHE and abs(self.alpha) < 90 or
			self.orientation == DROITE and abs(self.alpha) > 90):
			self.orientation = not self.orientation
		self.spr.FlipX(self.orientation)
		print 'ANIMPOS', self.anim_pos
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
		elif self.race == ELFE:
			seq = ELFESEQ
		if anim != self.anim and (self.anim not in (A_MEURT, A_DECOLE, A_CRIE) or self.anim_finie): # higher priority
			self.t = time.time()
			self.anim = anim
			self.anim_pos = 0
			self.anim_finie = False
			self.anim_max = len(seq[anim])

	def arm(self):
		if not self.projo:
			if self.race == NAIN:
				arme = sf.Sprite(IMG['n/b/b'])
				arme.SetCenter(6,12)
				arme.SetPosition(self.x + STATICOFS['n/b/b'][0], self.y + STATICOFS['n/b/b'][1])
				arme.SetRotation(self.alpha)
				return arme

	def fuckdrawon(self, app):
		spr = self.sprite()
		arm = self.arm()
		if arm is not None:
			app.Draw(arm)
		app.Draw(spr)