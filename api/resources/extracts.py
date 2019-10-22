from flask import abort, request
from flask_restful import Resource
from sqlalchemy.orm.exc import NoResultFound

from api.auth import check_auth
from api.common.utils import (filter_empty_strings, get_embedding,
                              jsonify_sqlalchemy, validate_embed,
                              validate_input)
from api.db import add_one, get_all, get_one, search_query
from api.models import Extract


class Extracts(Resource):
    decorators = [check_auth]

    def get(self, **kwargs):
        id_ = kwargs.get('id')
        args = request.args
        embed = get_embedding(args.get('embed'))
        if not validate_embed(Extract, embed):
            abort(404)
        # Search query parameters only valid when no id_
        query_params = {}
        query_params['library_abbrev'] = args.get('library_abbrev')
        query_params['number'] = args.get('number')
        # TODO: validate query parameters
        # Explicitly check for None incase of 0 id_
        if id_ != None:
            try:
                res = get_one(Extract, id_)
            except NoResultFound as e:
                abort(404, e)
            return jsonify_sqlalchemy(res, embed)
        else:
            if any(query_params.values()):
                return jsonify_sqlalchemy(search_query(Extract, query_params), embed)
            return jsonify_sqlalchemy(get_all(Extract), embed)

    def put(self, **kwargs):
        return {"message": "Method not implemented"}, 501

    def post(self, **kwargs):
        if any(kwargs):
            abort(404)
        data = request.get_json()
        if not data:
            abort(400, "No input provided")
        data = filter_empty_strings(data)
        if not validate_input(Extract, data):
            abort(400, "Invalid JSON input")
        id_ = add_one(Extract, data)
        return {"success": True, "link": f"/api/v1/extracts/{id_}", "id": id_}, 201

    def delete(self, **kwargs):
        return {"message": "Method not implemented"}, 501
