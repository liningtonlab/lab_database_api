from flask import abort, request
from flask_restful import Resource
from sqlalchemy.orm.exc import NoResultFound

from api.auth import check_auth
from api.common.utils import (filter_empty_strings, get_embedding,
                              jsonify_sqlalchemy, validate_embed,
                              validate_input)
from api.db import get_all, get_one, search_query
from api.models import ScreenPlate


class ScreenPlates(Resource):
    decorators = [check_auth]

    def get(self, **kwargs):
        id_ = kwargs.get('id')
        embed = get_embedding(request.args.get('embed'))
        if not validate_embed(ScreenPlate, embed):
            abort(404)
        # Explicitly check for None incase of 0 id_
        if id_ != None:
            try:
                res = get_one(ScreenPlate, id_)
            except NoResultFound as e:
                abort(404, e)
            return jsonify_sqlalchemy(res, embed=embed)
        else:
            return jsonify_sqlalchemy(get_all(ScreenPlate), embed=embed)

    def put(self, **kwargs):
        return {"message": "Method not implemented"}, 501

    def post(self, **kwargs):
        return {"message": "Method not implemented"}, 501

    def delete(self, **kwargs):
        return {"message": "Method not implemented"}, 501
