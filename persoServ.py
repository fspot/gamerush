import libvect

ELFE, NAIN = 0, 1
SPAWN_NAIN = (0,0)
SPAWN_ELFE = (0,0)

class PersoServ:
	def __init__(self, race, spawn)
		self.race = race
		self.contact = None
		self.vitesse = [0,0]
		self.position = spawn
		
		self.input_z = False
		self.input_q = False
		self.input_s = False
		self.input_d = False
		self.input_mouseL = False
		self.input_mouseR = False
	
		if (race == ELFE):
			self.vMaxCourse = 10
			self.AccCourse = 3
			self.AccAir = 3
			self.Frot = 0.3
			self.pdv
			
		else if (race == NAIN):
			self.vMaxCourse = 5
			self.AccCourse = 3
			self.AccAir = 10
			self.Frot = 0.3
			self.pdv

			# vitesse + grav + inputs (saut, depl) - frot si sol - capé vitesseMax
			# saut
			#	elfe: jetpack energy
			#	nain: contact
			#
			#
