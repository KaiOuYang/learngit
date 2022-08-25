

from sqlalchemy import Column,String,Integer,Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):

    __tablename__ = 'user'

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(Text)
    nation = Column(Text)
    uid = Column(Text)