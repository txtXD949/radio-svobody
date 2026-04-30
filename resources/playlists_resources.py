from flask_restful import Resource, abort
from flask import request, jsonify
from flask_login import current_user
from data import db_session
from data.playlists import Playlist
from data.playlist_tracks import PlaylistTrack
from data.tracks import Track
from .auth import check_api_key
from .playlist_parser import playlist_parser, playlist_track_parser, playlist_reorder_parser


class PlaylistListResource(Resource):
    def get(self):
        check_api_key()
        with db_session.create_session() as db_sess:
            playlists = db_sess.query(Playlist).filter(Playlist.user_id == current_user.id).all()
            return jsonify([p.to_dict() for p in playlists])

    def post(self):
        check_api_key()
        args = playlist_parser.parse_args()
        with db_session.create_session() as db_sess:
            playlist = Playlist(
                user_id=current_user.id,
                title=args['title']
            )
            db_sess.add(playlist)
            db_sess.commit()
            return jsonify(playlist.to_dict()), 201


class PlaylistResource(Resource):
    def delete(self, playlist_id):
        check_api_key()
        with db_session.create_session() as db_sess:
            playlist = db_sess.query(Playlist).filter(
                Playlist.id == playlist_id,
                Playlist.user_id == current_user.id
            ).first()

            if not playlist:
                abort(404, message='Playlist not found')

            db_sess.query(PlaylistTrack).filter(PlaylistTrack.playlist_id == playlist_id).delete()
            db_sess.delete(playlist)
            db_sess.commit()
            return jsonify({'success': True})


class PlaylistTracksResource(Resource):
    def get(self, playlist_id):
        check_api_key()
        with db_session.create_session() as db_sess:
            playlist = db_sess.query(Playlist).filter(
                Playlist.id == playlist_id,
                Playlist.user_id == current_user.id
            ).first()
            if not playlist:
                abort(404, message='Playlist not found')

            playlist_tracks = db_sess.query(PlaylistTrack).filter(
                PlaylistTrack.playlist_id == playlist_id
            ).order_by(PlaylistTrack.order).all()

            result = []
            for pt in playlist_tracks:
                track = pt.track
                result.append({
                    'playlist_track_id': pt.id,
                    'order': pt.order,
                    'track_id': track.id,
                    'title': track.title,
                    'artist': track.user.username if track.user else 'Unknown',
                    'likes_count': track.likes_count
                })
            return jsonify(result)

    def post(self, playlist_id):
        check_api_key()
        data = request.get_json()
        track_id = data.get('track_id') if data else None

        if not track_id:
            return {'message': 'track_id required'}, 400

        with db_session.create_session() as db_sess:
            playlist = db_sess.query(Playlist).filter(
                Playlist.id == playlist_id,
                Playlist.user_id == current_user.id
            ).first()
            if not playlist:
                return {'message': 'Playlist not found'}, 404

            track = db_sess.query(Track).get(track_id)
            if not track:
                return {'message': 'Track not found'}, 404

            existing = db_sess.query(PlaylistTrack).filter(
                PlaylistTrack.playlist_id == playlist_id,
                PlaylistTrack.track_id == track_id
            ).first()
            if existing:
                return {'message': 'Track already in playlist'}, 400

            max_order = db_sess.query(PlaylistTrack).filter(
                PlaylistTrack.playlist_id == playlist_id
            ).count()

            pt = PlaylistTrack(
                playlist_id=playlist_id,
                track_id=track_id,
                order=max_order
            )
            db_sess.add(pt)
            db_sess.commit()
            return {'success': True, 'order': max_order}, 201


class PlaylistTrackResource(Resource):
    def delete(self, playlist_id, track_id):
        check_api_key()
        with db_session.create_session() as db_sess:
            pt = db_sess.query(PlaylistTrack).filter(
                PlaylistTrack.playlist_id == playlist_id,
                PlaylistTrack.track_id == track_id
            ).first()

            if not pt:
                abort(404, message='Track not in playlist')

            deleted_order = pt.order
            db_sess.delete(pt)

            db_sess.query(PlaylistTrack).filter(
                PlaylistTrack.playlist_id == playlist_id,
                PlaylistTrack.order > deleted_order
            ).update({PlaylistTrack.order: PlaylistTrack.order - 1})

            db_sess.commit()
            return {'success': True}

    def put(self, playlist_id, track_id):
        check_api_key()
        args = playlist_reorder_parser.parse_args()
        direction = args['direction']

        with db_session.create_session() as db_sess:
            current = db_sess.query(PlaylistTrack).filter(
                PlaylistTrack.playlist_id == playlist_id,
                PlaylistTrack.track_id == track_id
            ).first()

            if not current:
                abort(404, message='Track not in playlist')

            if direction == 'up':
                neighbor = db_sess.query(PlaylistTrack).filter(
                    PlaylistTrack.playlist_id == playlist_id,
                    PlaylistTrack.order < current.order
                ).order_by(PlaylistTrack.order.desc()).first()
            else:
                neighbor = db_sess.query(PlaylistTrack).filter(
                    PlaylistTrack.playlist_id == playlist_id,
                    PlaylistTrack.order > current.order
                ).order_by(PlaylistTrack.order.asc()).first()

            if neighbor:
                current_order = current.order
                neighbor_order = neighbor.order
                current.order = neighbor_order
                neighbor.order = current_order
                db_sess.commit()

            return jsonify({'success': True})
