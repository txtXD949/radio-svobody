from flask_restful import abort, Resource
from flask import jsonify
from data import db_session
from data.genres import Genre
from .genres_parser import genre_parser
from .auth import check_api_key


def not_found_genre(genre_id):
    with db_session.create_session() as db_sess:
        genre = db_sess.query(Genre).get(genre_id)
        if not genre:
            abort(404, message=f'Genre {genre_id} not found')
        return genre


class GenreResource(Resource):
    def get(self, genre_id):
        check_api_key()
        genre = not_found_genre(genre_id)
        return jsonify({'genre': genre.to_dict()})

    def delete(self, genre_id):
        check_api_key()
        with db_session.create_session() as db_sess:
            genre = db_sess.query(Genre).get(genre_id)
            if not genre:
                abort(404, message=f'Genre {genre_id} not found')
            db_sess.delete(genre)
            db_sess.commit()
            return jsonify({'success': 'OK'})


class GenreListResource(Resource):
    def get(self):
        check_api_key()
        with db_session.create_session() as db_sess:
            genres = db_sess.query(Genre).all()
            return jsonify({'genres': [g.to_dict() for g in genres]})

    def post(self):
        check_api_key()
        args = genre_parser.parse_args()
        with db_session.create_session() as db_sess:
            genre = Genre(title=args['title'])
            db_sess.add(genre)
            db_sess.commit()
            return jsonify({'id': genre.id})
