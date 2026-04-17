from flask_restful import Resource
from flask import jsonify
from data import db_session
from data.tracks import Track
from data.users import User
from .auth import check_api_key
import sqlalchemy


class StatsResource(Resource):
    def get(self):
        check_api_key()
        db_sess = db_session.create_session()

        total_tracks = db_sess.query(Track).count()
        total_users = db_sess.query(User).count()
        total_likes = db_sess.query(sqlalchemy.func.sum(Track.likes_count)).scalar() or 0
        total_views = db_sess.query(sqlalchemy.func.sum(Track.views_count)).scalar() or 0

        top_tracks = db_sess.query(Track).order_by(Track.views_count.desc()).limit(5).all()

        return jsonify({
            'stats': {
                'total_tracks': total_tracks,
                'total_users': total_users,
                'total_likes': total_likes,
                'total_views': total_views,
                'top_tracks': [{'id': t.id, 'title': t.title, 'views': t.views_count} for t in top_tracks]
            }
        })
