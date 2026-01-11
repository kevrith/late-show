#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Episode, Guest, Appearance

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


@app.route('/')
def home():
    return '<h1>Late Show API</h1>'


class Episodes(Resource):
    def get(self):
        episodes = Episode.query.all()
        episodes_dict = [episode.to_dict(only=('id', 'date', 'number')) for episode in episodes]
        return make_response(jsonify(episodes_dict), 200)


class EpisodeByID(Resource):
    def get(self, id):
        episode = Episode.query.filter_by(id=id).first()

        if episode:
            episode_dict = episode.to_dict(only=(
                'id', 'date', 'number', 'appearances'
            ))
            return make_response(jsonify(episode_dict), 200)
        else:
            return make_response(jsonify({"error": "Episode not found"}), 404)

    def delete(self, id):
        episode = Episode.query.filter_by(id=id).first()

        if episode:
            db.session.delete(episode)
            db.session.commit()
            return make_response('', 204)
        else:
            return make_response(jsonify({"error": "Episode not found"}), 404)


class Guests(Resource):
    def get(self):
        guests = Guest.query.all()
        guests_dict = [guest.to_dict(only=('id', 'name', 'occupation')) for guest in guests]
        return make_response(jsonify(guests_dict), 200)


class Appearances(Resource):
    def post(self):
        data = request.get_json()

        try:
            new_appearance = Appearance(
                rating=data.get('rating'),
                episode_id=data.get('episode_id'),
                guest_id=data.get('guest_id')
            )

            db.session.add(new_appearance)
            db.session.commit()

            appearance_dict = new_appearance.to_dict(only=(
                'id', 'rating', 'guest_id', 'episode_id', 'episode', 'guest'
            ))

            return make_response(jsonify(appearance_dict), 201)

        except ValueError as e:
            return make_response(jsonify({"errors": [str(e)]}), 400)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"errors": ["validation errors"]}), 400)


api.add_resource(Episodes, '/episodes')
api.add_resource(EpisodeByID, '/episodes/<int:id>')
api.add_resource(Guests, '/guests')
api.add_resource(Appearances, '/appearances')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
