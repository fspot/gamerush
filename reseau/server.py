#!/usr/env/python
# -*- coding:utf-8 -*-

from twisted.internet import protocol, task, reactor
from myprotocol import MyProtocol
import msgpack, time
from random import randint
import moteur as motor
from persoServ import PersoServ
from c import *
import libvect

FREQ = 25  # nb de fois par secondes.

class Client(MyProtocol):
    def __init__(self, users, moteur):
        self.recu = ""  # buffer message recu
        self.size_remain = 0  # taille restante jusqu'a la fin du msg actuel
        self.users = users
        self.moteur = moteur
        self.state = "connection"

    def connectionMade(self):
        print '(+) New Client'

    def connectionLost(self, reason):
        if self.state == "chat":
            self.repeat({'id':self.perso.id, 't': 'dl'})
            self.moteur.detruirePerso(self.perso)
            del self.users[self.name]
        print '(-) 1 Quit'

    def repeat(self, msg, including_me=True):
        for u in self.users.values():
            if including_me or u is not self:
                u.write(msg)

    def handle(self, msg):
        #print " # Rcv:", msg
        if self.state == "chat":
            self.handle_chat(msg)
        elif self.state == "connection":
            self.handle_connection(msg)

    def handle_connection(self, msg):
        self.perso = self.moteur.creerPerso(msg['r'])
        self.name = msg['n']
        self.users[self.name] = self
        self.state = "chat"
        msg['id'] = self.perso.id
        msg['x'] = self.perso.position.x
        msg['y'] = self.perso.position.y
        msg['t'] = 'cr'  # création
        self.repeat(msg) # communiquer mon apparition aux autres
        for u in self.users.itervalues(): # ME communiquer les autres.
            if u is not self:
                self.write({
                    'id': u.perso.id,
                    'r': u.perso.race,
                    'x': u.perso.position.x,
                    'y': u.perso.position.y,
                    't': 'cr',
                    'n': self.name,
                })

    def handle_chat(self, msg):
        typ = msg['t']
        if typ == 'i':  # input
            print 'input', repr(msg)
            if msg['i'] in ('z', ' '):
                self.perso.input_z = msg['d']
            elif msg['i'] == 's':
                self.perso.input_s = msg['d']
            elif msg['i'] == 'q':
                self.perso.input_q = msg['d']
            elif msg['i'] == 'd':
                self.perso.input_d = msg['d']
            elif msg['i'] == 'cg':
                self.perso.input_mouseL = msg['d']
            elif msg['i'] == 'cd':
                self.perso.input_mouseR = msg['d']
        elif typ == 'm':  # mousemove : il y a x,y et a.
            self.perso.input_direction = libvect.FloatVector(msg['x'], msg['y'])
            self.perso.input_angle = msg['a']

class ClientFactory(protocol.Factory):
    users = {}
    moteur = motor.Moteur()
    t0 = time.time()

    def __init__(self):
        ClientFactory.moteur.factory = self

    def buildProtocol(self, addr):
        return Client(self.users, self.moteur)

    def send_all(self, msg):
        for u in self.users.itervalues():
            u.write(msg)

    def tick(self):
        print '<elapsed time : {0}>'.format(time.time()-self.t0)

        # vérifier les collisions + faire bouger toutes les entités
        # msgs = (u.perso.infos() for u in self.users.itervalues())
        msgs = self.moteur.tick()

        # broadcast des messages
        for m in msgs:
            print '<MSG>', m
            for u in self.users.itervalues():
                u.write(m)

def main():
    print '<reactor launched @ localhost:4577>'
    factory = ClientFactory()
    reactor.listenTCP(4577, factory)
    l = task.LoopingCall(factory.tick)
    l.start(1.0/FREQ) # 30x par secondes.
    reactor.run()

if __name__ == '__main__':
    main()
