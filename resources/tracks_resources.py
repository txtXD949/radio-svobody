from flask_restful import Resource, abort
from flask import jsonify, request
from data import db_session
from data.tracks import Track
from data.likes import Like
from .track_parser import track_parser
from .auth import check_api_key


def not_found_track(track_id):
    with db_session.create_session() as db_sess:
        track = db_sess.query(Track).get(track_id)
        if not track:
            abort(404, message=f'Track {track_id} not found')
        return track


class TrackResource(Resource):
    def get(self, track_id):
        check_api_key()
        track = not_found_track(track_id)
        return jsonify({'track': track.to_dict()})

    def delete(self, track_id):
        check_api_key()
        with db_session.create_session() as db_sess:
            track = db_sess.query(Track).get(track_id)
            if not track:
                abort(404, message=f'Track {track_id} not found')
            db_sess.delete(track)
            db_sess.commit()
            return jsonify({'success': 'OK'})

    def put(self, track_id):
        check_api_key()
        args = track_parser.parse_args()
        with db_session.create_session() as db_sess:
            track = db_sess.query(Track).get(track_id)
            if not track:
                abort(404, message=f'Track {track_id} not found')

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
        genre_id = request.args.get('genre_id', type=int)

        with db_session.create_session() as db_sess:
            if genre_id and genre_id > 0:
                tracks = db_sess.query(Track).filter(Track.genre_id == genre_id).all()
            else:
                tracks = db_sess.query(Track).all()

            tracks_data = [t.to_dict() for t in tracks]
            return jsonify({'tracks': tracks_data})

    def post(self):
        check_api_key()
        args = track_parser.parse_args()

        with db_session.create_session() as db_sess:
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
        data = request.get_json()
        user_id = data.get('user_id')

        if not user_id:
            return {'message': 'user_id required'}, 400

        with db_session.create_session() as db_sess:
            ex_like = db_sess.query(Like).filter(Like.track_id == track_id, Like.user_id == user_id).first()
            track = db_sess.get(Track, track_id)

            if ex_like:
                db_sess.delete(ex_like)
                track.likes_count -= 1
                liked = False
            else:
                like = Like(track_id=track_id, user_id=user_id)
                db_sess.add(like)
                track.likes_count += 1
                liked = True

            db_sess.commit()
            likes_count = track.likes_count
            return {'likes_count': likes_count, 'liked': liked}
