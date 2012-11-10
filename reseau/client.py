#!/usr/env/python
# -*- coding:utf-8 -*-

from twisted.internet import reactor, task
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint
from myprotocol import MyProtocol
from random import randint

# le client :
class Client(MyProtocol):

    def __init__(self):
        self.recu = ""  # buffer message recu
        self.size_remain = 0  # taille restante jusqu'a la fin du msg actuel

    def connectionMade(self):
        print "(>) Connected"
        nom = "joueur{0}".format(randint(1,999))
        self.write({'n': nom, 'r':'n'})  # race : nain
    
    def connectionLost(self, reason):
        print "(<) Disconnected"    
    
    def handle(self, msg):
        print " # Rcv:", msg

    def send_input(self, inp, down):
        # inp should be in : 'z', 'q', 'd', 'cg', 'cd'
        # espace == 'z'
        pass

    def send_mousemove(self, x, y):
        # envoie au serveur un angle entre la souris et le centre du perso
        # si ça fait longtemps qu'on ne l'a pas envoyé
        pass

class ClientFactory(Factory):
    def buildProtocol(self, addr):
        return Client()

def fct_reseau():
    endpoint = TCP4ClientEndpoint(reactor, "127.0.0.1", 4577)
    endpoint.connect(ClientFactory())
    reactor.run()

if __name__ == '__main__':
    fct_reseau()