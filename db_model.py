from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, BigInteger
from sqlalchemy_utils import database_exists, create_database
from config import user, password, host, database


db_string = f'mysql://{user}:{password}@{host}:3306/{database}'
engine = create_engine(db_string)
Base = declarative_base()

class Continent(Base):
    __tablename__ = 'continents'
    id_continent = Column(Integer, primary_key=True)
    continent = Column(String(50))

class Country(Base):
    __tablename__ = 'countries'
    id_country = Column(Integer, primary_key=True)
    country = Column(String(50))
    id_continent = Column(Integer, ForeignKey('continents.id_continent'))

class Population(Base):
    __tablename__ = 'live_population'
    id_data = Column(Integer, primary_key=True)
    measurement = Column(BigInteger)
    date_measurement = Column(Date)
    id_country = Column(Integer, ForeignKey('countries.id_country'))

class Year(Base):
    __tablename__ = 'years'
    id_year = Column(Integer, primary_key=True)
    year = Column(Integer)

class Age(Base):
    __tablename__ = 'ages'
    id_age = Column(Integer, primary_key=True)
    age = Column(Integer)

class Death(Base):
    __tablename__ = 'deaths'
    id_data = Column(Integer, primary_key=True)
    measurement = Column(BigInteger)
    sex = Column(String(10))
    id_year = Column(Integer, ForeignKey('years.id_year'))
    id_country = Column(Integer, ForeignKey('countries.id_country'))
    id_age = Column(Integer, ForeignKey('ages.id_age'))

class Birth(Base):
    __tablename__ = 'births'
    id_data = Column(Integer, primary_key=True)
    measurement = Column(BigInteger)
    id_year = Column(Integer, ForeignKey('years.id_year'))
    id_country = Column(Integer, ForeignKey('countries.id_country'))
    id_mother_age = Column(Integer, ForeignKey('ages.id_age'))

class Marriage(Base):
    __tablename__ = 'marriages'
    id_data = Column(Integer, primary_key=True)
    measurement = Column(BigInteger)
    id_year = Column(Integer, ForeignKey('years.id_year'))
    id_age = Column(Integer, ForeignKey('ages.id_age'))
    id_country = Column(Integer, ForeignKey('countries.id_country'))

class CountryData(Base):
    __tablename__ = 'country_data'
    id_data = Column(Integer, primary_key=True)
    id_population = Column(Integer, ForeignKey('live_population.id_data'))
    id_deaths = Column(Integer, ForeignKey('deaths.id_data'))
    id_births = Column(Integer, ForeignKey('births.id_data'))
    id_marriages = Column(Integer, ForeignKey('marriages.id_data'))


if not database_exists(engine.url):
    create_database(engine.url)
else:
    # Connect the database if exists.
    engine.connect()
    Base.metadata.create_all(engine)
