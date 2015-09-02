# pylint: disable=no-member
'''Tests for wald.backend.'''

from wald.backend import Node, Document


def test_add_node_to_session():
    '''Test adding node to document.'''
    document = Document()
    node = Node('foobar')
    document.add(node)
    document.save()
    assert node.node_id == 1
    assert node.parent_id is None


def test_create_node():
    '''Test creating node.'''
    node = Node(name='foobar', content='lorem ipsum dolor')
    assert node.name == 'foobar'
    assert node.content == 'lorem ipsum dolor'
    assert node.node_id is None
    assert node.parent is None


def test_create_children():
    '''Test creating children.'''
    document = Document()
    root = Node('root')
    child = Node('child', parent=root)
    document.add(root)
    document.add(child)
    document.save()
    assert root.parent is None
    assert child.parent is root
    assert root.node_id == 1
    assert child.node_id == 2
    assert root.parent_id is None
    assert child.parent_id == root.node_id


def test_get_document_roots():
    '''Test retrieving the root nodes.'''
    document = Document()
    document.add(Node('root'))
    node, = document.roots
    assert node.name == 'root'


def test_remove_root():
    '''Test removing a root node.'''
    document = Document()
    document.add(Node('root'))
    node, = document.roots
    document.remove(node)
    assert node not in document.roots
