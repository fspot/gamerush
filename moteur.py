
import persoServ
import carte
import itertools
import libvect
from c import *
import pdb
import tir as shoot


class Moteur:
	def __init__(self):
		self.nains = []
		self.nainsMorts = []
		self.elfes = []
		self.elfesMorts = []
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
		tir = shoot.Tir(pos, dirr, raceTirreur, self.idcount)
		self.idcount += 1
		self.tirs.append(tir)
		self.factory.send_all({'t':'cr','id':tir.id,'x':tir.pos.x,'y':tir.pos.y,'pr':tir.race})
		return tir

	def detruireTir(self, tir):
		if tir in self.tirs:
			self.tirs.remove(tir)

		self.factory.send_all({'t':'dl','id':tir.id})
		
		
	def detruirePerso(self,perso):
		if (perso.race == ELFE):
			if perso in self.elfes:
				self.elfes.remove(perso)
			if perso in self.elfesMorts:
				self.elfesMorts.remove(perso)

		else:	#NAIN
			if perso in self.nains:
				self.nains.remove(perso)
			if perso in self.nainsMorts:
				self.nainsMorts.remove(perso)

	def mortTemporaireElfe(self,elfe):
		elfe.anims.append(A_MEURT)
		self.elfes.remove(elfe)
		self.elfesMorts.append([REVIVE_COOLDOWN,elfe])

	def reviveElfes(self):
		for elfeTTL in self.elfesMorts:
			elfeTTL[0] -= 1
			if elfeTTL[0] == 0:
				self.elfesMorts.remove(elfeTTL)
				self.elfes.append(elfeTTL[1])
				elfeTTL[1].position = FloatVector(SPAWN_ELFE_X,SPAWN_ELFE_Y)




			
	def tick(self):
		self.reviveElfes()

		for perso in itertools.chain(self.nains, self.elfes):
			#mouvement
			acc = FloatVector(0,0)
			acc += GRAVITE
			
			if (perso.input_z):
				if (perso.race == ELFE and perso.jetpackEnergy > 0):
					acc += perso.AccSaut
					perso.jetpackEnergy -= JETPACK_CONSO
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
				if (abs(perso.vitesse.x) > perso.vMaxCourseX):
					perso.vitesse.x *= (perso.vMaxCourseX/abs(perso.vitesse.x))
			else:	#air
				if (abs(perso.vitesse.x) > perso.vMaxAirX):
					perso.vitesse.x *= (perso.vMaxAirX/abs(perso.vitesse.x))

			#limitation absolue (max COTE_CUBE/2)
			norme = perso.vitesse.Norm()
			if (norme > vMaxABSOLUE):
				perso.vitesse *= (vMaxABSOLUE/norme)

			perso.position += perso.vitesse
			#sortie ecran
			if (perso.position.x < 0):
				perso.position.x = 0.0
				perso.vitesse.x=0
			if (perso.bordDroit() > SIZE_X*COTE_CUBE):
				perso.position.x = SIZE_X*COTE_CUBE - perso.largeur
				perso.vitesse.x=0
			if (perso.position.y < 0):
				perso.position.y = 0.0
				perso.vitesse.y=0
			if (perso.bordBas() > SIZE_Y*COTE_CUBE):
				perso.position.y = SIZE_Y*COTE_CUBE - perso.largeur
				perso.vitesse.y=0
				
			newContact = False
			#collisions

			x_grid_start = int(perso.position.x//COTE_CUBE)
			x_grid_end = int(perso.bordDroit()//COTE_CUBE)
			y_grid_start = int(perso.position.y//COTE_CUBE)
			y_grid_end = int(perso.bordBas()//COTE_CUBE)
			for liste in self.carte.cubeGrid[x_grid_start:x_grid_end+1]:
				for cube in liste[y_grid_start:y_grid_end+1]:
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


			perso.contact = newContact
			if not newContact:
				perso.anims.append(A_TOMBE)

			#specifique race
			if perso.race == ELFE:
				if perso.jetpackEnergy < JETPACK_MAX:
					perso.jetpackEnergy += JETPACK_REFILL

				if perso.cooldown > 0:
					perso.cooldown -=1

				if perso.input_mouseL and perso.cooldown <= 0 :
					perso.cooldown = COOLDOWN_MAX
					newTir = self.creerTir(perso.lieuTir(), perso.input_direction, ELFE)


		for tir in self.tirs:
			#mvt tir
			tir.pos += tir.speed*tir.dirr
			#sortie terrain
			if tir.pos.x < 0 or tir.pos.x > SIZE_X*COTE_CUBE or tir.pos.y < 0 or tir.pos.y > SIZE_Y*COTE_CUBE:
				self.detruireTir(tir)
			else:
				if tir.race == ELFE:
					#colision nains
					for nain in self.nains:
						if tir.pos.x > nain.position.x and tir.pos.x < nain.bordDroit() and tir.pos.y > nain.position.y and tir.pos.y < nain.bordBas():
							if (nain.input_direction.scalaire(tir.dirr) < SCALAIRE_BOUCLIER):
								#renvoi!
								tir.race = NAIN
								tir.dirr = tir.dirr + (-2)*tir.dirr.scalaire(nain.input_direction)*nain.input_direction
							else:
								self.detruireTir(tir)
								nain.pdv -= 1
								nain.anims.append(A_CRIE)
								if nain.pdv == 0:
									self.nains.remove(nain)
									self.nainsMorts.append(nain)
									nain.anims.append(A_MEURT)
				else: #tirreur = nain
					for elfe in self.elfes:
							if (tir.pos.x > elfe.position.x and tir.pos.x < elfe.bordDroit() and tir.pos.y > elfe.position.y and tir.pos.y < elfe.bordBas()):
								self.mortTemporaireElfe(elfe)
								self.detruireTir(tir)


				#colision bloc
				x_grid = int(tir.pos.x//COTE_CUBE)
				y_grid = int(tir.pos.y//COTE_CUBE)
				if self.carte.cubeGrid[x_grid][y_grid] is not None:
					self.detruireTir(tir)
		

		for nain in self.nains:
			for elfe in self.elfes:
				if not (nain.bordDroit() < elfe.position.x or nain.bordBas() < elfe.position.y or nain.position.x > elfe.bordDroit() or nain.position.y > elfe.bordBas()):
					self.mortTemporaireElfe(elfe)
					nain.marteau = True
		elfesMorts2 = [elfesTTL[1] for elfesTTL in self.elfesMorts]
		return [perso.serialize() for perso in itertools.chain(self.nains, self.elfes, self.tirs, elfesMorts2, self.nainsMorts)]


if __name__ == '__main__':
	m = Moteur()
	m.creerPerso(NAIN)
	nain = m.tick()
	nain = m.tick()