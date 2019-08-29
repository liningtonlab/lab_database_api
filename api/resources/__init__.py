from flask import jsonify
from flask_restful import Resource
from api.resources.divers import Divers
from api.resources.divesites import DiveSites
from api.resources.libraries import Libraries
from api.resources.permits import Permits
from api.resources.samples import Samples
from api.resources.sampletypes import SampleTypes
from api.resources.screenplates import ScreenPlates

class Heartbeat(Resource):
    def get(self):
        return jsonify({})