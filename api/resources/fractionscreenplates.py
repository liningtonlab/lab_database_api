from flask import abort, request
from flask_restful import Resource
from sqlalchemy.orm.exc import NoResultFound

from api.common.utils import get_embedding, jsonify_sqlalchemy, validate_embed
from api.models import FractionScreenPlate, get_all, get_one


class FractionScreenPlates(Resource):
    def get(self, **kwargs):
        id_ = kwargs.get('id')
        embed = get_embedding(request.args.get('embed'))
        if not validate_embed(FractionScreenPlate, embed):
            abort(404)
        if id_:
            try:
                res = get_one(FractionScreenPlate, id_)
            except NoResultFound as e:
                abort(404, e)
            return jsonify_sqlalchemy(res, embed=embed)
        else:
            return jsonify_sqlalchemy(get_all(FractionScreenPlate), embed=embed)

    def put(self, **kwargs):
        pass

    def post(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass
