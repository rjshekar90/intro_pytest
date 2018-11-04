import sys  # std lib

from block import (Amount, Node, Transaction)  # local lib

import pytest   # 3rd party

# write a test that asserts that a failure occurs when
# a string is passed in for the difficulty
def test_bad_difficulty():
    node = Node('matt')
    with pytest.raises(TypeError):
        gb, hash = node.process_txns([], difficulty='2')


def test_add():
    res = 3 + 4
    assert res == 7

@pytest.mark.skip
def test_gen():
    node = Node('matt')
    gb, hash = node.process_txns([])
    assert hash[0] == '0'
#test_gen = pytest.skip(test_gen)

def test_difficulty():
    node = Node('matt')
    gb, hash = node.process_txns([], difficulty=2)
    assert hash[:2] == '00'

@pytest.mark.long    
def test_difficulty3():
    node = Node('matt')
    gb, hash = node.process_txns([], difficulty=5)
    assert hash[:5] == '00000'

@pytest.mark.txn    
def test_doc():
    node = Node('matt')
    #import pdb;pdb.set_trace()
    gb, hash = node.process_txns([])
    assert hash[0] == '0'

    # Pay Fred .1
    txn = Transaction([Amount(1, 'matt')],
         [Amount(.9, 'matt'), Amount(.1, 'fred')])
    b2, h2 = node.process_txns([txn])
    assert h2[0] == '0' #.startswith('1')


if __name__ == '__main__':
    pytest.main()
