from flask_restful import abort
from flask import request
from data import db_session
from data.api_key import ApiKey


def check_api_key():
    api_key = request.headers.get('X-API-Key')

    if not api_key:
        abort(401, message='API key required')

    with db_session.create_session() as db_sess:
        key_obj = db_sess.query(ApiKey).filter(
            ApiKey.key == api_key,
            ApiKey.is_active == True
        ).first()

        if not key_obj:
            abort(401, message='Invalid API key')

        return key_obj


def check_admin_key():
    key_obj = check_api_key()

    if not key_obj.name.lower().startswith('admin'):
        abort(403, message='Admin privileges required')

    return key_obj
