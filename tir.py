 
import libvect

class Tir:
	def __init__(self, pos, dirr, raceTireur, idt):
		self.id = idt
		self.pos = pos	#CEEEENTRE!
		self.dirr = dirr
		self.race = raceTireur

		self.speed = 7

	def serialize():
		dicti = {}
		dicti['id'] = self.id
		dicti['x'] = self.x
		dicti['y'] = self.y
		dicti['t'] = "mj"
		return dicti
