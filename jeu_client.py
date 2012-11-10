#!/usr/bin/env python
# -*- coding:utf-8 -*-

import threading, time, sys
import reseau.client as net
from PySFML import sf

# globaux 
FREQ = 10.0
APPW, APPH = 1000, 1000

_FOND = sf.Image()
_FOND.LoadFromFile("./img/img.png")
FOND = sf.Sprite(_FOND)
FOND.SetPosition(0,0) #(APPW/2, APPH/2)
FOND.Resize(APPW, APPH)

def boucle_de_rendu():
	app = sf.RenderWindow(sf.VideoMode(APPW, APPH), "PySFML test", sf.Style.Fullscreen)
	view = sf.View(sf.FloatRect(0, 0, APPW, APPH))
	app.SetView(view)
	e = sf.Event()
	while app.IsOpened():
		#print "window is still opened"
		while app.GetEvent(e):
		    if e.Type == sf.Event.Closed:
		        app.Close()
		    elif e.Type in (sf.Event.KeyPressed, sf.Event.KeyReleased):
		    	if e.Key.Code == sf.Key.Escape:
		    		app.Close()
		    	else:
		    		print 'key', e.Key.Code
		    elif e.Type in (sf.Event.MouseButtonPressed, sf.Event.MouseButtonReleased):
				print '1) mouseclic', e.MouseButton.Button, e.MouseButton.X, e.MouseButton.Y
				print '2) mouseclic', e.MouseButton.Button, app.ConvertCoords(e.MouseButton.X, e.MouseButton.Y)
		    elif e.Type == sf.Event.MouseMoved:
		    	pass #print 'mousemove', e.MouseMove.X, e.MouseMove.Y

		time.sleep(1/FREQ)
		# dessin
		app.Clear()
		app.Draw(FOND)
		app.Display()

def main():
	thread_reseau = threading.Thread(target=net.fct_reseau)
	rendu = threading.Thread(target=boucle_de_rendu)
	print '## le thread va starter'
	thread_reseau.start()
	print "## c'est bon :)."
	rendu.start()

if __name__ == '__main__':
	main()
