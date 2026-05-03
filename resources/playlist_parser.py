from flask_restful import reqparse

playlist_parser = reqparse.RequestParser()
playlist_parser.add_argument('title', required=True, help='Title is required')

playlist_track_parser = reqparse.RequestParser()
playlist_track_parser.add_argument('track_id', required=True, type=int, help='track_id is required')

playlist_reorder_parser = reqparse.RequestParser()
playlist_reorder_parser.add_argument('direction', required=True, choices=('up', 'down'), help='direction must be up or down')