#!/usr/env/python
# -*- coding:utf-8 -*-

from twisted.internet.protocol import Protocol
import struct, msgpack

class MyProtocol(Protocol):

    # ====== You must create these attributes and def handle ======
    # def __init__(self):
    #     self.recu = ""  # buffer message recu
    #     self.size_remain = 0  # taille restante jusqu'a la fin du msg actuel

    def dataReceived(self, data):
        while data:   
            if self.size_remain == 0:  # new message
                msg = self.recu + data
                if len(msg) >= 4:
                    byts, data = msg[:4], msg[4:]
                    self.size_remain = struct.unpack(">L", byts)[0]
                    self.recu = ""
                else:
                    self.recu += data
                    data = ""
            else:  # on attend la fin d'un msg
                if len(data) >= self.size_remain:  # fin du msg
                    self.recu += data[:self.size_remain]
                    data = data[self.size_remain:]
                    self.size_remain = 0
                    self._handle_raw(self.recu)  # cette fonction traite le msg recu
                    self.recu = ""
                else:
                    self.recu += data
                    self.size_remain -= len(data)
                    data = ""

    def _handle_raw(self, rawmsg):
        msg = msgpack.unpackb(rawmsg)
        self.handle(msg)

    def write(self, msg):
        rawmsg = msgpack.packb(msg)
        size = struct.pack(">L", len(rawmsg))  # big endian = network
        self.transport.write(size + rawmsg)
