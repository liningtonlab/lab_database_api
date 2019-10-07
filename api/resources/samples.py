from flask import abort, request
from flask_restful import Resource, reqparse
from sqlalchemy.orm.exc import NoResultFound

# from api.common.exc import ValidationException
# from api.common.utils import (get_relationships, jsonify_sqlalchemy,
#                               get_embedding)
from api.auth import check_auth, get_user_id
from api.common.utils import (filter_empty_strings, get_embedding,
                              jsonify_sqlalchemy, validate_embed,
                              validate_sample_input)
from api.db import add_one_sample, get_all, get_one, search_query
from api.models import Sample

# First attempt at getting relationships
# Should be easier to try and get a queried relationsip
# and handle the AttributeError exception
# relationships = get_relationships(Sample)


class Samples(Resource):
    decorators = [check_auth]
    
    def get(self, **kwargs):
        id_ = kwargs.get('id')
        # example of how to get collection endpoint info
        # collection = kwargs.get('collection')
        # collection_id = kwargs.get('coll_id')
        args = request.args
        embed = get_embedding(args.get('embed'))
        # return args
        if not validate_embed(Sample, embed):
            abort(404)
        # Search query parameters only valid when no id_
        query_params = {}
        query_params['name'] = args.get('name')
        # Explicitly check for None incase of 0 id_
        if id_ != None:
            try:
                res = get_one(Sample, id_)
            except NoResultFound as e:
                abort(404, e)
            return jsonify_sqlalchemy(res, embed=embed)
        else:
            if any(query_params.values()):
                return jsonify_sqlalchemy(search_query(Sample, query_params), embed)
            return jsonify_sqlalchemy(get_all(Sample), embed=embed)

    def put(self, **kwargs):
        return {"message": "Method not implemented"}, 501

    def post(self, **kwargs):
        if any(kwargs):
            abort(404)
        data = request.get_json()
        if not data:
            abort(400, "No input provided")
        data['insert_by'] = get_user_id(request)
        data = filter_empty_strings(data)
        if not validate_sample_input(data):
            abort(400, "Invalid JSON input")
        id_ = add_one_sample(data)
        return {"success": True, "link": f"/api/v1/samples/{id_}"}, 201

    def delete(self, **kwargs):
        return {"message": "Method not implemented"}, 501
