# PyDFS

# Components:
 1. **Master :** Will contain metadata
 2. **Minion :** Will contain actual file data
 3. **Client :** Interacts with 1 and 2 to do stuff
   
## Master:
Master will contain metadata. Which is: file name, blocks associated with it and address of those blocks. Data structures wise, it would look something like this.

## Minion:
Minions are relatively simple in operations and implementation. Given a block address either they can read or write and forward same block to next minion.



## Client:
Client will interact with both minions and master. Given a get or put operation, it will first contact master to query metadata and then pertaining minions to perform data operation.


-----

## Misc:
 1. Minions will be anticipating PORT and DATA_DIR as arguments. Blocks will be stored under DATA_DIR.
 2. Block size, replication factors, list of minions are hard coded in master.
 3. We are not storing metadata on disk.
