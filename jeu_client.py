#!/usr/bin/env python
# -*- coding:utf-8 -*-

import threading, time, sys
import reseau.client as net
from PySFML import sf
from pdb import set_trace as rrr
from twisted.internet import reactor
import animenv, persoclient

# globaux 
FREQ = 30.0
APPW, APPH = 1920, 1080

_FOND = sf.Image()
_FOND.LoadFromFile("./img/map.bmp")
FOND = sf.Sprite(_FOND)
FOND.SetPosition(0,0) #(APPW/2, APPH/2)
FOND.Resize(APPW, APPH)

KEYS = {
    ord('z'): 'z',
    ord('s'): 's',
    ord('q'): 'q',
    ord('d'): 'd',
    277: ' ',
}

GLOB = {}
GLOB['objets'] = {}

# code

def boucle_de_rendu():
    app = sf.RenderWindow(sf.VideoMode(APPW, APPH), "")#, sf.Style.Fullscreen)
    view = sf.View(sf.FloatRect(0, 0, APPW, APPH))
    app.SetView(view)
    e = sf.Event()

    # animations statiques
    nbanim = 0
    for anim in animenv.ANIMS:
        nbanim -= 1
        GLOB['objets'][nbanim] = persoclient.PersoClient(anim)

    while app.IsOpened():
        t0 = time.time()
        #print "window is still opened"
        while app.GetEvent(e):
            if e.Type == sf.Event.Closed:
                app.Close()
            elif e.Type == sf.Event.KeyPressed:
                if e.Key.Code == sf.Key.Escape:
                    app.Close()
                    reactor.stop()
                else:
                    k = e.Key.Code
                    if k in KEYS:
                        if 'sock' in GLOB: GLOB['sock'].send_input(KEYS[k], True)
            elif e.Type == sf.Event.KeyReleased:
                if e.Key.Code == sf.Key.Escape:
                    app.Close()
                else:
                    k = e.Key.Code
                    if k in KEYS:
                        if 'sock' in GLOB: GLOB['sock'].send_input(KEYS[k], False)
            elif e.Type == sf.Event.MouseButtonPressed:
                x = e.MouseButton.Button
                if x == sf.Mouse.Left:
                    x = 'cg'
                else:
                    x = 'cd'
                if 'sock' in GLOB: GLOB['sock'].send_input(x, True)
            elif e.Type == sf.Event.MouseButtonReleased:
                x = e.MouseButton.Button
                if x == sf.Mouse.Left:
                    x = 'cg'
                else:
                    x = 'cd'
                if 'sock' in GLOB: GLOB['sock'].send_input(x, False)
            elif e.Type == sf.Event.MouseMoved:
                x, y = app.ConvertCoords(e.MouseMove.X, e.MouseMove.Y)
                if 'sock' in GLOB and 'moi' in GLOB:
                    GLOB['sock'].send_mousemove(x, y)

        # dessin
        app.Clear()  # effacement
        app.Draw(FOND)  # blit du fond
        if 'objets' in GLOB:
            for obj in GLOB['objets'].values():
                obj.fuckdrawon(app)
                print obj.id
        app.Display()  # affichage !

        # attente :
        deltat = time.time() - t0
        try:  # au cas ou on rame
            time.sleep(1/FREQ - deltat)
        except:
            pass

def main():
    thread_reseau = threading.Thread(target=net.fct_reseau, args=(GLOB,))
    rendu = threading.Thread(target=boucle_de_rendu)
    print '## le thread va starter'
    thread_reseau.start()
    print "## c'est bon :)."
    rendu.start()

if __name__ == '__main__':
    main()
