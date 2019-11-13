import sys
import time
import random

from parallel_data import Node


class SecondaryNode(Node):

    def _onDataReceived(self, node, data):
        print " [<<] %sBytes from %s id:%s" %(len(data[1]), node, data[0])
        data[1] = data[1].upper()
        print " [>>] %sBytes to %s" %(len(data[1]), node)
        self.send(node, data)


host = sys.argv[1]
port = int(sys.argv[2])

node = SecondaryNode(host, port)

node.listen()
node.stopOnKeyboardInterrupt()
