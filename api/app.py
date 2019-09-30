from flask import Flask
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from api.config import app_config
from api.db import init_db
from api.resources import (Divers, DiveSites, Extracts, Fractions, Heartbeat,
                           Isolates, Libraries, MediaEP, Permits, Samples,
                           SampleTypes, ScreenPlates, Summary)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    api = Api(app)
    init_db(app)
    
    # TODO: Implement collections

    # Simple collections + resources
    api.add_resource(Summary, '/api/v1/')
    api.add_resource(Heartbeat, '/api/v1/heartbeat')
    api.add_resource(Divers, '/api/v1/divers', '/api/v1/divers/<string:id>')
    api.add_resource(DiveSites, '/api/v1/divesites', '/api/v1/divesites/<string:id>')
    api.add_resource(Extracts, '/api/v1/extracts', '/api/v1/extracts/<string:id>')
    api.add_resource(Fractions, '/api/v1/fractions', '/api/v1/fractions/<string:id>')
    api.add_resource(Isolates, '/api/v1/isolates', '/api/v1/isolates/<string:id>')
    api.add_resource(Libraries, '/api/v1/libraries', '/api/v1/libraries/<string:id>')
    api.add_resource(MediaEP, '/api/v1/media', '/api/v1/media/<string:id>')
    api.add_resource(Permits, '/api/v1/permits', '/api/v1/permits/<string:id>')
    api.add_resource(Samples, '/api/v1/samples', '/api/v1/samples/<string:id>',
        # Example collection endpoints
        # '/api/v1/samples/<int:id>/<string:collection>/',
        # '/api/v1/samples/<int:id>/<string:collection>/<int:coll_id>',
    )
    api.add_resource(SampleTypes, '/api/v1/sampletypes', '/api/v1/sampletypes/<string:id>')
    api.add_resource(ScreenPlates, '/api/v1/screenplates', '/api/v1/screenplates/<string:id>')

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    @app.errorhandler(400)
    def bad_request(e):
        return {"message":str(e)}, 400

    @app.errorhandler(404)
    def resource_not_found(e):
        return {"message":str(e)}, 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return {"message":str(e)}, 500

    return app
