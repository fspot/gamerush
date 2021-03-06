#!/usr/bin/python
# -*- coding:utf-8 -*-

from PySFML import sf
import time
from c import *
import son, random

A_MEURT, A_CRIE, A_DECOLE, A_VOLE, A_TOMBE, A_MARCHE, A_TETE = range(7)
GAUCHE, DROITE = True, False
NUAGE1, BAFFLES, DJ, PLATINES, NUAGE2, PNEU, BIBINE = range(1000,1007)

# doivent être des .png dans img/
_IMG = [
	'n/1', 'n/2', 'n/touched',  # normal
	'n/b/b', 'n/b/m', 'e/b/1',  # bouclier et marteau
	'e/a/1', 'e/v/1', 'e/v/2', # elfe qui vole et atterrit
	'd/bibine', 'd/n', 'd/n2', 'd/pneu', 'd/be', 'd/bn', 'd/dj1', 'd/dj2', 'd/pl1', 'd/pl2' # decor
]
_IMG += ['n/m/{}'.format(i) for i in range(1,11)]
_IMG += ['e/m/{}'.format(i) for i in range(1,9)]
_IMG += ['e/c/{}'.format(i) for i in range(1,10)]
_IMG += ['a/baf/b{}'.format(i) for i in range(1,5)]

STATICOFS = {
	'n/b/b': (13,18),
	'n/b/m': (0,0),
	'e/b/1': (13,22),
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
		{'d':600, 'i':IMG['n/m/10'], 'o':(0,-25)},
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
		{'d':0.1, 'i':IMG['e/m/1'], 'o':(0,0)},
		{'d':0.1, 'i':IMG['e/m/2'], 'o':(0,0)},
		{'d':0.1, 'i':IMG['e/m/3'], 'o':(0,0)},
		{'d':0.1, 'i':IMG['e/m/4'], 'o':(0,0)},
		{'d':0.1, 'i':IMG['e/m/5'], 'o':(0,0)},
		{'d':0.1, 'i':IMG['e/m/6'], 'o':(0,0)},
		{'d':0.1, 'i':IMG['e/m/7'], 'o':(0,0)},
		{'d':3.0, 'i':IMG['e/m/8'], 'o':(0,-5)},
	],
	A_TOMBE : [
		{'d':0.3, 'i':IMG['e/a/1'], 'o':(0,0)},
	],
	A_MARCHE : [
		{'d':0.1, 'i':IMG['e/c/1'], 'o':(0,0)},
		{'d':0.1, 'i':IMG['e/c/2'], 'o':(0,0)},
		{'d':0.1, 'i':IMG['e/c/3'], 'o':(0,0)},
		{'d':0.1, 'i':IMG['e/c/4'], 'o':(0,0)},
		{'d':0.1, 'i':IMG['e/c/5'], 'o':(0,0)},
		{'d':0.1, 'i':IMG['e/c/6'], 'o':(0,0)},
		{'d':0.1, 'i':IMG['e/c/7'], 'o':(0,0)},
		{'d':0.1, 'i':IMG['e/c/8'], 'o':(0,-5)},
		{'d':0.1, 'i':IMG['e/c/9'], 'o':(0,-5)},
	],
	A_DECOLE : [
		{'d':0.4, 'i':IMG['e/v/1'], 'o':(0,0)},
	],
	A_VOLE : [
		{'d':0.4, 'i':IMG['e/v/2'], 'o':(0,0)},
	],
	A_TETE : [
		{'d':0.4, 'i':IMG['e/v/2'], 'o':(0,0)},
	],
}

STATICSEQ = {
	NUAGE1 : [
		{'d':600, 'i':IMG['d/n'], 'o':(0,0)},
		{'d':600, 'i':IMG['d/n'], 'o':(0,0)},
	],

	BAFFLES : [
		{'d':0.1, 'i':IMG['a/baf/b1'], 'o':(0,0)},
		{'d':0.1, 'i':IMG['a/baf/b2'], 'o':(0,0)},
		{'d':0.15, 'i':IMG['a/baf/b3'], 'o':(0,0)},
		{'d':0.1, 'i':IMG['a/baf/b4'], 'o':(0,0)},
	],

	DJ : [
		{'d':0.3, 'i':IMG['d/dj1'], 'o':(0,0)},
		{'d':0.3, 'i':IMG['d/dj2'], 'o':(0,0)},
	],

	PLATINES : [
		{'d':0.2, 'i':IMG['d/pl1'], 'o':(0,0)},
		{'d':0.2, 'i':IMG['d/pl2'], 'o':(0,0)},
	],

	NUAGE2 : [
		{'d':600, 'i':IMG['d/n2'], 'o':(0,0)},
		{'d':600, 'i':IMG['d/n2'], 'o':(0,0)},
	],

	PNEU : [
		{'d':600, 'i':IMG['d/pneu'], 'o':(0,0)},
	],

	BIBINE : [
		{'d':600, 'i':IMG['d/bibine'], 'o':(0,0)},
	],
}

class PersoClient(object):
	def __init__(self, msg):
		self.x = msg['x']
		self.y = msg['y']
		self.id = msg['id']
		self.marto = 0
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
		self.t = 0
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
		self.spr = self.sprite()

	def sprite(self):
		if self.projo:
			if self.race == ELFE:
				self.spr = sf.Sprite(IMG['d/be'])
			else:
				self.spr = sf.Sprite(IMG['d/bn'])
			self.spr.SetPosition(self.x, self.y)
			return self.spr
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
		if 'm' in msg: self.marto = time.time()

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
			if self.race == ELFE and self.anim == A_DECOLE:
				son.sounds['jet'].Play()
			elif self.race == ELFE and self.anim == A_MEURT:
				son.sounds['plash'].Play()
			elif self.race == NAIN and self.anim == A_MEURT:
				s = random.choice(['m/a1', 'm/a2', 'm/a3'])
				son.sounds[s].Play()
			elif self.race == NAIN and self.anim == A_CRIE:
				s = random.choice(['t/a1', 't/a2'])
				son.sounds[s].Play()

	def arm(self):
		if not self.projo:
			if self.race == NAIN:
				if time.time() - self.marto < 5.0:
					arme = sf.Sprite(IMG['n/b/m'])
				else:
					arme = sf.Sprite(IMG['n/b/b'])
				arme.SetCenter(6,12)
				arme.SetPosition(self.x + STATICOFS['n/b/b'][0], self.y + STATICOFS['n/b/b'][1])
				arme.SetRotation(self.alpha)
				return arme
			elif self.race == ELFE:
				arme = sf.Sprite(IMG['e/b/1'])
				arme.SetCenter(6,12)
				arme.SetPosition(self.x + STATICOFS['e/b/1'][0], self.y + STATICOFS['e/b/1'][1])
				arme.SetRotation(self.alpha)
				return arme

	def fuckdrawon(self, app):
		spr = self.sprite()
		arm = self.arm()
		if arm is not None:
			app.Draw(arm)
		try:
			app.Draw(spr)
		except:
			print '>>>>>>>>>>>>ID WAS', self.id