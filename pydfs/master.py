import rpyc
import uuid
import math
import random
import configparser
import signal
import pickle
import sys
import os

from rpyc.utils.server import ThreadedServer

'''Constants Definition: BLOCK_SIZE, REPLICATION_FACTOR, and MINIONS are defined. These constants are used for block size, 
replication factor of the blocks, and the addresses of the minion servers.'''

BLOCK_SIZE = 100
REPLICATION_FACTOR = 2
MINIONS = {"1": ("127.0.0.1", 8000),
           "2": ("127.0.0.1", 9000),}


'''Class MasterService(rpyc.Service): Defines the MasterService class that extends rpyc.Service.
file_block dictionary tracks which blocks make up a file.
block_minion dictionary tracks which minions have a copy of a block.
minions dictionary holds the address information of each minion.'''

class MasterService(rpyc.Service):
    """
    file_block = {'file.txt': ["block1", "block2"]}
    block_minion = {"block1": [1,3]}
    minions = {"1": (127.0.0.1,8000), "3": (127.0.0.1,9000)}
    """

    file_block = {}
    block_minion = {}
    minions = MINIONS

    block_size = BLOCK_SIZE
    replication_factor = REPLICATION_FACTOR
'''exposed_read: Method to handle read requests for a file. It returns a mapping of block IDs to minion addresses for each block of the file.'''

    def exposed_read(self, file):

        mapping = []
        # iterate over all of the file's blocks
        for blk in self.file_block[file]:
            minion_addr = []
            # get all minions that contain that block
            for m_id in self.block_minion[blk]:
                minion_addr.append(self.minions[m_id])

            mapping.append({"block_id": blk, "block_addr": minion_addr})
        return mapping
'''exposed_write: Method to handle write requests. It calculates how many blocks are needed for the file and calls alloc_blocks.'''

    def exposed_write(self, file, size):

        self.file_block[file] = []

        num_blocks = int(math.ceil(float(size) / self.block_size))
        return self.alloc_blocks(file, num_blocks)
'''alloc_blocks: Allocates blocks for a file on random minions for replication.'''

    def alloc_blocks(self, file, num_blocks):
        return_blocks = []
        for i in range(0, num_blocks):
            block_id = str(uuid.uuid1()) # generate a block
            minion_ids = random.sample(     # allocate REPLICATION_FACTOR number of minions
                list(self.minions.keys()), self.replication_factor)
            minion_addr = [self.minions[m] for m in minion_ids]
            self.block_minion[block_id] = minion_ids
            self.file_block[file].append(block_id)

            return_blocks.append(
                {"block_id": block_id, "block_addr": minion_addr})

        return return_blocks

'''Starts a threaded server for the master service.'''

if __name__ == "__main__":
    t = ThreadedServer(MasterService(), port=2131, protocol_config={
    'allow_public_attrs': True,
})
    t.start()
