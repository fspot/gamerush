import math



class Vector:
	
	def __init__(self, x1=0, x2=0, y1=0, y2=0):
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
		
	def setPointDir(self, xp,yp,xd,yd):
		self.x1 = xp
		self.y1 = yp
		self.x2 = xp + xd
		self.y2 = yp + yd
		
	def Dir(self):
		return self.x2-self.x1,self.y2-self.y1
		
	def Norm(self):
		return math.sqrt( (self.x2-self.x1)**2 + (self.y2-self.y1)**2 )
		
		
		
		
class FloatVector:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def __add__(self, vect):
		return FloatVector(self.x+vect.x,self.y+vect.y)
		
	def __iadd__(self, vect):
		self.x += vect.x
		self.y += vect.y
		return self
	
	def __mul__(self, value):
		return FloatVector(self.x*value,self.y*value)
		
	def __rmul__(self, value):
		return self*value
	
	def Norm(self):
		return math.sqrt( self.x**2 + self.y**2 )
		
		
def addPts(p1,p2):
	return (p1[0]+p2[0],p1[1]+p2[1])

