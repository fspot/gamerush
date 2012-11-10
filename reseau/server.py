#!/usr/env/python
# -*- coding:utf-8 -*-

from twisted.internet import protocol, task, reactor
from myprotocol import MyProtocol
import msgpack, time

FREQ = 5.0

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

    def repeat(self, msg):
        for u in self.users.values():
            u.write(msg)

    def handle(self, msg):
        print " # Rcv:", msg
        if self.state == "chat":
            self.handle_chat(msg)
        elif self.state == "connection":
            self.handle_connection(msg)

    def handle_connection(self, msg):
        if 'n' in msg:
            self.name = msg['n']
            self.race = msg['r']
            self.users[self.name] = self
            self.state = "chat"
            self.repeat(msg)

    def handle_chat(self, msg):
        cheat = False
        if 'pos' in msg:  # check anti cheat sur la position
            try:
                map(int, msg['pos'])
                assert len(msg['pos']) == 3
                [self.x, self.y, self.z] = msg['pos']
            except:
                cheat = True
        if 'vie' in msg:  # check anti cheat sur la vie
            try:
                vie = int(msg['vie'])
                assert vie <= 100
                self.vie = vie
            except:
                cheat = True
        if not cheat:
            msg['id'] = self.id
            self.repeat(msg)

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
            u.write({'msg':'coucou'})

def main():
    print '<reactor launched @ localhost:4577>'
    factory = ClientFactory()
    reactor.listenTCP(4577, factory)
    l = task.LoopingCall(factory.tick)
    l.start(1.0/FREQ) # 30x par secondes.
    reactor.run()

if __name__ == '__main__':
    main()
