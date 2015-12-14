""":mod:`getpost.orm` --- object relational mapper module of getpost
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from .config import DevConfig as config


class ReprBase(object):
    def __repr__(self):
        return '%s(%s)' % (
            self.__class__.__name__,
            ', '.join(['%s=%r' % (key, getattr(self, key))
                       for key in sorted(self.__dict__.keys())
                       if not key.startswith('_')]
            )
        )

class DictBase(ReprBase):
    def as_dict(self, columns=None):
        if columns is None:
            columns = {column.name for column in self.__table__.columns}
        return {column: getattr(self, column) for column in columns}


Base = declarative_base(cls=DictBase)

engine = create_engine(config.DB_URI)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
