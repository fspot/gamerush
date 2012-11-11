 
import libvect

class Tir:
	def __init__(self, pos, dirr, raceTireur, idt):
		self.id = idt
		self.pos = libvect.FloatVector(pos.x, pos.y)	#CEEEENTRE!
		self.dirr = dirr
		self.race = raceTireur

		self.speed = 7

	def serialize(self):
		dicti = {}
		dicti['id'] = self.id
		dicti['x'] = self.pos.x
		dicti['y'] = self.pos.y
		dicti['t'] = "mj"
		return dicti
