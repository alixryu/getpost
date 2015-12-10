""":script:`getpost.create` --- script for creating model tables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from getpost.models import Base
from getpost.orm import engine

Base.metadata.create_all(engine)
