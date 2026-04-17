from flask_restful import reqparse as rq

track_parser = rq.RequestParser()
track_parser.add_argument('title', required=True, type=str)
track_parser.add_argument('genre_id', required=True, type=int)
track_parser.add_argument('subgenres', required=False, type=str, default='')
track_parser.add_argument('file_path', required=True, type=str)
track_parser.add_argument('users_id', required=True, type=int)
track_parser.add_argument('collaborations', required=False, type=str, default='')
