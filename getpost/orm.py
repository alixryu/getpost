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
        result = {}
        for column in columns:
            if hasattr(self, column):
                result[column] = getattr(self, column)
        return result
        # return {column: getattr(self, column) for column in columns}

class ManagedSession:
    def __init__(self, session_maker):
        self.session = session_maker()

    def __enter__(self):
        return self.session

    def __exit__(self, etype, evalue, etrace):
        success = all(arg is None for arg in (etype, evalue, etrace))
        if success:
            self.session.commit()
        else:
            self.session.rollback()
        return success

Base = declarative_base(cls=DictBase)

engine = create_engine(config.DB_URI)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
