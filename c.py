from libvect import FloatVector

ELFE, NAIN = 0, 1
SPAWN_NAIN = FloatVector(32,0.0)
SPAWN_ELFE = FloatVector(0.0,0.0)

JETPACK_REFILL = 0.5
JETPACK_CONSO = 1
JETPACK_MAX = 30

COTE_CUBE = 32

REVERSEGRID =[
	[0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,1],
	[1,1,1,1,1,1,1,1,1,1],
]

SIZE_X = len(REVERSEGRID[0])
SIZE_Y = len(REVERSEGRID)

GRAVITE = FloatVector(0, 1)
JETPACK_REFILL = 0.5
JETPACK_CONSO = 1
JETPACK_MAX = 30