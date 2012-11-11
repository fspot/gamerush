from libvect import FloatVector

ELFE, NAIN = 0, 1
SPAWN_NAIN_X = 1850
SPAWN_NAIN_Y = 700
SPAWN_ELFE_X = 32
SPAWN_ELFE_Y = 700


COOLDOWN_MAX = 10
REVIVE_COOLDOWN = 100

vMaxABSOLUE = 20 # max COTE_CUBE/2

COTE_CUBE = 32

REVERSEGRID = [[0 for i in range(60)] for j in range(28)]
REVERSEGRID.append([1 for i in range(60)])
REVERSEGRID.append([1 for i in range(60)])
REVERSEGRID.append([1 for i in range(60)])
REVERSEGRID.append([1 for i in range(60)])
REVERSEGRID.append([1 for i in range(60)])

SIZE_X = len(REVERSEGRID[0])
print SIZE_X
SIZE_Y = len(REVERSEGRID)

GRAVITE = FloatVector(0, 1)
JETPACK_REFILL = 0.25
JETPACK_CONSO = 1
JETPACK_MAX = 30

SCALAIRE_BOUCLIER = -0.6

A_MEURT, A_CRIE, A_DECOLE, A_VOLE, A_TOMBE, A_MARCHE, A_TETE = range(7)