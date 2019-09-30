from contextlib import contextmanager

from flask import abort, current_app
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session, sessionmaker

from api.common.sql_models import Base
from api.models import (Diver, Extract, Fraction, Library, Media, MediaRecipe,
                        Sample)

Session = scoped_session(sessionmaker(autoflush=True, autocommit=False))

def init_db(app=current_app):
    app.engine = create_engine(app.config.get('SQLALCHEMY_DATABASE_URI'), pool_size=8, pool_pre_ping=True)
    
    Session.configure(bind=app.engine)
    Base.metadata.create_all(bind=app.engine)

    def teardown_session(exception=None):
        Session.remove()

    app.teardown_request(teardown_session)


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


def add_one(cls, data):
    # create data access object
    dao = cls(**data)
    try:
        # add object to session
        with session_scope() as sess:
            sess.add(dao)
            # Need to flush to get id_
            sess.flush()
            id_ = dao.id
        return id_
    # Need to figure out what exceptions to catch
    except IntegrityError as e:
        print(e)
        abort(409, "SQL Integrity Error - possible duplicate or missing field")


def add_one_sample(data):
    """Build sample and associate divers if provided
    """
    diver_ids = data.pop('diver_ids', [])
    try:
        with session_scope() as sess:
            divers = sess.query(Diver).filter(Diver.id.in_(diver_ids)).all()
            sample = Sample(**data)
            sample.divers = divers
            # Get divers
            sess.add(sample)
            # Need to flush to get id_
            sess.flush()
            id_ = sample.id
        return id_
    # Need to figure out what exceptions to catch
    except IntegrityError as e:
        print(e)
        abort(409, "SQL Integrity Error - possible duplicate or missing field")


def add_media_with_recipe(data):
    """Build media with recipe and add to DB
    
    Take with two fields:
    1) media data dict
    2) media recipe list of mediarecipe data dicts

    Args:
        data (dict): {"media": {DATA}, "recipe": [{DATA},...]}
    """
    media = Media(**data['media'])
    for r in data['recipe']:
        media.recipe.append(MediaRecipe(**r))
    try:
        # add object to session
        with session_scope() as sess:
            sess.add(media)
            # Need to flush to get id_
            sess.flush()
            id_ = media.id
        return id_
    # Need to figure out what exceptions to catch
    except IntegrityError as e:
        print(e)
        abort(409, "SQL Integrity Error - possible duplicate or missing field")
    

def get_one(cls, id_, sess=Session):
    return sess.query(cls).filter_by(id=id_).one()


def get_all(cls, sess=Session):
    return sess.query(cls).all()


def search_query(cls, query_parameters, sess=Session):
    # Filter empty query parameters
    query = dict(filter(lambda x: x[1]!=None, query_parameters.items()))
    # unpack query parameters as kwargs
    return sess.query(cls).filter_by(**query).all()


def get_fraction_by_name(fraction_name, sess=Session):
    lib_abbrev = fraction_name.split('-')[0].replace('RL', '')
    extract_num = fraction_name.split('-')[-1][:4]
    prefac_code = fraction_name[-1]
    return sess.query(Fraction).filter(Fraction.code == prefac_code)\
                .join(Extract).filter(Extract.number == extract_num)\
                .join(Library).filter(Library.abbrev == lib_abbrev)\
                .first()
