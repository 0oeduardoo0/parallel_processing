from time import time
from parallel_data import Node, DataFragmentation


class MainNode(Node):

    def _onDataReceived(self, node, data):
        self.data_fragmentation.reconstruct(data)

        print " [i] %s parts of %s" %(self.data_fragmentation.reconstructed_parts, self.data_fragmentation.parts)

        if self.data_fragmentation.reconstruction_done:
            new_data = self.data_fragmentation.getReconstructedData()
            file = open('TEST.txt', 'w')
            data = file.write(new_data)
            file.close()
            self.stop()

    def process(self):
        nodes = [
            ('localhost', 9001),
            ('localhost', 9002),
            ('localhost', 9003),
            ('localhost', 9004)
        ]

        file = open('test.txt', 'r')
        data = file.read()
        file.close()

        self.data_fragmentation = DataFragmentation()
        fragments = self.data_fragmentation.fragment(data, 300)

        while 1:
            try:
                for node in nodes:
                    if self._isNotBusy(node):
                        self.send(node, fragments.next())

            except:
                break


main_node = MainNode('localhost', 9000)
main_node.listen()

start = time()

main_node.process()

enlapsed = time() - start
print " [.] Enlapsed time: %ss" %(enlapsed)
