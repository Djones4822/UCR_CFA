from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Agency(Base):
    __tablename__ = 'agency_staging'
    id = Column(Integer, primary_key=True)
    info = Column(JSON)
