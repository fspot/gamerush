#!/usr/env/python
# -*- coding:utf-8 -*-

from twisted.internet import reactor, task
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint
from myprotocol import MyProtocol
from random import randint
from persoclient import PersoClient
import time
import libvect
from c import *

# le client :
class Client(MyProtocol):

    def __init__(self, glob):
        self.recu = ""  # buffer message recu
        self.size_remain = 0  # taille restante jusqu'a la fin du msg actuel
        self.glob = glob
        self.glob['sock'] = self
        self.lastmousemove = time.time()
        self.state = "connection"

    def connectionMade(self):
        print "(>) Connected"
        nom = "joueur{0}".format(randint(1,999))
        self.write({'n': nom, 'r':NAIN})  # race : nain
    
    def connectionLost(self, reason):
        print "(<) Disconnected"    
    
    def handle(self, msg):
        print "### Rcv:", msg
        if self.state == "chat":
            self.handle_chat(msg)
        elif self.state == "connection":
            self.handle_connection(msg)

    def handle_connection(self, msg):
        self.glob['moi'] = PersoClient(msg)
        self.glob['objets'] = {msg['id']: self.glob['moi']}
        print 'MOI JE SUIS', msg['id']
        self.state = "chat"

    def handle_chat(self, msg):
        typ = msg['t']
        if typ == 'mj': # mise a jour d'un objet existant
            obj = self.glob['objets'][msg['id']]
            if obj is self.glob['moi'] and 'a' in msg: # on est maitre de notre angle, pas le réseau.
                del msg['a']
            obj.modify(msg)
        elif typ == 'cr': # création d'un nouvel objet
            print 'CREATION DE', msg['id']
            # import pdb; pdb.set_trace()
            self.glob['objets'][msg['id']] = PersoClient(msg)
            # import pdb; pdb.set_trace()
        elif typ == 'dl': # delete
            del self.glob['objets'][msg['id']]

    def send_input(self, inp, down):
        # inp should be in : 'z', 'q', 'd', 'cg', 'cd'
        # espace == 'z'
        self.write({'i':inp, 'd':down, 't':'i'})  # type : input

    def send_mousemove(self, x, y):
        # envoie au serveur un vecteur entre la souris et le centre du perso
        # si ça fait longtemps qu'on ne l'a pas envoyé
        t = time.time()
        if 'moi' in self.glob:
            posx, posy = self.glob['moi'].x, self.glob['moi'].y
            v = libvect.Vector(posx, x, posy, y)
            print "posx, x, posy, y == ", posx, x, posy, y
            dx, dy = v.vecteur_norme()
            alpha = v.angle()
            self.glob['moi'].alpha = alpha
            if t - self.lastmousemove > 0.900: # 20ms
                self.write({'x':dx, 'y':dy, 'a':alpha, 't':'m'})  # type : mousemove
            self.lastmousemove = t

class ClientFactory(Factory):
    def buildProtocol(self, addr):
        return Client(self.glob)

def fct_reseau(glob):
    endpoint = TCP4ClientEndpoint(reactor, "127.0.0.1", 4577)
    factory = ClientFactory()
    factory.glob = glob
    endpoint.connect(factory)
    reactor.run(installSignalHandlers=0)

if __name__ == '__main__':
    fct_reseau()