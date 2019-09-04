from flask import Flask
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from api.config import app_config
from api.db import init_db
from api.resources import (Divers, DiveSites, Extracts, Fractions,
                           FractionScreenPlates, Heartbeat, Isolates,
                           Libraries, MediaEP, Permits, Samples, SampleTypes,
                           ScreenPlates)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    api = Api(app)
    init_db(app)
    
    # TODO: Implement collections

    # Simple collections + resources
    api.add_resource(Heartbeat, '/api/v1/')
    api.add_resource(Divers, '/api/v1/divers', '/api/v1/divers/<int:id>')
    api.add_resource(DiveSites, '/api/v1/divesites', '/api/v1/divesites/<int:id>')
    api.add_resource(Extracts, '/api/v1/extracts', '/api/v1/extracts/<int:id>')
    api.add_resource(Fractions, '/api/v1/fractions', '/api/v1/fractions/<int:id>')
    api.add_resource(FractionScreenPlates, '/fractionscreenplates',
                     '/api/v1/fractionscreenplates/<int:id>')
    api.add_resource(Isolates, '/api/v1/isolates', '/api/v1/isolates/<int:id>')
    api.add_resource(Libraries, '/api/v1/libraries', '/api/v1/libraries/<int:id>')
    api.add_resource(MediaEP, '/api/v1/media', '/api/v1/media/<int:id>')
    api.add_resource(Permits, '/api/v1/permits', '/api/v1/permits/<int:id>')
    api.add_resource(Samples, '/api/v1/samples', '/api/v1/samples/<int:id>',
        # Example collection endpoints
        # '/api/v1/samples/<int:id>/<string:collection>/',
        # '/api/v1/samples/<int:id>/<string:collection>/<int:coll_id>',
    )
    api.add_resource(SampleTypes, '/api/v1/sampletypes', '/api/v1/sampletypes/<int:id>')
    api.add_resource(ScreenPlates, '/api/v1/screenplates', '/api/v1/screenplates/<int:id>')

    return app
