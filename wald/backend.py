from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

_Base = declarative_base()

class Node(_Base):
    __tablename__ = 'nodes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    content = Column(String)

class Backend(object):
    def __init__(self, url=None):
        self._url = url or 'sqlite:///:memory:'
        self._engine = create_engine(self._url, echo=True)
        _Base.metadata.create_all(self._engine)

    def create_session(self):
        Session = sessionmaker()
        Session.configure(bind=self._engine)
        return Session()
