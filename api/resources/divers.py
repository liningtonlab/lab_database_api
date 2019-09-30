from flask import abort, request
from flask_restful import Resource
from sqlalchemy.orm.exc import NoResultFound

from api.auth import check_auth
from api.common.utils import (get_embedding, jsonify_sqlalchemy,
                              validate_embed, validate_input)
from api.db import add_one, get_all, get_one, search_query
from api.models import Diver


class Divers(Resource):
    decorators = [check_auth]

    def get(self, **kwargs):
        id_ = kwargs.get('id')
        args = request.args
        embed = get_embedding(args.get('embed'))
        if not validate_embed(Diver, embed):
            abort(404)
        # Search query parameters only valid when no id_
        query_params = {}
        query_params['first_name'] = args.get('first_name')
        query_params['last_name'] = args.get('last_name')
        query_params['institution'] = args.get('institution')
        # TODO: validate query parameters
        # Explicitly check for None incase of 0 id_
        if id_ != None:
            try:
                res = get_one(Diver, id_)
            except NoResultFound as e:
                abort(404, e)
            return jsonify_sqlalchemy(res, embed=embed)
        else:
            if any(query_params.values()):
                return jsonify_sqlalchemy(search_query(Diver, query_params), embed)
            return jsonify_sqlalchemy(get_all(Diver), embed=embed)

    def put(self, **kwargs):
        return {"message": "Method not implemented"}, 501

    def post(self, **kwargs):
        if any(kwargs):
            abort(404)
        data = request.get_json()
        if not data:
            abort(400, "No input provided")
        if not validate_input(Diver, data):
            abort(400, "Invalid JSON input")
        id_ = add_one(Diver, data)
        return {"success": True, "link": f"/api/v1/divers/{id_}"}, 201

    def delete(self, **kwargs):
        return {"message": "Method not implemented"}, 501
