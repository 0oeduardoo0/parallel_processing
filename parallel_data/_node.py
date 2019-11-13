import json
import socket
import threading
from os import system
from struct import pack, unpack
from multiprocessing import Process


class Node():

    def __init__(self, host, port):
        system('clear')
        self.me = (host, port)
        self.nodes_availability = {}

    def __set_node_availability(self, node, status):
        node_name = "%s:%s" %(node[0], node[1])
        self.nodes_availability[node_name] = status

    def __listener(self):
        """Starts server and listener loop.
        """

        print " [i] starting %s..." %(self.__class__.__name__)
        print " [i] %s:%s" %(self.me)

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(self.me)
            self.socket.listen(1)
        except:
            print " [!] Error while starting server"
            print " [i] Is address already in use?"
            return

        print " [i] %s is listening..." %(self.__class__.__name__)

        while True:
            client, port = self.socket.accept()

            bs = client.recv(8)
            (handshake_length, ) = unpack('>Q', bs)

            handshake = client.recv(handshake_length)

            bs = client.recv(8)
            (data_size, ) = unpack('>Q', bs)

            data = ""
            data_received = 0
            while data_received < data_size:
                _data = client.recv(4096)

                if not _data:
                    break

                data += _data
                data_received += len(_data)

            if data == "%stop_listener%":
                break

            handshake = handshake.split(':')
            node = (handshake[0], int(handshake[1]))
            data = [int(handshake[2]), data]

            assert len(b'\00') == 1
            client.sendall(b'\00')

            self.__set_node_availability(node, True)
            self._onDataReceived(node, data)

        print "\n [!] stoping %s..." %(self.__class__.__name__)

        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

        print " [i] %s has been stoped" %(self.__class__.__name__)

    def __sender(self, data, node):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(node)

        handshake = "%s:%s:%s" %(self.me[0], self.me[1], data[0])

        data_length = pack('>Q', len(data[1]))
        handshake_length = pack('>Q', len(handshake))

        s.sendall(handshake_length)
        s.sendall(handshake)
        s.sendall(data_length)
        s.sendall(data[1])

        ack = s.recv(1)

        s.close()

    def _onDataReceived(self, node, data):
        pass

    def _isNotBusy(self, node):
        node_name = "%s:%s" %(node[0], node[1])

        if node_name in self.nodes_availability.keys():
            return self.nodes_availability[node_name]

        return True

    def stop(self):
        self.send(self.me, [1, "%stop_listener%"])

    def stopOnKeyboardInterrupt(self):
        try:
            while 1:
                pass
        except KeyboardInterrupt:
            self.stop()

    def listen(self):
        x = threading.Thread(target=self.__listener)
        x.start()

    def send(self, node, data):
        self.__set_node_availability(node, False)
        x = Process(target=self.__sender, args=(data, node))
        x.start()
        #x.join()
