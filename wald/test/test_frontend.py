'''Tests for wald.frontend.'''

from wald.frontend import Frame


def test_create_frame():
    '''Create a node.'''
    node = Frame()
    assert node is not None
