from flask_restful import reqparse

api_key_parser = reqparse.RequestParser()
api_key_parser.add_argument('name', required=True, type=str)
