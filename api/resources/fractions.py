from flask import abort, request
from flask_restful import Resource
from sqlalchemy.orm.exc import NoResultFound

from api.common.utils import get_embedding, jsonify_sqlalchemy, validate_embed
from api.models import Fraction, get_all, get_one


class Fractions(Resource):
    def get(self, **kwargs):
        id_ = kwargs.get('id')
        embed = get_embedding(request.args.get('embed'))
        if not validate_embed(Fraction, embed):
            abort(404)
        # Explicitly check for None incase of 0 id_
        if id_ != None:
            try:
                res = get_one(Fraction, id_)
            except NoResultFound as e:
                abort(404, e)
            return jsonify_sqlalchemy(res, embed=embed)
        else:
            return jsonify_sqlalchemy(get_all(Fraction), embed=embed)

    def put(self, **kwargs):
        pass

    def post(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass
