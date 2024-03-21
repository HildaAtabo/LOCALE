from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import sessionmaker
#from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:251426@localhost:5432/LocaleAppDatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = sqlalchemy.orm.declarative_base()
