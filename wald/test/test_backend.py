# pylint: disable=no-member, invalid-name
'''Tests for wald.backend.'''

from wald.backend import Node, Document


def test_create_node():
    '''Create a node.'''
    node = Node(name='node', content='Lorem ipsum dolor.')
    assert node.name == 'node'
    assert node.content == 'Lorem ipsum dolor.'
    assert node.node_id is None
    assert node.parent is None


def test_create_child_node():
    '''Create a child node.'''
    root = Node('root')
    child = Node('child', parent=root)
    assert child.parent is root
    assert child in root.children


def test_add_child_node():
    '''Add a child node.'''
    root = Node('root')
    node = Node('node')
    root.children.append(node)
    assert node.parent is root
    assert node in root.children


def test_remove_child_node():
    '''Remove a child node.'''
    root = Node('root')
    child = Node('child', parent=root)
    del root.children[0]
    assert child.parent is None
    assert child not in root.children


def test_add_node_to_document():
    '''Add a node to the document.'''
    document = Document()
    document.add(Node('root'))
    node, = document.roots
    assert node.name == 'root'


def test_remove_node_from_document():
    '''Remove a node from the document.'''
    document = Document()
    document.add(Node('root'))
    node, = document.roots
    document.remove(node)
    assert node not in document.roots


def test_save_document_with_root_node():
    '''Save a document with a root node.'''
    document = Document()
    node = Node('root')
    document.add(node)
    document.save()
    assert node.node_id == 1
    assert node.parent_id is None


def test_save_document_with_child_node():
    '''Save a document with a child node.'''
    document = Document()
    root = Node('root')
    child = Node('child', parent=root)
    document.add(root)
    document.save()
    assert root.parent is None
    assert child.parent is root
    assert root.node_id == 1
    assert child.node_id == 2
    assert root.parent_id is None
    assert child.parent_id == root.node_id
