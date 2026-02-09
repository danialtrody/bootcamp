from solution.exercise4 import binary_to_integer


def test_simple_binary():
    assert binary_to_integer("1101") == 13
    
def test_all_zeros():
    assert binary_to_integer("0000") == 0

def test_long_binary():
    assert binary_to_integer("1010101") == 85

def test_single_one():
    assert binary_to_integer("1") == 1

