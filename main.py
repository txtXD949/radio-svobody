from flask import Flask, jsonify
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from data import db_session
from data.api_key import ApiKey
from resources import (
    TrackResource, TrackListResource, TrackLikeResource,
    UserResource, UserListResource,
    GenreResource, GenreListResource,
    StatsResource,
    ApiKeyResource, ApiKeyDetailResource
)

app = Flask(__name__)
api = Api(app)


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    return jsonify({
        'error': e.description if hasattr(e, 'description') else str(e),
        'status_code': e.code
    }), e.code


# ресурсы
api.add_resource(TrackListResource, '/api/tracks')
api.add_resource(TrackResource, '/api/tracks/<int:track_id>')
api.add_resource(TrackLikeResource, '/api/tracks/<int:track_id>/like')
api.add_resource(UserListResource, '/api/users')
api.add_resource(UserResource, '/api/users/<int:user_id>')
api.add_resource(GenreListResource, '/api/genres')
api.add_resource(GenreResource, '/api/genres/<int:genre_id>')
api.add_resource(StatsResource, '/api/stats')
api.add_resource(ApiKeyResource, '/api/keys')
api.add_resource(ApiKeyDetailResource, '/api/keys/<int:key_id>')

if __name__ == '__main__':
    db_session.global_init('db/rs.db')

    session = db_session.create_session()
    if not session.query(ApiKey).first():
        admin_key = ApiKey(
            key=ApiKey.generate_key(),
            name='Admin Key'
        )
        session.add(admin_key)
        session.commit()
        print(f'ADMIN API KEY: {admin_key.key}')
    session.close()

    app.run(debug=True, host='127.0.0.1', port=5000)
