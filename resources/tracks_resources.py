from flask_restful import Resource, abort
from flask import jsonify, request
from data import db_session
from data.tracks import Track
from data.api_key import ApiKey
from .track_parser import track_parser


def check_api_key():
    api_key = request.headers.get('X-API-Key')

    if not api_key:
        abort(401, message='API key required')

    db_sess = db_session.create_session()
    key_obj = db_sess.query(ApiKey).filter(
        ApiKey.key == api_key,
        ApiKey.is_active == True
    ).first()
    db_sess.close()

    if not key_obj:
        abort(401, message='Invalid API key')


def not_found_track(track_id):
    db_sess = db_session.create_session()
    track = db_sess.query(Track).get(track_id)
    if not track:
        abort(404, message=f'Track {track_id} not found')
    return db_sess, track


class TrackResource(Resource):
    def get(self, track_id):
        check_api_key()
        db_sess, track = not_found_track(track_id)
        db_sess.commit()
        return jsonify({'track': track.to_dict()})

    def delete(self, track_id):
        check_api_key()
        db_sess, track = not_found_track(track_id)
        db_sess.delete(track)
        db_sess.commit()
        return jsonify({'success': 'OK'})

    def put(self, track_id):
        check_api_key()
        db_sess, track = not_found_track(track_id)
        args = track_parser.parse_args()

        track.title = args['title']
        track.genre_id = args['genre_id']
        track.subgenres = args['subgenres']
        track.file_path = args['file_path']
        track.users_id = args['users_id']
        track.collaborations = args['collaborations']

        db_sess.commit()
        return jsonify({'success': 'OK'})


class TrackListResource(Resource):
    def get(self):
        check_api_key()
        db_sess = db_session.create_session()
        tracks = db_sess.query(Track).all()
        return jsonify({'tracks': [t.to_dict() for t in tracks]})

    def post(self):
        check_api_key()  # Проверка ключа
        args = track_parser.parse_args()
        db_sess = db_session.create_session()

        track = Track(
            title=args['title'],
            genre_id=args['genre_id'],
            subgenres=args['subgenres'],
            file_path=args['file_path'],
            users_id=args['users_id'],
            collaborations=args['collaborations']
        )

        db_sess.add(track)
        db_sess.commit()
        return jsonify({'id': track.id})


class TrackLikeResource(Resource):
    def post(self, track_id):
        check_api_key()
        db_sess, track = not_found_track(track_id)
        track.likes_count += 1
        db_sess.commit()
        return jsonify({'success': 'OK', 'likes_count': track.likes_count})
