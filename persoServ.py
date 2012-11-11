import libvect
from c import *

class PersoServ:
	def __init__(self, race, id):
		self.id = id
		self.race = race
		self.contact = None
		self.vitesse = FloatVector(0.0,0.0)
		
		self.input_z = False
		self.input_q = False
		self.input_s = False
		self.input_d = False
		self.input_mouseL = False
		self.input_mouseR = False
		self.input_angle = False
		self.anims = []

		if (race == ELFE):
			self.vMaxCourseX = 10
			self.vMaxAirX = 10
			self.AccCourse = 5
			self.AccAir = 3
			self.AccSaut = FloatVector(0,-3)
			self.Frot = 0.3
			self.jetpackEnergy = JETPACK_MAX
			self.hauteur = 48
			self.largeur = 30
			self.position = FloatVector(SPAWN_ELFE_X,SPAWN_ELFE_Y)
			self.input_direction = FloatVector(1,0)
			self.cooldown = 0
			
		elif (race == NAIN):
			self.vMaxCourseX = 5
			self.vMaxAirX = 5
			self.AccCourse = 3
			self.AccAir = 2
			self.AccSaut = FloatVector(0,-150)
			self.Frot = 0.1
			self.pdv = 3
			self.hauteur = 37
			self.largeur = 25
			self.position = FloatVector(SPAWN_NAIN_X,SPAWN_NAIN_Y)
			self.input_direction = FloatVector(-1,0)
			self.marteau = False

		self.move_L = FloatVector(-self.AccCourse,0)
		self.move_R = FloatVector(self.AccCourse,0)
		self.move_L_air = FloatVector(-self.AccAir,0)
		self.move_R_air = FloatVector(self.AccAir,0)

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
		dicti['a'] = self.input_angle
		if (len(self.anims) > 0):
			dicti['an'] = min(self.anims)
			self.anims = []
		else :
			dicti['an'] = A_TETE

		if (self.race == NAIN and self.marteau):
			dicti['m'] = True
			self.marteau = False

		return dicti


