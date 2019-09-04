from api.common.sql_models import (Diver, DiveSite, Extract, Fraction,
                                   FractionScreenPlate, Isolate, IsolateStock,
                                   Library, Media, MediaRecipe, Permit, Sample,
                                   SampleType, ScreenPlate)
from api.db import Session

from contextlib import contextmanager

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def get_one(cls, id_, sess=Session):
    return sess.query(cls).filter_by(id=id_).one()

def get_all(cls, sess=Session):
    return sess.query(cls).all()
