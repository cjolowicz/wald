# pylint: disable=redefined-outer-name
'''Tests for wald.backend.'''

import pytest


@pytest.fixture
def session():
    '''Fixture returning a session.'''
    from wald.backend import Backend
    backend = Backend()
    return backend.create_session()


def test_node(session):
    '''Test wald.backend.Node.'''
    from wald.backend import Node
    node = Node(name='foobar', content='lorem ipsum dolor')
    session.add(node)
    session.commit()
