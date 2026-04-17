from flask_restful import reqparse as rq

user_parser = rq.RequestParser()
user_parser.add_argument('username', required=True, type=str)
user_parser.add_argument('email', required=True, type=str)
user_parser.add_argument('password', required=True, type=str)
