# pylint: disable=redefined-outer-name
'''Tests for wald.backend.'''

import pytest
from wald.backend import Node


@pytest.fixture
def session():
    '''Fixture returning a session.'''
    from wald.backend import Backend
    backend = Backend()
    return backend.create_session()


def test_add_node_to_session(session):
    '''Test adding node to session.'''
    node = Node('foobar')
    session.add(node)
    session.commit()
    assert node.node_id == 1
    assert node.parent_id is None


def test_create_node():
    '''Test creating node.'''
    node = Node(name='foobar', content='lorem ipsum dolor')
    assert node.name == 'foobar'
    assert node.content == 'lorem ipsum dolor'
    assert node.node_id is None
    assert node.parent is None


def test_create_children(session):
    '''Test creating children.'''
    root = Node('root')
    child = Node('child', parent=root)
    assert root.parent is None
    assert child.parent is root
    session.add(root)
    session.add(child)
    session.commit()
    assert root.node_id == 1
    assert child.node_id == 2
    assert root.parent_id is None
    assert child.parent_id == root.node_id
