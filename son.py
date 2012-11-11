from PySFML import sf

_liste = ['ds1', 'ds2', 'ds3', 'elf', 'jet', 'plash']
_bufs = []
sounds = {}
for e in _liste:
	x = sf.SoundBuffer()
	x.LoadFromFile('son/{}.ogg'.format(e))
	_bufs.append(x)
	y = sf.Sound(x)
	sounds[e] = y