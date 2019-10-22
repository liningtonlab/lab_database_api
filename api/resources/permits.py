import os

from flask import abort, current_app, request, send_file
from flask_restful import Resource
from sqlalchemy.orm.exc import NoResultFound

from api.auth import check_auth
from api.common.utils import (allowed_file, filter_empty_strings,
                              get_embedding, jsonify_sqlalchemy,
                              validate_embed, validate_input)
from api.db import add_one, get_all, get_one, search_query
from api.models import Permit
from werkzeug.utils import secure_filename

class Permits(Resource):
    decorators = [check_auth]

    def get(self, **kwargs):
        id_ = kwargs.get('id')
        args = request.args
        embed = get_embedding(args.get('embed'))
        if not validate_embed(Permit, embed):
            abort(404)
        # Search query parameters only valid when no id_
        query_params = {}
        query_params['name'] = args.get('name')
        query_params['iss_auth'] = args.get('iss_auth')
        # TODO: validate query parameters
        # Explicitly check for None incase of 0 id_
        if id_ != None:
            try:
                res = get_one(Permit, id_)
            except NoResultFound as e:
                abort(404, e)
            return jsonify_sqlalchemy(res, embed=embed)
        else:
            if any(query_params.values()):
                return jsonify_sqlalchemy(search_query(Permit, query_params), embed)
            return jsonify_sqlalchemy(get_all(Permit), embed=embed)

    def put(self, **kwargs):
        return {"message": "Method not implemented"}, 501

    def post(self, **kwargs):
        if any(kwargs):
            abort(404)
        data = request.get_json()
        if not data:
            abort(400, "No input provided")
        data = filter_empty_strings(data)
        if not validate_input(Permit, data):
            abort(400, "Invalid JSON input")
        id_ = add_one(Permit, data)
        return {"success": True, "link": f"/api/v1/permits/{id_}", "id": id_}, 201

    def delete(self, **kwargs):
        return {"message": "Method not implemented"}, 501


class PermitsFile(Resource):
    
    def get(self, **kwargs):
        id_ = kwargs.get('id')
        if not id_:
            abort(404)
        try:
            res = get_one(Permit, id_)
        except NoResultFound as e:
            abort(404, e)
        if not res.file_dir or not res.file_name:
            abort(404)
        UPLOAD_DIR =  os.getenv("UPLOAD_DIR", os.path.join(current_app.root_path, "uploads"))       
        file_path = os.path.join(UPLOAD_DIR, "permits", res.file_dir, res.file_name)
        if not os.path.exists(file_path):
            abort(404)
        try:
            return send_file(file_path, attachment_filename=res.file_name)
        except Exception as e:
            return {"success": False, "error": str(e)}

    def post(self, **kwargs):
        # Make sure permit is in DB already
        id_ = kwargs.get('id')
        if 'file' not in request.files:
            abort(404)
        if not id_:
            abort(404)
        try:
            res = get_one(Permit, id_)
        except NoResultFound as e:
            abort(404, e)
        UPLOAD_DIR =  os.getenv("UPLOAD_DIR", os.path.join(current_app.root_path, "uploads"))
        file_dir = os.path.join(UPLOAD_DIR, "permits", res.file_dir)
        file_path = os.path.join(file_dir, res.file_name)
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
        file_ = request.files['file']
        if file_.filename == '':
            abort(404)
        if os.path.exists(file_path):
            abort(409)
        if file_ and allowed_file(file_.filename):
            file_.save(file_path)
        return {"success": True, "id": id_}, 200