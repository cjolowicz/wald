# pylint: disable=redefined-outer-name
'''Tests for wald.backend.'''

import pytest


@pytest.fixture
def session():
    '''Fixture returning a session.'''
    from wald.backend import Backend
    backend = Backend()
    return backend.create_session()


def test_add_node_to_session(session):
    '''Test adding node to session.'''
    from wald.backend import Node
    node = Node(name='foobar', content='lorem ipsum dolor')
    session.add(node)
    session.commit()
    assert node.node_id == 1


def test_create_node():
    '''Test creating node.'''
    from wald.backend import Node
    node = Node(name='foobar', content='lorem ipsum dolor')
    assert node.name == 'foobar'
    assert node.content == 'lorem ipsum dolor'
    assert node.node_id is None
