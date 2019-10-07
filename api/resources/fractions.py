from flask import abort, request
from flask_restful import Resource
from sqlalchemy.orm.exc import NoResultFound

from api.auth import check_auth
from api.common.utils import (filter_empty_strings, get_embedding,
                              jsonify_sqlalchemy, validate_embed,
                              validate_input)
from api.db import add_one, get_all, get_one, get_fraction_by_name
from api.models import Fraction


class Fractions(Resource):
    decorators = [check_auth]

    def get(self, **kwargs):
        id_ = kwargs.get('id')
        args = request.args
        embed = get_embedding(args.get('embed'))
        if not validate_embed(Fraction, embed):
            abort(404)
        # Search query parameters only valid when no id_
        query_params = {}
        query_params['name'] = args.get('name')
        # Explicitly check for None incase of 0 id_
        if id_ != None:
            try:
                res = get_one(Fraction, id_)
            except NoResultFound as e:
                abort(404, e)
            return jsonify_sqlalchemy(res, embed=embed)
        else:
            # Keep form same as other methds
            # Use custom query that results one result or None
            # Make into list for consistency
            if any(query_params.values()):
                return jsonify_sqlalchemy([get_fraction_by_name(query_params['name'])], embed=embed)
            return jsonify_sqlalchemy(get_all(Fraction), embed=embed)

    def put(self, **kwargs):
        return {"message": "Method not implemented"}, 501

    def post(self, **kwargs):
        # Fractions require extract
        if any(kwargs):
            abort(404)
        data = request.get_json()
        if not data:
            abort(400, "No input provided")
        data = filter_empty_strings(data)
        if not validate_input(Fraction, data):
            abort(400, "Invalid JSON input")
        id_ = add_one(Fraction, data)
        return {"success": True, "link": f"/api/v1/fractions/{id_}"}, 201

    def delete(self, **kwargs):
        return {"message": "Method not implemented"}, 501
