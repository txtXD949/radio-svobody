from flask_restful import abort, Resource
from flask import jsonify
from data import db_session
from data.api_key import ApiKey
from .api_key_parser import api_key_parser
from .auth import check_admin_key


class ApiKeyResource(Resource):
    def post(self):
        check_admin_key()
        args = api_key_parser.parse_args()

        with db_session.create_session() as db_sess:
            api_key = ApiKey(
                key=ApiKey.generate_key(),
                name=args['name']
            )
            db_sess.add(api_key)
            db_sess.commit()

            return jsonify({
                'api_key': api_key.key,
                'name': api_key.name,
                'message': 'API key created'
            }), 201

    def get(self):
        check_admin_key()

        with db_session.create_session() as db_sess:
            keys = db_sess.query(ApiKey).all()

            return jsonify({
                'api_keys': [{
                    'id': k.id,
                    'name': k.name,
                    'created_at': str(k.created_at),
                    'is_active': k.is_active
                } for k in keys]
            })

class ApiKeyDetailResource(Resource):
    def delete(self, key_id):
        check_admin_key()

        with db_session.create_session() as db_sess:
            key = db_sess.query(ApiKey).get(key_id)
            if not key:
                abort(404, message=f'API key {key_id} not found')

            key.is_active = False
            db_sess.commit()

            return jsonify({'success': 'OK', 'message': 'API key deactivated'})
