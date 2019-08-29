from api.common.sql_models import (Diver, DiveSite, Extract, Fraction,
                                   FractionScreenPlate, Isolate, IsolateStock,
                                   Library, Media, MediaRecipe, Permit, Sample,
                                   SampleType, ScreenPlate)
from api.db import Session


"""Define Data Object Access classes for accessing more easily within Flask
without injecting depency of Flask-SQLAlchemy into model definitions"""

def get_one(cls, id_):
    return Session.query(cls).filter_by(id=id_).one()

def get_all(cls):
    return Session.query(cls).all()
