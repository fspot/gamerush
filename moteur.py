 
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
			print '0',perso.position.x
			#mouvement
			acc = FloatVector(0,0)
			acc += GRAVITE
			
			if (perso.input_z):
				if (perso.race == ELFE and perso.jetpackEnergy > 0):
					acc += perso.AccSaut
					jetpackEnergy -= JETPACK_CONSO
				elif (perso.race == NAIN and perso.contact):
					acc += perso.AccSaut
			if (perso.input_q):
				acc += perso.move_L
				
			if (perso.input_d):
				acc += perso.move_R
			print '1',perso.position.x	
			perso.vitesse += acc

			if (perso.contact):
				perso.vitesse += -perso.Frot*perso.vitesse
				norme = perso.vitesse.Norm()
				if (norme > perso.vMaxCourse):
					perso.vitesse *= (perso.vMaxCourse/norme)
			print '2',perso.position.x	
			perso.position += perso.vitesse
			#sortie ecran
			if (perso.position.x < 0):
				perso.position.x = 0.0
			if (perso.bordDroit > SIZE_X*COTE_CUBE):
				perso.position.x = (SIZE_X-1)*COTE_CUBE
			if (perso.position.y < 0):
				perso.position.y = 0.0
			if (perso.position.bordBas > SIZE_Y*COTE_CUBE):
				perso.position.y = (SIZE_Y-1)*COTE_CUBE
				
			print '3',perso.position.x
			#collisions
			for liste in self.carte.cubeGrid:
				for cube in liste:
					if cube is not None:
						#pdb.set_trace()
						left = (cube.borderLeft - perso.bordDroit());
						right = (cube.borderRight - perso.position.x);
						top = (cube.borderUp - perso.bordBas());
						bottom = (cube.borderDown - perso.position.y);
						
			 
						if not (left > 0 or right < 0 or top > 0 or bottom < 0):
							mtd = FloatVector(0.0,0.0)
							print 'a',mtd.x,mtd.y
							if abs(left) < right:
								mtd.x = left;
							else:
								mtd.x = right;
							print 'b',mtd.x,mtd.y
							if abs(top) < bottom:
								mtd.y = top;
							else:
								mtd.y = bottom;
							print 'c',mtd.x,mtd.y
				
							if abs(left) < right:
								mtd.X = left
							else:
								mtd.X = right
							print 'd',mtd.x,mtd.y
							if abs(top) < bottom:
								mtd.Y = top
							else:
								mtd.Y = bottom
							print 'e',mtd.x,mtd.y

							if abs(mtd.x) < abs(mtd.y):
								mtd.y = 0
								perso.vitesse.x=0
							else:
								mtd.x = 0
								perso.vitesse.y=0
	
							perso.position += mtd

			print '5',perso.position.x
			#specifique race
			if (perso.race == ELFE):
				if perso.jetpackEnergy < JETPACK_MAX:
					perso.jetpackEnergy += JETPACK_REFILL

		return [perso.serialize() for perso in itertools.chain(self.nains, self.elfes)]


if __name__ == '__main__':
	m = Moteur()
	m.creerPerso(NAIN)
	nain = m.tick()
	nain = m.tick()