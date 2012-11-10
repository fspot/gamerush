from const import *

class Cube:
	def __init__(self, posX, posY, h=False, b=False, g=False, d=False):
		self.X = posX
		self.Y = posY
		
		self.borderUp = self.Y*COTE_CUBE
		self.borderDown = (self.Y+1)*COTE_CUBE
		self.borderLeft = self.X*COTE_CUBE
		self.borderRight = (self.X+1)*COTE_CUBE
		
		
		
		'''self.Xborder = []
		self.Yborder = []
		
		if (h):
			self.Yborder.append(self.Y*COTE_CUBE)
		
		if (b):
			self.Yborder.append((self.Y+1)*COTE_CUBE)
		
		if (g):
			self.Xborder.append(self.X*COTE_CUBE)
			
		if (d):
			self.Xborder.append((self.X+1)*COTE_CUBE)'''
			
	
	
	
	
	
class Carte:
	def __init__(self):
		reverseGrid =[
			[1,0,1],
			[1,0,1],
			[1,0,1],
			[1,0,1]
		]
		
		self.grid = zip(*reverseGrid)
		
		col = {}
		lig = {}
		
		cubeGrid = [[None for j in range(SIZE_Y)] for i in range(SIZE_X)]

		
		for i in range(0,SIZE_X):
			for i in range(0,SIZE_Y):
				if i-1<0 or grid[i-1,j]:
					g=True
				else:
					g=False
					
				if i+1>=SIZE_X or grid[i+1,j]:
					d=True
				else:
					d=False
					
				if j-1<0 or grid[i,j-1]:
					h=True
				else:
					h=False
					
				if j+1>=SIZE_Y or grid[i,j+1]:
					b=True
				else:
					b=False
					
				if not (g and b and h and d):
					if j not in col:
						col[j] = []
						
					if i not in lig:
						lig[i] = []
					
					newCube = Cube(i,j,h,b,g,d)
					col[j].append(newCube)										
					lig[i].append(newCube)
					cubeGrid[i][j] = newCube
					

