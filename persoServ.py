import libvect
from c import *

class PersoServ:
	idcount = 0
	def __init__(self, race):
		self.id = PersoServ.idcount
		PersoServ.idcount += 1
		self.race = race
		self.contact = None
		self.vitesse = FloatVector(0.0,0.0)
		
		self.input_z = False
		self.input_q = False
		self.input_s = False
		self.input_d = False
		self.input_mouseL = False
		self.input_mouseR = False

		if (race == ELFE):
			self.vMaxCourse = 10
			self.AccCourse = 5
			self.AccSaut = FloatVector(0,-3)
			self.Frot = 0.3
			self.jetpackEnergy = JETPACK_MAX
			self.move_L = FloatVector(-AccCourse,0)
			self.move_R = FloatVector(AccCourse,0)
			self.hauteur = 10
			self.largeur = 10
			self.position = SPAWN_ELFE
			
		elif (race == NAIN):
			self.vMaxCourse = 5
			self.AccCourse = 3
			self.AccSaut = FloatVector(0,-10)
			self.Frot = 0.3
			self.pdv = 3
			self.move_L = FloatVector(-self.AccCourse,0)
			self.move_R = FloatVector(self.AccCourse,0)
			self.hauteur = 32
			self.largeur = 32
			self.position = SPAWN_NAIN

	def bordDroit(self):
		return self.position.x + self.largeur

	def bordBas(self):
		return self.position.y + self.hauteur

	def serialize(self):
		dicti = {}
		dicti['x'] = self.position.x
		dicti['y'] = self.position.y
		dicti['id'] = self.id
		dicti['t'] = 'mj'
		return dicti

