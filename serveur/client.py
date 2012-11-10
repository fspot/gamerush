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
        self.num = 3

    def connectionMade(self):
        print "(>) Connected"
        nom = "Lu" * randint(1,9)
        self.write({'name': nom})
    
    def connectionLost(self, reason):
        print "(<) Disconnected"    
    
    def handle(self, msg):
        print " # Rcv:", msg
        if self.num:
            self.num -= 1
            vie = int(self.num*50)
            self.write({'vie':vie})

class ClientFactory(Factory):
    def buildProtocol(self, addr):
        return Client()

if __name__ == '__main__':
    endpoint = TCP4ClientEndpoint(reactor, "127.0.0.1", 4577)
    endpoint.connect(ClientFactory())
    reactor.run()