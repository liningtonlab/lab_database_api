from flask import abort, request
from flask_restful import Resource
from sqlalchemy.orm.exc import NoResultFound

from api.auth import check_auth
from api.common.utils import (get_embedding, jsonify_sqlalchemy,
                              validate_embed, validate_input)
from api.db import add_one, get_all, get_one
from api.models import Library


class Libraries(Resource):
    decorators = [check_auth]

    def get(self, **kwargs):
        id_ = kwargs.get('id')
        embed = get_embedding(request.args.get('embed'))
        if not validate_embed(Library, embed):
            abort(404)
        # No need for search query here
        # Explicitly check for None incase of 0 id_
        if id_ != None:
            try:
                res = get_one(Library, id_)
            except NoResultFound as e:
                abort(404, e)
            return jsonify_sqlalchemy(res, embed=embed)
        else:
            return jsonify_sqlalchemy(get_all(Library), embed=embed)

    def put(self, **kwargs):
        return {"message": "Method not implemented"}, 501

    def post(self, **kwargs):
        if any(kwargs):
            abort(404)
        data = request.get_json()
        if not data:
            abort(400, "No input provided")
        if not validate_input(Library, data):
            abort(400, "Invalid JSON input")
        id_ = add_one(Library, data)
        return {"success": True, "link": f"/api/v1/libraries/{id_}"}, 201

    def delete(self, **kwargs):
        return {"message": "Method not implemented"}, 501
