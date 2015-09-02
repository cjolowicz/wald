import pytest

@pytest.fixture
def session():
    from wald.backend import Backend
    backend = Backend()
    return backend.create_session()

def test_node(session):
    from wald.backend import Node
    node = Node(name='foobar', content='lorem ipsum dolor')
    session.add(node)
    session.commit()
