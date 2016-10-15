from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Agency(Base):
    __tablename = 'agency_staging'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    info = Column(JSON)
