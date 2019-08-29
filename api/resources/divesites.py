from flask import abort
from sqlalchemy.orm.exc import NoResultFound

from api.common.utils import jsonify_sqlalchemy
from api.models import get_one, get_all, DiveSite
from flask_restful import Resource


class DiveSites(Resource):
    def get(self, **kwargs):
        id_ = kwargs.get('id')
        try:
            if id_:
                return jsonify_sqlalchemy(get_one(DiveSite, id_))
        except NoResultFound:
            abort(404)
        return jsonify_sqlalchemy(get_all(DiveSite))

    def put(self, **kwargs):
        pass

    def post(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass