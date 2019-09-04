from flask import abort, request
from flask_restful import Resource, reqparse
from sqlalchemy.orm.exc import NoResultFound

from api.common.exc import ValidationException
# from api.common.utils import (get_relationships, jsonify_sqlalchemy,
#                               get_embedding)
from api.common.utils import get_embedding, jsonify_sqlalchemy, validate_embed
from api.models import Sample, get_all, get_one

# First attempt at getting relationships
# Should be easier to try and get a queried relationsip
# and handle the AttributeError exception
# relationships = get_relationships(Sample)


class Samples(Resource):
    
    def get(self, **kwargs):
        id_ = kwargs.get('id')
        # example of how to get collection endpoint info
        # collection = kwargs.get('collection')
        # collection_id = kwargs.get('coll_id')
        embed = get_embedding(request.args.get('embed'))
        if not validate_embed(Sample, embed):
            abort(404)
        if id_:
            try:
                res = get_one(Sample, id_)
            except NoResultFound as e:
                abort(404, e)
            return jsonify_sqlalchemy(res, embed=embed)
        else:
            return jsonify_sqlalchemy(get_all(Sample), embed=embed)

    def put(self, **kwargs):
        pass

    def post(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass
