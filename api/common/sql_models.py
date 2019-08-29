#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ORM Mapping of Linington Lab Database
"""
from sqlalchemy import (Boolean, Column, Date, DateTime, Float, ForeignKey,
                        Integer, String, Table, create_engine, func)
# from sqlalchemy.dialects.mysql import DOUBLE, ENUM
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref, relationship, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.types import Text

Base = declarative_base()

# # Patch relationship to ignore typechecking...
# def my_relationship(*args, **kwargs):
#     return relationship(*args, **kwargs, enable_typechecks=False)

# Many-to-many Relation Tables
# Sample >-Sample_Diver-< Diver
sample_diver = Table(
    "sample_diver", Base.metadata,
    Column("sample_id", Integer, ForeignKey("sample.id"), primary_key=True),
    Column("diver_id", Integer, ForeignKey("diver.id"), primary_key=True)
)


# Sample Table ORM
class Sample(Base):
    __tablename__ = "sample"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    collection_number = Column(Integer, nullable=False)
    collection_year = Column(Integer, nullable=False)
    collection_date = Column(Date)
    color = Column(String(45))
    depth_ft = Column(Float)
    genus_species = Column(String(255))
    notes = Column(Text)
    insert_by = Column(Integer)
    insert_date = Column(DateTime)
    # ForeignKeys and relationships
    dive_site_id = Column(Integer, ForeignKey("dive_site.id"))
    dive_site = relationship("DiveSite", backref="samples")
    divers = relationship("Diver", secondary=sample_diver, backref="samples")
    sample_type_id = Column(Integer, ForeignKey("sample_type.id"))
    sample_type = relationship("SampleType")
    isolates = relationship("Isolate", backref="sample")
    permit_id = Column(Integer, ForeignKey("permit.id"))
    permit = relationship("Permit")


# Sample Type Table ORM
class SampleType(Base):
    __tablename__= "sample_type"
    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    description = Column(Text)
    notes = Column(Text)


# Dive site Table ORM
class DiveSite(Base):
    __tablename__ = "dive_site"
    id = Column(Integer, primary_key=True)
    name = Column(String(75))
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    notes = Column(Text)


# Diver Table ORM
class Diver(Base):
    """This class represents the diver table.

    More accurately described as collector...
    
    """
    __tablename__ = "diver"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(45))
    last_name = Column(String(45))
    institution = Column(String(255))
    email = Column(String(255))
    notes = Column(Text)



# Permit Table ORM
class Permit(Base):
    __tablename__ = "permit"
    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    iss_auth = Column(String(75), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    notes = Column(Text)
    file_dir = Column(String(45))
    file_name = Column(String(45))


# Isolate Table ORM
class Isolate(Base):
    __tablename__ = "isolate"
    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False, unique=True)
    color = Column(String(10))
    morphology = Column(String(20))
    sequence = Column(Text)
    sequence_dir = Column(String(45))
    sequence_file = Column(String(45))
    notes = Column(Text)
    insert_by = Column(Integer)
    insert_date = Column(DateTime)
    # ForeignKeys and relationships
    media_id = Column(Integer, ForeignKey("media.id"))
    media = relationship("Media")
    sample_id = Column(Integer, ForeignKey("sample.id"))
    extract = relationship("Extract", backref="isolate")
    stock = relationship("IsolateStock",
                         backref=backref("isolate", uselist=False))


# Strain Stock Table ORM
class IsolateStock(Base):
    __tablename__ = "isolate_stock"
    id = Column(Integer, primary_key=True)
    box = Column(Integer)
    box_position = Column(Integer)
    num_in_stock = Column(Integer)
    date_added = Column(Date)
    freezethaw = Column(Integer, default=0)
    volume_ul = Column(Integer, default=1000)
    insert_by = Column(Integer)
    insert_date = Column(DateTime)
    # ForeignKeys and relationships
    isolate_id = Column(Integer, ForeignKey("isolate.id"))


# Extract Table ORM
class Extract(Base):
    __tablename__ = "extract"
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    temp = Column(Integer)
    rpm = Column(Float)
    inoculation_date = Column(Date)
    growth_time_h = Column(Integer)
    volume_ml = Column(Float)
    mass_g = Column(Float)
    seal = Column(String(45))
    percent_inoculum = Column(Float)
    spring = Column(Boolean)
    shaken = Column(Boolean)
    flask_type = Column(String(15))
    flask_capacity_l = Column(Float)
    resin_mass_g = Column(Float)
    notes = Column(Text)
    insert_by = Column(Integer)
    insert_date = Column(DateTime)
    # ForeignKeys and relationships
    isolate_id = Column(Integer, ForeignKey("isolate.id"))
    media_id = Column(Integer, ForeignKey("media.id"))
    media = relationship("Media")
    library_id = Column(Integer, ForeignKey("library.id"))
    library = relationship("Library", backref="extracts")
    fractions = relationship("Fraction", back_populates="extract")


# Fraction Table ORM
class Fraction(Base):
    __tablename__ = "fraction"
    id = Column(Integer, primary_key=True)
    extract_id = Column(Integer, ForeignKey("extract.id"))
    extract = relationship("Extract")
    code = Column(String(45))

    @hybrid_property
    def name(self):
        ex = self.extract
        return "RL{}-{:04d}{}".format(
            ex.library.abbrev,
            ex.number,
            self.code
        )


# Media Table ORM
class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    notes = Column(Text)
    recipe = relationship("MediaRecipe",
                          backref=backref("media", uselist=False))


# Media Recipe Table ORM
class MediaRecipe(Base):
    __tablename__ = "media_recipe"
    id = Column(Integer, primary_key=True)
    media_id = Column(Integer, ForeignKey("media.id"))
    ingredient = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    unit = Column(String(255), nullable=False)
    notes = Column(Text)


# Library Table ORM
class Library(Base):
    __tablename__ = "library"
    id = Column(Integer, primary_key=True)
    abbrev = Column(String(5), nullable=False)
    name = Column(String(45), nullable=False)
    description = Column(String(255))
    notes = Column(Text)


# Screening Plate ORM
class ScreenPlate(Base):
    __tablename__ = "screen_plate"
    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    notes = Column(Text)


# Fraction >-< Screening Plate ORM
class FractionScreenPlate(Base):
    __tablename__ = "fraction_screen_plate"
    fraction_id = Column(Integer, ForeignKey("fraction.id"),
                         primary_key=True)
    fraction = relationship("Fraction")
    screen_plate_id = Column(Integer, ForeignKey("screen_plate.id"),
                             primary_key=True)
    screen_plate = relationship("ScreenPlate")
    well = Column(String(45))
    notes = Column(Text)


# # Should be a singleton object for instantiating DB connection
# class LiningtonDB(object):

#     Base = Base

#     def __init__(self, user="jvansan", passwd="password", host="localhost",
#                  dbname="linington_lab", port=3306):
#         conn_string = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4"\
#             .format(user, passwd, host, port, dbname)
#         self.engine = create_engine(conn_string)
#         self.Base.metadata.bind = self.engine
#         self.Base.metadata.create_all()

#     def start_session(self, autocommit=False, autoflush=True):
#         Session = sessionmaker(bind=self.engine, autocommit=autocommit, autoflush=autoflush)
#         return Session()

#     def get_fraction_by_name(self, sess, fraction_name):
#         lib_abbrev = fraction_name.split('-')[0].replace('RL', '')
#         extract_num = fraction_name.split('-')[-1][:4]
#         prefac_code = fraction_name[-1]
#         return sess.query(Fraction).filter(Fraction.code == prefac_code)\
#                     .join(Extract).filter(Extract.number == extract_num)\
#                     .join(Library).filter(Library.abbrev == lib_abbrev)\
#                     .first()
