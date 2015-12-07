""":mod:`getpost.create` --- script for creating model tables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from models import Base
from orm import engine

Base.metadata.create_all(engine)
