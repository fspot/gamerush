#!/usr/env/python
# -*- coding:utf-8 -*-

from twisted.internet import protocol, reactor
from myprotocol import MyProtocol
import msgpack

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

    def repeat(self, msg):
        for u in self.users.values():
            if u is not self:
                u.write(msg)

    def handle(self, msg):
        print " # Rcv:", msg
        if self.state == "chat":
            self.handle_chat(msg)
        elif self.state == "connection":
            self.handle_connection(msg)

    def handle_connection(self, msg):
        if 'name' in msg and msg['name']:
            self.name = msg['name']
            self.users[self.name] = self
            self.state = "chat"
            self.id = len(self.users)
            msg["id"] = self.id
            self.repeat(msg)
            for u in self.users.values():
                if u is not self:
                    self.write({'name':u.name, 'id':u.id})

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
    def buildProtocol(self, addr):
        return Client(self.users)

if __name__ == '__main__':
    print '<reactor launched @ localhost:4577>'
    reactor.listenTCP(4577, ClientFactory())
    reactor.run()