import itertools


class DataFragmentation():

    def __init__(self):
        self.parts = 0
        self.reconstructed = None
        self.reconstructed_parts = 0
        self.reconstruction_done = False

    def getReconstructedData(self):
        data = self.reconstructed[0]
        self.reconstructed.pop(0)

        for d in self.reconstructed:
            data += d

        return data

    def reconstruct(self, data):
        index = data[0]
        content = data[1]

        self.reconstructed[index] = content
        self.reconstructed_parts += 1

        if self.reconstructed_parts >= self.parts:
            self.reconstruction_done = True

    def fragment(self, data, parts):
        data_size = len(data)
        part_size = len(data) // parts
        chunk = range(0, data_size, part_size)

        self.parts = len(chunk)
        self.reconstructed = [[] for i in range(self.parts)]

        print " [i] %s Bytes of data" %(data_size)
        print " [i] %s Bytes per part" %(part_size)
        print " [i] %s parts" %(self.parts)

        fragment_counter = -1
        for i in chunk:
            fragment_counter += 1
            yield (fragment_counter, data[i:i + part_size])
