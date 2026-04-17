from flask_restful import reqparse as rq

genre_parser = rq.RequestParser()
genre_parser.add_argument('title', required=True, type=str)
