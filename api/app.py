from flask import Flask
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from api.db import init_db
from api.config import app_config
from api.resources import (Divers, DiveSites, Heartbeat, Libraries, Permits,
                           Samples, SampleTypes, ScreenPlates)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    api = Api(app)
    init_db(app)

    # Simple collections + resources
    api.add_resource(Heartbeat, '/')
    api.add_resource(Divers, '/divers', '/divers/<int:id>')
    api.add_resource(DiveSites, '/divesites', '/divesites/<int:id>')
    api.add_resource(Libraries, '/libraries', '/libraries/<int:id>')
    api.add_resource(Permits, '/permits', '/permits/<int:id>')
    api.add_resource(Samples, '/samples', '/samples/<int:id>',
        '/samples/<int:id>/<string:collection>/',
        '/samples/<int:id>/<string:collection>/<int:coll_id>',
    )
    api.add_resource(SampleTypes, '/sampletypes', '/sampletypes/<int:id>')
    api.add_resource(ScreenPlates, '/screenplates', '/screenplates/<int:id>')

    return app
