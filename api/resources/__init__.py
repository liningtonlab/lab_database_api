from flask import jsonify
from flask_restful import Resource
from api.resources.divers import Divers
from api.resources.divesites import DiveSites
from api.resources.extracts import Extracts
from api.resources.fractions import Fractions
from api.resources.fractionscreenplates import FractionScreenPlates
from api.resources.isolates import Isolates
from api.resources.libraries import Libraries
from api.resources.media import MediaEP
from api.resources.permits import Permits
from api.resources.samples import Samples
from api.resources.sampletypes import SampleTypes
from api.resources.screenplates import ScreenPlates

class Heartbeat(Resource):
    def get(self):
        return jsonify({})