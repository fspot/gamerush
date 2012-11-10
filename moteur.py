 
import persoServ
import carte
import itertools
import libvect
from c import *


class Moteur:
	def __init__(self)
		self.nains = []
		self.elfes = []
		self.tirs = []
		self.rebonds = []
		self.carte = Carte()
		
	def creerPerso(race)
		perso = PersoServ(race)
		if (race == ELFE):
			self.elfes.append(perso)
		else: #NAIN
			self.nains.append(perso)
			
		return PersoServ(race)
		
		
	def detruirePerso(perso)
		if (perso.race == ELFE):
			self.elfes.remove(perso)
		else:	#NAIN
			self.nains.remove(perso)

			
	def tick():

		for perso in itertools.chain(nains, elfes):
			
			#mouvement
			deplacement = perso.vitesse + GRAVITE
			
			if (perso.input_z):
				if (perso.race == ELFE and perso.jetpackEnergy > 0):
					deplacement += perso.AccSaut
					jetpackEnergy -= JETPACK_CONSO
				elif (perso.race == NAIN and perso.contact):
					deplacement += perso.AccSaut
			
			if (perso.input_q):
				deplacement += perso.move_L
				
			if (perso.input_d):
				deplacement += perso.move_R
				
			if (perso.contact):
				deplacement += -perso.Frot*deplacement
				norme = deplacement.Norm()
				if (norme > perso.vMaxCourse):
					deplacement *= (perso.vMaxCourse/norme)
				
			perso.position += deplacement
			#sortie ecran
			if (perso.position.x < 0):
				perso.position.x = 0.0
			if (perso.position.x > SIZE_X*COTE_CUBE):
				perso.position.x = SIZE_X*COTE_CUBE
			if (perso.position.y < 0):
				perso.position.y = 0.0
			if (perso.position.y > SIZE_Y*COTE_CUBE):
				perso.position.y = SIZE_Y*COTE_CUBE
				
			#collisions
			for liste in carte.cubeGrid:
				for cube in liste:
					left = (cube.borderLeft - perso.bordDroit);
					right = (cube.borderRight - perso.position.x);
					top = (borderUp - perso.bordBas);
					bottom = (cube.borderDown - perso.position.y);
					
		 
					if !(left > 0 || right < 0 || top > 0 || bottom < 0):
						mtd = FloatVector(0.0,0.0)
						if abs(left) < right:
							mtd.x = left;
						else:
							mtd.x = right;
						
						if abs(top) < bottom:
							mtd.y = top;
						else:
							mtd.y = bottom;
						
			
						if abs(left) < right:
							mtd.X = left
						else:
							mtd.X = right
						
						if abs(top) < bottom:
							mtd.Y = top
						else:
							mtd.Y = bottom
					

						if abs(mtd.x) < abs(mtd.y):
							mtd.y = 0
						else:
							mtd.x = 0
						
						perso.position += mtd
			
			#spécifique race
			if (perso.race == ELFE)
				if (perso.jetpackEnergy < JETPACK_MAX
					perso.jetpackEnergy += JETPACK_REFILL

		return [perso.serialize() for perso in itertools.chain(nains, elfes)]
