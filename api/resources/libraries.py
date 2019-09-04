from flask import abort, request
from flask_restful import Resource
from sqlalchemy.orm.exc import NoResultFound

from api.common.utils import get_embedding, jsonify_sqlalchemy, validate_embed
from api.models import Library, get_all, get_one


class Libraries(Resource):
    def get(self, **kwargs):
        id_ = kwargs.get('id')
        embed = get_embedding(request.args.get('embed'))
        if not validate_embed(Library, embed):
            abort(404)
        if id_:
            try:
                res = get_one(Library, id_)
            except NoResultFound as e:
                abort(404, e)
            return jsonify_sqlalchemy(res, embed=embed)
        else:
            return jsonify_sqlalchemy(get_all(Library), embed=embed)

    def put(self, **kwargs):
        pass

    def post(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass
