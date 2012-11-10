import libvect
from const import *

class PersoServ:
	def __init__(self, race, spawn):
		self.race = race
		self.contact = None
		self.vitesse = FloatVector(0.0,0.0)
		self.position = spawn
		
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
			
		elif (race == NAIN):
			self.vMaxCourse = 5
			self.AccCourse = 3
			self.AccSaut = FloatVector(0,-10)
			self.Frot = 0.3
			self.pdv = 3
			self.move_L = FloatVector(-AccCourse,0)
			self.move_R = FloatVector(AccCourse,0)
			self.hauteur = 10
			self.largeur = 10

			
	def bordDroit(self):
		return self.position.x + self.largeur
		
	def bordBas(self):
		return self.position.y + self.hauteur

	def serialize(self):
		dict = {}
		dict['x'] = self.position.x
		dict['y'] = self.position.y
		return dict