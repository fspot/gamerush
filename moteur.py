
import persoServ
import carte
import itertools
import libvect
from c import *
import pdb


class Moteur:
	def __init__(self):
		self.nains = []
		self.nainsMorts = []
		self.elfes = []
		self.tirs = []
		self.carte = carte.Carte()
		self.idcount = 0
		
	def creerPerso(self,race):
		perso = persoServ.PersoServ(race,self.idcount)
		self.idcount += 1
		if (race == ELFE):
			self.elfes.append(perso)
		else: #NAIN
			self.nains.append(perso)
			
		return perso

	def creerTir(self, pos, dirr, raceTirreur):
		tir = Tir(pos, dirr, raceTirreur)
		self.tirs.append(tir)
		self.factory.send_all({'t':'cr','id':tir.id,'x':tir.pos.x,'y':tir.pos.y,'tr':tir.race})
		return tir

	def detruireTir(self, tir):
		self.tir.remove(tir)
		self.factory.send_all({'t':'dl','id':tir.id})
		
		
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
					if (perso.contact):
						perso.anims.append(A_DECOLE)
					else:
						perso.anims.append(A_VOLE)
				elif (perso.race == NAIN and perso.contact):
					acc += perso.AccSaut

			if (perso.input_q):
				if (perso.contact):
					acc += perso.move_L
					perso.anims.append(A_MARCHE)
				else: #air
					acc += perso.move_L_air

				
			if (perso.input_d):
				if (perso.contact):
					acc += perso.move_R	
					perso.anims.append(A_MARCHE)
				else: #air
					acc += perso.move_R_air

			perso.vitesse += acc

			if (perso.contact):
				perso.vitesse += -perso.Frot*perso.vitesse
				norme = perso.vitesse.Norm()
				if (norme > perso.vMaxCourse):
					perso.vitesse *= (perso.vMaxCourse/norme)
			perso.position += perso.vitesse
			#sortie ecran
			if (perso.position.x < 0):
				perso.position.x = 0.0
				perso.vitesse.x=0
			if (perso.bordDroit() > SIZE_X*COTE_CUBE):
				perso.position.x = SIZE_X*COTE_CUBE - perso.largeur
				print 'SORTIIIEEE'
				perso.vitesse.x=0
			if (perso.position.y < 0):
				perso.position.y = 0.0
				perso.vitesse.y=0
			if (perso.bordBas() > SIZE_Y*COTE_CUBE):
				perso.position.y = SIZE_Y*COTE_CUBE - perso.largeur
				perso.vitesse.y=0
				
			newContact = False
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
							newContact = True
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
								perso.vitesse.x=0
							else:
								mtd.x = 0
								perso.vitesse.y=0
							perso.position += mtd
						else:
							perso.contact = False

			#specifique race
			if (perso.race == ELFE):
				if perso.jetpackEnergy < JETPACK_MAX:
					perso.jetpackEnergy += JETPACK_REFILL

				if perso.cooldown > 0:
					perso.cooldown -=1

				if perso.input_mouseL and perso.cooldown <= 0 :
					perso.cooldown = COOLDOWN_MAX
					newTir = self.creerTir(perso.position, perso.dirr, ELFE)


			perso.contact = newContact
			if not newContact:
				perso.anims.append(A_TOMBE)
				print 'tombe'
			else:
				print 'pas tombe'

		for tir in self.tirs:
			#mvt tir
			tir.pos += tir.speed*tir.dirr
			#sortie terrain
			if tir.pos.x < 0 or tir.pos.x > SIZE_X*COTE_CUBE or tir.pos.y < 0 or tir.pos.y > SIZE_Y*COTE_CUBE:
				self.detruireTir(tir)
			else:
				if tir.race == ELFE:
					#colision nains
					for nain in nains:
						if tir.pos.x > nain.x and tir.pos.x < nain.bordDroit() and tir.pos.y > nain.y and tir.pos.y < nain.bordBas():
							if (nain.input_direction.scalaire(tir.dirr) < SCALAIRE_BOUCLIER):
								#renvoi!
								self.tirs.race = NAIN
								tir.dirr = tir.dirr - 2*tir.dirr.scalaire(nain.input_direction)*nain.input_direction
							else:
								self.detruireTir(tir)
								nain.pdv -= 1
								nain.anims.append(A_CRIE)
								if nain.pdv == 0:
									self.nains.remove(nain)
									self.nainsMorts.append(nain)
									nain.anims.append(A_MORT)
				else: #tirreur = nain
					for elfe in elfes:
							if tir.pos.x > elfe.x and tir.pos.x < elfe.bordDroit() and tir.pos.y > elfe.y and tir.pos.y < elfe.bordBas():
								if (perso.input_direction.scalaire(tir.dirr) < SCALAIRE_BOUCLIER):
									elfe.anims.append(A_MORT)
									self.detruireTir(tir)
									#gerer elfes morts + repop A FAIIIIIRE


				#colision bloc
				x_grid = tir.pos.x//COTE_CUBE
				y_grid = tir.pos.y//COTE_CUBE
				if self.carte.cubeGrid[x_grid][y_grid] is not None:
					self.detruireTir(tir)
				
		return [perso.serialize() for perso in itertools.chain(self.nains, self.elfes)]


if __name__ == '__main__':
	m = Moteur()
	m.creerPerso(NAIN)
	nain = m.tick()
	nain = m.tick()