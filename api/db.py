from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from api.common.sql_models import Base

Session = scoped_session(sessionmaker())

def init_db(app=current_app):
    app.engine = create_engine(app.config.get('SQLALCHEMY_DATABASE_URI'))
    
    Session.configure(bind=app.engine)
    Base.metadata.create_all(bind=app.engine)

    def teardown_session(exception=None):
        Session.remove()

    app.teardown_request(teardown_session)
