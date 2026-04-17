from flask_restful import abort, Resource
from flask import jsonify
from data import db_session
from data.users import User
from .users_parser import user_parser
from .auth import check_api_key


def not_found_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        abort(404, message=f'User {user_id} not found')
    return db_sess, user


class UserResource(Resource):
    def get(self, user_id):
        check_api_key()
        db_sess, user = not_found_user(user_id)
        return jsonify({'user': user.to_dict()})

    def delete(self, user_id):
        check_api_key()
        db_sess, user = not_found_user(user_id)
        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        check_api_key()
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify({'users': [u.to_dict() for u in users]})

    def post(self):
        check_api_key()
        args = user_parser.parse_args()
        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.username == args['username']).first():
            abort(400, message=f'Username {args["username"]} already exists')

        if db_sess.query(User).filter(User.email == args['email']).first():
            abort(400, message=f'Email {args["email"]} already exists')

        user = User(
            username=args['username'],
            email=args['email']
        )
        user.set_password(args['password'])

        db_sess.add(user)
        db_sess.commit()
        return jsonify({'id': user.id})
