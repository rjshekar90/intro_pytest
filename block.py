"""
http://bit.ly/pytest-feb-14-2018

Coin - chain of signatures
Chain - seq of hash(block, prev_hash)
Proof of Work - (POW) - Hash that starts with zero's
Block - header (hash, nonce), data

>>> node = Node('matt')
>>> gb, hash = node.process_txns([])
>>> # Pay Fred .1
>>> txn = Transaction([Amount(1, 'matt')],
...     [Amount(.9, 'matt'), Amount(.1, 'fred')])
>>> b2, h2 = node.process_txns([txn])
>>> b2
<block.Block object at ...>
>>> h2[0]
'0'

"""

import hashlib


MINING_COST = 1

class Amount:
    def __init__(self, amount, uuid):
        self.amount = amount
        self.uuid = uuid

    def todict(self):
        return {'uuid': self.uuid, 'amount': self.amount}


class Transaction:
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs

    def todict(self):
        return {'inputs': [i.todict() for i in self.inputs],
                'outputs': [o.todict() for o in self.outputs]
                }


class Block:
    def __init__(self, txns, prev_hash, difficulty):
        self.txns = txns
        self.prev_hash = prev_hash
        self.nonce = None
        self.difficulty = difficulty

    def todict(self, nonce):
        body = {'txns': [t.todict() for t in self.txns]}
        header = {'prev_hash': self.prev_hash,
                  'body_hash': get_hash(body),
                  'difficulty': self.difficulty,
                  'nonce': nonce}
        return {'header': header, 'body': body}

    def get_hash(self, nonce):
        return get_hash(self.todict(nonce))

    
def get_hash(data_dict):
    sha = hashlib.sha256()
    sha.update(str(data_dict).encode('utf8'))
    return sha.hexdigest()   


class Node:
    def __init__(self, uuid):
        self.uuid = uuid
        self.blocks = []

    def process_txns(self, txns, difficulty=1):
        # payment to ourself
        txns.insert(0, Transaction([],
            [Amount(MINING_COST, self.uuid)]))
        # prev hash
        if self.blocks:
            prev_hash = self.blocks[-1].prev_hash
        else:
            prev_hash = ''
        block = Block(txns, prev_hash, difficulty)
        nonce = 0
        while True:
            hash = block.get_hash(nonce)
            if hash.startswith('0'*difficulty):
                block.nonce = nonce
                self.blocks.append(block)
                return block, hash
            nonce += 1
        
                    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    


    
