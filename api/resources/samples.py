from flask import abort, request
from flask_restful import Resource, reqparse
from sqlalchemy.orm.exc import NoResultFound

from api.common.exc import ValidationException
from api.common.utils import (get_relationships, jsonify_sqlalchemy,
                              validate_embedding)
from api.models import get_one, get_all, Sample

relationships = get_relationships(Sample)


class Samples(Resource):
    def get(self, **kwargs):
        id_ = kwargs.get('id')
        collection = kwargs.get('collection')
        collection_id = kwargs.get('coll_id')
        if id_:
            try:
                sample = get_one(Sample, id_)
            except NoResultFound:
                abort(404)
            if collection in relationships:
                pass
                # result = 
            else:
                try:
                    embed = validate_embedding(request.args.get('embed'), relationships, '/samples')
                except ValidationException as e:
                    abort(404, e)
                return jsonify_sqlalchemy(sample, embed=embed)
        else:
            return jsonify_sqlalchemy(get_all(Sample))

    def put(self, **kwargs):
        pass

    def post(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass
