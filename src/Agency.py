# The Agency class represents a policing agency

from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base

# Use SQL Alchemy's declarative base functionality
# to facilitate storing agency info the database
Base = declarative_base()


class Agency(Base):
    """
    Class to represent an agency
    Because the fields will vary across sources,
    store info in a JSON column to allow variable schema
    """
    __tablename__ = 'agency_staging'
    id = Column(Integer, primary_key=True)
    info = Column(JSON)
