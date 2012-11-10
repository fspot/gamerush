 
import persoServ
import carte
import itertools
import libvect
from c import *
import pdb


class Moteur:
	def __init__(self):
		self.nains = []
		self.elfes = []
		self.tirs = []
		self.rebonds = []
		self.carte = carte.Carte()
		
	def creerPerso(self,race):
		perso = persoServ.PersoServ(race)
		if (race == ELFE):
			self.elfes.append(perso)
		else: #NAIN
			self.nains.append(perso)
			
		return perso
		
		
	def detruirePerso(self,perso):
		if (perso.race == ELFE):
			self.elfes.remove(perso)
		else:	#NAIN
			self.nains.remove(perso)

			
	def tick(self):

		for perso in itertools.chain(self.nains, self.elfes):
			
			#mouvement
			acc = FloatVector(0,0)
			acc += GRAVITE
			
			if (perso.input_z):
				if (perso.race == ELFE and perso.jetpackEnergy > 0):
					acc += perso.AccSaut
					jetpackEnergy -= JETPACK_CONSO
				elif (perso.race == NAIN and perso.contact):
					acc += perso.AccSaut
			pdb.set_trace()
			if (perso.input_q):
				acc += perso.move_L
				
			if (perso.input_d):
				acc += perso.move_R
				
			perso.vitesse += acc

			if (perso.contact):
				perso.vitesse += -perso.Frot*perso.vitesse
				norme = perso.vitesse.Norm()
				if (norme > perso.vMaxCourse):
					perso.vitesse *= (perso.vMaxCourse/norme)
				
			perso.position += perso.vitesse
			pdb.set_trace()
			#sortie ecran
			if (perso.position.x < 0):
				perso.position.x = 0.0
			if (perso.position.x > SIZE_X*COTE_CUBE):
				perso.position.x = SIZE_X*COTE_CUBE
			if (perso.position.y < 0):
				perso.position.y = 0.0
			if (perso.position.y > SIZE_Y*COTE_CUBE):
				perso.position.y = SIZE_Y*COTE_CUBE
				
			pdb.set_trace()
			#collisions
			for liste in self.carte.cubeGrid:
				for cube in liste:
					left = (cube.borderLeft - perso.bordDroit());
					right = (cube.borderRight - perso.position.x);
					top = (cube.borderUp - perso.bordBas());
					bottom = (cube.borderDown - perso.position.y);
					
		 
					if not (left > 0 or right < 0 or top > 0 or bottom < 0):
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
			
			#specifique race
			if (perso.race == ELFE):
				if perso.jetpackEnergy < JETPACK_MAX:
					perso.jetpackEnergy += JETPACK_REFILL

		return [perso.serialize() for perso in itertools.chain(self.nains, self.elfes)]


if __name__ == '__main__':
	m = Moteur()
	m.creerPerso(NAIN)
	pdb.set_trace()
	nain = m.tick()
	pdb.set_trace()
	nain = m.tick()
	pdb.set_trace()