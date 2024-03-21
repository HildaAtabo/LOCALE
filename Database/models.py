from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Developers(Base):
    __tablename__ = 'developers' #This is the name of the table in the database

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    api_key = Column(String(50), nullable=False)

class Nigeria(Base):
    __tablename__ = 'nigeria' #This is the name of the table in the database

    id = Column(Integer, primary_key=True, index=True)
    region =  Column(String(50), nullable=False)
    state =  Column(String(50), nullable=False)
    
    


class Regions(Base):
    __tablename__ = 'regions' #This is the name of the table in the database

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    state =  Column(String(50), nullable=False)
   
class States(Base):
    __tablename__= 'states' #This is the name of the table in the database
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    lga = Column(String(50), nullable=False)
    