from flask_restful import abort, Resource
from flask import jsonify
from data import db_session
from data.genres import Genre
from .genres_parser import genre_parser
from .auth import check_api_key


def not_found_genre(genre_id):
    db_sess = db_session.create_session()
    genre = db_sess.query(Genre).get(genre_id)
    if not genre:
        abort(404, message=f'Genre {genre_id} not found')
    return db_sess, genre


class GenreResource(Resource):
    def get(self, genre_id):
        check_api_key()
        db_sess, genre = not_found_genre(genre_id)
        return jsonify({'genre': genre.to_dict()})

    def delete(self, genre_id):
        check_api_key()
        db_sess, genre = not_found_genre(genre_id)
        db_sess.delete(genre)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class GenreListResource(Resource):
    def get(self):
        check_api_key()
        db_sess = db_session.create_session()
        genres = db_sess.query(Genre).all()
        return jsonify({'genres': [g.to_dict() for g in genres]})

    def post(self):
        check_api_key()
        args = genre_parser.parse_args()
        db_sess = db_session.create_session()

        genre = Genre(title=args['title'])
        db_sess.add(genre)
        db_sess.commit()
        return jsonify({'id': genre.id})
