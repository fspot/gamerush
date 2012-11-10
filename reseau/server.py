#!/usr/env/python
# -*- coding:utf-8 -*-

from twisted.internet import protocol, task, reactor
from myprotocol import MyProtocol
import msgpack, time
from random import randint

FREQ = 0.5  # nb de fois par secondes.

class Client(MyProtocol):
    def __init__(self, users):
        self.recu = ""  # buffer message recu
        self.size_remain = 0  # taille restante jusqu'a la fin du msg actuel
        self.users = users
        self.state = "connection"

    def connectionMade(self):
        print '(+) New Client'

    def connectionLost(self, reason):
        if self.state == "chat":
            del self.users[self.name]
        print '(-) 1 Quit'
        self.repeat({'d':self.name})

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
        self.name = msg['n']
        self.race = msg['r']
        self.users[self.name] = self
        self.state = "chat"
        self.id = randint(1,9999)
        msg['id'] = self.id
        msg['p'] = [randint(1,1000), randint(1,500)]  # position de pop
        msg['t'] = 'cr'  # création
        self.repeat(msg)

    def handle_chat(self, msg):
        typ = msg['t']
        if typ == 'i':  # input
            print 'input', repr(msg)
        elif typ == 'm':  # mousemove
            print 'mousemove', repr(msg)
        # cheat = False
        # if 'pos' in msg:  # check anti cheat sur la position
        #     try:
        #         map(int, msg['pos'])
        #         assert len(msg['pos']) == 3
        #         [self.x, self.y, self.z] = msg['pos']
        #     except:
        #         cheat = True
        # if 'vie' in msg:  # check anti cheat sur la vie
        #     try:
        #         vie = int(msg['vie'])
        #         assert vie <= 100
        #         self.vie = vie
        #     except:
        #         cheat = True
        # if not cheat:
        #     msg['id'] = self.id
        #     self.repeat(msg)

class ClientFactory(protocol.Factory):
    users = {}
    t0 = time.time()

    def buildProtocol(self, addr):
        return Client(self.users)

    def tick(self):
        print '<elapsed time : {0}>'.format(time.time()-self.t0)

        # vérifier les collisions + faire bouger toutes les entités
        # msgs = (u.perso.infos() for u in self.users.itervalues())

        # broadcast des messages
        for u in self.users.itervalues():
            for dest in self.users.itervalues():
                u.write({'t':'mj', 'id':u.id})

def main():
    print '<reactor launched @ localhost:4577>'
    factory = ClientFactory()
    reactor.listenTCP(4577, factory)
    l = task.LoopingCall(factory.tick)
    l.start(1.0/FREQ) # 30x par secondes.
    reactor.run()

if __name__ == '__main__':
    main()
